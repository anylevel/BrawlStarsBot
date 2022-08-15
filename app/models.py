from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    token = fields.CharField(max_length=9, default=None)
    clan_token = fields.CharField(max_length=9, null=True)
    player = fields.ForeignKeyField('models.Player', related_name='player')

    def __str__(self):
        return f'{self.name}:{self.token}:{self.clan_token}'


class Player(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100, null=True)
    token = fields.CharField(max_length=9, default=None)
    trophies = fields.IntField(null=True)
    battle_log = fields.data.JSONField(null=True)

    # def __str__(self):
    #     return f'{self.name}:{self.trophies}'
# TODO сделать еще одну модель типа токен-battlelog и сделать foreign key! разобраться с ним!
# TODO подумать нужно ли добавлять поля типа процент выйграша проигрыш и тд
