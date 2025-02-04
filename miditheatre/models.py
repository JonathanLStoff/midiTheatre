from django.db.models import Model, CharField, IntegerField, PositiveIntegerField, Manager
from django.core.validators import MinValueValidator, MaxValueValidator

THEME_CHOICES = [
            ('light', 'Light Mode'),
            ('dark', 'Dark Mode'),
        ]
class settingUser(Model):
    objects = Manager()
    theme = CharField(max_length=10, choices=THEME_CHOICES)
    go_key = IntegerField(
                        validators=[MinValueValidator(1), MaxValueValidator(256)],
                        help_text="Keycode for 'Go' action"
                    )
    stop_key = IntegerField(
                        validators=[MinValueValidator(1), MaxValueValidator(256)],
                        help_text="Keycode for 'Stop' action"
                    )
class actionPath(Model):
    objects=Manager()
    category = CharField(max_length=255, unique=True)
    parent = CharField(max_length=255, unique=True)
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