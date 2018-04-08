from datetime import date, datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Task(models.Model):
    """
    Task Docs
    """
    HIGH_PRIORITY = 'H'
    MEDIUM_PRIORITY = 'M'
    LOW_PRIORITY = 'L'
    PRIORITY_LEVELS = (
        (HIGH_PRIORITY, 'High Priority'),
        (MEDIUM_PRIORITY, 'Medium Priority'),
        (LOW_PRIORITY, 'Low Priority'),
    )

    # Fields
    title = models.CharField(max_length=200, help_text="Enter a task name")
    due_date = models.DateField(help_text="Enter a due date")
    position = models.PositiveIntegerField()
    priority = models.CharField(max_length=1, choices=PRIORITY_LEVELS, default=MEDIUM_PRIORITY,
                                help_text="Enter a priority level")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    done = models.BooleanField(default=False)

    notes = models.TextField(null=True, blank=True, help_text="Enter task notes")
    context_tags = models.ManyToManyField('ContextTag', null=True, blank=True)
    parent_task = models.ForeignKey("self", null=True, blank=True)
    done_at = models.DateTimeField(null=True, blank=True)

    @property
    def is_overdue(self):
        if self.due_date and date.today() > self.due_date:
            return True
        return False

    # Metadata
    class Meta:
        ordering = ["priority", "parent_task__id", "position"]

    # Methods
    def get_subtasks(self):
        """assume sub-tasks are only allowed to go 1 level deep"""
        if not self.parent_task:
            return Task.objects.all().filter(parent_task=self)
        return None

    def save(self, *args, **kwargs):
        if self.done:
            self.completed_date = datetime.now()
        super(Task, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        Returns the url to access a particular task instance.
        """
        return reverse('task-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the Task object (in Admin site etc.)
        """
        return self.title


class ContextTag(models.Model):
    """
    Context Tag docs
    """

    # Fields
    type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Metadata
    class Meta:
        ordering = ["type"]

    # Methods
    def __str__(self):
        """
        String for representing the Task object (in Admin site etc.)
        """
        return '%s' % (self.name)
