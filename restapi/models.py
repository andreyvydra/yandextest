from django.db import models


class OfferAndCategory(models.Model):
    class ElementTypes(models.TextChoices):
        CATEGORY = 'CATEGORY'
        OFFER = 'OFFER'

    uuid = models.UUIDField(unique=True)
    type = models.CharField(max_length=8, choices=ElementTypes.choices)

    name = models.CharField(max_length=128)
    price = models.PositiveIntegerField(null=True)
    date = models.DateTimeField()

    parent = models.ForeignKey(
        "OfferAndCategory",
        related_name='children',
        to_field='uuid',
        on_delete=models.CASCADE,
        null=True
    )
