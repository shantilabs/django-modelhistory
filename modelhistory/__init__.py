import logging

from django.db.models import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver

from models import AbstractHistoryModel


logger = logging.getLogger(__name__)


def create_history_model(model_class, fields, related_name='history'):
    history_class = type(model_class.__name__ + 'History', (AbstractHistoryModel,), dict(
        instance=ForeignKey(model_class, related_name=related_name),
        Meta=type('Meta', (object, AbstractHistoryModel.Meta,), dict()),
        __module__=model_class.__module__,
    ))

    def save_diff(sender, instance, **kwargs):
    	logger.info('save diff for %s', instance)

        prev_diff = first_or_none(history_class.objects.filter(instance=instance))
        if prev_diff:
            prev = dict((k, v2) for k, _v1, v2 in prev_diff.diff)
        else:
            prev = {}

    	logger.info('previous data: %s', prev)

        diff = []
        for k in fields:
            v1 = prev.get(k)
            v2 = getattr(instance, k, None)
            if v1 != v2:
                diff.append((k, v1, v2))

        if diff:
            h = history_class(instance=instance)
            h.diff = diff
            h.save()

    # FIXME: doesnt work
    # post_save.connect(save_diff, sender=model_class)

    # hack
    history_class.save_diff = staticmethod(save_diff)
    history_class.model_class = models

    return history_class


def first_or_none(lst):
    try:
        return lst[0]
    except IndexError:
        return None

