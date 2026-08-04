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

- Nao implementar etapas futuras sem autorizacao explicita.
- Sem alterar a API externa.
- Sem commits sem ordem expressa.

## Etapa Atual

Etapa 14 de Criterios Avancados de Sorteio por Partida concluida em 2026-08-04.

Implementado:

- Secao opcional "Criterios avancados" na tela de detalhe da partida.
- Blocos visuais por time possivel, calculados a partir dos presentes e da sugestao de jogadores por time.
- Multiselects para `force_together` e `force_apart`.
- Conversao do formulario HTML para arrays de arrays de nomes aceitos pela API externa.
- Validacao central no servico de sorteio para rejeitar jogador ausente e duplicidade dentro do mesmo grupo.
- Testes de payload, validacao e renderizacao/envio pela tela.

## Proximo Passo

Se aprovado, validar manualmente no navegador o preenchimento mobile/desktop dos criterios avancados. Deploy efetivo nao foi executado.






