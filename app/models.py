from tortoise.models import Model
from tortoise import fields


class User(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    token = fields.CharField(max_length=9, default=None)
    club_token = fields.CharField(max_length=9, null=True)

    def __str__(self):
        return f'{self.name}:{self.token}:{self.club_token}'


class Player(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    token = fields.CharField(max_length=9)
    trophies = fields.IntField()
    highest_trophies = fields.IntField()
    battle_log = fields.data.JSONField(default=list())
    user = fields.OneToOneField('models.User', related_name='players')

    class Meta:
        ordering = ["-trophies", "-highest_trophies"]

    def __str__(self):
        return f'Name:{self.name}\n\t\t  Token:#{self.token}\n\t\t  Trophies:{self.trophies}\n'


class Club(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    token = fields.CharField(max_length=9)
    trophies = fields.IntField()
    user = fields.OneToOneField('models.User', related_name='clans')

    class Meta:
        ordering = ["-trophies", "name"]

    def __str__(self):
        return f'Name:{self.name}\n\t\t  Token:#{self.token}\n\t\t  Trophies:{self.trophies}\n'

# TODO сделать еще одну модель типа токен-battlelog и сделать foreign key! разобраться с ним!
# TODO подумать нужно ли добавлять поля типа процент выйграша проигрыш и тд
