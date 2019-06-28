from datetime import datetime

from django.db.models import Q, Count, Avg
from pytz import UTC

from db.models import User, Blog, Topic


def create():
    """
    Создать пользователя first_name = u1, last_name = u1.
    Создать пользователя first_name = u2, last_name = u2.
    Создать пользователя first_name = u3, last_name = u3.
    Создать блог title = blog1, author = u1.
    Создать блог title = blog2, author = u1.
    Подписать пользователей u1 u2 на blog1, u2 на blog2.
    Создать топик title = topic1, blog = blog1, author = u1.
    Создать топик title = topic2_content, blog = blog1, author = u3, created = 2017-01-01.
    Лайкнуть topic1 пользователями u1, u2, u3.
    :return: None
    """
    u1 = User.objects.create(first_name="u1", last_name="u1")
    u2 = User.objects.create(first_name="u2", last_name="u2")
    u3 = User.objects.create(first_name="u3", last_name="u3")

    blog1 = Blog.objects.create(title="blog1", author=u1)
    blog2 = Blog.objects.create(title="blog2", author=u1)

    blog1.subscribers.add(u1, u2)
    blog2.subscribers.add(u2)

    topic1 = Topic.objects.create(title="topic1", blog=blog1, author=u1)
    topic2_content = Topic.objects.create(
        title="topic2_content",
        blog=blog1,
        author=u3,
        # both of the following variants are valid
        # created=datetime(year=2017, month=1, day=1, tzinfo=UTC)
        created="2017-01-01"
    )
    topic1.likes.add(u1, u2, u3)


def edit_all():
    """
    Поменять first_name на uu1 у всех пользователей
    :return:
    """
    User.objects.all().update(first_name="uu1")


def edit_u1_u2():
    """
    Поменять first_name на uu1 у пользователей, у которых first_name u1 или u2
    :return:
    """
    User.objects.filter(
        (Q(first_name="u1") | Q(first_name="u2"))
    ).update(first_name="uu1")


def delete_u1():
    """
    удалить пользователя с first_name u1
    :return:
    """
    User.objects.filter(first_name="u1").delete()


def unsubscribe_u2_from_blogs():
    """
    отписать пользователя с first_name u2 от блогов
    :return:
    """
    Blog.subscribers.through.objects.filter(user__first_name='u2').delete()


def get_topic_created_grated():
    """
    Найти топики у которых дата создания больше 2018-01-01
    :return:
    """
    # both of the following variants are valid
    # return Topic.objects.filter(created__gt="2018-01-01")
    return Topic.objects.filter(created__gt=datetime(year=2018, month=1, day=1, tzinfo=UTC))


def get_topic_title_ended():
    """
    Найти топик у которого title заканчивается на content
    :return:
    """
    return Topic.objects.filter(title__endswith="content")


def get_user_with_limit():
    """
    Получить 2х первых пользователей (сортировка в обратном порядке по id)
    :return:
    """
    return User.objects.all().order_by("-id")[:2]


def get_topic_count():
    """
    Получить количество топиков в каждом блоге, назвать поле topic_count, отсортировать по topic_count по возрастанию
    :return:
    """
    return Blog.objects.annotate(topic_count=Count("topic")).order_by("topic_count")


def get_avg_topic_count():
    """
    Получить среднее количество топиков в блоге
    :return:
    """
    return Blog.objects.annotate(topic_count=Count("topic")).aggregate(avg=Avg("topic_count"))


def get_blog_that_have_more_than_one_topic():
    """
    Найти блоги, в которых топиков больше одного
    :return:
    """
    return Blog.objects.annotate(topic_count=Count("topic")).filter(topic_count__gt=1)


def get_topic_by_u1():
    """
     Получить все топики автора с first_name u1
    :return:
    """
    return Topic.objects.filter(author__first_name="u1")


def get_user_that_dont_have_blog():
    """
    Найти пользователей, у которых нет блогов, отсортировать по возрастанию id
    :return:
    """
    return User.objects.filter(blog__isnull=True).order_by("id")


def get_topic_that_like_all_users():
    """
    Найти топик, который лайкнули все пользователи
    :return:
    """
    return Topic.objects.annotate(likes_count=Count("likes")).filter(likes_count=User.objects.count())


def get_topic_that_dont_have_like():
    """
    Найти топики, у которы нет лайков
    :return:
    """
    return Topic.objects.filter(likes__isnull=True)
