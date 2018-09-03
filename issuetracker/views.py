from django.shortcuts import render

# Create your views here.
def issuetrackerhome(request):
    return render(request, "issue_tracker_home.html")
