Leia `AGENTS.md` e os artefatos em `documentation/`.

Prepare e valide a conexão do projeto com o Neon para produção.

Contexto:

* O desenvolvimento local deve continuar usando PostgreSQL via Docker.
* O Neon será usado somente como banco de produção.
* As credenciais estão no arquivo local `.env`
* Não exiba, copie, registre ou versione valores desse arquivo.
* Garanta que `.env` esteja no `.gitignore`.

Tarefas:

1. Identifique o driver PostgreSQL usado pelo SQLAlchemy.
2. Verifique se a URL `postgresql://` precisa ser normalizada para o driver atual.
3. Configure a aplicação para usar `DATABASE_URL`.
4. Configure o Alembic para priorizar `DATABASE_DIRECT_URL`, usando `DATABASE_URL` apenas como fallback.
5. Preserve integralmente o funcionamento do PostgreSQL local via Docker.
6. Teste a conexão com o Neon usando `SELECT 1`.
7. Valide que existe apenas uma head do Alembic.
8. Execute `alembic upgrade head` no Neon.
9. Execute novamente `alembic upgrade head` para confirmar idempotência.
10. Não apague, sobrescreva ou importe dados locais.
11. Não faça deploy no Render.
12. Não exponha credenciais na saída.

Ao final, informe somente:

* arquivos alterados;
* testes executados;
* resultado da conexão;
* resultado das migrações;
* pendências encontradas.
