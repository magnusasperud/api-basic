from app import app
from functools import wraps
from flask import request, jsonify
import datetime
import jwt


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if ' ' in auth_header:
                token = auth_header.split(" ")[1]

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

@app.route('/token', methods=['POST'])
def generate_token():
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode(
        {
            'exp': expiration
        }, 
        app.config['SECRET_KEY'], 
        algorithm="HS256"
    )

    return jsonify({
        'token': token,
        'expiration': expiration.strftime("%Y-%m-%d %H:%M:%S")
    })