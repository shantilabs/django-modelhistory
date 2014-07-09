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
        current_state = dict((k, getattr(instance, k, None)) for k in fields)

        prev_diff = first_or_none(history_class.objects.filter(instance=instance))
        if prev_diff and prev_diff.raw_state:
            prev_state = prev_diff.state 
        else:
            prev_state = dict((k, None) for k in fields)

        diff = []
        for k in fields:
            v1 = prev_state.get(k)
            v2 = current_state.get(k)
            if v1 != v2:
                diff.append((k, v1, v2))

        if diff:
            logger.info('diff: %r', diff)
            h = history_class(instance=instance)
            h.diff = diff
            h.state = current_state
            h.save()
        else:
            logger.info('empty diff')

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

