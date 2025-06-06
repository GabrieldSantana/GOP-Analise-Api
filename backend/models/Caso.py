from bson import ObjectId
from datetime import datetime

class Caso:
    def __init__(self, _id=None, nome=None, local=None, descricao=None, tipo=None, 
                 peritoResponsavel=None, status=None, dataHora=None, createdAt=None, dataFechamento=None):
        self._id = ObjectId(_id) if _id else None
        self.nome = nome
        self.local = local
        self.descricao = descricao
        self.tipo = tipo
        self.peritoResponsavel = peritoResponsavel
        self.status = status if status else 'Em andamento'
        self.dataHora = dataHora
        self.createdAt = createdAt if createdAt else datetime.now()
        self.dataFechamento = dataFechamento

    @classmethod
    def from_dict(cls, data):
        return cls(
            _id=data.get('_id'),
            nome=data.get('nome'),
            local=data.get('local'),
            descricao=data.get('descricao'),
            tipo=data.get('tipo'),
            peritoResponsavel=data.get('peritoResponsavel'),
            status=data.get('status', 'Em andamento'),
            dataHora=data.get('dataHora'),
            createdAt=data.get('createdAt'),
            dataFechamento=data.get('dataFechamento')
        )

    def to_dict(self):
        return {
            'nome': self.nome,
            'local': self.local,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'peritoResponsavel': self.peritoResponsavel,
            'status': self.status,
            'dataHora': self.dataHora,
            'createdAt': self.createdAt,
            'dataFechamento': self.dataFechamento
        }