import operator
from uuid import UUID

from flask import Blueprint, g, current_app, session, jsonify, redirect, request
from api.decos import authed
from functools import reduce
from playhouse.shortcuts import model_to_dict
import json

from models.LiteBans import Ban, Kick, Mute, History

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/test')
@authed
def test_endpoint():
    test_ban = Mute.select().where((Mute.id == 15)).get()

    return model_to_dict(test_ban)


@api.route('/stats')
@authed
def server_stats():
    from mcstatus import MinecraftServer

    server = MinecraftServer.lookup("proxy.cavern")

    status = server.status()

    # query = server.query()

    return jsonify({'player_count': status.players.online, 'ping': status.latency, 'online_players': 'All'})


CAN_FILTER = ['id', 'user_uuid', 'moderator_uuid', 'reason', 'moderator', 'user']
CAN_SORT = ['id', 'user_uuid', 'moderator_uuid', 'created_at', 'expires_at']


def search_users(query=None):
    queries = []

    if type(query) == UUID:
        queries.append((History.uuid == query))

    else:
        queries.append((History.name ** '%{}%'.format(query.replace('%', ''))))

    users = History.select().where(reduce(operator.or_, queries))
    if len(users) == 0:
        return []

    return [i.uuid for i in users[:25]]


@api.route('/bans')
@authed
def get_bans():
    user = History.alias()

    page = int(request.values.get('page', 1))
    if page < 1:
        page = 1

    limit = int(request.values.get('limit', 1000))
    if limit < 1 or limit > 1000:
        limit = 1000

    q = Ban.select(Ban)
    q = Ban.select(Ban, user).join(user, on=((Ban.uuid == user.uuid).alias('user')))

    queries = []
    if 'filtered' in request.values:
        filters = json.loads(request.values['filtered'])

        for f in filters:
            if f['id'] not in CAN_FILTER:
                continue

            elif f['id'] == 'reason':
                queries.append(Ban.reason ** ('%' + f['value'].lower().replace('%', '') + '%'))
            elif f['id'] == 'user':
                queries.append(Ban.user_id.in_(search_users(f['value'])))
            elif f['id'] == 'moderator':
                queries.append(Ban.banned_by_name.in_(search_users(f['value'])))
            else:
                queries.append(getattr(Ban, f['id']) == f['value'])

    if queries:
        q = q.where(
            (Ban) &
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
                    getattr(Ban, s['id']).desc()
                )
            else:
                sorted_fields.append(
                    getattr(Ban, s['id'])
                )

    results = {
        "pages": len(q) // limit,
        "bans": []
    }
    if sorted_fields:
        q = q.order_by(*sorted_fields)
    else:
        q = q.order_by(Ban.id.desc())

    q = q.paginate(
        page,
        limit,
    )

    results["bans"] = [jsonify(i) for i in q]

    return results, 200
