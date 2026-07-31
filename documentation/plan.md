# Volley Draw - Plano Inicial

## Etapa 1 - Preparacao do Projeto

- Objetivo: criar estrutura minima da aplicacao sem funcionalidades.
- Modulos esperados: configuracao FastAPI, estrutura `app/`, templates base, testes base.
- Tarefas: iniciar projeto, definir configuracao, criar healthcheck, preparar layout base.
- Conclusao: aplicacao sobe localmente e teste minimo passa.
- Dependencias: revisao e aprovacao dos artefatos.
- Riscos: criar estrutura maior que o necessario.

## Etapa 2 - Banco e Migracoes

- Objetivo: configurar PostgreSQL, SQLAlchemy e Alembic.
- Modulos esperados: conexao, base declarativa, migracoes iniciais.
- Tarefas: configurar engine/sessao, criar modelos iniciais aprovados, gerar migracao.
- Conclusao: migracoes aplicam e revertem em ambiente local.
- Dependencias: etapa 1.
- Riscos: definir campos definitivos antes da validacao do fluxo.

## Etapa 3 - Cadastro de Jogadores

- Objetivo: implementar regras de jogador no backend.
- Modulos esperados: modelo, schemas/formularios, rotas, servicos simples.
- Tarefas: criar, editar, ativar/desativar, validar notas e calcular media.
- Conclusao: testes cobrem validacoes e persistencia.
- Dependencias: etapa 2.
- Riscos: inconsistencia da media se armazenada sem protecao.

## Etapa 4 - Interface dos Jogadores

- Objetivo: criar telas responsivas para manutencao de jogadores.
- Modulos esperados: templates Jinja2 e fragmentos HTMX.
- Tarefas: listar, cadastrar, editar, alternar ativo, exibir media.
- Conclusao: fluxo funciona no navegador desktop e mobile.
- Dependencias: etapa 3.
- Riscos: excesso de interacao antes de validar uso real.

## Etapa 5 - Partidas e Presencas

- Objetivo: permitir criar partida e selecionar presentes.
- Modulos esperados: modelos de partida/presenca, rotas e templates.
- Tarefas: criar partida, listar ativos, marcar/desmarcar presenca.
- Conclusao: partida guarda lista de presentes.
- Dependencias: etapas 3 e 4.
- Riscos: nomes duplicados entre presentes.

## Etapa 6 - Integracao com API

- Objetivo: consumir a API publica de sorteio.
- Modulos esperados: cliente HTTPX, servico de payload, tratamento de erros.
- Tarefas: validar contrato da API, montar payload, chamar endpoint, tratar falhas.
- Conclusao: chamada real ou mockada em teste retorna times.
- Dependencias: etapa 5.
- Riscos: API indisponivel, contrato divergente, ausencia de identificador.

## Etapa 7 - Persistencia e Exibicao do Sorteio

- Objetivo: salvar e mostrar o resultado do sorteio.
- Modulos esperados: modelo de sorteio, templates de resultado.
- Tarefas: persistir parametros, payload, resposta bruta e resultado normalizado.
- Conclusao: resultado permanece acessivel apos recarregar a pagina.
- Dependencias: etapa 6.
- Riscos: resposta da API mudar de formato.

## Etapa 8 - Compartilhamento

- Objetivo: gerar texto simples para WhatsApp.
- Modulos esperados: funcao de formatacao e template.
- Tarefas: formatar times, incluir nome/data da partida se definido, permitir copia.
- Conclusao: texto gerado confere com resultado exibido.
- Dependencias: etapa 7.
- Riscos: formato final depender de preferencia do organizador.

## Etapa 9 - Historico

- Objetivo: consultar partidas e sorteios anteriores.
- Modulos esperados: rotas e templates de historico/detalhe.
- Tarefas: listar partidas, filtrar ordenacao basica, abrir detalhe do sorteio.
- Conclusao: historico permite recuperar resultados salvos.
- Dependencias: etapa 7.
- Riscos: volume futuro exigir paginacao.

## Etapa 10 - Testes

- Objetivo: consolidar cobertura essencial.
- Modulos esperados: testes de regras, rotas e integracao mockada.
- Tarefas: cobrir validacoes, media, presencas, payload, persistencia de sorteio.
- Conclusao: suite automatizada passa localmente.
- Dependencias: etapas anteriores.
- Riscos: testar detalhes de UI com baixo retorno inicial.

## Etapa 11 - Docker

- Objetivo: preparar ambiente local reproduzivel.
- Modulos esperados: Dockerfile e docker-compose.
- Tarefas: configurar app e PostgreSQL, variaveis e comandos de migracao.
- Conclusao: ambiente sobe com comando documentado.
- Dependencias: aplicacao funcional minima.
- Riscos: antecipar configuracao de deploy.

## Etapa 12 - Preparacao para Deploy

- Objetivo: deixar aplicacao pronta para publicacao controlada.
- Modulos esperados: configuracao de producao, checklist e documentacao.
- Tarefas: revisar variaveis, banco, migracoes, logs e dominio da API externa.
- Conclusao: checklist de deploy validado.
- Dependencias: etapas 1 a 11.
- Riscos: requisitos de hospedagem ainda nao definidos.
