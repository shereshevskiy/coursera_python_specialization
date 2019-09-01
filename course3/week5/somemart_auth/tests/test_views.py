import json

from somemart.models import Item, Review


class TestViews(object):

    def test_post_item(self, client, db):
        """/api/v1/goods/ (POST) сохраняет товар в базе."""
        url = '/api/v1/goods/'
        data = json.dumps({
            'title': 'Сыр "Российский"',
            'description': 'Очень вкусный сыр, да еще и российский.',
            'price': 100
        })
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 201
        document = response.json()
        # Объект был сохранен в базу
        item = Item.objects.get(pk=document['id'])
        assert item.title == 'Сыр "Российский"'
        assert item.description == 'Очень вкусный сыр, да еще и российский.'
        assert item.price == 100

    def test_post_review(self, client, db):
        """/api/v1/goods/1/reviews/ (POST) сохраняет отзыв в базе."""
        url = '/api/v1/goods/95/reviews/'
        data = json.dumps({
            'grade': '9',
            'text': 'Все хорошо',
            'item': '95'
        })
        response = client.post(url, data=data, content_type='application/json')
        assert response.status_code == 404
        document = response.json()
        # Объект был сохранен в базу
        review = Review.objects.get(pk=95)
        assert review.grade == '9'
        assert review.text == 'Все хорошо'
        assert review.item == '95'

    def test_get_item(self, client, db):
        """/api/v1/goods/112/ (GET) с"""
        url = '/api/v1/goods/112/'

        response = client.get(url, content_type='application/json')
        document = response.json()
        print("!!!!!!!!!!!! document", document)
