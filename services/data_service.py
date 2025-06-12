from services.database import Database
from models.usuario import Usuario
from models.evidencia import Evidencia
from models.vitima import Vitima
from models.caso import Caso
import pickle
import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from bson import ObjectId
from datetime import datetime
import pytz

def get_data_for_dashboard():
    db = Database()
    try:
        usuarios = [Usuario.from_dict(doc) for doc in db.get_collection('usuarios').find().limit(100)]
        evidencias = [Evidencia.from_dict(doc) for doc in db.get_collection('evidencias').find().limit(100)]
        vitimas = [Vitima.from_dict(doc) for doc in db.get_collection('vitimas').find().limit(100)]
        casos = [Caso.from_dict(doc) for doc in db.get_collection('casos').find().limit(100)]

        processed_data = {
            'usuarios': [u.to_dict() for u in usuarios],
            'evidencias': [e.to_dict() for e in evidencias],
            'vitimas': [v.to_dict() for v in vitimas],
            'casos': [c.to_dict() for c in casos]
        }

        model_path = os.path.join(os.path.dirname(__file__), '../models/model.pkl')
        if os.path.exists(model_path):
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
                if isinstance(model, (RandomForestClassifier)) or hasattr(model, 'feature_importances_'):
                    features = ["idade", "etnia", "tipo_caso"]
                    importances = model.feature_importances_.tolist() if hasattr(model, 'feature_importances_') else []
                else:
                    features, importances = [], []
        else:
            features, importances = [], []

        return {
            "features": features,
            "importances": importances,
            "data": processed_data
        }
    finally:
        db.close_connection()

def get_casos_por_perito(nome_perito):
    db = Database()
    try:
        total_casos = db.get_collection('casos').count_documents({})

        match_stage = {}
        if nome_perito:
            usuarios = db.get_collection('usuarios').find({'nome': {'$regex': nome_perito, '$options': 'i'}})
            usuario_ids = [u['_id'] for u in usuarios]
            match_stage['peritoResponsavel'] = {'$in': usuario_ids}

        pipeline = [
            {'$match': match_stage},
            {'$group': {'_id': '$peritoResponsavel', 'count': {'$sum': 1}}},
            {'$lookup': {
                'from': 'usuarios',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'perito'
            }},
            {'$unwind': '$perito'},
            {'$project': {'nome_perito': '$perito.nome', 'count': 1}}
        ]

        casos_perito = list(db.get_collection('casos').aggregate(pipeline))
        perito_data = {item['nome_perito']: item['count'] for item in casos_perito}
        perito_data['Outros'] = total_casos - sum(perito_data.values())

        return {'casos_por_perito': perito_data, 'total_casos': total_casos}
    finally:
        db.close_connection()

def get_vitimas_estatisticas(filters):
    db = Database()
    try:
        query = {}
        if filters.get('etnia'):
            query['etnia'] = filters['etnia']
        if filters.get('genero'):
            query['genero'] = filters['genero']
        if filters.get('idade'):
            query['idade'] = filters['idade']

        documents = list(db.get_collection('vitimas').find(query).limit(100))
        df = pd.DataFrame(documents)

        aggregations = {
            'etnia_count': df['etnia'].value_counts().to_dict() if not df.empty else {},
            'genero_count': df['genero'].value_counts().to_dict() if not df.empty else {},
            'idade_count': df['idade'].value_counts().to_dict() if not df.empty else {}
        }

        processed_data = [Vitima.from_dict(doc).to_dict() for doc in documents]
        return {'data': processed_data, 'aggregations': aggregations}
    finally:
        db.close_connection()

def get_casos_distribuicao(filters):
    db = Database()
    try:
        query = {}
        if filters.get('local'):
            query['local'] = filters['local']
        if filters.get('status'):
            query['status'] = filters['status']
        if filters.get('data_inicio') or filters.get('data_fim'):
            query['dataHora'] = {}
            if filters.get('data_inicio'):
                query['dataHora']['$gte'] = datetime.fromisoformat(filters['data_inicio']).replace(tzinfo=pytz.UTC)
            if filters.get('data_fim'):
                query['dataHora']['$lte'] = datetime.fromisoformat(filters['data_fim']).replace(tzinfo=pytz.UTC)

        documents = list(db.get_collection('casos').find(query).limit(100))
        df = pd.DataFrame(documents)

        aggregations = {
            'local_count': df['local'].value_counts().to_dict() if not df.empty else {},
            'status_count': df['status'].value_counts().to_dict() if not df.empty else {},
            'data_count': df['dataHora'].dt.to_period('M').astype(str).value_counts().sort_index().to_dict() if not df.empty and 'dataHora' in df else {}
        }

        processed_data = [Caso.from_dict(doc).to_dict() for doc in documents]
        return {'data': processed_data, 'aggregations': aggregations}
    finally:
        db.close_connection()

def get_evidencias_por_caso(caso_id, tipo_evidencia):
    db = Database()
    try:
        match_stage = {}
        if caso_id:
            match_stage['casoId'] = ObjectId(caso_id)
        if tipo_evidencia:
            match_stage['tipoEvidencia'] = tipo_evidencia

        pipeline = [
            {'$match': match_stage},
            {'$group': {'_id': '$casoId', 'count': {'$sum': 1}}},
            {'$lookup': {
                'from': 'casos',
                'localField': '_id',
                'foreignField': '_id',
                'as': 'caso'
            }},
            {'$unwind': '$caso'},
            {'$project': {'nome_caso': '$caso.nome', 'count': 1}}
        ]

        evidencias_caso = list(db.get_collection('evidencias').aggregate(pipeline))
        evidencias_data = {item['nome_caso']: item['count'] for item in evidencias_caso}

        documents = list(db.get_collection('evidencias').find(match_stage).limit(100))
        processed_data = [Evidencia.from_dict(doc).to_dict() for doc in documents]
        return {'data': processed_data, 'aggregations': {'evidencias_por_caso': evidencias_data}}
    finally:
        db.close_connection()