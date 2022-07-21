from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    token = fields.CharField(max_length=10, default=None)

    def __str__(self):
        return f'{self.name}:{self.token}'
