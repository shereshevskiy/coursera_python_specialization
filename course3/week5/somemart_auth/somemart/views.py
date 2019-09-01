import base64
import json

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Item, Review

from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow import ValidationError


class ReviewSchema(Schema):
    # id = fields.Int(dump_only=True)
    grade = fields.Int(validate=Range(1, 10), strict=True)
    text = fields.Str(validate=Length(min=1, max=1024))


class ItemSchema(Schema):
    # id = fields.Int(dump_only=True)
    title = fields.Str(validate=Length(min=1, max=64))
    description = fields.Str(validate=Length(min=1, max=1024))
    price = fields.Int(validate=Range(1, 1000000), strict=True)


class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        # Здесь должен быть ваш код
        try:
            document = json.loads(request.body)
            schema = ItemSchema(strict=True)
            loaded_document = schema.load(document)
            loaded_data = loaded_document.data

            if 'HTTP_AUTHORIZATION' in request.META:
                basic_login_password_coded = request.META['HTTP_AUTHORIZATION']
                if basic_login_password_coded.split()[0].lower() == "basic":
                    login_password_coded = basic_login_password_coded.split()[1]
                    login_password = base64.standard_b64decode(login_password_coded.encode('ascii'))
                    login, password = login_password.decode("utf-8").split(":")
                    user = authenticate(username=login, password=password)

                    if user is not None:
                        if user.is_staff:
                            item = Item.objects.create(title=loaded_data["title"], description=loaded_data["description"],
                                                       price=int(loaded_data["price"]))
                            data = {"id": item.pk}
                            return JsonResponse(data, status=201)
                        else:
                            return HttpResponse(status=403)
                    else:
                        return HttpResponse(status=401)

        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.messages}, status=400)


class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        # Здесь должен быть ваш код
        try:
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            loaded_document = schema.load(document)
            data = loaded_document.data

            item = Item.objects.get(pk=item_id)

            review = Review.objects.create(item=item_id, grade=data["grade"], text=data["text"])

            return JsonResponse({"id": review.id}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.messages}, status=400)
        except Item.DoesNotExist:
            return JsonResponse({'errors': 'Product with this id does not exist'}, status=404)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        # Здесь должен быть ваш код
        try:
            item = Item.objects.get(id=item_id)

            query = Review.objects.filter(item=item_id).order_by('-id')
            reviews = list(query[:5].values())
            data = {
                "id": int(item.id),
                "title": item.title,
                "description": item.description,
                "price": int(item.price),
                "reviews": reviews
            }
            return JsonResponse(data, status=200)
        except Item.DoesNotExist:
            return JsonResponse({'errors': 'Product with this id does not exist'}, status=404)
