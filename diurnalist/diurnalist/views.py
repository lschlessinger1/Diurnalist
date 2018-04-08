from django.views import generic
from django.shortcuts import redirect


class MainPage(generic.TemplateView):
    template_name = "main.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("tasks/tasks")
        return super(MainPage, self).get(request, *args, **kwargs)


class AboutPage(generic.TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutPage, self).get_context_data(**kwargs)
        context['active_item'] = 'about'
        return context

