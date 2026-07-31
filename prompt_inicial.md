Estamos iniciando um novo projeto chamado `volley-draw`.

O diretório ainda não possui implementação nem os artefatos spec-driven. Nesta etapa, sua responsabilidade é analisar a proposta e criar a documentação inicial. Não escreva código de produção.

## Contexto

O projeto será uma aplicação web responsiva para organizar sorteios semanais de times de vôlei.

Atualmente, o processo é feito manualmente em uma planilha:

* manter a lista de jogadores;
* conferir nomes;
* atualizar as habilidades;
* marcar quem participará;
* montar o payload;
* chamar uma API de sorteio;
* organizar e compartilhar os times.

O objetivo é substituir esse processo por uma aplicação simples, bonita, funcional e prática.

Já existe uma API pública responsável pelo sorteio dos times. Inicialmente, a nova aplicação deve consumir essa API, sem reimplementar o algoritmo.

Documentação da API existente:

`https://apiteams-q4s3.onrender.com/api/doc`

## Stack inicialmente considerada

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

A stack ainda deve ser avaliada nos artefatos, mas não deve ser substituída sem justificativa técnica clara.

## Escopo pretendido para o MVP

O MVP deve permitir:

1. cadastrar jogadores;
2. editar jogadores;
3. ativar ou desativar jogadores;
4. armazenar as notas dos cinco fundamentos:

   * saque;
   * recepção;
   * levantamento;
   * ataque;
   * bloqueio;
5. calcular a média aritmética dos cinco fundamentos;
6. criar uma partida;
7. selecionar os jogadores presentes;
8. definir os parâmetros do sorteio;
9. enviar os jogadores presentes para a API existente;
10. exibir os times sorteados;
11. armazenar o resultado do sorteio;
12. gerar um texto simples para compartilhamento no WhatsApp;
13. consultar o histórico de partidas e sorteios.

## Identificação dos jogadores

A nova aplicação terá um identificador interno para cada jogador.

A API de sorteio existente ainda não recebe nem devolve o identificador do jogador. Atualmente, ela trabalha com nome e habilidades.

Considere esta limitação na análise.

A primeira integração pode utilizar nomes únicos, mas a documentação deve registrar o risco dessa abordagem e avaliar uma evolução compatível da API para aceitar uma referência opcional, como `player_id` ou `reference`.

Não altere a API existente nesta etapa.

## Modelo conceitual inicial do jogador

Considere inicialmente:

* id;
* nome;
* apelido opcional;
* saque;
* recepção;
* levantamento;
* ataque;
* bloqueio;
* média geral;
* ativo;
* data de criação;
* data de atualização.

As habilidades devem utilizar uma escala de 0 a 5, permitindo uma casa decimal.

A média geral deve corresponder à média aritmética dos cinco fundamentos.

Avalie nos artefatos se a média deve ser armazenada, calculada dinamicamente ou protegida por alguma estratégia de consistência.

## Fora do MVP

Não inclua inicialmente:

* aplicativo mobile nativo;
* campeonatos;
* pagamentos;
* gestão de quadras;
* upload obrigatório de fotos;
* múltiplas organizações;
* integração com o projeto de terceiros;
* estatísticas esportivas avançadas;
* chat;
* notificações;
* autenticação social;
* arquitetura de microsserviços.

A interface deve ser responsiva e preparada para uso pelo navegador do celular.

## Metodologia

Crie os seguintes arquivos:

* `documentation/spec.md`;
* `documentation/analysis.md`;
* `documentation/plan.md`;
* `documentation/context.compact.md`.

### `spec.md`

Deve registrar:

* problema;
* objetivo;
* usuários;
* escopo do MVP;
* requisitos funcionais;
* requisitos não funcionais;
* regras de negócio;
* critérios de aceite;
* itens fora do escopo;
* dúvidas ainda abertas.

### `analysis.md`

Deve registrar:

* análise da solução;
* avaliação da stack;
* proposta de arquitetura;
* integração com a API existente;
* modelo de dados inicial;
* fluxos principais;
* riscos;
* limitações;
* decisões e alternativas consideradas;
* impacto da ausência de identificador na API de sorteio.

Não trate decisões ainda não confirmadas como definitivas.

### `plan.md`

Deve dividir o trabalho em etapas pequenas e verificáveis.

Considere, no mínimo:

1. preparação do projeto;
2. banco e migrações;
3. cadastro de jogadores;
4. interface dos jogadores;
5. partidas e presenças;
6. integração com a API;
7. persistência e exibição do sorteio;
8. compartilhamento;
9. histórico;
10. testes;
11. Docker;
12. preparação para deploy.

Cada etapa deve conter:

* objetivo;
* arquivos ou módulos esperados;
* tarefas;
* critérios de conclusão;
* dependências;
* riscos relevantes.

### `context.compact.md`

Deve conter apenas o contexto essencial para futuras sessões:

* propósito do sistema;
* stack;
* escopo atual;
* principais entidades;
* regras fundamentais;
* integração externa;
* decisões confirmadas;
* restrições;
* etapa atual;
* próximo passo.

Evite repetir integralmente os demais documentos.

## Restrições

* Não implemente código de produção.
* Não instale dependências.
* Não configure Docker.
* Não gere migrações.
* Não crie tabelas.
* Não altere a API de sorteio.
* Não adicione funcionalidades fora do MVP.
* Não use arquitetura excessivamente complexa.
* Não crie abstrações prematuras.
* Não assuma requisitos que não foram informados.
* Registre dúvidas relevantes sem bloquear a criação dos artefatos.
* Trabalhe em modo econômico de tokens.
* Evite duplicação entre os documentos.

## Resultado esperado

Ao final:

1. crie os quatro arquivos dentro de `documentation/`;
2. apresente os arquivos criados;
3. resuma as principais decisões propostas;
4. destaque dúvidas, riscos e decisões que dependem de aprovação;
5. indique qual artefato deve ser revisado primeiro;
6. não inicie a implementação.
