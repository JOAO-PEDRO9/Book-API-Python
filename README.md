# Book API

API simples em Python puro para manipulação de livros com CI/CD via GitHub Actions e deploy automático na Render.

## Rotas
- `GET /books` – Lista todos os livros.
- `GET /books/<id>` – Mostra um livro por ID.
- `POST /books` – Adiciona um novo livro (JSON: title, author).

## Execução local
```bash
python server.py
```

Teste de deploy manual via celular
