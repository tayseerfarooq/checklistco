# # clients/serializers.py
# from rest_framework import serializers
# from .models import Service, TimelineTask

# class TimelineTaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TimelineTask
#         fields = ['id', 'title', 'description', 'due_date', 'status', 'completed_at']

# class ServiceSerializer(serializers.ModelSerializer):
#     milestones = TimelineTaskSerializer(source='timeline_tasks', many=True, read_only=True)
#     progress = serializers.SerializerMethodField()

#     class Meta:
#         model = Service
#         fields = ['id', 'title', 'description', 'status', 'start_date', 'end_date', 'progress', 'milestones']

#     def get_progress(self, obj):
#         tasks = obj.timeline_tasks.all()
#         total = tasks.count()
#         if total == 0:
#             return 0
#         done = tasks.filter(status='done').count()
#         return int(done / total * 100)


# clients/serializers.py
# clients/serializers.py
from rest_framework import serializers
from .models import Service, TimelineTask

class TimelineTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimelineTask
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'current',
            'created_at',
            'completed_at'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    milestones = TimelineTaskSerializer(source='timeline_tasks', many=True, read_only=True)
    progress = serializers.SerializerMethodField()

    class Meta:
        model = Service
        fields = [
            'id',
            'title',
            'status',
            'progress',
            'milestones'
        ]

    def get_progress(self, obj):
        tasks = obj.timeline_tasks.all()
        total = tasks.count()
        if total == 0:
            return 0
        done = tasks.filter(completed=True).count()
        return int(done / total * 100)