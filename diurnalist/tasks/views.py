import django.forms as forms
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.core.mail import send_mail, BadHeaderError
from django.views import generic
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Task


class UserOwnershipMixin(UserPassesTestMixin):
    """
    helper class that checks if the current user is the owner of the object
    """

    def test_func(self):
        owner = self.get_object().created_by
        return self.request.user == owner


class DateTypeInput(forms.DateInput):
    """ Change default input type for DateField to date
    https://code.djangoproject.com/ticket/21470
    """
    input_type = 'date'


class DateTimeTypeInput(forms.DateInput):
    """ Change default input type for DateTimeField to datetime
    https://code.djangoproject.com/ticket/21470
    """
    input_type = 'datetime'


def index(request):
    return render(
        request,
        'main.html',
    )


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 20
    context_object_name = 'task_list'
    template_name = 'tasks/task_list.html'
    done = True

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)

        context['high_priority_tasks'] = Task.objects.filter(created_by=self.request.user, priority=Task.HIGH_PRIORITY,
                                                             parent_task=None, done=False)
        context['medium_priority_tasks'] = Task.objects.filter(created_by=self.request.user,
                                                               priority=Task.MEDIUM_PRIORITY, parent_task=None,
                                                               done=False)
        context['low_priority_tasks'] = Task.objects.filter(created_by=self.request.user, priority=Task.LOW_PRIORITY,
                                                            parent_task=None, done=False)
        return context

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user, parent_task=None)


class TaskForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TaskForm, self).__init__(*args, **kwargs)

        # add form-control class to each visible field for Bootstrap 3
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        if self.instance:
            self.fields['parent_task'].queryset = Task.objects.filter(created_by=self.user, parent_task=None,
                                                                      done=False)

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ["position", "created_by", "done", "done_at"]
        widgets = {
            'due_date': DateTypeInput()
        }


class TaskDetailView(generic.DetailView, LoginRequiredMixin, UserOwnershipMixin):
    model = Task


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    permission_required = 'tasks.add_task'

    def get_form_kwargs(self):
        kwargs = super(TaskCreate, self).get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        # TODO: set task position
        task_position = 0
        form.instance.position = task_position

        return super(TaskCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['active_item'] = 'create_task'
        context['form_title'] = 'Create Task'
        context['submit_value'] = 'Create Task'
        return context


class TaskUpdate(LoginRequiredMixin, UserOwnershipMixin, UpdateView):
    model = Task
    form_class = TaskForm

    def get_context_data(self, **kwargs):
        context = super(TaskUpdate, self).get_context_data(**kwargs)
        context['form_title'] = 'Update Task'
        context['submit_value'] = 'Update Task'
        return context


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('tasks')


def mark_done(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    task.done_at = timezone.now()
    task.done = True
    task.save()

    return HttpResponseRedirect(reverse('tasks'))


class TaskSearchListView(LoginRequiredMixin, generic.ListView):
    """
    Show a list of tasks filtered by the search query
    """
    model = Task
    paginate_by = 20
    context_object_name = 'task_list'
    template_name = 'tasks/task_search_list_view.html'

    def get_context_data(self, **kwargs):
        context = super(TaskSearchListView, self).get_context_data(**kwargs)
        query = self.request.GET['query']
        results = Task.objects.filter(title__icontains=query, created_by=self.request.user)
        context['query'] = query
        context['results'] = results
        return context


class TaskDoneListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 20
    context_object_name = 'task_list'
    template_name = 'tasks/task_list.html'

    def get_context_data(self, **kwargs):
        context = super(TaskDoneListView, self).get_context_data(**kwargs)
        context['active_item'] = 'tasks_completed'

        context['high_priority_tasks'] = Task.objects.filter(created_by=self.request.user, priority=Task.HIGH_PRIORITY,
                                                             parent_task=None, done=True)
        context['medium_priority_tasks'] = Task.objects.filter(created_by=self.request.user,
                                                               priority=Task.MEDIUM_PRIORITY, parent_task=None,
                                                               done=True)
        context['low_priority_tasks'] = Task.objects.filter(created_by=self.request.user, priority=Task.LOW_PRIORITY,
                                                            parent_task=None, done=True)
        return context

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user, parent_task=None)


def share(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    subject = request.user.username + " shared a task with you"
    message = request.POST.get('message', '')
    from_email = "noreplay@diurnalist.com"
    to_email = request.POST.get('to_email', '')
    recipient_list = [to_email]

    if not message:
        message = "Hello, " + request.user.username + " shared the task: '" + task.title + "' with you"

    if subject and message and from_email:
        try:
            send_mail(subject, message, from_email, recipient_list)
        except BadHeaderError:
            return HttpResponse('Invalid header found.')

        messages.success(request, 'Task shared with ' + to_email + '.')
        return HttpResponseRedirect(reverse('tasks'))
    else:
        return HttpResponse('Make sure all fields are entered and valid.')
