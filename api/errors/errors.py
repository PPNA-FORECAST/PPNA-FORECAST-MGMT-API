from flask import Flask, request, jsonify

def handle_not_found_error(error): # Handles 404 errors
    message = str(error)
    return jsonify({'msg': message}), 404

def handle_forbidden_error(error): # Handles 403 error
    message = str(error)
    return jsonify({'msg': message}), 403

def handle_conflict_error(error): # Handles 409 errors
    message = str(error)
    return jsonify({'msg': message}), 409

def handle_unauthorized_error(error): # Handles 401 errors
    message = str(error)
    return jsonify({'msg': message}), 401

def handle_bad_request_error(error): # Handles 400 errors
    message = str(error)
    return jsonify({'msg': message}), 400

