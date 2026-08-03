# Deploy no Render

## Web Service

1. No Render, crie um novo Web Service a partir do repositorio.
2. Selecione runtime Docker.
3. Use o Dockerfile em `./Dockerfile`.
4. Nao crie PostgreSQL no Render; use o Neon ja configurado.
5. Configure health check em `/health`.

## Variaveis

Obrigatorias no Render:

- `APP_ENV=production`
- `DEBUG=false`
- `DATABASE_URL`: URL do Neon.
- `SECRET_KEY`: segredo forte da sessao.
- `DRAW_API_URL=https://apiteams-q4s3.onrender.com`
- `DRAW_API_TIMEOUT=20`
- `LOG_LEVEL=INFO`
- `SESSION_COOKIE_SECURE=true`

Gere `SECRET_KEY` com valor aleatorio forte e configure somente no painel do Render. Nao versionar esse valor.

## Neon

Use a connection string do Neon em `DATABASE_URL`. A aplicacao normaliza `postgresql://` para `postgresql+psycopg://`.

## Primeiro deploy

1. Confirme que as migracoes ja foram aplicadas no Neon.
2. Acione o deploy pelo Render.
3. Valide os logs do build e da inicializacao.
4. Acesse `/health` e confirme HTTP 200.
5. Crie o primeiro usuario no ambiente de producao com `python -m app.cli.users create ...` usando shell/job apropriado do provedor.

## Migracoes futuras

Nao rodam automaticamente no `CMD` do container. Execute `alembic upgrade head` manualmente antes de publicar versoes que dependam de novas migracoes.

## Rollback

Use rollback para uma versao anterior pelo painel do Render. Se houver migracao incompatibilizante, valide plano manual de downgrade antes de reverter codigo.

## Limitacoes do plano gratuito

O servico pode dormir por inatividade, ter cold start e recursos limitados. O banco de producao permanece no Neon.