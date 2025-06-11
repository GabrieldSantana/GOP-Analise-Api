from bson import ObjectId
from datetime import datetime

class Evidencia:
    def __init__(self, _id=None, casoId=None, arquivoId=None, nomeArquivo=None, tipoArquivo=None, 
                tipoEvidencia=None, descricao=None, coletadoPor=None, createdAt=None):
        self._id = _id if _id else None
        self.casoId = casoId if casoId else None
        self.arquivoId = arquivoId if arquivoId else None
        self.nomeArquivo = nomeArquivo
        self.tipoArquivo = tipoArquivo
        self.tipoEvidencia = tipoEvidencia
        self.descricao = descricao
        self.coletadoPor = coletadoPor if coletadoPor else None
        self.createdAt = createdAt if createdAt else datetime.now()

    @classmethod
    def from_dict(cls, data):
        return cls(
            _id=data.get('_id'),
            casoId=data.get('casoId'),
            arquivoId=data.get('arquivoId'),
            nomeArquivo=data.get('nomeArquivo'),
            tipoArquivo=data.get('tipoArquivo'),
            tipoEvidencia=data.get('tipoEvidencia'),
            descricao=data.get('descricao'),
            coletadoPor=data.get('coletadoPor'),
            createdAt=data.get('createdAt')
        )

    def to_dict(self):
        return {
            # 'casoId': self.casoId,
            # 'arquivoId': self.arquivoId,
            'nomeArquivo': self.nomeArquivo,
            'tipoArquivo': self.tipoArquivo,
            'tipoEvidencia': self.tipoEvidencia,
            'descricao': self.descricao,
            # 'coletadoPor': self.coletadoPor,
            'createdAt': self.createdAt
        }