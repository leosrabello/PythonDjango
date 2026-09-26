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

Teste rápido: abra `http://127.0.0.1:8000/api/` — a raiz navegável do `DefaultRouter`, com links para categorias e produtos.

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
| DELETE | `/api/categorias/{id}/`  | remove se não houver produtos | 204 · 400 · 404 |

O relacionamento usa `on_delete=PROTECT`: uma categoria com produtos não pode ser removida. Nesse caso a API responde `400` com uma mensagem explicativa; apague ou mova os produtos antes de tentar novamente.

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

### Status HTTP

- `200 OK`: consultas e atualizações bem-sucedidas (`GET`, `PUT`, `PATCH`);
- `201 Created`: criação bem-sucedida (`POST`);
- `204 No Content`: exclusão bem-sucedida (`DELETE`);
- `400 Bad Request`: payload/filtro inválido ou tentativa de excluir categoria protegida;
- `404 Not Found`: recurso solicitado não existe;
- `500 Internal Server Error`: falha inesperada no servidor; não representa um resultado normal da API.

### Coleção Postman/Insomnia

Importe `postman/Loja de Eletrônicos API.postman_collection.json` no Postman ou Insomnia. A coleção cobre a raiz `/api/`, CRUD de categorias e produtos, filtro, busca, ordenação, paginação e exemplos de `400`/`404`. Execute os requests na ordem apresentada: ela cria registros de teste, verifica que `PROTECT` barra a exclusão de categoria e, em seguida, exclui primeiro o produto e depois a categoria. A variável `baseUrl` pode ser alterada para apontar para outra instância.


## Divisão do trabalho

- **Frente 1 — Fundação/Infra:** este esqueleto (feito). Projeto, app, settings, DRF, .env, paginação.
- **Frente 2 — Categoria:** model, ModelSerializer, ViewSet e registro no router — CRUD em `/api/categorias/` (feito).
- **Frente 3 — Produto:** model com `ForeignKey`, migração do relacionamento, serializer aninhado, CRUD em `/api/produtos/` (feito).
- **Frente 4 — Roteamento, status codes e entrega:** concluída — `DefaultRouter` incluído sob `/api/`, status HTTP semânticos, integridade `PROTECT`, coleção Postman/Insomnia e documentação revisada.

As implementações das frentes ficam organizadas em `core/models.py`, `serializers.py`, `views.py` e `urls.py`.
