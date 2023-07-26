from django.core import checks
from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):

    description = "Ordering field on a unique filed"

    def __init__(self, unique_for_filed=None, *args, **kwargs):
        self.unique_for_filed = unique_for_filed
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        return [
            *super().check(**kwargs),
            *self._check_for_field_attribute(**kwargs),
        ]

    def _check_for_field_attribute(self, **kwargs):
        if self.unique_for_filed is None:
            return [
                checks.Error('OrderField must define a unique')
            ]
        elif self.unique_for_filed not in [f.name for f in self.model._meta.get_fields()]:
            return [
                checks.Error('OrderField entered does not match')
            ]
        return []

    def pre_save(self, model_instance, add):

        if getattr(model_instance, self.attname) is None:
            qs = self.model.objects.all()
            try:
                query = {self.unique_for_filed : getattr(model_instance, self.unique_for_filed)}
                qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1

            except ObjectDoesNotExist:
                value = 1

            return value

        else:
            return super().pre_save(model_instance, add)


