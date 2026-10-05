# Biblioteca Sabedoria Eterna

Sistema de gerenciamento de livros desenvolvido em **Python** com **MongoDB Atlas**, criado como projeto prático da faculdade Anhanguera.

O projeto implementa um CRUD completo (Create, Read, Update e Delete) em um banco de dados NoSQL na nuvem, com validação de dados, logs estruturados, tratamento de erros e criação de índices para melhor performance.

---

## Funcionalidades

- **Conexão segura** com MongoDB Atlas
- **Validação de documentos** antes da inserção
- **Create**: inserção de novos livros
- **Read**: consultas filtradas por autor
- **Update**: incremento de quantidade em estoque
- **Delete**: exclusão em massa por gênero
- **Índices** nas coleções (`autor`, `genero`, `titulo`)
- **Logs estruturados** com timestamp
- **Medição de tempo** das operações
- **Tratamento de erros** com `PyMongoError`

---

## Tecnologias utilizadas

- Python 3
- [PyMongo](https://pymongo.readthedocs.io/)
- MongoDB Atlas
- `logging` (logs estruturados)
- `bson.ObjectId`

---

## Pré-requisitos

- Python 3.8 ou superior
- Conta no [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- Cluster criado e string de conexão disponível
- Biblioteca `pymongo` instalada

```bash
pip install pymongo
```

---

## Como executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/biblioteca-sabedoria-eterna.git
cd biblioteca-sabedoria-eterna
```

2. Abra o arquivo principal e substitua a variável `uri` pela string de conexão do seu cluster MongoDB Atlas:

```python
uri = "mongodb+srv://<usuario>:<senha>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
```

3. Execute o script:

```bash
python main.py
```

> **Importante:** nunca versione sua string de conexão com usuário e senha reais. Use variáveis de ambiente ou um arquivo `.env` em projetos reais.

---

## Estrutura do projeto

```
biblioteca-sabedoria-eterna/
├── main.py          # Script principal com todas as operações CRUD
└── README.md
```

---

## Operações realizadas

| Operação | Descrição                                      |
|----------|------------------------------------------------|
| Create   | Inserção de livros com validação de campos     |
| Read     | Busca de livros por lista de autores           |
| Update   | Incremento da quantidade do livro "O Nome do Vento" |
| Delete   | Remoção de todos os livros do gênero Fantasia  |
| Índices  | Criação de índices em `autor`, `genero` e `titulo` |

---

## Exemplo de documento

```json
{
  "_id": ObjectId("..."),
  "titulo": "O Nome do Vento",
  "autor": "Patrick Rothfuss",
  "ano_publicacao": 2007,
  "genero": "Fantasia",
  "quantidade": 10
}
```

---

## Aprendizados

Este projeto foi desenvolvido durante uma aula prática da **Anhanguera**, com o objetivo de aplicar conceitos de:

- Bancos de dados NoSQL
- Operações CRUD
- Validação de dados
- Boas práticas de logging e tratamento de erros
- Uso de banco de dados em nuvem (MongoDB Atlas)

---

## Autor

Desenvolvido como parte das atividades acadêmicas da **Faculdade Anhanguera**.
