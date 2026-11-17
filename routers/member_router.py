from flask import Blueprint, jsonify, request

from services import member_service

bp = Blueprint("members", __name__)


@bp.route("/members", methods=["GET"])
def list_members():
    return jsonify(member_service.list_members())


@bp.route("/members/<int:member_id>", methods=["GET"])
def get_member(member_id):
    return jsonify(member_service.get_member(member_id))


@bp.route("/members", methods=["POST"])
def create_member():
    data = request.get_json(silent=True) or {}
    return jsonify(member_service.create_member(data)), 201


@bp.route("/members/<int:member_id>/loans", methods=["GET"])
def member_loans(member_id):
    return jsonify(member_service.get_member_loans(member_id))
