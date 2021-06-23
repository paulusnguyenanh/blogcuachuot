from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from blog.models import BlogPost
from blog.forms import CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account


def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return HttpResponseRedirect('/login/')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		context['success_message'] = "Done!!!"
		form = CreateBlogPostForm()


	context['form'] = form

	return render(request, "blog/create_blog.html", context)


def detail_blog_view(request, slug):
    context = {}
    blog_post = get_object_or_404(BlogPost, slug=slug)
    blog_post.views = blog_post.views +1
    blog_post.save()


    context={'blog_post': blog_post}

    return render(request, 'blog/detail_blog.html', context)


def edit_blog_view(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect('must_authenticate')

    blog_post = get_object_or_404(BlogPost, slug=slug)
    if request.POST:
        form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context['success_message'] = "Updated"
            blog_post = obj

    form = UpdateBlogPostForm(
        initial={
            "title": blog_post.title,
            "body": blog_post.body,
            "content": blog_post.content,
            "image": blog_post.image,
			"categories":blog_post.categories,
        }
    )
    context['form'] = form

    return render(request, 'blog/edit_blog.html', context)

def get_blog_queryset(query=None):
	queryset = []
	queries = query.split(" ")
	for q in queries:
		posts = BlogPost.objects.filter(
			Q(title__contains=q)|
			Q(body__icontains=q)
			).distinct()
		for post in posts:
			queryset.append(post)

	# create unique set and then convert to list
	return list(set(queryset))


def dashboard(request):
	user =request.user
	if request.user.is_authenticated:
		posts = BlogPost.objects.all()
		return  render(request, 'blog/dashboard.html',{'posts':posts})
	else:
		return HttpResponseRedirect('/login/')

def delete_post(request,slug):
	if request.user.is_authenticated:
		if request.POST:
			pi = BlogPost.objects.get(slug=slug)
			pi.delete()
			return HttpResponseRedirect('/blog/dashboard/')
	else:
		return HttpResponseRedirect('/login/')