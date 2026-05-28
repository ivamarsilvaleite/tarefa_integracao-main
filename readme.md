API Trabalho N703

API REST desenvolvida em Python com FastAPI para a disciplina Técnicas de Integração de Sistemas.

Integrantes

Consultar o ficheiro INTEGRANTES.md.

Tecnologias Utilizadas

Python 3

FastAPI

Uvicorn

HTTPX

Pytest

APIs Externas Utilizadas

IBGE API (cidades e estados)

Open-Meteo API (dados climáticos)

Como Executar o Projeto

1. Instalar dependências

pip install fastapi uvicorn httpx pytest


2. Executar o servidor na porta obrigatória (3000)

py -m uvicorn src.main:app --port 3000 --reload


3. Aceder à documentação interativa

http://localhost:3000/docs


Como Executar os Testes

Testes automatizados com Pytest

py -m pytest


Testes no Postman

Executar as requisições da coleção:

docs/postman_collection.json


Endpoints Disponíveis

Health Check

GET /api/v1/health


Retorna o status da API.

Buscar clima por cidade

GET /api/v1/clima/{cidade}


Exemplo:

GET /api/v1/clima/Fortaleza


Listar cidades por estado

GET /api/v1/cidades/{uf}?limite=5


Exemplo:

GET /api/v1/cidades/CE?limite=5


Estrutura do Projeto

/
├── README.md
├── INTEGRANTES.md
├── src/
├── tests/
└── docs/
    └── postman_collection.json


Tratamento de Erros

400 Bad Request → parâmetros inválidos

404 Not Found → recurso não encontrado

503 Service Unavailable → serviço externo indisponível

Observações

Projeto acadêmico.

API desenvolvida com foco em integração de sistemas.

Dados retornados dependem da disponibilidade das APIs externas.
