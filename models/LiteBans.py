from database import LBBaseModel
from peewee import IntegerField, DateField, TextField, TimeField, BooleanField, UUIDField


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

    def serialize(self, user=None, include_metadata=False):
        base = {
            "id": str(self.id), "uuid": self.uuid, "ip": self.ip,
            "reason": self.reason, "banned_by_uuid": self.banned_by_uuid, "banned_by_name": self.banned_by_name,
            "removed_by_uuid": self.removed_by_uuid, "removed_by_name": self.removed_by_name, "removed_by_date": self.removed_by_date,
            "time": self.time, "until": self.until, "server_scope": self.server_scope, "server_origin": self.server_origin,
            "silent": self.silent, "ipban": self.ipban, "ipban_wildcard": self.ipban_wildcard, "active": self.active,
            "removed_by_reason": self.removed_by_reason, "user": (user and user.serialize()) or {'uuid': str(self.user_id), "ip": self.ip}
        }

        if include_metadata:
            base['metadata'] = self.metadata

        return base


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

    def serialize(self, user=None, include_metadata=False):
        base = {
            "id": str(self.id), "uuid": self.uuid, "ip": self.ip,
            "reason": self.reason, "banned_by_uuid": self.banned_by_uuid, "banned_by_name": self.banned_by_name,
            "time": self.time, "until": self.until, "server_scope": self.server_scope, "server_origin": self.server_origin,
            "silent": self.silent, "ipban": self.ipban, "ipban_wildcard": self.ipban_wildcard, "active": self.active,
            "user": (user and user.serialize()) or {'uuid': str(self.user_id), "ip": self.ip}
        }

        if include_metadata:
            base['metadata'] = self.metadata

        return base


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

    def serialize(self, user=None, include_metadata=False):
        base = {
            "id": str(self.id), "uuid": self.uuid, "ip": self.ip,
            "reason": self.reason, "banned_by_uuid": self.banned_by_uuid, "banned_by_name": self.banned_by_name,
            "removed_by_uuid": self.removed_by_uuid, "removed_by_name": self.removed_by_name, "removed_by_date": self.removed_by_date,
            "time": self.time, "until": self.until, "server_scope": self.server_scope, "server_origin": self.server_origin,
            "silent": self.silent, "ipban": self.ipban, "ipban_wildcard": self.ipban_wildcard, "active": self.active,
            "removed_by_reason": self.removed_by_reason, "user": (user and user.serialize()) or {'uuid': str(self.user_id), "ip": self.ip}
        }

        if include_metadata:
            base['metadata'] = self.metadata

        return base


class History(LBBaseModel):
    class Meta:
        table_name = 'litebans_history'

    id = IntegerField(primary_key=True)
    date = DateField()
    name = TextField()
    uuid = TextField()
    ip = TextField()

    def serialize(self, include_metadata=False):
        base = {
            "id": str(self.id), "uuid": self.uuid, "ip": self.ip,
            "name": self.name, "date": self.date
        }

        if include_metadata:
            base['metadata'] = self.metadata

        return base
