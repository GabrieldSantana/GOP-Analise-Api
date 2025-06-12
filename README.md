
# GOP Analysis API

Este é um projeto de API desenvolvida com Flask que fornece endpoints para análise de dados relacionados a casos, vítimas, evidências e usuários, integrando-se a um banco de dados MongoDB. A API é projetada para dashboards e análises estatísticas, utilizando bibliotecas como Pandas e XGBoost para processamento de dados.

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação Flask.
- `routes/api.py`: Definição das rotas da API.
- `models/`: Modelos de dados (ex.: `caso.py`, `evidencia.py`, `vitima.py`, `usuario.py`).
- `services/`: Lógica de serviço, incluindo conexão com o banco de dados (`database.py`) e processamento de dados (`data_service.py`).
- `requirements.txt`: Dependências do projeto.
- `.env`: Arquivo para variáveis de ambiente (ex.: URI do MongoDB).
- Outros arquivos como `.gitignore` e `README.md`.

## Pré-requisitos

- Python 3.11.x  
- MongoDB (local ou remoto, como MongoDB Atlas)

Variáveis de ambiente definidas no arquivo `.env`:

```
MONGODB_URI=URI de conexão com o MongoDB  
DATABASE_NAME=Nome do banco de dados  
COLLECTION_NAME=Nome da coleção (opcional)  
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

## Configuração

Clone o repositório:

```bash
git clone https://github.com/GabrieldSantana/GOP-Analise-Api.git
cd GOP-Analise-Api
```

Configure as variáveis de ambiente em um arquivo `.env`:

```text
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/<db>?retryWrites=true&w=majority
DATABASE_NAME=seu_banco
COLLECTION_NAME=sua_colecao
```

Execute localmente:

```bash
python app.py
```

A API estará disponível em http://localhost:5000.

## Endpoints da API

Todos os endpoints estão disponíveis sob o prefixo `/api` e retornam respostas em formato JSON.

### 1. `/api/dashboard/coefficients` (GET)

**Descrição:** Retorna os coeficientes (importâncias de features) de um modelo treinado.

**Parâmetros:** Nenhum

**Retorno (200):**
```json
{
  "features": ["idade", "etnia", "tipo_caso"],
  "importances": [0.45, 0.35, 0.20]
}
```

**Erro (500):**
```json
{ "error": "Mensagem de erro" }
```

### 2. `/api/dashboard/peritos` (GET)

**Descrição:** Retorna a distribuição de casos por perito

**Parâmetros:** `nome_perito` (opcional)

**Retorno (200):**
```json
{
  "casos_por_perito": {
    "João Silva": 5,
    "Maria Oliveira": 3,
    "Outros": 2
  },
  "total_casos": 10
}
```

**Erro (500):**
```json
{ "error": "Mensagem de erro" }
```

### 3. `/api/dashboard/vitimas` (GET)

**Descrição:** Estatísticas de vítimas com filtros

**Parâmetros:** `etnia`, `genero`, `idade` (todos opcionais)

**Retorno (200):**
```json
{
  "data": [...],
  "aggregations": {
    "etnia_count": {"Branca": 2, "Preta": 1},
    "genero_count": {"Masculino": 2, "Feminino": 1},
    "idade_count": {30: 1, 25: 1}
  }
}
```

**Erro (500):**
```json
{ "error": "Mensagem de erro" }
```

### 4. `/api/dashboard/casos` (GET)

**Descrição:** Distribuição de casos com filtros

**Parâmetros:** `local`, `status`, `data_inicio`, `data_fim` (opcionais)

**Retorno (200):**
```json
{
  "data": [...],
  "aggregations": {
    "local_count": {"Cidade A": 2, "Cidade B": 1},
    "status_count": {"Em andamento": 2, "Fechado": 1},
    "data_count": {"2025-06": 3}
  }
}
```

**Erro (500):**
```json
{ "error": "Mensagem de erro" }
```

### 5. `/api/dashboard/evidencias` (GET)

**Descrição:** Número de evidências por caso

**Parâmetros:** `caso_id`, `tipo_evidencia` (opcionais)

**Retorno (200):**
```json
{
  "data": [...],
  "aggregations": {
    "evidencias_por_caso": {
      "Caso 1": 3,
      "Caso 2": 2
    }
  }
}
```

**Erro (500):**
```json
{ "error": "Mensagem de erro" }
```

### 6. `/` (GET)

**Descrição:** Health check da API

**Retorno (200):**
```json
{ "status": "ok" }
```

## Deploy

A API foi implantada no Render:

**URL:** https://gop-analise-api.onrender.com

**Start Command:**  
```
gunicorn -b 0.0.0.0:$PORT app:create_app
```

**Nota:** Certifique-se que `gunicorn==21.2.0` está no `requirements.txt`.

## Contribuição

1. Faça um fork do repositório.
2. Crie uma branch: `git checkout -b feature/nova-feature`
3. Commit: `git commit -m "Adiciona nova feature"`
4. Push: `git push origin feature/nova-feature`
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
