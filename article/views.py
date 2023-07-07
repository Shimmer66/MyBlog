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
        article_post_form = ArticleForm(request.POST,request.FILES)
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
        context = {'article_post_form': article_post_form,'colums':columns}
        return render(request, 'article/create.html', context)


@login_required(login_url='/user/login/')
def article_safe_delete(request, id):
    if request.method == 'POST':

        article = Article.objects.get(id=request.user.id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许POST请求！')


@login_required(login_url='/user/login/')
def article_update(request, id):
    article = Article.objects.get(id=request.user.id)
    if request.method == 'POST':
        article_post_form = ArticleForm(data=request.POST)
        if article_post_form.is_valid():
            if request.POST['column']!='None':
                article.column=ArticleColumn.objects.get(id=request.POST['column'])
            else:
                article.column=None
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        article_post_form = ArticleForm()
        column=ArticleColumn.objects.all()
        context = {'article': article, "article_post_form": article_post_form,'column':column}
        return render(request, 'article/update.html', context)

# def test(request):
#     articles = Article.objects.all()

#     li = [1, 2, 3, 4, 5, 6, 47, 8, ]
#     context = {'a': li}
#     return render(request, 'article/test.html', context)
