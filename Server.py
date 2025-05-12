import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dados em memória
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"}
]

class BookHandler(BaseHTTPRequestHandler):

    def send_response_and_log(self, code, message):
        self.send_response(code)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(message).encode())
        logging.info(f"Response: {code} - {message}")

    def do_GET(self):
        try:
            if self.path.startswith("/books/"):
                self.get_book_by_id()
            elif self.path == "/books":
                self.get_all_books()
            else:
                self.send_response_and_log(404, {"error": "Not Found"})
        except Exception as e:
            logging.error(f"Error handling GET request: {e}")
            self.send_response_and_log(500, {"error": "Internal Server Error"})

    def do_POST(self):
        try:
            if self.path == "/books":
                self.create_book()
            else:
                self.send_response_and_log(404, {"error": "Not Found"})
        except Exception as e:
            logging.error(f"Error handling POST request: {e}")
            self.send_response_and_log(500, {"error": "Internal Server Error"})

    def get_all_books(self):
        logging.info("Getting all books")
        self.send_response_and_log(200, books)

    def get_book_by_id(self):
        try:
            book_id = int(self.path.split("/")[2])
            logging.info(f"Getting book with ID: {book_id}")
            book = next((book for book in books if book["id"] == book_id), None)
            if book:
                self.send_response_and_log(200, book)
            else:
                self.send_response_and_log(404, {"error": "Book not found"})
        except ValueError:
            self.send_response_and_log(400, {"error": "Invalid book ID"})

    def create_book(self):
        try:
            content_length = int(self.headers.get('Content-Length'))
            post_data = self.rfile.read(content_length)
            new_book_data = json.loads(post_data.decode())
            new_book = {
                "id": len(books) + 1,
                "title": new_book_data["title"],
                "author": new_book_data["author"]
            }
            books.append(new_book)
            logging.info(f"Creating book: {new_book}")
            self.send_response_and_log(201, new_book)
        except json.JSONDecodeError:
            self.send_response_and_log(400, {"error": "Invalid JSON"})
        except KeyError:
            self.send_response_and_log(400, {"error": "Missing 'title' or 'author'"})
        except ValueError as e:
            logging.error(f"ValueError: {e}")
            self.send_response_and_log(400, {"error": "Bad Request"})  # Ou outra mensagem apropriada

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, BookHandler)
    logging.info('Servidor rodando na porta 8000...')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        logging.info("Servidor interrompido manualmente.")
    except Exception as e:
        logging.error(f"Erro inesperado no servidor: {e}")

if __name__ == '__main__':
    run()
