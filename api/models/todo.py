from tortoise.models import Model
from tortoise.fields import IntField, BooleanField, CharField


class Todo(Model):
    id = IntField(pk=True)
    task = CharField(max_length=100, null=False)
    done = BooleanField(default=False, null=False)
