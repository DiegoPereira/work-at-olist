from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Channel(models.Model):
    name = models.CharField(max_length=256, unique=True,
                            db_column='name', blank=True)

    class Meta:
        ordering = ['-id']


class Categories(MPTTModel):
    name = models.CharField(max_length=256)
    channel = models.ForeignKey(Channel, db_column='channelName', blank=True)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']
