from django.shortcuts import render, HttpResponse
from home.models import Contact
from django.contrib import messages
from blog.models import Post
from django.db.models import Q

def home(request): 
    return render(request, "home/home.html")

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content =request.POST['content']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")

def about(request): 
    return render(request, "home/about.html")


def search(request):
    query = request.GET.get('query', '').strip()
    if len(query)>78:
        allPosts=Post.objects.none()
    else:
        allPosts = []
    if query:
        allPosts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(slug__icontains=query) |
            Q(author__icontains=query) 
        )
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    return render(request, 'home/search.html', {'allPosts': allPosts, 'query': query})

