# Fastapi CRUD

## Stack:

1. **Banco de Dados**: PostgreSQL
2. **Migrations**: [Flyway](https://www.red-gate.com/products/flyway/)
3. **Framework Rest API**: [FastAPI](https://fastapi.tiangolo.com/)
4. **Conteinerização**: [Docker](https://www.docker.com/)
5. **Linguagem de programação**: Python 3.8

## Endpoints:
    
1. **Music Service**: http://127.0.0.1:5000/docs/
    - Esse serviço possui a API Rest de cadastro de músicas.

## Comandos:

1. No diretório **/fastapi_crud** reside o arquivo *docker-compose.yml*.
2. Executar o comando **docker compose up** para criar toda a infraestrutura.
3. Executar o comando **docker compose down --remove-orphans** para destruir toda a infraestrutura.
4. Executar o comando **docker compose up -- build** para recriar toda a estrutura.
5. Executar o comando **docker exec -it <CONTAINER ID> bash** para entrar em um container específico.
