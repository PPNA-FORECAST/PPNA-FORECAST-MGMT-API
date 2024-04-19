from flask import Flask, request, jsonify

def handle_not_found_error(error): #Handles 404 errors
    message = str(error)
    return jsonify({'error': message}), 404




