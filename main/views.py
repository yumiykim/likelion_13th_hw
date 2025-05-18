from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import *
from .models import Comment
from django.db.models import Count

def mainpage(request):
    return render(request, 'main/mainpage.html')

def secondpage(request):
    posts = Post.objects.all()
    return render(request, 'main/secondpage.html', {'posts' : posts})

def new_post(request):
    return render(request, 'main/new-post.html')

def detail(request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'GET':
        comments = Comment.objects.filter(post=post)
        return render(request, 'main/detail.html', {'post':post, 'comments': comments})

    elif request.method == 'POST':
        new_comment = Comment()
        new_comment.post = post
        new_comment.writer=request.user
        new_comment.content = request.POST['content']
        new_comment.pub_date = timezone.now()
        new_comment.save()
        return redirect('main:detail', id)
    

def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user == comment.writer:
        post_id = comment.post.id
        comment.delete()
        return redirect('main:detail', post_id)
    else:
        return redirect('main:secondpage')



def create(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')  # 로그인 안 했으면 로그인 페이지로

    if request.method == 'POST':
        new_post = Post()
        new_post.author = request.user
        new_post.headline = request.POST['headline']
        new_post.mood = request.POST.get('mood', '')
        new_post.reflection = request.POST['reflection']
        new_post.created_at = timezone.now()
        new_post.is_shared = request.POST.get('is_shared') == 'on'

        if 'photo' in request.FILES:
            new_post.photo = request.FILES['photo']

        new_post.save()

        # 해시태그 추출 및 저장
        words = new_post.reflection.replace('\n', ' ').split()  # 공백 + 줄바꿈
        tag_list = []

        for w in words:
            if w.startswith('#') and len(w) > 1:
                tag_list.append(w[1:])

        for tag_name in tag_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            new_post.tags.add(tag)

        return redirect('main:detail', new_post.id)
    
    return redirect('main:new-post')




def edit(request, id):
    edit_post = get_object_or_404(Post, pk=id)
    return render(request, 'main/edit.html', {"post": edit_post})


def update(request, id):
    post = get_object_or_404(Post, pk=id)

    if not request.user.is_authenticated or request.user != post.author:
        return redirect('accounts:login')

    if request.method == 'POST':
        post.headline = request.POST['headline']
        post.mood = request.POST.get('mood', '')
        post.reflection = request.POST['reflection']
        post.is_shared = request.POST.get('is_shared') == 'on'
        post.created_at = timezone.now()  # 수정 시간 갱신

        if 'photo' in request.FILES:
            post.photo = request.FILES['photo']

        post.save()

        post.tags.clear() # 기존 태그 제거
        
        # 해시태그 추출
        words = post.reflection.replace('\n', ' ').split(' ')
        tag_list = []
        for word in words:
            word = word.strip()
            if word.startswith('#') and len(word) > 1:
                tag_list.append(word[1:])

        for tag_name in tag_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            post.tags.add(tag)

        return redirect('main:detail', post.id)

    return redirect('main:edit', post.id)

def delete(request, id):
    post = get_object_or_404(Post, pk=id)
    post.delete()
    return redirect('main:secondpage')

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detail.html', {'post': post})



def tag_list(request): #모든 태그 목록을 볼 수 있는 페이지
    tags = Tag.objects.annotate(num_posts=Count('posts')).filter(num_posts__gt=0)
    return render(request, 'main/tag-list.html', {'tags': tags})

def tag_posts(request, tag_id): #특정 태그를 가진 게시글의 목록을 볼 수 있는 페이지
    tag=get_object_or_404(Tag, id=tag_id)
    posts=tag.posts.all()
    return render(request, 'main/tag-post.html', {
        'tag':tag,
        'posts':posts
    })