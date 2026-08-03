# Volley Draw - Contexto Compacto

## Proposito

Aplicacao web responsiva para substituir planilha no cadastro de jogadores, organizacao de partidas e sorteio equilibrado de times de volei.

## Stack

Python, FastAPI, Jinja2, HTMX, Tailwind CSS, PostgreSQL, SQLAlchemy, Alembic, HTTPX, Pytest e Docker Compose.

## Escopo Atual

MVP com jogadores, notas dos cinco fundamentos, media geral, partidas, presencas, integracao com API externa de sorteio, persistencia do resultado, texto para WhatsApp e historico.

## Entidades Principais

- Jogador.
- Partida.
- Presenca.
- Sorteio.

## Regras Fundamentais

- Notas de 0 a 5 com uma casa decimal.
- Media geral = media aritmetica de saque, recepcao, levantamento, ataque e bloqueio.
- Jogadores inativos nao aparecem por padrao na selecao de presenca.
- Historico deve preservar resultado de sorteios.

## Integracao Externa

API publica de sorteio: `https://apiteams-q4s3.onrender.com/api/doc`.

No MVP, consumir a API sem alterar seu contrato. Risco principal: API trabalha com nome/habilidades e nao com id interno. Usar nomes unicos inicialmente e avaliar evolucao futura com `player_id` ou `reference` opcional.

## Decisoes Confirmadas

- Nao reimplementar o algoritmo de sorteio inicialmente.
- Nao criar funcionalidades fora do MVP.
- Seguir desenvolvimento spec-driven por etapas autorizadas.
- Criar documentacao antes de codigo de producao.

## Restricoes

- Nao implementar Etapa 13 ou posteriores sem autorizacao explicita.
- Sem alterar a API externa.
- Sem commits sem ordem expressa.

## Etapa Atual

Etapa 12 de Docker concluida com Dockerfile, docker-compose app+PostgreSQL, migration no startup e README com comandos locais.

## Proximo Passo

Autorizar explicitamente a Etapa 13 - Preparacao para Deploy, se o ambiente Docker estiver aprovado.






