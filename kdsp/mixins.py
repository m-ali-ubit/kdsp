from django.db import models


class CreateUpdateMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    last_updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True
