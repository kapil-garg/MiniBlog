from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import Post
from django.contrib.auth.models import Group


def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'blog/home.html', context)


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        user_groups = user.groups.all()
        context = {
            'posts': posts,
            'full_name': full_name,
            'groups': user_groups
        }
        return render(request, 'blog/dashboard.html', context)
    else:
        return HttpResponseRedirect("/login/")


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                post_object = Post(title=title, desc=desc)
                post_object.save()
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request, id):
    if request.user.is_authenticated:
        post = Post.objects.get(pk=id)
        if request.method == 'POST':
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                form.save()
        else:
            form = PostForm(instance=post)
        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post_object = Post.objects.get(pk=id)
            post_object.delete()
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully!!')
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        print(request.user)
        return HttpResponseRedirect('/dashboard/')


def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations!! you are author now")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = SignUpForm()
    context = {
        'form': form
    }
    return render(request, 'blog/signup.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')



