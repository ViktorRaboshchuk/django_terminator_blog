from django.shortcuts import render, redirect
from blog.forms import CommentForm, UserEditForm, ProfileEditForm, CreateUserForm
from blog.models import Post, Profile
from blog.utils import valid

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


def index(request):
    posts = Post.objects.all().order_by('-title')
    paginator = Paginator(posts, 3) # Show 3 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'posts': posts, 'page_obj': page_obj}
    return render(request, 'blog/index.html', context=context)


def post(request, pk):
    post = Post.objects.get(id=pk)
    comments = post.comments.all().order_by('-created_on')
    new_comment = None
    comment_form = CommentForm(request=request, readonly_form=False)

    if request.method == 'POST':
        if request.user.is_authenticated:
            comment_form = CommentForm(request=request, data=request.POST, readonly_form=True)
            valid(comment_form, post)
            return redirect('/')
    # else:
    #     comment_form = CommentForm(request=request)

    context = {'post': post, 'comments': comments, 'new_comment': new_comment, 'comment_form': comment_form}
    return render(request, 'blog/post_detail.html', context=context)


def about(request):
    return render(request, 'blog/about.html')


@login_required(login_url='/login/')
def profile(request):
    if request.method == 'POST':
        print(request.POST)
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
    else:
        # print(request.user.profile)
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    context = {'user_form': user_form, 'profile_form': profile_form}
    return render(request, 'blog/profile.html', context=context)

def register(request):
    form = CreateUserForm()
    new_user = None
    profile = None
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = form.save(commit=False)
            # Set the chosen password
            new_user.set_password(form.cleaned_data['password1'])
            # Save the User object
            new_user.save()
            profile = Profile.objects.create(user=new_user)

    return render(request, 'registration/registration.html', {'form':form, 'new_user':new_user, 'profile':profile})

    context = {'form': form}
    return render(request, 'blog/registration.html', context=context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')

    context = {}
    return render(request, 'blog/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/login')
