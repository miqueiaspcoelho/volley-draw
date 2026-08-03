# Checklist de Deploy

- [ ] Web Service criado no Render com runtime Docker.
- [ ] Dockerfile configurado em `./Dockerfile`.
- [ ] Nenhum PostgreSQL criado no Render.
- [ ] `DATABASE_URL` configurada com Neon.
- [ ] `SECRET_KEY` forte configurada no painel.
- [ ] `SESSION_COOKIE_SECURE=true` em producao com HTTPS.
- [ ] `DRAW_API_URL` aponta para a API externa aprovada.
- [ ] Health check configurado em `/health`.
- [ ] Migracoes aplicadas manualmente antes do deploy quando houver novas revisoes.
- [ ] Logs verificados na saida padrao do Render.
- [ ] `/health` retorna HTTP 200 apos deploy.
- [ ] Primeiro usuario criado no ambiente de producao.
- [ ] Nenhum arquivo `.env` versionado ou copiado para a imagem.