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

Correcao em 2026-08-04:

- Problema observado: os multiselects nativos exigiam Ctrl/Shift para selecionar mais de um jogador em desktop; ao clicar em outro jogador, a selecao anterior podia ser perdida.
- Impacto: `force_together` e `force_apart` chegavam incompletos ao backend quando o usuario selecionava por cliques simples.
- Solucao adotada: substituir os multiselects por checkboxes com o mesmo `name`, preservando o formato urlencoded de multiplos valores e o contrato da API.

Correcao adicional em 2026-08-04:

- Problema observado: a quantidade de blocos dos criterios avancados ficava presa ao calculo inicial do backend.
- Impacto: ao alterar `Por time`, por exemplo 24 presentes e 4 por time, a tela continuava exibindo 4 blocos em vez de 6.
- Solucao adotada: renderizar blocos suficientes para os presentes e sincronizar a visibilidade pelo calculo `ceil(presentes / jogadores_por_time)`, desabilitando campos ocultos.

## Etapa 15 - Melhorias Visuais: Navegacao

Arquivos envolvidos:

- `app/templates/base.html`: ponto central da navegacao global.
- `app/templates/home.html`: entrada visual com atalhos para as abas existentes.
- `app/templates/players/index.html` e fragmentos de jogadores: remocao de link global redundante e ajuste estetico.
- `app/templates/matches/index.html`, `app/templates/matches/detail.html`, `app/templates/history/index.html`, `app/templates/history/detail.html` e `app/templates/auth/login.html`: ajuste visual sem alterar formularios, rotas ou campos.

Fluxo atual observado:

- Antes da etapa, a home concentrava links para Jogadores, Partidas, Historico e logout.
- As paginas internas usavam links `Inicio` ou `Voltar`; nao havia menu global no `base.html`.
- O projeto usa Tailwind por CDN e classes inline nos templates.

Decisoes:

- Implementar o menu no `base.html`, sem nova dependencia.
- Ocultar a navegacao na tela de login para evitar logout/menu antes da autenticacao.
- Manter links contextuais `Voltar` nos detalhes.
- Usar a paleta de `documentation/colorsdefault.md`.

Impacto tecnico:

- Sem alteracao de backend, banco, API, schemas ou regras de negocio.
- Risco principal: regressao de renderizacao Jinja ou de seletores esperados nos testes de pagina.

## Etapa 16 - Melhorias Visuais da Tela de Partida

Arquivos envolvidos:

- `app/templates/matches/detail.html`: tela principal de operacao da partida.
- `tests/test_draws.py`: testes de renderizacao e envio do formulario.

Escopo:

- Alteracao puramente visual em cards, botoes, campos, criterios avancados, resultado e lista de presentes.
- Sem alteracao de rotas, schemas, services, banco, nomes de campos ou contrato da API.

Riscos:

- Quebrar seletores esperados nos testes.
- Alterar acidentalmente `name`, `action`, `hx-post` ou estrutura enviada pelo formulario.

## Etapa 17 - Melhorias Visuais da Tela de Jogadores

Arquivos envolvidos:

- `app/templates/players/index.html`: cabecalho e importacao CSV.
- `app/templates/players/_form.html`: formulario de cadastro/edicao.
- `app/templates/players/_list.html`: listagem, status, media e acoes.
- `tests/test_player_pages.py`: cobertura de renderizacao e fluxo HTML existente.

Escopo:

- Alteracao puramente visual em hierarquia, espacamento, cards, badges, botoes e estados.
- Sem alteracao de rotas, actions, nomes de campos, validacoes, banco ou regras de negocio.

## Etapa 18 - Filtro de Presencas na Partida

Arquivos envolvidos:

- `app/templates/matches/detail.html`: lista de jogadores ativos e script local.
- `tests/test_draws.py`: cobertura de renderizacao do filtro na tela da partida.

Fluxo:

- O organizador digita no campo de busca da secao Presentes.
- A lista renderizada de jogadores ativos e filtrada no navegador por texto.
- Os formularios de presenca continuam enviando `player_id` e `present` para a mesma rota.

Impacto tecnico:

- Sem alteracao de backend, banco, API externa ou regras de sorteio.
- Risco principal: ocultar linhas no frontend sem feedback quando nao houver resultado.
