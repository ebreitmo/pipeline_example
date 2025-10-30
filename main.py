#!/usr/bin/env python
"""
Mascot: a microservice for serving mascot data
"""
import json

from flask import Flask, abort, jsonify, make_response

API = Flask(__name__)

# Load the data
with open("data.json", "r", encoding="utf8") as data:
    MASCOTS = json.load(data)


@API.route("/health", methods=["GET"])
def health_check():
    """
    Function: health_check
    Input: none
    Returns: A simple health status response
    """
    return jsonify(
        {"status": "healthy", "service": "mascot", "mascots_loaded": len(MASCOTS)}
    )


@API.route("/", methods=["GET"])
def get_mascots():
    """
    Function: get_mascots
    Input: none
    Returns: A list of mascot objects
    """
    return jsonify(MASCOTS)


@API.route("/<guid>", methods=["GET"])
def get_mascot(guid):
    """
    Function: get_mascot
    Input: a mascot GUID
    Returns: The mascot object with GUID matching the input
    """
    for mascot in MASCOTS:
        if guid == mascot["guid"]:
            return jsonify(mascot)
    abort(404)
    return None


@API.errorhandler(404)
def not_found(error):
    """
    Function: not_found
    Input: The error
    Returns: HTTP 404 with r
    """
    return make_response(jsonify({"error": str(error)}), 404)


if __name__ == "__main__":
    from waitress import serve

    serve(API, host="0.0.0.0", port=8080)
