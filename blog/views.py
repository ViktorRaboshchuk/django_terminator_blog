""" Class based views for rendering data"""
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from blog.forms import CommentForm, UserEditForm, ProfileEditForm, CreateUserForm
from blog.models import Post, Profile, Comment


class MoviesList(ListView):
    """ List of all movies """
    model = Post
    paginate_by = 3
    template_name = 'blog/index.html'


class MovieDetailView(DetailView):
    """ Each movies page """
    model = Post
    form_class = CommentForm
    template_name = 'blog/post_detail.html'

    def get_context_data(self):
        """ adding data for templates rendering"""
        context = super().get_context_data()

        comments = Comment.objects.filter(post=self.get_object()).order_by('-created_on')
        context['comments'] = comments
        if self.request.user.is_authenticated:
            context['comment_form'] = self.form_class(instance=self.get_object())

        return context

    def post(self, request, *args, **kwargs):
        """ save new comments """
        comment_form = self.form_class(request.POST)
        if comment_form.is_valid():
            # Create comment object but not save to DB yet
            new_comment = comment_form.save(commit=False)
            # Assign current post to comment
            new_comment.post = self.get_object()
            # Save comment to DB
            new_comment.save()

        return self.get(self, request, *args, **kwargs)


def about(request):
    """ Theme page"""
    return render(request, 'blog/about.html')


class ProfileView(View):
    """ Rendering and saving data about user"""
    template_name = 'blog/profile.html'

    def get(self, request):
        """ renders user data"""
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, self.template_name,
                      {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request,):
        """ save new user profile data"""
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect('/profile/')

        return render(request, self.template_name,
                      {'user_form': user_form, 'profile_form': profile_form})


class UserRegistration(CreateView):
    """ User Sing Up proccess"""
    form_class = CreateUserForm
    success_url = reverse_lazy('login')
    template_name = 'registration/registration.html'

    def form_valid(self, form):
        """Force the user to request.user"""
        new_user = form.save()
        new_user.save()
        Profile.objects.create(user=new_user)

        return super().form_valid(form)
