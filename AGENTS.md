# AGENTS.md

## Projeto

O `volley-draw` é uma aplicação para gerenciamento de jogadores e geração de times equilibrados para partidas de vôlei.

Stack principal:

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Alembic
* Pydantic
* Pytest
* Docker
* Neon Database
* Render

## Objetivo deste arquivo

Este arquivo define como agentes de IA devem analisar, modificar, testar e documentar o projeto.

As instruções deste arquivo devem ser seguidas antes de qualquer implementação.

---

## Regras gerais

1. Leia o código existente antes de propor alterações.
2. Não crie uma nova arquitetura sem necessidade comprovada.
3. Preserve o padrão atual do projeto.
4. Faça alterações pequenas, objetivas e fáceis de revisar.
5. Evite refatorações fora do escopo da demanda.
6. Não altere contratos de API sem documentar o impacto.
7. Não remova comportamentos existentes sem autorização explícita.
8. Não adicione dependências sem necessidade.
9. Não exponha credenciais, tokens, senhas ou URLs privadas.
10. Nunca versionar arquivos `.env`.

## Compatibilidade

Toda alteração deve permanecer compatível com:

* execução local;
* Docker;
* PostgreSQL;
* Neon Database;
* deploy no Render;
* migrações Alembic existentes.

SQLite não deve ser usado como referência para comportamentos específicos do PostgreSQL.

---

## Fluxo spec-driven

Antes de implementar uma demanda relevante, utilize os artefatos:

* `documentation/spec.md`
* `documentation/analysis.md`
* `documentation/plan.md`
* `documentation/context.compact.md`

### spec.md

Deve conter:

* problema;
* comportamento atual;
* comportamento esperado;
* regras de negócio;
* critérios de aceitação;
* pontos fora do escopo.

### analysis.md

Deve conter:

* arquivos envolvidos;
* fluxo atual;
* possíveis causas;
* riscos;
* dependências;
* alternativas consideradas;
* impacto técnico.

Não implementar durante a etapa de análise.

### plan.md

Deve conter:

* etapas de implementação;
* arquivos que serão alterados;
* testes necessários;
* validações;
* estratégia de rollback quando aplicável.

### context.compact.md

Deve conter somente o contexto necessário para continuar a demanda com baixo consumo de tokens:

* objetivo;
* decisões tomadas;
* arquivos relevantes;
* regras importantes;
* pendências;
* próximo passo.

## Ordem padrão

1. Investigar.
2. Atualizar `spec.md`.
3. Atualizar `analysis.md`.
4. Apresentar os achados.
5. Atualizar `plan.md`.
6. Validar o plano.
7. Implementar.
8. Executar testes.
9. Atualizar `context.compact.md`.
10. Apresentar resumo final.

Para correções pequenas e claramente delimitadas, os documentos podem ser atualizados de forma resumida.

---

## Arquitetura

Respeite as responsabilidades já existentes no projeto.

De forma geral:

* rotas recebem e validam requisições HTTP;
* schemas definem entrada e saída;
* serviços ou controllers concentram regras de negócio;
* models e repositories realizam persistência;
* configurações ficam centralizadas em `app/core`;
* migrações ficam em `migrations`;
* comandos administrativos ficam em `app/cli`.

Não colocar consultas SQL, regras complexas ou acesso direto ao banco dentro das rotas.

Não duplicar regras de negócio entre API, CLI e outros pontos de entrada.

Quando uma regra for usada por mais de uma interface, extraí-la para uma camada reutilizável.

---

## Banco de dados

O banco de produção é PostgreSQL hospedado no Neon.

### Regras

* Toda mudança estrutural deve possuir migração Alembic.
* Não alterar tabelas manualmente como solução definitiva.
* Não editar migrações já aplicadas em produção.
* Criar uma nova migração para cada mudança posterior.
* Verificar se existe apenas uma Alembic head.
* Migrações devem ser seguras e, quando possível, reversíveis.
* Operações repetidas não devem causar inconsistência.
* Respeitar constraints, índices e relacionamentos existentes.
* Evitar consultas N+1.
* Avaliar concorrência em operações de sorteio, cadastro e atualização.

### Comandos de validação

```bash
alembic heads
alembic current
alembic upgrade head
```

Sempre que possível, validar também uma segunda execução de:

```bash
alembic upgrade head
```

Ela não deve criar novas alterações nem falhar.

### DATABASE_URL

A conexão deve ser obtida por variável de ambiente.

O projeto pode receber uma URL no formato:

```text
postgresql://...
```

Quando necessário para o SQLAlchemy, a aplicação deve normalizar para:

```text
postgresql+psycopg://...
```

Não registrar a URL completa do banco em logs.

Não incluir credenciais reais em:

* código;
* documentação;
* testes;
* commits;
* mensagens de erro;
* exemplos versionados.

---

## Regras do sorteio

Alterações no algoritmo de sorteio devem preservar as regras de negócio já definidas.

Antes de modificar o algoritmo:

1. identificar os critérios atuais;
2. registrar os casos de borda;
3. criar ou atualizar testes;
4. comparar os resultados antes e depois;
5. evitar resultados dependentes da ordem acidental dos registros.

O sorteio deve considerar, conforme as regras existentes:

* quantidade de jogadores;
* número de times;
* nível ou overall dos jogadores;
* equilíbrio entre os times;
* jogadores que ficaram de fora;
* distribuição de mulheres, quando aplicável;
* critérios de desempate;
* comportamento quando não for possível cumprir todas as restrições.

Quando uma restrição não puder ser cumprida, o sistema deve priorizar as regras explicitamente definidas no domínio e retornar um resultado válido e previsível.

O algoritmo não deve depender de valores fixos que poderiam estar configurados no banco ou na requisição.

Testes do sorteio devem cobrir pelo menos:

* quantidade exata de jogadores;
* jogadores excedentes;
* jogadores insuficientes;
* níveis muito diferentes;
* quantidade ímpar;
* múltiplas mulheres no mesmo time;
* ausência de mulheres em outros times;
* impossibilidade matemática de distribuição perfeita;
* repetição do sorteio;
* entrada inválida.

Quando houver aleatoriedade, os testes devem usar uma semente controlada ou abstração equivalente.

---

## Usuários e segurança

A criação de usuários administrativos deve ocorrer por comando CLI ou fluxo explicitamente autorizado.

Exemplo de comando:

```bash
python -m app.cli.users create <usuario> "<nome>" --pin "<pin>"
```

Regras:

* não criar usuário padrão automaticamente em produção;
* não salvar PIN em texto puro;
* não exibir hashes ou credenciais em logs;
* validar duplicidade antes da criação;
* retornar mensagens claras no CLI;
* não colocar credenciais em Dockerfile ou `render.yaml`;
* não incluir credenciais reais em exemplos de documentação.

Comandos administrativos devem reutilizar as mesmas regras de domínio da aplicação.

---

## API

As rotas devem:

* utilizar schemas Pydantic;
* retornar status HTTP apropriado;
* possuir contratos de resposta claros;
* evitar retornos `null` acidentais;
* tratar registros inexistentes;
* tratar conflitos e entradas inválidas;
* não retornar exceções internas ao cliente;
* manter consistência no formato das respostas.

Erros esperados de negócio não devem gerar erro HTTP 500.

Erros inesperados devem ser registrados sem expor dados sensíveis.

---

## Testes

Toda correção deve incluir ou atualizar testes quando houver comportamento verificável.

Antes de concluir:

```bash
pytest
```

Quando a alteração envolver banco, testar com PostgreSQL sempre que possível.

Os testes devem ser:

* determinísticos;
* independentes;
* rápidos;
* claros;
* sem dependência de dados de produção;
* sem dependência de credenciais reais.

Não considerar uma implementação concluída se os testes existentes falharem.

Não alterar testes apenas para esconder um comportamento incorreto.

---

## Docker

O projeto deve continuar executando por Docker.

O comando de inicialização da aplicação deve respeitar a variável `PORT`, necessária em ambientes como o Render.

Exemplo esperado:

```bash
uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
```

Não assumir que o serviço Docker local está disponível dentro do Render.

Não usar `docker compose exec` quando o container ainda não estiver em execução.

Para comandos pontuais locais, verificar se o formato correto é:

```bash
docker compose run --rm app <comando>
```

Variáveis de ambiente do Compose devem ser configuradas no próprio arquivo Compose ou carregadas pelo ambiente antes da execução.

---

## Render

O deploy no Render deve:

* usar variáveis de ambiente configuradas no painel;
* utilizar a porta fornecida por `PORT`;
* executar migrações de forma controlada;
* não depender de arquivos locais não versionados;
* não depender do Docker Compose;
* usar health check quando disponível;
* impedir que segredos apareçam nos logs.

Variáveis esperadas podem incluir:

```text
DATABASE_URL
ENVIRONMENT
SECRET_KEY
```

Nunca preencher valores reais em arquivos versionados.

Antes de alterar configurações de deploy, verificar:

* `Dockerfile`;
* comando de inicialização;
* configuração de porta;
* variáveis obrigatórias;
* migrações;
* health check;
* logs de inicialização.

---

## Estilo de código

* Seguir o padrão já utilizado no projeto.
* Usar nomes claros.
* Evitar abstrações prematuras.
* Manter funções pequenas e com responsabilidade única.
* Utilizar type hints nas funções novas ou alteradas.
* Evitar comentários que apenas repetem o código.
* Comentar decisões que não sejam óbvias.
* Não adicionar código morto.
* Não deixar prints de depuração.
* Não capturar exceções genericamente sem tratamento adequado.

Priorizar legibilidade sobre soluções excessivamente genéricas.

---

## Escopo das alterações

Antes de modificar um arquivo, confirmar que ele pertence ao escopo da demanda.

Não realizar sem autorização:

* reorganização geral de diretórios;
* troca de framework;
* troca de ORM;
* alteração ampla da arquitetura;
* renomeação em massa;
* atualização geral de dependências;
* mudanças estéticas em arquivos não relacionados;
* alterações de deploy fora da demanda;
* remoção de compatibilidade existente.

---

## Git

Os commits devem ser pequenos e relacionados a uma única intenção.

Usar mensagens no imperativo, por exemplo:

```text
Adiciona configuração para o Neon
Corrige distribuição de jogadores
Cria migração para usuários
Ajusta inicialização no Render
Adiciona testes do sorteio
```

Não incluir no commit:

* `.env`;
* credenciais;
* bancos locais;
* arquivos temporários;
* caches;
* logs;
* artefatos de IDE;
* arquivos não relacionados à demanda.

Antes de concluir, verificar:

```bash
git status
git diff
```

Todo arquivo não versionado deve ser mencionado no relatório final.

Não adicionar arquivos não relacionados apenas para deixar o working tree limpo.

---

## Uso econômico de tokens

Durante a investigação:

* leia primeiro os arquivos diretamente relacionados;
* use buscas específicas;
* evite reler arquivos inteiros sem necessidade;
* atualize `context.compact.md`;
* não repita grandes blocos de código;
* apresente somente os trechos relevantes;
* não gere documentação redundante.

Quando já existir uma decisão registrada, reutilizá-la em vez de reiniciar a análise.

---

## Relatório final obrigatório

Ao concluir uma implementação, apresentar:

### Arquivos alterados

Lista objetiva dos arquivos criados ou modificados.

### Alterações realizadas

Resumo das mudanças de comportamento.

### Testes executados

Comandos executados e resultados.

### Banco de dados

Informar:

* migração criada;
* migração aplicada;
* Alembic head;
* validação da conexão;
* eventuais limitações.

### Deploy

Informar se houve ou não deploy.

Nunca afirmar que houve deploy quando apenas os arquivos foram preparados.

### Pendências

Informar claramente:

* arquivos não versionados;
* testes não executados;
* validações manuais necessárias;
* riscos conhecidos;
* configurações externas ainda necessárias.

---

## Conduta esperada do agente

O agente deve:

* investigar antes de alterar;
* fazer inferências apenas quando sustentadas pelo código;
* diferenciar fato, hipótese e recomendação;
* não inventar resultados de testes;
* não inventar sucesso de conexão;
* não inventar deploy;
* não esconder falhas;
* interromper mudanças destrutivas sem autorização;
* entregar a solução mais simples que cumpra os critérios.

Quando não for possível validar algo, registrar explicitamente:

```text
Não validado: <motivo>
```

Quando houver uma hipótese:

```text
Hipótese: <descrição>
Evidência: <arquivo, função ou comportamento observado>
Validação necessária: <procedimento>
```


## Ambiente Python

Antes de instalar dependências ou criar artefatos que dependam de pacotes Python, crie e use um ambiente virtual local em `.venv`.

As dependências do projeto devem ser instaladas dentro de `.venv`, não no Python global do sistema.
