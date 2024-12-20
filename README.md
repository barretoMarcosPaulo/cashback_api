# Projeto de Cashback API - OBoticário

Este projeto é uma implementação de uma API para integração com o sistema de cashback da OBoticário. A API permite consultar o cashback acumulado de um revendedor, levando em consideração o CPF do revendedor para buscar as informações.

## 🚀 Funcionalidades

- **Cadastro de Revendedor**: Permite cadastrar novos revendedores.
- **Cadastro de Vendas**: Permite cadastrar novas vendas.
- **Listagem de Vendas**: Permite listar as vendas do mês atual e calcular seu cashback.
- **Consulta de Cashback Acumulado**: Permite consultar o cashback acumulado para um revendedor específico.
- **Autenticação**: A API utiliza token Bearer para autenticação nas requisições.

## 📦 Tecnologias Utilizadas

- **Python**: Linguagem de programação.
- **FastAPI**: Framework web moderno e rápido para construção de APIs.
- **SQLAlchemy**: ORM para interagir com o banco de dados.
- **Requests**: Biblioteca para realizar requisições HTTP.
- **Pydantic**: Para validação e parsing de dados.

## 🧑‍💻  Levantando o Ambiente

- No diretorio do projeto, executar: poetry install
- Ativar ambiente virtual: poetry shell
- Executar: docker-compose up --build
- Executar migration no banco: alembic upgrade head
- Executar o servidor web: make run-api

## Observações
1. A documentação da api está disponível no swagger, basta acessar localhost:8000/docs com a aplicação rodando
2. Decidi não colocar o .env no arquivo gitignore para facilitar os testes de quem clonar o repo

