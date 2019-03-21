# e-Praças Backend

O e-Praças é um sistema para gestão das Praças CEUs quem tem as seguintes funcionalidades: 
1. Transparência e divulgação das atividades das Praças CEUs a todos os cidadãos; 
2. apoio ao planejamento, monitoramento e avaliação das atividades desenvolvidas nos espaços; 
3. fornecimento de indicadores (relatórios e estatísticas) para a avaliação e melhoria contínua da gestão dos CEUs; e 
4. apoio à comunicação entre municípios, MinC, gestores e comunidades dos CEUs

Este é o repositório da API do sistema. O repositório da interface web pode ser encontrado [aqui](https://gitlab.com/decko/epracas-frontend)

## Configurando o ambiente de desenvolvimento
As depêndencias estão listadas em [requirements.txt](requirements.txt). Além disso, você também precisará de um banco Postgres e de um servidor de identificação OpenID Connect. Ainda, foi utilizado o paradigma do 12factor, possibilitando a configuração da aplicação através da injeção de valores pelas variaveis de ambiente.

1. [Ambiente de desenvolvimento local](#ambiente-de-desenvolvimento-local)
2. [Ambiente de desenvolvimento containerizado](#ambiente-de-desenvolvimento-containerizado)
3. [Configurando as variáveis de ambiente](#configurando-as-variáveis-de-ambiente)

### Ambiente de desenvolvimento local
O backend do e-Praças é desenvolvido utilizando Python na versão 3.6 ou superior. Uma sugestão é utilizar o virtualenv para criar um ambiente isolado e só depois instalar as dependências. Para instalar as dependencias do sistema, você deve ter o pip e usar o seguinte comando: 
```bash
pip install -r requirements.txt
```
Você precisa ainda de acesso a uma instancia do Postgres para utilizar como banco de dados.

Para rodar o servidor de desenvolvimento:
```bash
make runserver
```

Para a suite de testes, existem basicamente três comandos:
```bash
make test
```
que irá rodar a suite de testes aproveitando um banco de testes previamente criado. Isto reduz drasticamente o tempo de execução dos testes.

```bash
make test-createdb
```
que irá rodar a suite de testes criando um novo banco. Você deve rodar este comando quando seus testes envolverem mudanças em algum Model da aplicação.

```bash
make test-watch
```
que irá manter o pytest verificando os arquivos de teste. Ao alterar algum desses arquivos, os testes serão executados automáticamente. Caso algum teste falhe, este será o primeiro teste a ser executado na próxima rodada.

### Ambiente de desenvolvimento containerizado
A aplicação encontra-se preparada para ser executada como um container Docker.
Você pode utilizar o docker-compose para subir os serviços necessários para subir o ambiente.
Execute os seguintes comandos para subir o ambientena porta 8000:
```bash
docker-compose up
```

### Configurando as variáveis de ambiente
Como o e-Praças se utiliza de aspectos do 12factor app, algumas caracteristicas da aplicação podem ser modificadas ao instanciar variaveis de ambiente.

Todas elas já possuem um valor padrão que pode ser utilizado no ambiente de desenvolvimento, MAS VOCÊ DEVE ALTERAR ESSES VALORES AO UTILIZAR A APLICAÇÃO EM UM AMBIENTE DE PRODUÇÃO!!!

| Variável        | Descrição | 
|-----------------|---------------------------------------|
| SECRET_KEY      | Chave a ser utilizada pelo Django para validar uma sessão de login. Verifique o manual do Django para maiores informações
| DEBUG           | Inicia a aplicação com o modo Debug ativado. Padrão **False**
| ALLOWED_HOSTS   | Uma lista, separada por virgula(,) contendo os nomes de Host e IPs com permissão para acessar a aplicação. Padrão: **localhost**
| DATABASES       | Uma URL con credenciais de acesso a um banco Postgres. Padrão: **postgres://epracas:epracas123@localhost/epracas_db** 
| OIDC_ENDPOINT   | Uma URL do serviço de identidade compativel com OpenID Connect(OIDC) a ser utilizado. Padrão: **https://id.cultura.gov.br**
| OIDC_AUDIENCES  | Uma string contendo um identificador unico gerado pelo serviço de identidade OIDC. Padrão: **18_t41s2lf05w0cwkw480owccsk4wwscgw00wo0s0so8c8c8c8ck**
| RAVEN_DSN_URL   | Uma URL com credenciais de acesso ao sistema de monitoramento do estado da aplicação. Verifique a documentação do Sentry e da sua instância.


## Sugestões de deploy

1. [Utilizando uma receita git](#utilizando-uma-receita-git)

### Utilizando uma receita git
Uma maneira simples de fazer o deploy, é clonar o repositório na maquina de produção, e realizar um pull(de preferência usando --rebase) a cada merge da _master_.
Não se esquecendo de rodar os comandos para sincronizar o estado dos Models no banco de dados, aplicar as migrações necessárias e reiniciar o servidor de aplicação.
```bash
./manage.py makemigrations
./manage.py migrate
sudo supervisorctl restart epracas
```
