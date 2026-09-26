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

> Depois que as Frentes 2 e 3 criarem os models, rode
> `python manage.py makemigrations` e `python manage.py migrate` de novo.

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
    ├── models.py           # entidades (Frentes 2 e 3)
    ├── serializers.py      # validação + JSON (Frentes 2 e 3)
    ├── views.py            # CRUD - ViewSets (Frentes 2 e 3)
    └── urls.py             # router do DRF (registra os ViewSets)
```

## Divisão do trabalho

- **Frente 1 — Fundação/Infra:** este esqueleto (feito). Projeto, app, settings, DRF, .env, paginação.
- **Frente 2 — Categoria:** model, ModelSerializer, ViewSet e registro no router — CRUD em `/api/categorias/`.
- **Frente 3 — Produto:** model com `ForeignKey`, migração do relacionamento, serializer aninhado, CRUD em `/api/produtos/`.
- **Frente 4 — Roteamento, status codes e entrega:** router geral, códigos HTTP, integridade no DELETE, coleção Postman, revisão final.

Onde cada frente pluga está marcado com comentários em `core/models.py`, `serializers.py`, `views.py` e `urls.py`.
