from datetime import datetime, date
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, current_user
from app import db
from app.models.user_progress import UserProgress

pregnancy_bp = Blueprint("pregnancy", __name__, url_prefix="/pregnancy")

# ── Week-by-week baby development data ──────────────────────────────────────
WEEK_DATA = {
    4:  {"size": "Semente de papoula", "size_cm": 0.1, "weight_g": None, "highlight": "O embrião se implantou! Órgãos vitais começam a se formar."},
    5:  {"size": "Semente de gergelim", "size_cm": 0.13, "weight_g": None, "highlight": "O coração primitivo começa a bater."},
    6:  {"size": "Lentilha", "size_cm": 0.6, "weight_g": None, "highlight": "Broto dos braços e pernas aparecem."},
    7:  {"size": "Mirtilo", "size_cm": 1.0, "weight_g": None, "highlight": "O cérebro cresce rapidamente."},
    8:  {"size": "Framboesa", "size_cm": 1.6, "weight_g": 1, "highlight": "Todos os órgãos vitais estão se formando."},
    9:  {"size": "Azeitona", "size_cm": 2.3, "weight_g": 2, "highlight": "O bebê já move os braços e pernas."},
    10: {"size": "Morango", "size_cm": 3.1, "weight_g": 4, "highlight": "As unhas começam a crescer."},
    11: {"size": "Lima", "size_cm": 4.1, "weight_g": 7, "highlight": "Os órgãos genitais se desenvolvem."},
    12: {"size": "Ameixa", "size_cm": 5.4, "weight_g": 14, "highlight": "O risco de aborto diminui significativamente."},
    13: {"size": "Pêssego", "size_cm": 7.4, "weight_g": 23, "highlight": "As impressões digitais estão se formando."},
    14: {"size": "Limão", "size_cm": 8.7, "weight_g": 43, "highlight": "O bebê consegue fazer expressões faciais."},
    15: {"size": "Maçã", "size_cm": 10.1, "weight_g": 70, "highlight": "O bebê pode sentir luz através da barriga."},
    16: {"size": "Abacate", "size_cm": 11.6, "weight_g": 100, "highlight": "Talvez você sinta os primeiros movimentos!"},
    17: {"size": "Pera", "size_cm": 13.0, "weight_g": 140, "highlight": "O bebê desenvolve gordura corporal."},
    18: {"size": "Pimentão", "size_cm": 14.2, "weight_g": 190, "highlight": "Ele consegue ouvir sua voz agora!"},
    19: {"size": "Manga", "size_cm": 15.3, "weight_g": 240, "highlight": "Os movimentos ficam cada vez mais frequentes."},
    20: {"size": "Banana", "size_cm": 16.4, "weight_g": 300, "highlight": "Metade da gestação! O vernix caseoso aparece."},
    21: {"size": "Cenoura", "size_cm": 26.7, "weight_g": 360, "highlight": "O bebê engole líquido amniótico regularmente."},
    22: {"size": "Espiga de milho", "size_cm": 27.8, "weight_g": 430, "highlight": "As sobrancelhas e pestanas estão visíveis."},
    23: {"size": "Toranja", "size_cm": 28.9, "weight_g": 501, "highlight": "O bebê tem seus próprios ciclos de sono."},
    24: {"size": "Milho", "size_cm": 30.0, "weight_g": 600, "highlight": "Os pulmões produzem surfactante para respirar."},
    25: {"size": "Couve-flor", "size_cm": 34.6, "weight_g": 660, "highlight": "A pele fica menos transparente."},
    26: {"size": "Cebola", "size_cm": 35.6, "weight_g": 760, "highlight": "Os olhos abrem pela primeira vez."},
    27: {"size": "Couve-rábano", "size_cm": 36.6, "weight_g": 875, "highlight": "O bebê reage ao toque na barriga."},
    28: {"size": "Berinjela", "size_cm": 37.6, "weight_g": 1005, "highlight": "O terceiro trimestre começa! O cérebro cresce muito."},
    29: {"size": "Abóbora acorn", "size_cm": 38.6, "weight_g": 1153, "highlight": "Os ossos estão se endurecendo."},
    30: {"size": "Repolho", "size_cm": 39.9, "weight_g": 1319, "highlight": "A medula óssea assume a produção de glóbulos vermelhos."},
    31: {"size": "Coco", "size_cm": 41.1, "weight_g": 1502, "highlight": "Todos os cinco sentidos estão funcionando."},
    32: {"size": "Jicama", "size_cm": 42.4, "weight_g": 1702, "highlight": "O bebê pratica respirar sugando e engolindo."},
    33: {"size": "Abacaxi", "size_cm": 43.7, "weight_g": 1918, "highlight": "O crânio ainda está mole para facilitar o parto."},
    34: {"size": "Abóbora butternut", "size_cm": 45.0, "weight_g": 2146, "highlight": "As unhas chegaram na ponta dos dedos."},
    35: {"size": "Melão honeydew", "size_cm": 46.2, "weight_g": 2383, "highlight": "Os rins estão totalmente funcionais."},
    36: {"size": "Alface-romana", "size_cm": 47.4, "weight_g": 2622, "highlight": "O bebê perde o lanugo (pelos finos)."},
    37: {"size": "Acelga", "size_cm": 48.6, "weight_g": 2859, "highlight": "Considerado a termo! Pode nascer a qualquer momento."},
    38: {"size": "Ruibarbo", "size_cm": 49.8, "weight_g": 3083, "highlight": "O cérebro e os pulmões continuam amadurecendo."},
    39: {"size": "Mini melancia", "size_cm": 50.7, "weight_g": 3288, "highlight": "O bebê está pronto para o mundo!"},
    40: {"size": "Abóbora grande", "size_cm": 51.2, "weight_g": 3462, "highlight": "Data prevista do parto! Que momento especial."},
}

def _get_week_info(week: int) -> dict:
    """Get development info for a given week, interpolating if not in table."""
    week = max(4, min(42, week))
    # Find closest week
    if week in WEEK_DATA:
        return WEEK_DATA[week]
    # Find nearest
    keys = sorted(WEEK_DATA.keys())
    closest = min(keys, key=lambda k: abs(k - week))
    return WEEK_DATA[closest]


@pregnancy_bp.get("/progress")
@jwt_required()
def get_progress():
    progress = current_user.progress
    if not progress:
        return jsonify({"msg": "Progresso não encontrado"}), 404

    data = progress.to_dict()
    week = progress.current_week
    week_info = _get_week_info(week)
    data["week_info"] = week_info
    return jsonify(data), 200


@pregnancy_bp.put("/progress")
@jwt_required()
def update_progress():
    data = request.get_json(force=True, silent=True) or {}
    progress = current_user.progress

    if not progress:
        from app.models.user_progress import UserProgress
        progress = UserProgress(user_id=current_user.id)
        db.session.add(progress)

    if "baby_name" in data:
        progress.baby_name = data["baby_name"].strip() or "Bebê"

    if "due_date" in data and data["due_date"]:
        try:
            progress.due_date = date.fromisoformat(data["due_date"])
            progress.pregnancy_start = None  # clear other field
        except ValueError:
            return jsonify({"msg": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    if "pregnancy_start" in data and data["pregnancy_start"]:
        try:
            progress.pregnancy_start = date.fromisoformat(data["pregnancy_start"])
            progress.due_date = None  # clear other field
        except ValueError:
            return jsonify({"msg": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    db.session.commit()

    result = progress.to_dict()
    result["week_info"] = _get_week_info(progress.current_week)
    return jsonify(result), 200


@pregnancy_bp.get("/timeline/<int:week>")
def get_week_timeline(week: int):
    if week < 1 or week > 42:
        return jsonify({"msg": "Semana deve ser entre 1 e 42"}), 400

    week_info = _get_week_info(week)
    trimester = 1 if week <= 13 else (2 if week <= 26 else 3)

    return jsonify({
        "week": week,
        "trimester": trimester,
        "trimester_label": f"{trimester}º Trimestre",
        **week_info,
    }), 200


@pregnancy_bp.get("/timeline")
def get_full_timeline():
    result = []
    for week in range(4, 41):
        info = _get_week_info(week)
        trimester = 1 if week <= 13 else (2 if week <= 26 else 3)
        result.append({"week": week, "trimester": trimester, **info})
    return jsonify(result), 200
