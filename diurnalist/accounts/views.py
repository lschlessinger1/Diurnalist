from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def deactivate(request):
    user = request.user
    user.is_active = False
    user.save()
    messages.success(request, 'Profile successfully deactivated.')
    return redirect('index')
