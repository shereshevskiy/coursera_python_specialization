from django.shortcuts import render
from db.query import *

# Create your views here.


def index(request):

    context = {
        "db_tests": {
            "create": create(),
            "get_topic_that_like_all_users": get_topic_that_like_all_users(),
            "get_topic_that_dont_have_like": get_topic_that_dont_have_like(),
            "get_avg_topic_count": get_avg_topic_count(),
            "get_topic_title_ended": get_topic_title_ended
        },
        "other_tests": {"test key1": "test value1"}
    }
    return render(request, 'index.html', context=context)
