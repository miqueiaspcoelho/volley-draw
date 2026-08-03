Leia obrigatoriamente:

* `AGENTS.md`
* `documentation/spec.md`
* `documentation/analysis.md`
* `documentation/plan.md`
* `documentation/context.compact.md`
* `README.md`
* `Dockerfile`
* `docker-compose.yml`
* `.env.example`

Prepare o projeto para deploy da aplicação web no Render usando Docker.

## Contexto

* O desenvolvimento local continua usando Docker Compose com PostgreSQL local.
* Em produção, somente o container da aplicação será publicado no Render.
* O PostgreSQL de produção já está configurado no Neon.
* As migrações já foram executadas com sucesso no Neon.
* A aplicação usa FastAPI, Uvicorn, SQLAlchemy, Alembic e psycopg.
* Não deve ser criado banco PostgreSQL no Render.
* Não execute o deploy efetivo.

## Tarefas

1. Audite a configuração atual do projeto para execução no Render.
2. Ajuste o `Dockerfile` para iniciar a aplicação usando:

   * host `0.0.0.0`;
   * variável de ambiente `PORT`;
   * porta `8000` como fallback local.
3. O comando final deve ser compatível com:
   `uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}`
4. Não use `docker compose` dentro do container de produção.
5. Preserve integralmente o funcionamento local do `docker-compose.yml`.
6. Confirme que nenhum serviço PostgreSQL local será iniciado no Render.
7. Verifique se o Dockerfile:

   * possui diretório de trabalho correto;
   * copia apenas os arquivos necessários;
   * instala as dependências corretamente;
   * não inclui `.env`;
   * não inclui credenciais;
   * não executa migrações automaticamente no `CMD`;
   * expõe a porta apenas como documentação, sem depender dela.
8. Crie ou revise `.dockerignore` incluindo, quando aplicável:

   * `.git`;
   * `.env`;
   * `.env.*`;
   * `.venv`;
   * `__pycache__`;
   * `.pytest_cache`;
   * arquivos temporários;
   * banco local;
   * logs;
   * documentação temporária sensível.
9. Preserve `.env.example` sem valores reais.
10. Verifique se a aplicação possui endpoint público:
    `GET /health`
11. O health check deve:

    * responder sem autenticação;
    * validar aplicação e banco;
    * não chamar a API externa;
    * não expor detalhes internos;
    * retornar status HTTP apropriado.
12. Confirme que a aplicação aceita as variáveis de produção existentes, especialmente:

    * `APP_ENV`;
    * `DEBUG`;
    * `DATABASE_URL`;
    * `SECRET_KEY`;
    * `DRAW_API_URL`;
    * `DRAW_API_TIMEOUT`;
    * `LOG_LEVEL`;
    * `SESSION_COOKIE_SECURE`.
13. Não adicione variáveis que o projeto não utiliza.
14. Confirme que `DATABASE_URL` aceita a URL do Neon e normaliza:
    `postgresql://`
    para:
    `postgresql+psycopg://`
15. Verifique se cookies de sessão ficam seguros em produção e continuam funcionando localmente em HTTP.
16. Garanta que logs sejam enviados para a saída padrão e não dependam de arquivos locais.
17. Verifique se nenhum dado persistente depende do sistema de arquivos do container.
18. Crie `render.yaml` somente se isso realmente simplificar o deploy.

Caso crie `render.yaml`, configure apenas um Web Service Docker, contendo:

* runtime Docker;
* plano gratuito;
* caminho do Dockerfile;
* health check `/health`;
* auto deploy;
* variáveis sem valores secretos;
* segredos marcados para configuração manual no painel.

Não configure banco de dados no Render.

## Documentação

Crie ou atualize:

* `documentation/deploy.md`;
* `documentation/deploy-checklist.md`;
* `README.md`;
* `documentation/context.compact.md`;
* `documentation/plan.md`.

Em `documentation/deploy.md`, documente objetivamente:

1. criação do Web Service no Render;
2. seleção do runtime Docker;
3. caminho do Dockerfile;
4. variáveis de ambiente necessárias;
5. geração de `SECRET_KEY`;
6. configuração do Neon;
7. health check `/health`;
8. primeiro deploy;
9. validação dos logs;
10. teste pós-deploy;
11. aplicação manual de futuras migrações;
12. rollback;
13. limitações do plano gratuito.

## Validações

Execute:

1. build local da imagem Docker;
2. inicialização local usando `PORT=8000`;
3. teste do endpoint `/health`;
4. testes automatizados;
5. verificação de importação da aplicação;
6. busca por segredos versionados;
7. inspeção do conteúdo final da imagem para confirmar que arquivos `.env` não foram copiados;
8. confirmação de que o container inicia sem depender do serviço `db` do Docker Compose.

Não utilize o banco Neon em testes destrutivos.

## Restrições

* Não realize o deploy no Render.
* Não altere funcionalidades de negócio.
* Não altere regras do sorteio.
* Não altere o contrato da API externa.
* Não execute migrações no Neon.
* Não coloque credenciais no código.
* Não versione `.env`.
* Não remova o PostgreSQL local do Docker Compose.
* Não implemente novas funcionalidades.
* Faça apenas alterações necessárias para produção.

## Resultado esperado

Ao final, informe somente:

* diagnóstico inicial;
* arquivos criados;
* arquivos alterados;
* comando final do container;
* variáveis obrigatórias no Render;
* resultado do build Docker;
* resultado dos testes;
* resultado do health check;
* itens que ainda devem ser configurados manualmente no painel do Render;
* confirmação de que nenhum segredo foi versionado.
