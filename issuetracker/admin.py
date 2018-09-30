from django.contrib import admin
from .models import Ticket, Comment, Fund, ProgressLog

# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment
    readonly_fields = ('author', 'comment_date',)

class TicketAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    readonly_fields = (
        'author',
        'type',
        'upvote_user',
        'submission_date',
        'last_modified',
        'upvote_fund',
    )

class FundAdmin(admin.ModelAdmin):
    readonly_fields = ('ticket', 'user', 'fund',)

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Fund, FundAdmin)
admin.site.register(ProgressLog)
