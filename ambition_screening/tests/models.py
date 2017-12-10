from django.db import models
from edc_reportable.units import TEN_X_9_PER_LITER, IU_LITER


class BloodResult(models.Model):

    platelets = models.IntegerField(
        null=True,
        blank=True)

    platelets_units = models.CharField(
        verbose_name='units',
        max_length=10,
        choices=((TEN_X_9_PER_LITER, TEN_X_9_PER_LITER), ),
        default=TEN_X_9_PER_LITER,
        null=True,
        blank=True)

    neutrophil = models.DecimalField(
        decimal_places=2,
        max_digits=4,
        null=True,
        blank=True)

    neutrophil_units = models.CharField(
        verbose_name='units',
        max_length=10,
        choices=((TEN_X_9_PER_LITER, TEN_X_9_PER_LITER), ),
        default=TEN_X_9_PER_LITER,
        null=True,
        blank=True)

    alt = models.IntegerField(
        verbose_name='ALT',
        null=True,
        blank=True)

    alt_units = models.CharField(
        verbose_name='units',
        max_length=10,
        choices=((IU_LITER, IU_LITER), ),
        default=IU_LITER,
        null=True,
        blank=True)
