from django.contrib import admin
from payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """ Отображение получателей в административной панели. """
    list_display = ('id', 'payday', 'paid_course', 'paid_lesson', 'user',)
