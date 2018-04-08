from django.shortcuts import render
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfilePage(LoginRequiredMixin, generic.TemplateView):
    template_name = "profiles/view_profile.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect("login")
        return super(ProfilePage, self).get(request, *args, **kwargs)
