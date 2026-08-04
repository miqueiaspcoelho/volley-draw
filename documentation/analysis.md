# Volley Draw - Analise Inicial

## Analise da Solucao

A solucao deve substituir a planilha por uma aplicacao web server-rendered, com foco em operacao rapida pelo celular. O MVP deve manter dados locais de jogadores, partidas e resultados, mas delegar o algoritmo de sorteio para a API publica existente.

## Avaliacao da Stack

A stack proposta e adequada ao MVP:

- FastAPI: backend simples, tipado e testavel.
- Jinja2 + HTMX: suficiente para interface responsiva sem SPA.
- Tailwind CSS: permite evoluir UI rapidamente com baixo custo.
- PostgreSQL: adequado para historico e integridade relacional.
- SQLAlchemy + Alembic: padrao consistente para modelos e migracoes.
- HTTPX: cliente HTTP apropriado para integracao externa.
- Pytest: cobre regras, servicos e rotas.
- Docker Compose: util para ambiente local e preparacao de deploy.

Nao ha justificativa tecnica inicial para substituir a stack.

## Arquitetura Proposta

- Backend FastAPI com rotas HTML e, se necessario, endpoints internos para HTMX.
- Camada de modelos SQLAlchemy para entidades persistidas.
- Templates Jinja2 para paginas e fragmentos.
- Servico de sorteio responsavel por montar payload, chamar API externa e normalizar resposta.
- Repositorios ou funcoes de acesso a dados apenas quando reduzirem duplicidade real.
- Configuracao por variaveis de ambiente, sem expor segredos no repositorio.

## Integracao com API Existente

A API publica em `https://apiteams-q4s3.onrender.com/api/doc` deve ser consumida inicialmente sem alteracao. Como a documentacao nao foi confirmada nesta etapa, a etapa de integracao deve validar:

- endpoint usado para sorteio;
- metodo HTTP;
- campos obrigatorios do payload;
- formato das habilidades;
- parametros de configuracao dos times;
- formato da resposta;
- erros esperados.

No MVP, a aplicacao pode enviar nome e habilidades. Como a API nao recebe nem devolve identificador interno do jogador, o pareamento do resultado dependera de nomes unicos.

Evolucao recomendada da API: aceitar campo opcional `player_id` ou `reference` e devolve-lo no resultado, mantendo compatibilidade com clientes atuais.

## Modelo de Dados Inicial

Entidades previstas:

- Jogador: id, nome, apelido opcional, saque, recepcao, levantamento, ataque, bloqueio, media geral, ativo, criado em, atualizado em.
- Partida: id, data/hora, status, observacao opcional, criado em, atualizado em.
- Presenca: partida, jogador, snapshot opcional das notas usadas.
- Sorteio: partida, parametros enviados, payload enviado, resposta recebida, times normalizados, criado em.

A media geral pode ser calculada dinamicamente para evitar inconsistencia. Se houver necessidade de consulta/ordenacao frequente, avaliar coluna armazenada com protecao por validacao ou coluna gerada.

## Fluxos Principais

- Cadastro de jogador: organizador informa dados e notas; sistema valida escala e calcula media.
- Preparacao da partida: organizador cria partida e seleciona presentes ativos.
- Sorteio: sistema monta payload, chama API externa, exibe retorno e persiste resultado.
- Compartilhamento: sistema gera texto simples com times para copia manual.
- Historico: organizador consulta partidas anteriores e seus sorteios.

## Riscos e Limitacoes

- Ausencia de identificador na API externa pode causar associacao incorreta quando houver nomes duplicados.
- Mudancas no contrato da API externa podem quebrar o sorteio.
- Disponibilidade ou latencia da API externa afeta a operacao da partida.
- Persistir apenas resposta normalizada pode dificultar auditoria; guardar payload e resposta bruta reduz esse risco.
- Autenticacao nao definida pode limitar uso em ambiente publico.

## Decisoes e Alternativas

- Usar API externa no MVP, sem reimplementar algoritmo.
- Manter aplicacao server-rendered, evitando complexidade de SPA.
- Comecar com nome unico como referencia operacional, registrando risco.
- Preferir media calculada dinamicamente ate haver necessidade clara de persistencia.
- Evitar funcionalidades fora do MVP para preservar escopo.

## Impacto da Ausencia de Identificador

Sem `player_id` ou `reference`, o resultado da API so pode ser reconciliado por nome. Isso exige nomes unicos no contexto do sorteio e torna alteracoes de nome mais sensiveis para historico. A aplicacao deve preservar snapshots do payload e da resposta para manter rastreabilidade.

## Etapa 14 - Criterios Avancados de Sorteio

Arquivos envolvidos:

- `app/templates/matches/detail.html`: formulario de sorteio na tela da partida.
- `app/routers/match_pages.py`: leitura do formulario HTML e conversao dos grupos selecionados.
- `app/services/draws.py`: montagem e validacao central do payload enviado para a API externa.
- `tests/test_draws.py`: cobertura de payload, validacoes e tela.

Fluxo definido:

- A tela da partida exibe uma secao opcional de criterios avancados no formulario de sorteio.
- A quantidade de blocos visuais de times e calculada a partir dos presentes e da sugestao atual de jogadores por time.
- Cada bloco oferece dois multiselects: `force_together` e `force_apart`.
- O formulario envia nomes de jogadores presentes para preservar o contrato da API externa.
- O servico valida que os nomes pertencem aos presentes e que nao ha duplicidade dentro do mesmo grupo.

Impacto tecnico:

- Nao houve alteracao estrutural de banco.
- O contrato externo permanece o mesmo: `force_together` e `force_apart` continuam como arrays de arrays de nomes.
- Chamadas sem criterios avancados continuam usando listas vazias.
