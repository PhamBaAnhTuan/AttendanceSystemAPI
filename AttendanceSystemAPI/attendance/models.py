# from django.db import models
# import uuid
# from django.utils import timezone

# class AttendanceSession(models.Model):
#    id = models.CharField(
#       max_length=10, primary_key=True, editable=False, unique=True
#    )   
#    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
#    scope = models.TextField(default="admin", null=True, blank=True)
#    created_at = models.DateTimeField(default=timezone.now)
#    updated_at = models.DateTimeField(auto_now=True)

#    def __str__(self):
#       return self.name
   
#    def get_scope(self):
#       return self.scope.strip().split()
   
#    class Meta:
#       db_table = "roles"