from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app import db

users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.get("/me")
@jwt_required()
def get_me():
    """
    Perfil do usuário autenticado
    ---
    tags: [Usuários]
    security:
      - BearerAuth: []
    responses:
      200:
        description: Perfil do usuário
    """
    return jsonify(current_user.to_dict()), 200


@users_bp.put("/me")
@jwt_required()
def update_me():
    """
    Atualizar perfil
    ---
    tags: [Usuários]
    security:
      - BearerAuth: []
    parameters:
      - in: body
        name: body
        schema:
          type: object
          properties:
            name:     {type: string}
            email:    {type: string}
            password: {type: string}
    responses:
      200:
        description: Perfil atualizado
      409:
        description: E-mail já em uso
    """
    data = request.get_json(force=True, silent=True) or {}
    user = current_user

    if "name" in data and (data["name"] or "").strip():
        user.name = data["name"].strip()

    if "email" in data and (data["email"] or "").strip():
        new_email = data["email"].strip().lower()
        if new_email != user.email:
            from app.models.user import User
            if db.session.query(User).filter_by(email=new_email).first():
                return jsonify({"msg": "E-mail já está em uso"}), 409
            user.email = new_email

    if "password" in data and len(data.get("password") or "") >= 6:
        user.set_password(data["password"])

    db.session.commit()
    return jsonify({"msg": "Perfil atualizado com sucesso", "user": user.to_dict()}), 200


@users_bp.delete("/me")
@jwt_required()
def delete_me():
    """
    Excluir conta
    ---
    tags: [Usuários]
    security:
      - BearerAuth: []
    responses:
      200:
        description: Conta removida
    """
    db.session.delete(current_user)
    db.session.commit()
    return jsonify({"msg": "Conta removida com sucesso"}), 200
