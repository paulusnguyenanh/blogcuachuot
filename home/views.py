import urllib

from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from operator import attrgetter
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from blog.views import get_blog_queryset
from blog.models import BlogPost
from blog.models import Category
from home.models import Headline

BLOG_POSTS_PER_PAGE = 2


def home_screen_view(request, *args, **kwargs):
    context = {}

    # Search
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    blog_posts = sorted(get_blog_queryset(query), key=attrgetter('date_updated'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    blog_posts_paginator = Paginator(blog_posts, BLOG_POSTS_PER_PAGE)
    try:
        blog_posts = blog_posts_paginator.page(page)
    except PageNotAnInteger:
        blog_posts = blog_posts_paginator.page(BLOG_POSTS_PER_PAGE)
    except EmptyPage:
        blog_posts = blog_posts_paginator.page(blog_posts_paginator.num_pages)

    cats = Category.objects.all()
    context={'blog_posts': blog_posts, 'cats':cats }

    return render(request, "home/home.html", context)


def news_list(request):
	headlines = Headline.objects.all()
	context = {
		'object_list': headlines,
	}
	return render(request, "home/news.html", context)

def scrape(request):
	url = 'https://dantri.com.vn/su-kien.htm'
	page = urllib.request.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	News = soup.find('div', class_='col col--main').find_all("a", class_="news-item__avatar")
	old_headline = Headline.objects.all()
	old_headline.delete()

	for artcile in News:
		main = artcile
		image = artcile.find("img")
		image_src = image.attrs['lazy-src']
		title = main.find("img")['alt']
		link = main['href']

		new_headline = Headline()
		new_headline.title = title
		new_headline.url = "https://dantri.com.vn/" + link
		new_headline.image = image_src

		new_headline.save()

	return redirect("../news/")
