from django.db import models
from django.contrib.postgres.fields import JSONField


class Video(models.Model):

    def __str__(self):
        return self.name

    name = models.CharField(max_length=100, unique=True)
    v_length = models.CharField(max_length=100)
    topic = models.CharField(max_length=100)
    is_processed = models.BooleanField(default=False)
    video = models.CharField(max_length=200)
    navigation = JSONField(default=None, null=True)


class Frame(models.Model):
    name = models.CharField(max_length=100, unique=True)
    f_number = models.IntegerField()
    f_type = models.CharField(max_length=100)
    image = models.ImageField(upload_to="frames")
    timestamp = models.IntegerField()
    content = models.TextField(default=None, null=True)
    is_anchor = models.BooleanField(default=False, null=True)
    topics = JSONField(default=None, null=True)
    anchor_label = models.CharField(max_length=100, default=None, null=True)
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )

