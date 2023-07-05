from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Article
from .forms import ArticleForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import markdown


# Create your views here.
def article_list(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'article/list.html', context)


def article_detail(request, id):
    article = Article.objects.get(id=id)
    article.content = markdown.markdown(article.content,
                                        extensions=[
                                            'markdown.extensions.extra',
                                            'markdown.extensions.codehilite',
                                        ])
    context = {'article': article}

    return render(request, 'article/detail.html', context)


def article_create(request):
    # print(request.method)
    if request.method == 'POST':
        article_post_form = ArticleForm(data=request.POST)
        print((article_post_form.is_valid()))
        if article_post_form.is_valid():
            new_article = article_post_form.save(commit=False)
            new_article.author = User.objects.get(id=1)
            new_article.save()
            return redirect('article:article_list')
        else:
            print(article_post_form.errors)

            return HttpResponse("表单内容有误，请重新填写。")
    else:
        article_post_form = ArticleForm()
        context = {'article_post_form': article_post_form}
        return render(request, 'article/create.html', context)


def article_safe_delete(request, id):
    if request.method == 'POST':

        article = Article.objects.get(id=id)
        article.delete()
        return redirect('article:article_list')
    else:
        return HttpResponse('仅允许POST请求！')


def article_update(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        article_post_form = ArticleForm(data=request.POST)
        if article_post_form.is_valid():
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.save()
            return redirect('article:article_detail', id=id)
        else:
            return HttpResponse('表单内容有误，请重新填写。')
    else:
        article_post_form = ArticleForm()
        context = {'article': article, "article_post_form": article_post_form}
        return render(request, 'article/update.html', context)

# def test(request):
#     articles = Article.objects.all()
#     li = [1, 2, 3, 4, 5, 6, 47, 8, ]
#     context = {'a': li}
#     return render(request, 'article/test.html', context)
