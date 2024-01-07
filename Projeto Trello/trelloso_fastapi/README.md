# TADS Trelloso-API

Backend desenvolvido em FastAPI para simular funcionalidades báscias do Trelloso. Esse projeto é um Toy Problema que usei para conhecer mais as novas versões dos frameworks FastAPI, Pydantic e SQLModel e não deve ser usado como modelo para um sistema real que vai para ambiente de produção!

A configuração a seguir é muito importante, sem ela os containers não irão funcionar corretamente!!!!!!

## Configuração <== NÃO PULAR ESSA ETAPA!!!!!

1. Entrar no diretório do projeto

```bash
cd trelloso_fastapi
```

2. Copiar o arquivo .env.example para .env

```bash
cp .env.example .env
```

3. Alterar as propriedades que achar necessário

    a. A porta informada na propriedade POSTGRES_PORT é a porta interna para o container, o banco será acessado via localhost através da porta 5437.


## Instalação com Docker

1. Entrar no diretório do projeto

```bash
cd trelloso_fastapi
```

2. Criar a imagem do projeto

```bash
docker compose build
```

3. Iniciar o sistema

    a. Dessa forma o terminal ficará exibindo o log dos containers e quando for fechado os containers serão parados automaticamente

    ```bash
    docker compose up
    ```

    b. Dessa forma o terminal não exibirá os log e será liberado após o início dos containers. Nesse caso é preciso analisar os logs dos containers individualmente

    ```bash
    docker compose up -d
    ```

4.  Acessar a página de endpoints: http://localhost:8087/docs

5. Analisar os logs dos containers

```bash
docker logs -f trello_fastapi
```

6. Parar os containers iniciandos no passo 3a

```bash
docker compose stop
```

7. Após a criação da imagem e dos container, para iniciar novamente os containers basta dar um **start** no compose. Isso é necessário quando o computador é reinciado ou o terminal foi fechado com os containers iniciados no passo 3a

```bash
docker compose start
```
# Trello
