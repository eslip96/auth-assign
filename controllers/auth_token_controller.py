from flask import jsonify, request
from flask_bcrypt import check_password_hash
from datetime import datetime, timedelta
from db import db
from models.auth_token import AuthTokens, auth_token_schema
from models.users import Users


def auth_token_add(req):
    post_data = req.json
    email = post_data.get('email')
    password = post_data.get('password')
    if not email or not password:
        return jsonify({'message': 'invalid login'}), 401

    user_data = db.session.query(Users).filter(Users.email == email).first()
    if user_data is None:
        return jsonify({'message': 'invalid login'}), 401

    is_password_valid = check_password_hash(user_data.password, password)
    if not is_password_valid:
        return jsonify({'message': 'invalid password'}), 401

    now_datetime = datetime.utcnow()
    expiration_datetime = now_datetime + timedelta(hours=12)

    existing_tokens = db.session.query(AuthTokens).filter(AuthTokens.user_id == user_data.user_id).all()
    if existing_tokens:
        for token in existing_tokens:
            if token.expiration < now_datetime:
                db.session.delete(token)

    new_token = AuthTokens(user_data.user_id, expiration_datetime)
    db.session.add(new_token)
    db.session.commit()

    return jsonify({'message': 'auth success', 'account authorized': auth_token_schema.dump(new_token)}), 200
