from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Job, Playbook


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class PlaybookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Playbook
        fields = ['uuid', 'name', 'run_command']


class JobSerializer(serializers.HyperlinkedModelSerializer):
    requested_by = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    playbook = serializers.PrimaryKeyRelatedField(
        queryset=Playbook.objects.all(), allow_null=False, required=True
    )

    class Meta:
        model = Job
        fields = ['uuid', 'playbook', 'requested_by', 'created_on', 'status', 'log']
        read_only_fields = ['status', 'log']

    def validate_requested_by(self, requested_by):
        """We will automatically set `requested_by`, so skip default validation"""
        pass

    def create(self, validated_data):
        validated_data['requested_by'] = self.context['request'].user
        job = Job(**validated_data)
        job.save()
        return job
