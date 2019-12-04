from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import CommentForm

register = template.Library()


@register.simple_tag
def get_comment_count(obj):
    """
    :param obj: 可以是任意类型
    :return:
    """
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comment_form = CommentForm(initial={
        'content_type': content_type.model,
        'object_id': obj.pk,
        'reply_comment_id': '0',  # 顶级评论设置为0
    })

    return comment_form


@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type,
                                      object_id=obj.pk, parent=None)
    return comments