from flask import Blueprint, jsonify, request

from src.data.event_handler import EventHandler
from src.http_types.http_request import HttpRequest

event_route_bp = Blueprint("event_route", __name__)


@event_route_bp.route("/events", methods=["POST"])
def create_event():
    http_request = HttpRequest(body=request.json)
    event_handler = EventHandler()

    http_request = event_handler.register(http_request)

    return jsonify(http_request.body), http_request.status_code
