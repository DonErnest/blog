from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from webapp.forms import ArticleForm
from webapp.models import Article


class CreateView(TemplateView):
    form_class = None
    template_name = None
    model = None
    redirect_url = None

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, context={'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            self.object = self.model.objects.create(**form.cleaned_data)
            return redirect(self.get_redirect_url())
        return render(request, self.template_name, context={'form': form})


    def get_redirect_url(self):
        # self.object.pk
        return self.redirect_url