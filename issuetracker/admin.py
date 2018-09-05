from django.contrib import admin
from .models import Ticket, Comment

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment

class TicketAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Comment)
