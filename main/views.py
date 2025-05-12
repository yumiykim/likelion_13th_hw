from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *

def mainpage(request):
    return render(request, 'main/mainpage.html')

def secondpage(request):
    posts = Post.objects.all()
    return render(request, 'main/secondpage.html', {'posts' : posts})

def new_post(request):
    return render(request, 'main/new-post.html')

def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'main/detail.html', {'post': post})


def create(request):
    if request.method == 'POST':
        new_post = Post()
        new_post.author = request.user
        new_post.headline = request.POST['headline']
        new_post.nickname = request.POST['nickname']
        new_post.mood = request.POST.get('mood', '')
        new_post.reflection = request.POST['reflection']
        new_post.created_at = timezone.now()
        new_post.is_shared = request.POST.get('is_shared') == 'on'

        if 'photo' in request.FILES:
            new_post.photo = request.FILES['photo']

        new_post.save()
        return redirect('main:detail', new_post.id)
    
    return redirect('main:new-post')

def edit(request, id):
    edit_post = get_object_or_404(Post, pk=id)
    return render(request, 'main/edit.html', {"post": edit_post})

def update(request, id):
    post = get_object_or_404(Post, pk=id)

    if request.method == 'POST':
        post.headline = request.POST['headline']
        post.nickname = request.POST['nickname']
        post.mood = request.POST.get('mood', '')
        post.reflection = request.POST['reflection']
        post.is_shared = request.POST.get('is_shared') == 'on'
        post.created_at = timezone.now()  # 수정 시간 갱신

        if 'photo' in request.FILES:
            post.photo = request.FILES['photo']

        post.save()
        return redirect('main:detail', post.id)

    return redirect('main:edit', post.id)

def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('main:secondpage')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})