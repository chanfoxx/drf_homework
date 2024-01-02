from django.contrib import admin

from online_courses.models import Lesson, Course


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """ Отображение получателей в административной панели. """
    list_display = ('id', 'title',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """ Отображение получателей в административной панели. """
    list_display = ('id', 'title',)
