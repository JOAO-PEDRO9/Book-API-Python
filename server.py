from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from books_data import books

class BookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/books":
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(books).encode())
        elif self.path.startswith("/books/"):
            try:
                book_id = int(self.path.split("/")[-1])
                book = next((b for b in books if b["id"] == book_id), None)
                if book:
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(book).encode())
                else:
                    self.send_error(404, "Book not found")
            except ValueError:
                self.send_error(400, "Invalid ID")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/books":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)

            new_book = {
                "id": len(books) + 1,
                "title": data["title"],
                "author": data["author"]
            }
            books.append(new_book)

            self.send_response(201)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(new_book).encode())
        else:
            self.send_error(404)

def run():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, BookHandler)
    print('Running server on port 8000...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
