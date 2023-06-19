from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class ChatRecordsModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    fat_count = models.IntegerField(default=0)
    stupid_count = models.IntegerField(default=0)
    dumb_count = models.IntegerField(default=0)
    total_calls = models.IntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.total_calls = self.fat_count + self.stupid_count + self.dumb_count
        super(ChatRecordsModel, self).save(*args, **kwargs)

    class Meta:
        db_table = 'chat_records'
