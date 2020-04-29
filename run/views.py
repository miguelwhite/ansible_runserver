from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Job, Playbook
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import JobSerializer, PlaybookSerializer


class JobsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    queryset = Job.objects.all().order_by('-created_on')
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlaybooksViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows jobs to be viewed or edited.
    """
    queryset = Playbook.objects.all().order_by('-name')
    serializer_class = PlaybookSerializer
    permission_classes = [permissions.IsAuthenticated]
