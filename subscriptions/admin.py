from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """ Отображение подписок в административной панели. """
    list_display = ('id', 'course', 'subscriber', 'is_subscribed',)
