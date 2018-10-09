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
        'upvote_fund',
        'upvote_user',
        'submission_date',
        'last_modified',
    )
    exclude = (
        'upvote_fund',
        'upvote_user',
        'submission_date',
        'last_modified',
    )

    """
    Referring code from:
    https://stackoverflow.com/questions/17613559/django-readonly-field-only-on-change-but-not-when-creating
    """
    def get_readonly_fields(self, request, obj=None):
        if obj: #This is the case when obj is already created i.e. it's an edit
            return ['author', 'type']
        else:
            return []

class FundAdmin(admin.ModelAdmin):
    readonly_fields = ('ticket', 'user', 'fund',)

admin.site.register(Ticket, TicketAdmin)
admin.site.register(Fund, FundAdmin)
admin.site.register(ProgressLog)
