# Volley Draw - Plano Inicial

## Acompanhamento

- Etapa 1 - Preparacao do Projeto: concluida em 2026-07-31.
- Etapa 2 - Banco e Migracoes: concluida em 2026-08-03.
- Etapa 3 - Cadastro de Jogadores: concluida em 2026-08-03.
- Etapa 4 - Interface dos Jogadores: concluida em 2026-08-03.
- Etapa 5 - Partidas e Presencas: concluida em 2026-08-03.
- Etapa 6 - Integracao com API: concluida em 2026-08-03.
- Etapa 7 - Persistencia e Exibicao do Sorteio: concluida em 2026-08-03.
- Etapa 8 - Compartilhamento: concluida em 2026-08-03.
- Etapa 9 - Historico: concluida em 2026-08-03.
- Etapa 10 - Autenticacao com Usuarios e PIN: concluida em 2026-08-03.
- Etapa 11 - Testes: concluida em 2026-08-03.
- Etapa 12 - Docker: concluida em 2026-08-03.
- Etapa 13 - Preparacao para Deploy: concluida em 2026-08-03.
- Etapa 14 - Criterios Avancados de Sorteio por Partida: concluida em 2026-08-04.
- Etapa 15 - Melhorias Visuais: Navegacao Lateral Responsiva: concluida em 2026-08-04.
- Etapa 16 - Melhorias Visuais da Tela de Partida: concluida em 2026-08-04.


## Etapa 1 - Preparacao do Projeto

Status: concluida em 2026-07-31.

- Objetivo: criar estrutura minima da aplicacao sem funcionalidades.
- Modulos esperados: configuracao FastAPI, estrutura `app/`, templates base, testes base.
- Tarefas: iniciar projeto, definir configuracao, criar healthcheck, preparar layout base.
- Conclusao: aplicacao sobe localmente e teste minimo passa.
- Dependencias: revisao e aprovacao dos artefatos.
- Riscos: criar estrutura maior que o necessario.

## Etapa 2 - Banco e Migracoes

Status: concluida em 2026-08-03.

- Objetivo: configurar PostgreSQL, SQLAlchemy e Alembic.
- Modulos esperados: conexao, base declarativa, migracoes iniciais.
- Tarefas: configurar engine/sessao, criar modelos iniciais aprovados, gerar migracao.
- Conclusao: migracoes aplicam e revertem em ambiente local.
- Dependencias: etapa 1.
- Riscos: definir campos definitivos antes da validacao do fluxo.

## Etapa 3 - Cadastro de Jogadores

Status: concluida em 2026-08-03.

- Objetivo: implementar regras de jogador no backend.
- Modulos esperados: modelo, schemas/formularios, rotas, servicos simples.
- Tarefas: criar, editar, ativar/desativar, validar notas e calcular media.
- Conclusao: testes cobrem validacoes e persistencia.
- Dependencias: etapa 2.
- Riscos: inconsistencia da media se armazenada sem protecao.

## Etapa 4 - Interface dos Jogadores

Status: concluida em 2026-08-03.

- Objetivo: criar telas responsivas para manutencao de jogadores.
- Modulos esperados: templates Jinja2 e fragmentos HTMX.
- Tarefas: listar, cadastrar, editar, alternar ativo, exibir media.
- Conclusao: fluxo funciona no navegador desktop e mobile.
- Dependencias: etapa 3.
- Riscos: excesso de interacao antes de validar uso real.

## Etapa 5 - Partidas e Presencas

Status: concluida em 2026-08-03.

- Objetivo: permitir criar partida e selecionar presentes.
- Modulos esperados: modelos de partida/presenca, rotas e templates.
- Tarefas: criar partida, listar ativos, marcar/desmarcar presenca.
- Conclusao: partida guarda lista de presentes.
- Dependencias: etapas 3 e 4.
- Riscos: nomes duplicados entre presentes.

## Etapa 6 - Integracao com API

Status: concluida em 2026-08-03.

- Objetivo: consumir a API publica de sorteio.
- Modulos esperados: cliente HTTPX, servico de payload, tratamento de erros.
- Tarefas: validar contrato da API, montar payload, chamar endpoint, tratar falhas.
- Conclusao: chamada real ou mockada em teste retorna times.
- Dependencias: etapa 5.
- Riscos: API indisponivel, contrato divergente, ausencia de identificador.

## Etapa 7 - Persistencia e Exibicao do Sorteio

Status: concluida em 2026-08-03.

- Objetivo: salvar e mostrar o resultado do sorteio.
- Modulos esperados: modelo de sorteio, templates de resultado.
- Tarefas: persistir parametros, payload, resposta bruta e resultado normalizado.
- Conclusao: resultado permanece acessivel apos recarregar a pagina.
- Dependencias: etapa 6.
- Riscos: resposta da API mudar de formato.

## Etapa 8 - Compartilhamento

Status: concluida em 2026-08-03.

- Objetivo: gerar texto simples para WhatsApp.
- Modulos esperados: funcao de formatacao e template.
- Tarefas: formatar times, incluir nome/data da partida se definido, permitir copia.
- Conclusao: texto gerado confere com resultado exibido.
- Dependencias: etapa 7.
- Riscos: formato final depender de preferencia do organizador.

## Etapa 9 - Historico

Status: concluida em 2026-08-03.

- Objetivo: consultar partidas e sorteios anteriores.
- Modulos esperados: rotas e templates de historico/detalhe.
- Tarefas: listar partidas, filtrar ordenacao basica, abrir detalhe do sorteio.
- Conclusao: historico permite recuperar resultados salvos.
- Dependencias: etapa 7.
- Riscos: volume futuro exigir paginacao.

## Etapa 10 - Autenticacao com Usuarios e PIN

Status: concluida em 2026-08-03.

- Objetivo: restringir acesso ao app com usuarios locais e PIN.
- Modulos esperados: tabela users, hash de PIN, login/logout, sessao por cookie, protecao de rotas.
- Tarefas: criar modelo e migracao de users, servico de autenticacao, tela de login, middleware/dependencia de sessao, seed ou CLI para primeiro usuario.
- Conclusao: app exige login para acessar jogadores, partidas, sorteios e historico.
- Dependencias: etapa 9.
- Riscos: recuperacao de acesso depender de seed/CLI ou edicao administrativa; PIN fraco exige HTTPS e segredo de sessao forte em producao.

## Etapa 11 - Testes

Status: concluida em 2026-08-03.

- Objetivo: consolidar cobertura essencial.
- Modulos esperados: testes de regras, rotas e integracao mockada.
- Tarefas: cobrir validacoes, media, presencas, payload, persistencia de sorteio, historico e autenticacao.
- Conclusao: suite automatizada passa localmente.
- Dependencias: etapas anteriores.
- Riscos: testar detalhes de UI com baixo retorno inicial.

## Etapa 12 - Docker

Status: concluida em 2026-08-03.

- Objetivo: preparar ambiente local reproduzivel.
- Modulos esperados: Dockerfile e docker-compose.
- Tarefas: configurar app e PostgreSQL, variaveis e comandos de migracao.
- Conclusao: ambiente sobe com comando documentado.
- Dependencias: aplicacao funcional minima.
- Riscos: antecipar configuracao de deploy.

## Etapa 13 - Preparacao para Deploy

Status: concluida em 2026-08-03.

- Objetivo: deixar aplicacao pronta para publicacao controlada.
- Modulos esperados: configuracao de producao, checklist e documentacao.
- Tarefas: revisar variaveis, banco, migracoes, logs, dominio da API externa, HTTPS, segredo de sessao e usuario inicial.
- Conclusao: checklist de deploy validado para Neon e Render Docker, sem executar deploy efetivo.
- Dependencias: etapas 1 a 12.
- Riscos: requisitos de hospedagem ainda nao definidos.

## Etapa 14 - Criterios Avancados de Sorteio por Partida

Status: concluida em 2026-08-04.

- Objetivo: adicionar na aba de partidas uma forma simples e visualmente clara de preencher os criterios opcionais da API externa `force_together` e `force_apart`, considerando a quantidade de times configurada para a partida.
- Comportamento esperado: para cada um dos N times possiveis, o organizador pode definir dois grupos independentes:
  - grupo `force_together`: jogadores que devem ser mantidos juntos quando a API conseguir cumprir a restricao;
  - grupo `force_apart`: jogadores que devem ser separados quando a API conseguir cumprir a restricao.
- Regra principal: ambos os criterios sao opcionais. Se nenhum grupo for definido, o sorteio deve continuar funcionando com o payload atual, sem alterar o comportamento existente.
- Proposta de interface: adicionar uma secao expansivel ou painel "Criterios avancados" dentro da tela da partida, abaixo da selecao de presentes e antes da acao de sortear. A secao deve iniciar recolhida ou visualmente secundaria para nao poluir o fluxo principal.
- Organizacao visual sugerida:
  - renderizar um bloco por time, de `Time 1` ate `Time N`, derivado da quantidade de times informada;
  - dentro de cada bloco, exibir duas areas lado a lado em desktop e empilhadas no mobile: "Manter juntos" e "Separar";
  - cada area deve permitir selecionar multiplos jogadores presentes na partida;
  - usar nomes claros e textos curtos de ajuda para reforcar que os campos sao opcionais.
- Forma eficiente de preenchimento: reutilizar a lista de jogadores presentes ja carregada na partida, evitando nova consulta ou novo fluxo de cadastro. Quando a lista de presentes mudar, os seletores dos criterios devem refletir apenas jogadores ainda presentes.
- Validacoes de UI/backend a planejar antes da implementacao:
  - nao permitir jogador inexistente ou ausente nos grupos;
  - evitar duplicidade dentro do mesmo grupo;
  - avaliar se o mesmo jogador pode aparecer em grupos conflitantes do mesmo time e, se nao puder, retornar erro claro;
  - manter o envio sem esses campos quando todos os grupos estiverem vazios;
  - garantir que a estrutura enviada esteja aderente ao contrato atual da API externa.
- Arquivos provaveis a alterar:
  - templates da tela/fragmentos de partidas;
  - schemas ou formularios relacionados ao sorteio;
  - servico que monta o payload para a API externa;
  - testes do payload e validacoes de entrada;
  - documentacao `spec.md`, `analysis.md`, `plan.md` e `context.compact.md`.
- Testes necessarios:
  - sorteio sem criterios avancados preserva payload atual;
  - preenchimento de `force_together` para um ou mais times;
  - preenchimento de `force_apart` para um ou mais times;
  - combinacao dos dois criterios;
  - grupos vazios nao quebram a chamada;
  - jogador ausente ou duplicado gera erro esperado;
  - quantidade de blocos acompanha a quantidade de times.
- Validacoes:
  - revisar contrato real da API antes de implementar os nomes e formato exato dos campos;
  - executar testes automatizados relacionados a partidas, payload e integracao mockada;
  - validar responsividade da tela em desktop e mobile.
- Rollback: remover a secao de criterios avancados da interface e deixar o servico de payload ignorando `force_together` e `force_apart`, preservando o fluxo atual de sorteio.
- Conclusao: tela de partida permite informar criterios avancados opcionais em blocos por time possivel; backend envia os grupos para a API externa e valida jogadores ausentes ou duplicados.
- Correcao 2026-08-04: substituir multiselects nativos por checkboxes para permitir marcar varios jogadores por cliques simples, sem alterar nomes de campos, parser do formulario ou contrato da API.
- Correcao 2026-08-04: fazer os blocos de criterios avancados acompanharem o campo `Por time`; exemplo, 24 presentes e 4 por time exibem 6 blocos.

## Etapa 15 - Melhorias Visuais: Navegacao Lateral Responsiva

Status: concluida em 2026-08-04.

- Objetivo: adicionar navegacao global responsiva por menu lateral estilo hamburger, com fundo desfocado ao abrir, usando a paleta definida em `documentation/colorsdefault.md`.
- Arquivos alterados: templates base, home, jogadores, partidas, historico e login; documentacao spec-driven.
- Escopo: somente visual estetico. Sem alteracao de funcionalidade, rotas, contratos de API, banco ou migracoes.
- Tarefas:
  - criar header com botao hamburger em `base.html`;
  - criar drawer lateral com Inicio, Jogadores, Partidas, Historico e Sair;
  - aplicar overlay com `backdrop-blur`;
  - destacar rota atual no menu;
  - remover links globais `Inicio` redundantes das paginas principais;
  - ajustar bordas, botoes e campos para a paleta oficial.
- Testes necessarios: suite automatizada existente para garantir que paginas e formularios continuam renderizando e funcionando.
- Validacoes: abrir menu, fechar por botao, overlay e Escape; validar visual em mobile e desktop.
- Rollback: reverter alteracoes dos templates da etapa e manter documentacao anterior.
- Conclusao: navegacao lateral responsiva implementada sem alterar comportamento funcional.

## Etapa 16 - Melhorias Visuais da Tela de Partida

Status: concluida em 2026-08-04.

- Objetivo: modernizar visualmente a tela de detalhe da partida, mantendo comportamento atual.
- Arquivos a alterar: `app/templates/matches/detail.html`, testes de renderizacao quando necessario e documentacao spec-driven.
- Escopo: hierarquia, espacamento, cards, botoes, lista de presentes, criterios avancados, resultado e WhatsApp.
- Fora do escopo: backend, banco, API externa, regras de sorteio, nomes de campos, rotas e novas dependencias.
- Testes: executar suite automatizada existente.
- Conclusao: tela de detalhe da partida recebeu ajustes visuais em hierarquia, secoes, campos, botoes, criterios avancados, resultado e lista de presentes, sem alterar comportamento funcional.



