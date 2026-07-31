AGENTS.md

## Projeto

Este repositório contém uma aplicação web para cadastro de jogadores, organização de partidas e sorteio equilibrado de times de vôlei.

## Metodologia

O desenvolvimento segue uma abordagem spec-driven.

Antes de implementar uma etapa:

1. leia `documentation/spec.md`;
2. leia `documentation/analysis.md`;
3. leia `documentation/plan.md`;
4. leia `documentation/context.compact.md`;
5. identifique a etapa autorizada;
6. não implemente etapas futuras.

Quando os artefatos ainda não existirem, a primeira tarefa deve ser criá-los e submetê-los à revisão antes da implementação.

## Diretrizes

* Trabalhe em modo econômico de tokens.
* Não repita informações já documentadas.
* Faça alterações pequenas e verificáveis.
* Não altere comportamento fora do escopo solicitado.
* Evite abstrações prematuras.
* Evite arquitetura excessiva.
* Priorize clareza e manutenção.
* Não implemente funcionalidades sem autorização.
* Informe arquivos alterados ao concluir.
* Informe testes executados e seus resultados.
* Registre riscos e limitações encontrados.
* Preserve compatibilidade com a stack definida nos artefatos.

## Stack prevista

* Python;
* FastAPI;
* Jinja2;
* HTMX;
* Tailwind CSS;
* PostgreSQL;
* SQLAlchemy;
* Alembic;
* HTTPX;
* Pytest;
* Docker Compose.

A stack somente deve ser modificada quando houver justificativa registrada e aprovação.

## Organização

A documentação spec-driven deve permanecer em:

* `documentation/spec.md`;
* `documentation/analysis.md`;
* `documentation/plan.md`;
* `documentation/context.compact.md`.

## Implementação

Não implemente todo o plano de uma vez.

Implemente somente a etapa explicitamente autorizada pelo usuário. Ao concluir, pare e apresente o resultado para avaliação.

## Ambiente Python

Antes de instalar dependências ou criar artefatos que dependam de pacotes Python, crie e use um ambiente virtual local em `.venv`.

As dependências do projeto devem ser instaladas dentro de `.venv`, não no Python global do sistema.
