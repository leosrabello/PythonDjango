# Loja de Eletrônicos API (Django + DRF)

API RESTful em Django REST Framework — tema **loja de eletrônicos**. Entidades: **Categoria** (1:N) **Produto**.

## Stack
Django · Django REST Framework · django-environ

## Como rodar

```bash
# 1. criar e ativar o ambiente virtual
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. instalar dependências
pip install -r requirements.txt

# 3. configurar variáveis de ambiente
cp .env.example .env             # ajuste SECRET_KEY e DATABASE_URL se quiser

# 4. aplicar as migrações
python manage.py migrate

# 5. rodar o servidor
python manage.py runserver       # http://127.0.0.1:8000/api/
```

Teste rápido: abra `http://127.0.0.1:8000/api/` — a raiz navegável do DRF.

### Rodar os testes

```bash
python manage.py test core
```

## Estrutura

```
loja-api/
├── manage.py               # utilitário de linha de comando do Django
├── requirements.txt
├── .env.example
├── config/                 # o projeto (configuração)
│   ├── settings.py         # DRF, banco, .env, paginação
│   └── urls.py             # inclui as rotas da API sob /api/
└── core/                   # o app do domínio
    ├── models.py           # Categoria e Produto (feitos)
    ├── serializers.py      # validação + JSON
    ├── views.py            # CRUD - ViewSets
    ├── urls.py             # router do DRF (registra os ViewSets)
    ├── tests.py            # testes de API
    └── migrations/         # 0001: Categoria · 0002: Produto + relacionamento
```

## Endpoints

### Categoria — `/api/categorias/` (Frente 2)

| Método | Rota                     | O que faz            | Status               |
|--------|--------------------------|----------------------|----------------------|
| GET    | `/api/categorias/`       | lista (paginada, 10) | 200                  |
| POST   | `/api/categorias/`       | cria                 | 201 · 400            |
| GET    | `/api/categorias/{id}/`  | detalha              | 200 · 404            |
| PUT    | `/api/categorias/{id}/`  | substitui (completo) | 200 · 400 · 404      |
| PATCH  | `/api/categorias/{id}/`  | altera campos soltos | 200 · 400 · 404      |
| DELETE | `/api/categorias/{id}/`  | remove               | 204 · 404            |

Corpo do POST/PUT (`descricao` é opcional; `nome` é obrigatório e único):

```json
{ "nome": "Notebooks", "descricao": "Portáteis e ultrabooks" }
```

Resposta da lista (paginação nativa do DRF, `PAGE_SIZE = 10`):

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    { "id": 1, "nome": "Notebooks", "descricao": "Portáteis e ultrabooks" }
  ]
}
```

### Produto — `/api/produtos/` (Frente 3)

| Método | Rota                    | O que faz            | Status          |
|--------|-------------------------|----------------------|-----------------|
| GET    | `/api/produtos/`       | lista (paginada, 10) | 200             |
| POST   | `/api/produtos/`       | cria                 | 201 · 400       |
| GET    | `/api/produtos/{id}/`  | detalha              | 200 · 404       |
| PUT    | `/api/produtos/{id}/`  | substitui (completo) | 200 · 400 · 404 |
| PATCH  | `/api/produtos/{id}/`  | altera campos soltos | 200 · 400 · 404 |
| DELETE | `/api/produtos/{id}/`  | remove               | 204 · 404       |

Na escrita, envie o relacionamento pelo campo `categoria_id`:

```json
{
  "nome": "Notebook Pro",
  "descricao": "Notebook para trabalho",
  "preco": "4999.90",
  "estoque": 8,
  "categoria_id": 1
}
```

Na leitura, a categoria é retornada de forma aninhada:

```json
{
  "id": 1,
  "nome": "Notebook Pro",
  "descricao": "Notebook para trabalho",
  "preco": "4999.90",
  "estoque": 8,
  "categoria": {
    "id": 1,
    "nome": "Notebooks",
    "descricao": "Portáteis e ultrabooks"
  }
}
```

Filtros disponíveis na listagem:

- `?categoria=1` filtra pelo ID da categoria;
- `?search=notebook` busca em nome/descrição do produto e nome da categoria;
- `?ordering=preco` ordena por nome, preço ou estoque (prefixe com `-` para ordem decrescente);
- `?page=2` navega entre páginas de 10 itens.


## Divisão do trabalho

- **Frente 1 — Fundação/Infra:** este esqueleto (feito). Projeto, app, settings, DRF, .env, paginação.
- **Frente 2 — Categoria:** model, ModelSerializer, ViewSet e registro no router — CRUD em `/api/categorias/` (feito).
- **Frente 3 — Produto:** model com `ForeignKey`, migração do relacionamento, serializer aninhado, CRUD em `/api/produtos/` (feito).
- **Frente 4 — Roteamento, status codes e entrega:** router geral, códigos HTTP, integridade no DELETE, coleção Postman, revisão final.

As implementações das frentes ficam organizadas em `core/models.py`, `serializers.py`, `views.py` e `urls.py`.
