import operator
import re

from flask import Blueprint, g, jsonify, request
from api.decos import authed
from functools import reduce
import json

from models.LiteBans import Ban, Kick, Mute, History

api = Blueprint('api', __name__, url_prefix='/api')

reeeeee_uuid = re.compile(r"\b[0-9a-f]{8}\b-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-\b[0-9a-f]{12}\b")


# @api.route('/test')
# @authed
# def test_endpoint():
#     test_ban = Mute.select().where((Mute.id == 15)).get()
#
#     return model_to_dict(test_ban)


@api.route('/stats')
@authed
def server_stats():
    from mcstatus import MinecraftServer

    server = MinecraftServer.lookup("proxy.cavern")

    status = server.status()

    # query = server.query()

    return jsonify({'player_count': status.players.online, 'ping': status.latency, 'online_players': 'All'})


CAN_FILTER = ['id', 'user_uuid', 'moderator_uuid', 'reason', 'moderator', 'user']
CAN_SORT = ['id', 'user_uuid', 'moderator_uuid', 'created_at', 'expires_at', 'moderator', 'user']


def search_users(query=None):
    queries = []

    if reeeeee_uuid.match(query):
        queries.append((History.uuid == query))

    else:
        queries.append((History.name ** '%{}%'.format(query.replace('%', ''))))

    users = History.select().where(reduce(operator.or_, queries))

    print(users.sql())

    if len(users) == 0:
        return []

    return [i.uuid for i in users[:25]]


@api.route('/infractions')
@authed
def get_infractions():

    infraction = Ban.alias()

    if request.values.get('type'):
        type = request.values.get('type')
        print(g.user.permissions)
        if type == "ban" and g.user.has_permission("litebans.view.ban"):
            pass
        elif type == "mute" and g.user.has_permission("litebans.view.mute"):
            infraction = Mute.alias()
        elif type == "kick" and g.user.has_permission("litebans.view.kick"):
            infraction = Kick.alias()
        else:
            return "Permission Denied", 200
    elif not g.user.has_permission("litebans.view.ban"):
        return "Permission Denied", 200

    page = int(request.values.get('page', 1))
    if page < 1:
        page = 1

    limit = int(request.values.get('limit', 20))
    if limit < 1 or limit > 1000:
        limit = 1000

    q = infraction.select(infraction, History).join(History, on=(infraction.uuid == History.uuid).alias('user'))

    queries = []
    if 'filtered' in request.values:
        filters = json.loads(request.values['filtered'])

        for f in filters:
            if f['id'] not in CAN_FILTER:
                continue

            elif f['id'] == 'id':
                queries.append(infraction.id == int(f['value']))
            elif f['id'] == 'reason':
                queries.append(infraction.reason ** ('%' + f['value'].lower().replace('%', '') + '%'))
            elif f['id'] == 'user':
                if reeeeee_uuid.match(f['value']):
                    queries.append(infraction.uuid ** ('%' + f['value'].replace('%', '') + '%'))
                else:
                    queries.append(History.name ** ('%' + f['value'].replace('%', '') + '%'))
            elif f['id'] == 'moderator':
                if reeeeee_uuid.match(f['value']):
                    queries.append(infraction.banned_by_uuid ** ('%' + f['value'].replace('%', '') + '%'))
                else:
                    queries.append(infraction.banned_by_name ** ('%' + f['value'].replace('%', '') + '%'))
            else:
                queries.append(getattr(infraction, f['id']) == f['value'])

    if queries:
        q = q.where(
            reduce(operator.and_, queries)
        )

    sorted_fields = []
    if 'sorted' in request.values:
        sort = json.loads(request.values['sorted'])

        for s in sort:
            if s['id'] not in CAN_SORT:
                continue

            if s['desc']:
                sorted_fields.append(
                    getattr(infraction, s['id']).desc()
                )
            else:
                sorted_fields.append(
                    getattr(infraction, s['id'])
                )

    results = {
        "pages": len(q) // limit,
        "infractions": []
    }
    if sorted_fields:
        q = q.order_by(*sorted_fields)
    else:
        q = q.order_by(infraction.id.desc())

    q = q.paginate(
        page,
        limit,
    )

    results["infractions"] = [i.serialize(user=i.user) for i in q]

    if not g.user.has_permission("litebans.view.ip"):
        for inf in results["infractions"]:
            inf["ip"] = "REDACTED"
            inf["user"]["ip"] = "REDACTED"

    return results, 200
