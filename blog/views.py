from django.shortcuts import render,get_object_or_404
from .models import Post 
from django.utils import timezone
from .forms import *
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

def author_check(view_func):
    def wrapper(request,pk,*args,**kwargs):
        post=get_object_or_404(Post,pk=pk)
        if(post and not str(request.user.username)==str(post.author)):
            print(str(request.user.username),str(post.author))
            messages.warning(request,f'You are not logged in as the author. Please Log In to continue.')
            return redirect('/login')
        else:
            return view_func(request,pk,*args,**kwargs)
    return wrapper

def post_list(request):
	posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.created_date = timezone.now()
            post.published_date = timezone.now()
            post.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form,'action':0})

@author_check
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostEdit(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostEdit(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form,'action':1,'post':post})

@author_check
def post_delete(request,pk):
    item=Post.objects.get(id=pk)

    context={'item':item}
    if(request.method=='POST'):
        item.delete()
        return redirect('/post_list')
    return render(request,'blog/post_delete.html',context)