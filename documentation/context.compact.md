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

Etapa 16 - Melhorias Visuais da Tela de Partida concluida em 2026-08-04.

Implementado:

- `force_together` e `force_apart` na tela de detalhe da partida agora devem usar checkboxes com o mesmo `name` por grupo.
- Motivo: o multiselect nativo removia a selecao anterior em cliques simples, enviando grupos incompletos para a API.
- Os blocos dos criterios avancados sao sincronizados no frontend por `ceil(presentes / players_per_team)`; blocos ocultos ficam com inputs desabilitados.
- Backend nao precisa mudar: `_advanced_groups` ja le multiplos valores urlencoded por campo.
- Nova etapa deve ser puramente visual em `app/templates/matches/detail.html`, sem alterar rotas, nomes de campos, payload ou regras.
- Implementado: cabecalho de partida com badges, card de sorteio refinado, criterios em chips selecionaveis, resultado mais escaneavel, WhatsApp e lista de presentes com estados visuais melhores.

## Proximo Passo

Validar manualmente no navegador a tela de detalhe de uma partida com banco local disponivel. Deploy efetivo nao foi executado.






