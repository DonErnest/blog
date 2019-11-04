from django.contrib.auth import login
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

from accounts.forms import SignUpForm, UserChangeForm, UserChangePasswordForm
from accounts.models import Profile, Token
from to_do_list.settings import HOST_NAME


def send_token(user, subject, message, redirect_url):
    token = Token.objects.create(user=user)
    url = HOST_NAME + reverse(redirect_url, kwargs={'token': token})
    print(url)
    try:
        user.email_user(subject, message.format(url=url))
    except ConnectionRefusedError:
        print('Could not send email. Server error.')

def register_view(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'register.html', context={'form': form})
    elif request.method == 'POST':
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            Profile.objects.create(user=user)
            send_token(user,
                       'Вы зарегистрировались на сайте localhost:8000.',
                       'Для активации перейдите по ссылке: {url}',
                       redirect_url='accounts:user_activate')
            return redirect('webapp:index')
        else:
            return render(request, 'register.html', context={'form': form})


def user_activate_view(request, token):
    token = get_object_or_404(Token, token=token)
    user = token.user
    user.is_active = True
    user.save()
    token.delete()
    login(request, user)
    return redirect('webapp:index')


class UserDetailView(DetailView):
    model = User
    template_name = 'user_detail.html'
    context_object_name = 'user_obj'


class UserChangeView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_update.html'
    context_object_name = 'user_obj'
    form_class = UserChangeForm

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:user_detail', kwargs={'pk': self.object.pk})


class UserChangePasswordView(UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'user_change_password.html'
    form_class = UserChangePasswordForm
    context_object_name = 'user_obj'

    def test_func(self):
        return self.get_object() == self.request.user

    def get_success_url(self):
        return reverse('accounts:login')
