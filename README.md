
# Bot

Raven - um bot que envia alertas de ações para o telegram

## Instalando python 

Sugestão, usar o asdf para instalar o python e poder gerenciar versões. Executar na raiz do projeto

### Instalando o ASDF

https://asdf-vm.com/#/core-manage-asdf-vm

### Instalando Python com o ASDF

https://github.com/danhper/asdf-python


```bash
$ sudo apt-get install libpq-dev python-dev
$ asdf plugin-add python 
$ asdf install python 3.7.4
$ asdf global python 3.7.4
```

## Instalar as dependencias 

Para instalar as dependencias do projeto executar usando o pip e habilitar o comando 'gunicorn'

```bash
$ pip3 install -r requirements.txt
$ pip3 install chrononaut
$ asdf reshim python
```

## Aplicação
- /app : arquivos da aplicação
- /bin : utilitários para o console
- /config : váriaveis de ambientes, configuração de log e arquivos de DDL
- /docker : arquivos para criar o postgreSQL local
- /ecs : arquivos da parametrização para as tasks do ecs
- /jenkins : arquivos do pipeline do jenkins
- /packages : arquivos de dependências para criar a imagem da aplicação
- /tests : arquivos de testes
- .bumpversion.cfg : arquivo para versionamento da aplicação
- .dockerignore : ignore do docker
- .gitignore : ignore do git
- console.sh : arquivo para testes no console
- Dockerfile : docker file para criar o container da aplicação
- init.sh : arquivo utilitaria para: iniciar aplicação/ executar lint / executar tests
- requirements.txt : arquivo dependências da aplicação

## Executar a aplicação

Para inicializar a aplicação

```bash
$ ./init.sh
```

Para inicializar a aplicação e executar os testes unitários

```bash
$ ./init.sh -t
```

Caso não consiga executar o sh acima, rodar o comando abaixo para dar permissão no arquivo sh

```bash
$ sudo chmod +x init.sh
```


## Criação do banco de dados

```bash
$ docker/start_local_database.sh 
```

Para somente criar o container do banco de dados execute:

```bash
$ docker/start_local_database.sh build_image

```

Para somente executar as migration execute 

```bash
$ docker/start_local_database.sh migrate
```

### Configuração:
 - Conexão: localhost:5405/db_raven
 - Schema: raven
 - Usuário: raven_adm
 - Senha: raven_adm


## Executar testes

```bash
$ ./init.sh -test
```

## Executar lint e auto format

Autopep8 - format
Docs: https://pypi.org/project/autopep8/

autoflake - remove import
Docs: https://pypi.org/project/autoflake/

flake8 - lint
Docs: https://pypi.org/project/flake8/


```bash
$ pip3 install --upgrade autopep8
$ pip3 install --upgrade autoflake
$ pip3 install --upgrade flake8
$ asdf reshim python
```

Executar o Lint + remove import + format

```bash
$ ./init.sh -lint
```

Executar apenas o format

```bash
$ ./init.sh -format
```

## Remover arquivos de cache

```bash
$ py3clean .
```


## CRON 

https://cron-job.org/en/members/jobs/

## WEBHOOK

https://api.telegram.org/bot1119179717:AAHbh_7Y6vaCo2SjAcu7ITYEVaiTthiticY/setWebhook?url=https://ravensp.herokuapp.com/1119179717:AAHbh_7Y6vaCo2SjAcu7ITYEVaiTthiticY