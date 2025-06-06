from bson import ObjectId
from datetime import datetime

class Vitima:
    def __init__(self, _id=None, casoId=None, NIC=None, nome=None, genero=None, idade=None, 
                 cpf=None, endereco=None, etnia=None, odontograma=None, anotacaoAnatomia=None, createdAt=None):
        self._id = ObjectId(_id) if _id else None
        self.casoId = ObjectId(casoId) if casoId else None
        self.NIC = NIC
        self.nome = nome
        self.genero = genero
        self.idade = idade
        self.cpf = cpf
        self.endereco = endereco
        self.etnia = etnia
        self.odontograma = odontograma if odontograma else {
            'superiorEsquerdo': [],
            'superiorDireito': [],
            'inferiorEsquerdo': [],
            'inferiorDireito': []
        }
        self.anotacaoAnatomia = anotacaoAnatomia
        self.createdAt = createdAt if createdAt else datetime.now()

    @classmethod
    def from_dict(cls, data):
        return cls(
            _id=data.get('_id'),
            casoId=data.get('casoId'),
            NIC=data.get('NIC'),
            nome=data.get('nome', 'Não identificado'),
            genero=data.get('genero', 'Não identificado'),
            idade=data.get('idade'),
            cpf=data.get('cpf', 'Não identificado'),
            endereco=data.get('endereco', 'Não identificado'),
            etnia=data.get('etnia', 'Não identificado'),
            odontograma=data.get('odontograma'),
            anotacaoAnatomia=data.get('anotacaoAnatomia'),
            createdAt=data.get('createdAt')
        )

    def to_dict(self):
        return {
            '_id': self._id,
            'casoId': self.casoId,
            'NIC': self.NIC,
            'nome': self.nome,
            'genero': self.genero,
            'idade': self.idade,
            'cpf': self.cpf,
            'endereco': self.endereco,
            'etnia': self.etnia,
            'odontograma': self.odontograma,
            'anotacaoAnatomia': self.anotacaoAnatomia,
            'createdAt': self.createdAt
        }