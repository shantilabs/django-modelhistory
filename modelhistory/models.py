from django.db import models
from django.conf import settings
from django.utils.module_loading import import_by_path


serializer_name = getattr(settings, 'MODELHISTORY_SERIALIZER', 'modelhistory.serializers.PickleSerializer')
serializer = import_by_path(serializer_name)()


class AbstractHistoryModel(models.Model):
    datetime = models.DateTimeField(auto_now_add=True, db_index=True)
    raw_diff = models.TextField(editable=False, blank=True, default='')
    raw_state = models.TextField(editable=False, blank=True, default='')

    def get_diff(self):
        return serializer.loads(self.raw_diff)

    def set_diff(self, val):
        self.raw_diff = serializer.dumps(val)

    diff = property(get_diff, set_diff)

    def get_state(self):
        return serializer.loads(self.raw_state)

    def set_state(self, val):
        self.raw_state = serializer.dumps(val)

    state = property(get_state, set_state)

    def __unicode__(self):
        return u';\n '.join(u'%s: %s => %s' % t for t in self.diff) or '(empty)'

    class Meta:
        abstract = True
        ordering = ('-datetime',)
