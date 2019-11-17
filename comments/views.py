from django.shortcuts import render, redirect
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse


def submit_comment(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))

    # 数据检查
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message':'用户未登录', 'redirect_to': referer})
    text = request.POST.get('text', '').strip()
    if text == '':
        return render(request, 'error.html', {'message': '评论内容为空', 'redirect_to': referer})
    try:
        content_type = request.POST.get('content_type', '')
        object_id = request.POST.get('object_id', '')
        model_class = ContentType.objects.get(model=content_type).model_class()  # 获取具体的模型
        model_obj = model_class.objects.get(pk=int(object_id))  # 获取具体的对象
    except Exception as e:
        return render(request, 'error.html', {'message': '评论文章不存在', 'redirect_to': referer})

    # 检查通过，保存数据
    comment = Comment()
    comment.commenter = request.user
    comment.comment_content = text
    comment.content_object = model_obj
    comment.save()

    return redirect(referer)
