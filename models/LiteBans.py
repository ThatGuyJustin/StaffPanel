from database import LBBaseModel
from peewee import IntegerField, DateField, TextField, TimeField, BooleanField, UUIDField


class Ban(LBBaseModel):
    class Meta:
        table_name = 'litebans_bans'

    id = IntegerField(primary_key=True)
    uuid = UUIDField()
    ip = TextField()
    reason = TextField()
    banned_by_uuid = UUIDField()
    banned_by_name = TextField()
    removed_by_uuid = UUIDField
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
    uuid = UUIDField()
    ip = TextField()
    reason = TextField()
    banned_by_uuid = UUIDField()
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
    uuid = UUIDField()
    ip = TextField()
    reason = TextField()
    banned_by_uuid = UUIDField()
    banned_by_name = TextField()
    removed_by_uuid = UUIDField()
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


class History(LBBaseModel):
    class Meta:
        table_nam = 'litebans_history'

    id = IntegerField(primary_key=True)
    date = DateField()
    name = TextField()
    uuid = UUIDField()
    ip = TextField()
