import json

from django.http import JsonResponse
from django.shortcuts import render
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from marshmallow import ValidationError as MarshmallowError
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .forms import DummyForm
from .schemas import REVIEW_SCHEMA, ReviewSchema


class FormDummyView(View):

    def get(self, request):
        form = DummyForm()
        return render(request, 'form.html', {'form': form})

    def post(self, request):
        form = DummyForm(request.POST)
        if form.is_valid():
            context = form.cleaned_data
            return render(request, 'form.html', context)
        else:
            return render(request, 'error.html', {'error': form.errors})

        # text = request.POST.get('text')
        # grade = request.POST.get('grade')
        # image = request.FILES.get('image')
        # content = image.read()
        # context = {
        #     'text': text,
        #     'grade': grade,
        #     'content': content
        # }
        # return render(request, 'form.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class SchemaView(View):

    def post(self, request):
        try:
            document = json.loads(request.body)
            validate(document, REVIEW_SCHEMA)
            return JsonResponse(document, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except ValidationError as exc:
            return JsonResponse({'errors': exc.message}, status=400)


@method_decorator(csrf_exempt, name='dispatch')
class MarshView(View):

    def post(self, request):
        try:
            document = json.loads(request.body)
            schema = ReviewSchema(strict=True)
            data = schema.load(document)
            return JsonResponse(data.data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)
        except MarshmallowError as exc:
            return JsonResponse({'errors': exc.messages}, status=400)
