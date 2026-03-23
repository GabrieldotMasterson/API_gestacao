from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, current_user
from app import db
from app.models.user import User
from app.models.user_progress import UserProgress

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.post("/register")
def register():
    """
    Cadastrar novo usuário
    ---
    tags: [Autenticação]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [name, email, password]
          properties:
            name:     {type: string, example: Maria Silva}
            email:    {type: string, example: maria@email.com}
            password: {type: string, example: "123456"}
    responses:
      201:
        description: Usuário criado e token gerado
      400:
        description: Dados inválidos
      409:
        description: E-mail já cadastrado
    """
    data     = request.get_json(force=True, silent=True) or {}
    name     = (data.get("name")     or "").strip()
    email    = (data.get("email")    or "").strip().lower()
    password =  data.get("password") or ""

    if not name or not email or not password:
        return jsonify({"msg": "Nome, e-mail e senha são obrigatórios"}), 400
    if len(password) < 6:
        return jsonify({"msg": "A senha deve ter pelo menos 6 caracteres"}), 400
    if db.session.query(User).filter_by(email=email).first():
        return jsonify({"msg": "E-mail já cadastrado"}), 409

    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    progress = UserProgress(user_id=user.id)
    db.session.add(progress)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "user": user.to_dict()}), 201


@auth_bp.post("/login")
def login():
    """
    Login do usuário
    ---
    tags: [Autenticação]
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required: [email, password]
          properties:
            email:    {type: string, example: maria@email.com}
            password: {type: string, example: "123456"}
    responses:
      200:
        description: Login realizado, token retornado
      401:
        description: Credenciais inválidas
    """
    data     = request.get_json(force=True, silent=True) or {}
    email    = (data.get("email")    or "").strip().lower()
    password =  data.get("password") or ""

    if not email or not password:
        return jsonify({"msg": "E-mail e senha são obrigatórios"}), 400

    user = db.session.query(User).filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"msg": "E-mail ou senha inválidos"}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token, "user": user.to_dict()}), 200


@auth_bp.get("/me")
@jwt_required()
def me():
    """
    Dados do usuário autenticado
    ---
    tags: [Autenticação]
    security:
      - BearerAuth: []
    responses:
      200:
        description: Dados do usuário atual
      401:
        description: Não autenticado
    """
    return jsonify(current_user.to_dict()), 200
