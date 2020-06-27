
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
- /bin/init.sh : arquivo utilitario para: iniciar aplicação/ executar lint / executar tests
- /bin/deploy.sh : arquivo para fazer deploy no heroku
- /bin/migrate.py : arquivo para executar alterações DDL no banco de dados
- /config : váriaveis de ambientes, configuração de log e arquivos de DDL
- /docker : arquivos para criar o postgreSQL local
- /tests : arquivos de testes
- .dockerignore : ignore do docker
- .gitignore : ignore do git
- Dockerfile : docker file para criar o container da aplicação
- requirements.txt : arquivo dependências da aplicação

## Executar a aplicação

Para inicializar a aplicação

```bash
$ ./init.sh
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
$ python bin/migrate.py db upgrade
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


## API Stocks Data
- https://www.alphavantage.co/documentation/
- https://finnhub.io/docs/api

mês corrente:
bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_D05052020.ZIP

últimos 12 meses:
bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_M052020.ZIP

YEAR:
http://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2020.ZIP