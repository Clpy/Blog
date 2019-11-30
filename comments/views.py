from .models import Comment
from django.http import JsonResponse
from .forms import CommentForm


def submit_comment(request):
    comment_form = CommentForm(request.POST, user=request.user)  # 获取post请求的数据
    data = {}

    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.commenter = comment_form.cleaned_data['user']
        comment.comment_content = comment_form.cleaned_data['comment_content']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']  # 判断是否是回复（or评论）

        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.commenter
        comment.save()

        # 返回数据
        data['status'] = 'SUCCESS'
        data['commenter'] = comment.commenter.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_content'] = comment.comment_content

        if not parent is None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''

        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]

    return JsonResponse(data, safe=False)