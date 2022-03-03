from peewee import IntegerField, DateField, TextField, Field, BooleanField

from database import CPBaseModel


class CPUser(CPBaseModel):
    class Meta:
        table_name = "co_user"

    rowid = IntegerField()
    time = DateField()
    user = TextField()
    uuid = TextField()


class ArtMap(CPBaseModel):
    class Meta:
        table_name = "co_art_map"

    rowid = IntegerField()
    id = IntegerField()
    art = TextField()


class Block(CPBaseModel):
    class Meta:
        table_name = "co_block"

    rowid = IntegerField()
    time = DateField()
    user = TextField()
    wid = IntegerField()
    x = IntegerField()
    y = IntegerField()
    z = IntegerField()
    type = IntegerField()
    data = IntegerField()
    meta = Field()
    action = Field()
    rolled_back = BooleanField()


class BlockDataMap(CPBaseModel):
    class Meta:
        table_name = "co_blockdata_map"

    rowid = IntegerField()
    id = IntegerField()
    data = TextField()


class Chat(CPBaseModel):
    class Meta:
        table_name = "co_chat"

    rowid = IntegerField()
    time = DateField()
    user = TextField()
    wid = IntegerField()
    x = IntegerField()
    y = IntegerField()
    z = IntegerField()
    message = TextField()


class Commands(CPBaseModel):
    class Meta:
        table_name = "co_command"

    rowid = IntegerField()
    time = DateField()
    user = TextField()
    wid = IntegerField()
    x = IntegerField()
    y = IntegerField()
    z = IntegerField()
    message = TextField()

