from django.db.models import Model, CharField, IntegerField, PositiveIntegerField, TextField, Manager, ForeignKey, CASCADE, DateTimeField, JSONField
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
    show_current = ForeignKey('show', on_delete=CASCADE, blank=True, null=True)
class actionPath(Model):

    objects = Manager()
    category = CharField(max_length=255, unique=True)
    parent = ForeignKey('self', null=True, blank=True, on_delete=CASCADE)
    def __str__(self) -> str:
        path_parent = self.parent
        tries = 0
        running_path:str = "/" + str(self.category)
        if not path_parent:
            return running_path
        while True:
            running_path = "/" + str(path_parent.category) + running_path
            if not path_parent.parent:
                break
            path_parent:actionPath = path_parent.parent
            tries += 1
            if tries > 100:
                break
        return str(running_path)
class action(Model):
    
    objects = Manager()
    path = ForeignKey(actionPath, on_delete=CASCADE, blank=True, null=True)
    name = CharField(max_length=255)
    channel = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(127)]
    )
    key = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(127)]
    )
    value = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(127)]
    )

    class Meta:
        unique_together = ('path', 'name')

    def __str__(self) -> str:
        return str(self.name)
class show(Model):
    objects = Manager()
    name = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    actions = JSONField(blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.name)