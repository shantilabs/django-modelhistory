Model changes tracking.

Install.
```!shell
pip install -e git://github.com/shantilabs/django-modelhistory.git#egg=holidays
```

Usage:
```!python
from django.db import models
from django.db.models.signals import post_save

from modelhistory import create_history_model


class Customer(models.Model):
    address = models.TextField()
    name = models.CharField(max_length=100)
    email = models.EmailField()


CustomerHistory = create_history_model(Customer, (
    'address',
    'email',
))

post_save.connect(CustomerHistory.save_diff, sender=CustomerHistory.model_class)

```
