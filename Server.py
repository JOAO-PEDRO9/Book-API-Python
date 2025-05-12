import json
from http.server import BaseHTTPRequestHandler, HTTPServer

# Dados em memória (simulando um banco de dados)
books = [
    {"id": 1, "title": "1984", "author": "George Orwell"},
    {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"}
]

class BookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/books/"):
            self.get_book_by_id()
        elif self.path == "/books":
            self.get_all_books()
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def do_POST(self):
        if self.path == "/books":
            self.create_book()
        else:
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not Found"}).encode())

    def get_all_books(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(books).encode())

    def get_book_by_id(self):
        try:
            book_id = int(self.path.split("/")[2])
            book = next((book for book in books if book["id"] == book_id), None)
            if book:
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(book).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Book not found"}).encode())
        except ValueError:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid book ID"}).encode())

    def create_book(self):
        content_length = int(self.headers.get('Content-Length'))
        post_data = self.rfile.read(content_length)
        try:
            new_book_data = json.loads(post_data.decode())
            new_book = {
                "id": len(books) + 1,
                "title": new_book_data["title"],
                "author": new_book_data["author"]
            }
            books.append(new_book)
            self.send_response(201)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(new_book).encode())
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
        except KeyError:
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing 'title' or 'author'"}).encode())

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, BookHandler)
    print('Servidor rodando na porta 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
