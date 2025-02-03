from django.db.models import Model, CharField, IntegerField, PositiveIntegerField, Manager
from django.core.validators import MinValueValidator, MaxValueValidator

class action(Model):
    
    objects = Manager()
    
    name:CharField = CharField(max_length=255, unique=True)
    channel:IntegerField = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(127)]
    )
    key:IntegerField = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(127)]
    )
    value:IntegerField = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(127)]
    )
    order:PositiveIntegerField = PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return str(self.name)