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

- Deploy previsto no Render como Web Service Docker.
- Comando do container: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}.
- Usar DATABASE_URL na aplicacao com Neon.
- Usar DATABASE_DIRECT_URL para Alembic quando disponivel; DATABASE_URL fica como fallback.
- URLs postgresql:// sao normalizadas para postgresql+psycopg://.
- Manter .env, .env.* e .env.neon fora do versionamento e da imagem.
- Configurar SECRET_KEY forte em producao.
- Configurar SESSION_COOKIE_SECURE=true somente com HTTPS.
- Criar usuario inicial com python -m app.cli.users create ... no ambiente de producao.
- Executar alembic upgrade head manualmente antes de publicar versoes com novas migracoes.
- Nao importar dados locais no banco de producao.

Detalhes: documentation/deploy.md e documentation/deploy-checklist.md.
