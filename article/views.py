from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

from comment.models import Comment
from .models import Article, ArticleColumn
from .forms import ArticleForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import markdown


# Create your views here.
def article_list(request):
    search = request.GET.get('search')
    order = request.GET.get('order')
    if search:
        if order == 'total_views':
            article_list = Article.objects.filter(Q(content__icontains=search) | Q(title__icontains=search)).order_by(
                '-total_views')
        else:
            article_list = Article.objects.filter(Q(content__icontains=search) | Q(title__icontains=search)).order_by(
                '-created_date')
    else:
        if order == 'total_views':
            article_list = Article.objects.all().order_by('-total_views')
            order = 'total_views'
        else:
            article_list = Article.objects.all()
            order = 'normal'
    paginator = Paginator(article_list, 6)
    page = request.GET.get('page')
    articles = paginator.get_page((page))
    context = {'articles': articles, 'order': order, 'search': search}
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = Article.objects.get(id=id)
    article.total_views += 1
    article.save(update_fields=['total_views'])
    comments = Comment.objects.filter(article=id)
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    article.content = md.convert(article.content)
    context = {'article': article, 'toc': md.toc, 'comments': comments}
    return render(request, 'article/detail.html', context)


@login_required(login_url='/user/login/')
def article_create(request):
    # print(request.method)
    if request.method == 'POST':
        article_post_form = ArticleForm(request.POST, request.FILES)
        print((article_post_form.is_valid()))
        if article_post_form.is_valid():

            # 已有代码
            new_article = article_post_form.save(commit=False)

            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])

            new_article.author = User.objects.get(id=request.user.id)
            new_article.save()
            return redirect('article:article_list')
        else:
            print(article_post_form.errors)

            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticleForm()
        columns = ArticleColumn.objects.all()
        context = {'article_post_form': article_post_form, 'colums': columns}
        return render(request, 'article/create.html', context)


@login_required(login_url='/user/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':
        article = Article.objects.get(id=id)
        if request.user != article.author:
            return HttpResponse("抱歉，你无权修改这篇文章。")
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许POST请求！')


@login_required(login_url='/user/login/')
def article_update(request, id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新titile、body字段
    GET方法进入初始表单页面
    id： 文章的 id
    """
    # 获取需要修改的具体文章对象
    article = Article.objects.get(id=id)
    # 过滤非作者的用户
    if request.user != article.author:
        return HttpResponse("抱歉，你无权修改这篇文章。")
    # print(request.method)
    # 判断用户是否为 POST 提交表单数据
    if request.method == "POST":
        print('post')
        # 将提交的数据赋值到表单实例中
        article_post_form = ArticleForm(data=request.POST)
        # 判断提交的数据是否满足模型的要求
        if request.POST.get('column') != 'none':
            # 保存文章栏目
            article.column = ArticleColumn.objects.get(id=request.POST.get('column'))
            print(article.column.id,'idid')
        else:
            article.column = None
        if article_post_form.is_valid():
            # 保存新写入的 title、body 数据并保存
            article.title = request.POST['title']
            article.body = request.POST['content']
            if request.FILES.get('title_image'):
                article.title_image = request.FILES.get('title_image')
            article.save()
            # 完成后返回到修改后的文章中。需传入文章的 id 值
            return redirect("article:article_detail", id=id)
        # 如果数据不合法，返回错误信息
        else:
            return HttpResponse("表单内容有误，请重新填写。")

    # 如果用户 GET 请求获取数据
    else:

        # 创建表单类实例
        article_post_form = ArticleForm()
        # 文章栏目
        columns = ArticleColumn.objects.all()
        # 赋值上下文，将 article 文章对象也传递进去，以便提取旧的内容
        context = {
            'article': article,
            'article_post_form': article_post_form,
            'columns': columns,
        }

        # 将响应返回到模板中
        return render(request, 'article/update.html', context)
# def test(request):
#     articles = Article.objects.all()

#     li = [1, 2, 3, 4, 5, 6, 47, 8, ]
#     context = {'a': li}
#     return render(request, 'article/test.html', context)
