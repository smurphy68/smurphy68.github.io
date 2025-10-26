from flask import Flask, request, jsonify
from db_controller import DatabaseController
from onion import *
import uuid
import requests
import json

app = Flask(__name__)
db = DatabaseController()

@app.route('/device_login', methods=['POST'])
def device_login():
    content = request.get_json()
    if not content or 'passkey' not in content:
        return "Bad Request", 400
    passkey = content['passkey'] 
    if db.validate_user(passkey):
        auth_token = str(uuid.uuid4())
        _ = db.add_session(auth_token)

        global return_address, headers
        return_address = request.remote_addr
        headers = {'Content-Type': 'application/json'}

        return jsonify({"message": "Login successful", "auth_token": auth_token}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/test', methods=['POST'])
@authentication_required(db)
def test():
    print(request.get_json())
    auth_token = request.get_json()["auth_token"]
    return jsonify({"message": "auth_token accepted", "auth_token": auth_token + " BUT VERIFIED"})

@app.route('/lights', methods=["GET", "POST"])
@authentication_required(db)
def lights():
    print("Turning on the lights")
    test = json.dumps({"request": "humble"})
    req = requests.request("GET", f"http://{return_address}:5000", headers=headers, data=test)
    print(req)
    return "test"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)