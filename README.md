# Flask + MySQL API

Este projeto é uma **API REST** desenvolvida em **Python** utilizando o framework **Flask**, integrada com um banco de dados **MySQL**.  
O objetivo é **aprender e praticar** conceitos de desenvolvimento de APIs, persistência de dados e boas práticas de organização de código.  

**Importante:** Este projeto foi criado **exclusivamente para fins de estudo** e não deve ser utilizado em produção sem ajustes de segurança e otimização.

---

## Funcionalidades

A API permite gerenciar **usuários** e suas **tarefas**:

- **Usuários**
  - Criar usuário (`POST /users`)
  - Listar todos os usuários (`GET /users`)
  - Consultar usuário por ID (`GET /users/<id>`)
  - Atualizar usuário (`PUT /users/<id>`)
  - Deletar usuário (`DELETE /users/<id>`)
  - Login de usuário (`POST /login`)

- **Tarefas**
  - Criar tarefa vinculada a um usuário (`POST /users/<id>/tarefas`)
  - Listar tarefas de um usuário (`GET /users/<id>/tarefas`)
  - Atualizar tarefa (`PUT /users/<id>/tarefas/<tarefa_id>`)
  - Deletar tarefa (`DELETE /users/<id>/tarefas/<tarefa_id>`)
