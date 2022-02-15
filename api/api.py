# -*- coding: utf-8 -*-
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