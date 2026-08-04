# Volley Draw - Especificacao Inicial

## Problema

O sorteio semanal de times de volei e feito manualmente em planilha, exigindo manutencao de jogadores, conferencia de nomes, atualizacao de habilidades, marcacao de presenca, montagem de payload, chamada manual de API externa e compartilhamento dos times.

## Objetivo

Criar uma aplicacao web responsiva, simples e pratica para cadastrar jogadores, organizar partidas, enviar participantes para a API publica de sorteio e armazenar os resultados.

## Usuarios

- Organizador da partida: cadastra jogadores, registra presencas, executa sorteios e compartilha resultados.
- Jogadores: recebem os times sorteados por texto compartilhado, inicialmente fora da aplicacao.

## Escopo do MVP

- Cadastro, edicao e ativacao/desativacao de jogadores.
- Registro das notas de saque, recepcao, levantamento, ataque e bloqueio.
- Calculo da media aritmetica geral.
- Criacao de partidas.
- Selecao de jogadores presentes.
- Definicao dos parametros de sorteio.
- Envio dos jogadores presentes para a API externa existente.
- Exibicao e persistencia dos times sorteados.
- Geracao de texto simples para WhatsApp.
- Consulta de historico de partidas e sorteios.

## Requisitos Funcionais

- RF01: Permitir cadastrar jogador com nome, apelido opcional, cinco notas tecnicas e status ativo.
- RF02: Permitir editar dados e notas de jogador existente.
- RF03: Permitir ativar ou desativar jogador sem remover seu historico.
- RF04: Calcular a media geral a partir dos cinco fundamentos.
- RF05: Permitir criar uma partida.
- RF06: Permitir selecionar jogadores presentes entre jogadores ativos.
- RF07: Permitir informar parametros necessarios para o sorteio.
- RF08: Enviar os presentes para a API publica de sorteio.
- RF09: Exibir os times retornados pela API.
- RF10: Armazenar o resultado do sorteio vinculado a partida.
- RF11: Gerar texto simples para compartilhamento no WhatsApp.
- RF12: Permitir consultar historico de partidas e sorteios.
- RF13: Permitir informar criterios opcionais `force_together` e `force_apart` na tela da partida antes do sorteio.
- RF14: Exibir navegacao global por menu lateral responsivo, acionado por hamburger, com acesso as abas existentes.
- RF15: Melhorar visualmente a tela de detalhe da partida sem alterar regras de negocio, rotas ou contratos.
- RF16: Melhorar visualmente a tela de jogadores sem alterar regras de cadastro, edicao, importacao ou ativacao.

## Requisitos Nao Funcionais

- Aplicacao responsiva, com uso prioritario em navegador mobile.
- Interface simples, objetiva e facil de operar durante a organizacao da partida.
- Navegacao responsiva deve preservar as telas existentes e usar a paleta definida em `documentation/colorsdefault.md`.
- Melhorias visuais devem preservar comportamento, payloads e compatibilidade mobile.
- Persistencia em PostgreSQL.
- Backend em Python com FastAPI.
- Templates server-side com Jinja2 e interacoes progressivas com HTMX.
- Estilos com Tailwind CSS.
- Testes automatizados com Pytest para regras e fluxos principais.
- Integracao HTTP com a API externa via HTTPX.
- Evolucao incremental por etapas pequenas e verificaveis.

## Regras de Negocio

- As notas dos fundamentos devem usar escala de 0 a 5, permitindo uma casa decimal.
- A media geral deve ser a media aritmetica simples dos cinco fundamentos.
- Jogadores desativados nao devem aparecer por padrao na selecao de presenca.
- Historico de partidas e sorteios deve preservar dados suficientes para auditoria do resultado exibido.
- No MVP, a integracao com a API externa pode usar nomes unicos como identificador operacional.
- Nomes duplicados representam risco e devem ser prevenidos ou tratados antes do sorteio.
- Os criterios `force_together` e `force_apart` sao opcionais; quando nao preenchidos, o sorteio deve manter o comportamento padrao.
- Os criterios avancados devem usar apenas jogadores presentes na partida e nao devem aceitar nomes duplicados dentro do mesmo grupo.

## Criterios de Aceite

- O organizador consegue manter a lista de jogadores ativos.
- O organizador consegue criar uma partida e marcar presentes.
- A aplicacao consegue chamar a API externa com os jogadores presentes.
- O resultado retornado e exibido e persistido.
- O historico permite consultar partidas e sorteios anteriores.
- O texto para WhatsApp pode ser copiado e compartilhado manualmente.
- O organizador consegue selecionar grupos opcionais de jogadores para manter juntos ou separar, por blocos visuais de times possiveis.
- Nos criterios avancados, cada jogador marcado deve permanecer selecionado ao marcar outro jogador do mesmo grupo.
- A quantidade de blocos dos criterios avancados deve acompanhar a quantidade de jogadores presentes dividida por `Por time`, arredondando para cima.
- A tela de detalhe da partida deve ter hierarquia visual clara para sorteio, criterios, resultado, WhatsApp e presentes.
- A tela de jogadores deve ter hierarquia visual clara para cadastro, importacao, listagem, media e status.
- O organizador consegue abrir o menu lateral, ver o fundo desfocado e navegar entre Inicio, Jogadores, Partidas e Historico.
- Nenhuma funcionalidade fora do MVP e implementada sem nova autorizacao.

## Fora do Escopo

- Aplicativo mobile nativo.
- Campeonatos.
- Pagamentos.
- Gestao de quadras.
- Upload obrigatorio de fotos.
- Multiplas organizacoes.
- Integracao com projeto de terceiros.
- Estatisticas esportivas avancadas.
- Chat.
- Notificacoes.
- Autenticacao social.
- Microsservicos.

## Duvidas Abertas

- Quais parametros exatos a API externa exige para o sorteio.
Descricao: Realiza o sorteio balanceado de times.

Campos do payload:

Campo	Tipo	Obrigatorio	Padrao	Descricao
players	array	Sim	-	Lista de jogadores que participarao do sorteio.
players_per_team	number	Nao	6	Quantidade maxima de jogadores por time.
range	number	Nao	2	Intervalo usado para agrupar jogadores por overall antes da distribuicao.
force_together	array de arrays	Nao	[]	Grupos de nomes que devem ficar no mesmo time.
force_apart	array de arrays	Nao	[]	Grupos de nomes que nunca podem ficar no mesmo time.
Campos de cada jogador:

Campo	Tipo	Descricao
name	string	Nome unico do jogador.
serving	number	Nota de saque.
passing	number	Nota de passe.
setting	number	Nota de levantamento.
attacking	number	Nota de ataque.
blocking	number	Nota de bloqueio.

{
  "players_per_team": 6,
  "range": 2,
  "force_together": [
    [
      "Miqueias",
      "David"
    ]
  ],
  "force_apart": [
    [
      "Joao",
      "Pedro"
    ]
  ],
  "players": [
    {
      "name": "Miqueias",
      "serving": 5,
      "passing": 4,
      "setting": 3,
      "attacking": 5,
      "blocking": 4
    },
    {
      "name": "David",
      "serving": 4,
      "passing": 4,
      "setting": 3,
      "attacking": 4,
      "blocking": 5
    },
    {
      "name": "Joao",
      "serving": 3,
      "passing": 5,
      "setting": 4,
      "attacking": 3,
      "blocking": 4
    },
    {
      "name": "Pedro",
      "serving": 4,
      "passing": 3,
      "setting": 4,
      "attacking": 5,
      "blocking": 3
    }
  ]
}
- Qual formato exato de payload e resposta da API externa.
{
  "success": true,
  "data": {
    "leftovers": [],
    "teams": [
      {
        "team_name": "Time 1",
        "average_overall": 4.1,
        "total_overall": 8.2,
        "players": [
          {
            "name": "Miqueias",
            "overall": 4.2
          },
          {
            "name": "David",
            "overall": 4.0
          }
        ]
      }
    ]
  }
}
- Se o MVP tera autenticacao simples ou uso local por um unico organizador. -> possuir autenticacao (sistema web)
- Se nomes de jogadores devem ser globalmente unicos ou apenas unicos entre ativos. -> inicialmente globalmente unicos
- Se a media geral sera armazenada, calculada dinamicamente ou protegida por coluna gerada/validacao. -> media calculada
- Quais campos devem compor o texto padrao de WhatsApp. deve seguir o padrão abaixo:
Time 1

* David
* Daniel conv lucas l
* Nayra conv yan
* Jean

Time 2

* Arthur conv césar
* Paulo rubim
* Leticia conv lucas l
* Camila

Time 3

* Victor
* Filipe conv lucas
* César
* Izabel

Time 4

* Higor
* Samuel conv cesar
* Gustavo conv victor
* Stela conv victor

Time 5

* Geanderson conv yan
* Well conv lucas
* Ingridy conv lucas
* Joao conv yan

Time 6

* Daniel
* Yan
* Luene
* Lucas lima

