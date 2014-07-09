Model changes tracking.

Install.
```!shell
pip install -e git://github.com/shantilabs/django-modelhistory.git#egg=holidays
```

Usage:
```!python
# models.py
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

post_save.connect(CustomerHistory.save_diff, sender=Customer)


# admin.py (optional)
from django.contrib import admin
from modelhistory.admin import HistoryInline
from models import CustomerHistory

class CustomerHistoryInline(HistoryInline):
    model = CustomerHistory

class CustomerAdmin(admin.ModelAdmin):
    inlines = [CustomerHistoryInline]

admin.site.register(models.Customer, CustomerAdmin)


# settings.py (optional)

MODELHISTORY_SERIALIZER = 'modelhistory.serializers.PickleSerializer'  # default
#MODELHISTORY_SERIALIZER = 'modelhistory.serializers.JsonSerializer'  
 
```

Sample template usage:
```
<table class="table table-condensed">
    {% for h in customer.history.all %}
        <thead>
            <tr>
                <th colspan="3" class="text-center">{{ h.datetime }}</th>
            </tr>
        </thead>
        <tbody>
            {% for k, v1, v2 in h.diff %}
                <tr>
                    <th>{{ k }}</th>
                    <td>{{ v1|default:'-' }}</td>
                    <td>{{ v2|default:'-' }}</td>
                </tr>
            {% endfor %}
        </tbody>
    {% endfor %}
</table>
```
