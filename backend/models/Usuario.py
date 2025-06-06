from bson import ObjectId

class Usuario:
    def __init__(self, _id=None, cpf=None, email=None, nome=None, cargo=None, senha=None):
        self._id = ObjectId(_id) if _id else None
        self.cpf = cpf
        self.email = email
        self.nome = nome
        self.cargo = cargo
        self.senha = senha

    @classmethod
    def from_dict(cls, data):
        return cls(
            _id=data.get('_id'),
            cpf=data.get('cpf'),
            email=data.get('email'),
            nome=data.get('nome'),
            cargo=data.get('cargo'),
            senha=data.get('senha')
        )

    def to_dict(self):
        return {
            # '_id': self._id,
            'cpf': self.cpf,
            'email': self.email,
            'nome': self.nome,
            'cargo': self.cargo,
            'senha': self.senha
        }