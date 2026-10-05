from pymongo.errors import PyMongoError
from pymongo import MongoClient
from pprint import pprint
from bson import ObjectId
import logging
import time

# Substitui o uso de print() por logs estruturados com timestamps
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# === Conexão com o MongoDB Atlas ===
uri = "link_do_seu_cluster_mongodb_atlas"  # Substitua pelo link do seu cluster MongoDB Atlas

try:
    client = MongoClient(uri)

    #Escolhe o banco e a coleção
    db = client ["biblioteca_sabedoria_eterna"]
    collection = db ["livros"]

    # Teste rápido para validar a conexão com o Atlas
    client.admin.command('ping')
    logging.info("Conexão com o MongoDB Atlas realizada com sucesso.")

    def validate_book(book_dict):
        """
        Verifica se todos os campos obrigatórios estão presentes e não são nulos ou vazios.
        """
        required_fields = ["titulo", "autor", "ano_publicacao", "genero", "quantidade"]
        for field in required_fields:
            if field not in book_dict or book_dict[field] is None or book_dict[field] == "":
                logging.error(f"Validação falhou: O campo '{field}' é obrigatório.")
                return False
        return True

    # === Dados iniciais ===
    if collection.count_documents({"titulo": "O Nome do Vento"}) == 0:
        collection.insert_one({
            "_id": ObjectId(),
            "titulo": "O Nome do Vento",
            "autor": "Patrick Rothfuss",
            "ano_publicacao": 2007,
            "genero": "Fantasia",
            "quantidade": 10
    })
    logging.info("Livro inicial 'O Nome do Vento' inserido.\n")

    # === 1. Create ===
    print("\n=== 1. Create - Adicionar novos livros ===")

    # Livro 1 (Tesla)
    new_book = {
        "_id": ObjectId(),
        "titulo": "Tesla: A Vida e A Loucura do Gênio que Iluminou o Mundo",
        "autor": "Marko Perko, Stephen M. Stahl",
        "ano_publicacao": 2023,
        "genero": "Biografia, Histórias reais, Ciência e tecnologia",
        "quantidade": 5
    }

    # Livro 2 (Darwin)
    new_book2 = {
        "_id": ObjectId(),
        "titulo": "A Origem das Espécies",
        "autor": "Charles Darwin",
        "ano_publicacao": 1859,
        "genero": "Literatura científica, Biologia",
        "quantidade": 7
    }

    for book in [new_book, new_book2]:
        # === Chamada da validação de estrutura do documento ===
        if not validate_book(book):
            logging.warning(f"Inserção abortada para o livro: {book.get('titulo', 'Desconhecido')}")
            continue

        exists = collection.find_one({"titulo": book["titulo"]})

        if exists:
            logging.warning(f"Atenção: O livro '{book['titulo']}' já existe na coleção.")
        else:
            result = collection.insert_one(book)
            logging.info(f"Livro inserido com sucesso. ID: {result.inserted_id}")

        pprint(collection.find_one({"titulo": book["titulo"]}))
        print()

    # === 2. Read ===
    print("=== 2. Read - Listar livros")

    # === Monitora tempo de leitura ===
    start_read = time.time()

    books = list(collection.find({
        "autor": {
            "$in": [
                "Marko Perko, Stephen M. Stahl",
                "Patrick Rothfuss",
                "Charles Darwin"
            ]
        }
    }))

    temp_read = (time.time() - start_read) * 1000
    logging.info(f"Consulta de leitura executada em {temp_read:.2f} ms.")

    print(f"Total de livros encontrados: {len(books)}")
    for book in books:
        pprint(book)
    print()

    # === 3. Update ===
    print("=== 3. Update - Incrementar quantidade de 'O Nome do Vento' ===")

    before = collection.find_one({"titulo": "O Nome do Vento"})
    print("Antes da atualização:")
    pprint(before)

    start_update = time.time()
    result_update = collection.update_one(
        {"titulo": "O Nome do Vento"},
        {"$inc": {"quantidade": 3}}
    )
    temp_update = (time.time() - start_update) * 1000

    logging.info(f"Atualização executada em {temp_update:.2f} ms. Documentos modificados: {result_update.modified_count}")

    after = collection.find_one({"titulo": "O Nome do Vento"})
    print("Depois da atualização:")
    pprint(after)
    print()


    # === 4. Delete ===
    print("=== 4. Delete - Remover todos os livros do gênero Fantasia ===")

    # Busca os livros antes da exclusão
    books_fantasy = list(collection.find({"genero": "Fantasia"}))
    print(f"Livros de Fantasia encontrados: {len(books_fantasy)}")

    if len(books_fantasy) > 0:
        print("\nLivros que serão removidos:")
        for book in books_fantasy:
            print(f"- {book['titulo']} (Autor: {book['autor']})")

        start_delete = time.time()
        result_delete = collection.delete_many({"genero": "Fantasia"})
        temp_delete = (time.time() - start_delete) * 1000

        logging.info(f"\nExclusão executada em {temp_delete:.2f} ms. Documentos removidos: {result_delete.deleted_count}")
    else:
        logging.info("Nenhum livro de Fantasia encontrado para remoção.")

    qty_after = collection.count_documents({"genero": "Fantasia"})
    print(f"Livros de Fantasia depois da exclusão: {qty_after}")
    print()

    # === Indices ===
    print("=== Índices na coleção 'livros' ===")
    collection.create_index("autor")
    collection.create_index("genero")
    collection.create_index("titulo")
    print("Índices criados com sucesso.")
    print()

except PyMongoError as e:
    logging.error(f"Ocorreu um erro na operação do MongoDB: {e}")
except Exception as e:
    logging.error(f"Ocorreu um erro inesperado: {e}")

finally:
    # === Fechar Conexão ===
    if 'client' in locals():
        client.close()
        logging.info("Conexão encerrada com sucesso.")