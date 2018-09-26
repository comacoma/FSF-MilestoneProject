import django_filters
from .models import Ticket, ProgressLog

class TicketFilter(django_filters.FilterSet):
    class Meta:
        model = Ticket
        fields = {
            'title': ['icontains'],
            'type': ['exact'],
        }
