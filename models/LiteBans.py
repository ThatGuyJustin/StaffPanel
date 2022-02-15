from database import LBBaseModel
from peewee import IntegerField, DateField, TextField, TimeField, BooleanField


class Ban(LBBaseModel):
    class Meta:
        table_name = 'litebans_bans'

    id = IntegerField(primary_key=True)
    uuid = TextField()
    ip = TextField()
    reason = TextField()
    banned_by_uuid = TextField()
    banned_by_name = TextField()
    removed_by_uuid = TextField()
    removed_by_name = TextField()
    removed_by_date = DateField()
    time = TimeField()
    until = TimeField()
    server_scope = TextField()
    server_origin = TextField()
    silent = BooleanField()
    ipban = BooleanField()
    ipban_wildcard = BooleanField()
    active = BooleanField()
    removed_by_reason = TextField()


class Kick(LBBaseModel):
    class Meta:
        table_name = 'litebans_kicks'

    id = IntegerField(primary_key=True)
    uuid = TextField()
    ip = TextField()
    reason = TextField()
    banned_by_uuid = TextField()
    banned_by_name = TextField()
    time = TimeField()
    until = TimeField()
    server_scope = TextField()
    server_origin = TextField()
    silent = BooleanField()
    ipban = BooleanField()
    ipban_wildcard = BooleanField()
    active = BooleanField()

class Mute(LBBaseModel):
    class Meta:
        table_name = 'litebans_mutes'

    id = IntegerField(primary_key=True)
    uuid = TextField()
    ip = TextField()
    reason = TextField()
    banned_by_uuid = TextField()
    banned_by_name = TextField()
    removed_by_uuid = TextField()
    removed_by_name = TextField()
    removed_by_date = DateField()
    time = TimeField()
    until = TimeField()
    server_scope = TextField()
    server_origin = TextField()
    silent = BooleanField()
    ipban = BooleanField()
    ipban_wildcard = BooleanField()
    active = BooleanField()
    removed_by_reason = TextField()
