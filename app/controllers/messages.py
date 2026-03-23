from datetime import date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    jwt_required, current_user, get_jwt_identity, verify_jwt_in_request
)
from app import db
from app.models.message import Message, Category
from app.models.saved_message import SavedMessage
from app.models.user_progress import UserProgress

messages_bp = Blueprint("messages", __name__, url_prefix="/messages")


def _pick_message(slug: str, week: int = 1):
    day = date.today().timetuple().tm_yday
    cat = db.session.query(Category).filter_by(slug=slug).first()
    if not cat:
        return None
    msgs = (db.session.query(Message)
            .filter(Message.category_id == cat.id, Message.active.is_(True),
                    Message.week_min <= week, Message.week_max >= week)
            .order_by(Message.day_index).all())
    if not msgs:
        msgs = (db.session.query(Message)
                .filter(Message.category_id == cat.id, Message.active.is_(True))
                .order_by(Message.day_index).all())
    if not msgs:
        return None
    return msgs[day % len(msgs)].to_dict()


def _week_from_token() -> int:
    try:
        verify_jwt_in_request(optional=True)
        uid = get_jwt_identity()
        if uid:
            p = db.session.query(UserProgress).filter_by(user_id=int(uid)).first()
            if p:
                return p.current_week
    except Exception:
        pass
    return 1


# ── Public message endpoints ──────────────────────────────────────────────────

@messages_bp.get("/daily")
def get_daily():
    """Mensagem do dia --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("daily", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/health")
def get_health():
    """Dica de saúde --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("health", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/nutrition")
def get_nutrition():
    """Nutrição --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("nutrition", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/curiosity")
def get_curiosity():
    """Curiosidade --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("curiosity", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/medical")
def get_medical():
    """Alerta médico --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("medical", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/categories")
def get_categories():
    """Categorias --- tags: [Mensagens] responses: {200: {description: ok}}"""
    return jsonify([c.to_dict() for c in db.session.query(Category).all()]), 200


# ── Saved messages (JWT required) ─────────────────────────────────────────────

@messages_bp.get("/saved")
@jwt_required()
def get_saved():
    """Mensagens salvas --- tags: [Favoritos] security: [{BearerAuth: []}] responses: {200: {description: ok}}"""
    saved = (db.session.query(SavedMessage)
             .filter_by(user_id=current_user.id)
             .order_by(SavedMessage.saved_at.desc()).all())
    return jsonify([s.to_dict() for s in saved]), 200


@messages_bp.post("/saved")
@jwt_required()
def save_message():
    """
    Salvar mensagem
    ---
    tags: [Favoritos]
    security: [{BearerAuth: []}]
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [message_id]
            properties:
              message_id:
                type: integer
                example: 1
    responses:
      201: {description: Salvo}
      404: {description: Não encontrado}
    """
    # FIX 422: aceita tanto JSON body quanto form data
    data = request.get_json(force=True, silent=True) or {}
    raw_id = data.get("message_id")

    if raw_id is None:
        return jsonify({"msg": "message_id é obrigatório"}), 400

    try:
        message_id = int(raw_id)
    except (ValueError, TypeError):
        return jsonify({"msg": "message_id deve ser um número inteiro"}), 400

    msg = db.session.get(Message, message_id)
    if not msg:
        return jsonify({"msg": f"Mensagem {message_id} não encontrada"}), 404

    existing = (db.session.query(SavedMessage)
                .filter_by(user_id=current_user.id, message_id=message_id).first())
    if existing:
        return jsonify({"msg": "Mensagem já salva", "saved": existing.to_dict()}), 200

    saved = SavedMessage(user_id=current_user.id, message_id=message_id)
    db.session.add(saved)
    db.session.commit()
    return jsonify({"msg": "Salva com sucesso", "saved": saved.to_dict()}), 201


@messages_bp.delete("/saved/<int:saved_id>")
@jwt_required()
def unsave_message(saved_id: int):
    """Remove salvo por ID do registro --- tags: [Favoritos] security: [{BearerAuth: []}] responses: {200: {description: ok}}"""
    saved = db.session.get(SavedMessage, saved_id)
    if not saved or saved.user_id != current_user.id:
        return jsonify({"msg": "Não encontrado"}), 404
    db.session.delete(saved)
    db.session.commit()
    return jsonify({"msg": "Removido dos favoritos"}), 200


@messages_bp.delete("/saved/by-message/<int:message_id>")
@jwt_required()
def unsave_by_message(message_id: int):
    """Remove salvo por ID da mensagem --- tags: [Favoritos] security: [{BearerAuth: []}] responses: {200: {description: ok}}"""
    saved = (db.session.query(SavedMessage)
             .filter_by(user_id=current_user.id, message_id=message_id).first())
    if not saved:
        return jsonify({"msg": "Não encontrado"}), 404
    db.session.delete(saved)
    db.session.commit()
    return jsonify({"msg": "Removido dos favoritos"}), 200


# ── Widget-specific endpoints (each widget gets its OWN message type) ─────────

@messages_bp.get("/strength")
def get_strength():
    """Mensagens de Força --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("strength", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/nature")
def get_nature():
    """Mensagens da Natureza --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("nature", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/serenity")
def get_serenity():
    """Mensagens de Serenidade --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("serenity", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/ocean")
def get_ocean():
    """Mensagens do Oceano --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("ocean", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/body")
def get_body():
    """Mensagens Seu Corpo --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("body", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/tenderness")
def get_tenderness():
    """Mensagens de Ternura --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("tenderness", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/night")
def get_night():
    """Mensagens da Noite --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("night", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/floral")
def get_floral():
    """Mensagens Florais --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("floral", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/sunrise")
def get_sunrise():
    """Mensagens do Sol --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("sunrise", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)


@messages_bp.get("/transformation")
def get_transformation():
    """Mensagens de Transformação --- tags: [Mensagens] responses: {200: {description: ok}}"""
    week = request.args.get("week", type=int) or _week_from_token()
    msg = _pick_message("transformation", week)
    return (jsonify(msg), 200) if msg else (jsonify({"msg": "Sem mensagens"}), 404)
