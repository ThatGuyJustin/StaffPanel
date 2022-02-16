from flask import Blueprint, g, current_app, session, jsonify, redirect, request
from api.decos import authed
from playhouse.shortcuts import model_to_dict

from models.LiteBans import Ban, Kick, Mute

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

    #query = server.query()

    return jsonify({'player_count': status.players.online, 'ping': status.latency, 'online_players': 'All'})