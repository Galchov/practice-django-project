"""
This is an example of creating an abstract and reusable app models, 
which will make the app not being dependent on any other particular apps. 
Therefore, it can be used in other projects without changing its functionality.
"""


from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Tag(models.Model):
    label = models.CharField(max_length=255)


class TaggedItem(models.Model):
    # What tag is applied to what object
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,   # If tag deleted, remove from all associated tagged objects
    )
    # Type of the object (product, video, artice, etc.)
    # ID of the object
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
