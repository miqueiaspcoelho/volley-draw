# Volley Draw

## Docker local

Subir app e PostgreSQL:

```powershell
docker compose up --build
```

Acessar:

```text
http://127.0.0.1:8005
```

Criar primeiro usuario:

```powershell
docker compose exec app python -m app.cli.users create user_name "name" --pin "XXXXX"
```

Parar:

```powershell
docker compose down
```


## Producao

Checklist validado para Neon:

- Usar DATABASE_URL na aplicacao.
- Usar DATABASE_DIRECT_URL para Alembic quando disponivel; DATABASE_URL fica como fallback.
- URLs postgresql:// sao normalizadas para postgresql+psycopg://.
- Manter .env e .env.neon fora do versionamento.
- Configurar VOLLEY_DRAW_SESSION_SECRET forte em producao.
- Configurar VOLLEY_DRAW_SESSION_COOKIE_SECURE=true somente com HTTPS.
- Criar usuario inicial com python -m app.cli.users create ... no ambiente de producao.
- Executar alembic upgrade head antes de iniciar a aplicacao.
- Nao importar dados locais no banco de producao.
