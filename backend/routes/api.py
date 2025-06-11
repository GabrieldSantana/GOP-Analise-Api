from flask import Blueprint, jsonify, request
from services.data_service import get_data_for_dashboard, get_casos_por_perito, get_vitimas_estatisticas, get_casos_distribuicao, get_evidencias_por_caso

api_bp = Blueprint('api', __name__)

@api_bp.route('/dashboard/coefficients', methods=['GET'])
def get_coefficients():
    try:
        data = get_data_for_dashboard()
        return jsonify({"features": data["features"], "importances": data["importances"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/dashboard/peritos', methods=['GET'])
def get_casos_perito():
    try:
        nome_perito = request.args.get('nome_perito')
        data = get_casos_por_perito(nome_perito)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/dashboard/vitimas', methods=['GET'])
def get_vitimas_stats():
    try:
        filters = {
            'etnia': request.args.get('etnia'),
            'genero': request.args.get('genero'),
            'idade': request.args.get('idade', type=int)
        }
        data = get_vitimas_estatisticas(filters)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/dashboard/casos', methods=['GET'])
def get_casos_dist():
    try:
        filters = {
            'local': request.args.get('local'),
            'data_inicio': request.args.get('data_inicio'),
            'data_fim': request.args.get('data_fim'),
            'status': request.args.get('status')
        }
        data = get_casos_distribuicao(filters)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/dashboard/evidencias', methods=['GET'])
def get_evidencias_caso():
    try:
        caso_id = request.args.get('caso_id')
        tipo_evidencia = request.args.get('tipo_evidencia')
        data = get_evidencias_por_caso(caso_id, tipo_evidencia)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500