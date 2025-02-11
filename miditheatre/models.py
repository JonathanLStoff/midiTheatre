from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import (
    CASCADE,
    SET_NULL,
    CharField,
    DateTimeField,
    ForeignKey,
    IntegerField,
    JSONField,
    Manager,
    Model,
    PositiveIntegerField,
    TextField,
    UUIDField,
)

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
    class Meta:
        unique_together = ('category', 'parent')
        
class action(Model):
    
    objects = Manager()
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    path = ForeignKey(actionPath, on_delete=CASCADE, blank=True, null=True)
    name = CharField(max_length=255)
    channel = IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(15)]
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
    
    def delete(self, using=None, keep_parents=False):
        for show_mod in show.objects.all():
            for index, action in enumerate(show_mod.actions):
                if action == self.id:
                    show_mod.actions.pop(index) # Remove the action from the show
                    show_mod.save()
        return super().delete(using=using, keep_parents=keep_parents)
class show(Model):
    objects = Manager()
    name = CharField(max_length=255)
    description = TextField(blank=True, null=True)
    created = DateTimeField(auto_now_add=True)
    updated = DateTimeField(auto_now=True)
    actions = JSONField(blank=True, null=True, default=list) # List of action {id: str, type: float}
    selected_action = IntegerField(blank=True, null=True, default=0)
    
    def __str__(self) -> str:
        return str(self.name)
    
class link_tracker(Model):
    objects = Manager()
    linked_actions = JSONField(blank=True, null=True, default=list)
    name = CharField(max_length=255)
    id = UUIDField(primary_key=True, default=uuid4, editable=False)
    
    
    def __str__(self) -> str:
        return str(self.name)