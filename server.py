import json
   from http.server import HTTPServer, BaseHTTPRequestHandler
   
   # Dados iniciais (simulando um banco de dados em memória)
   books = [
       {"id": 1, "title": "1984", "author": "George Orwell"},
       {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"}
   ]
   
   class BooksHandler(BaseHTTPRequestHandler):
   
       def do_GET(self):
           if self.path == '/books':
               self.send_response(200)
               self.send_header('Content-type', 'application/json')
               self.end_headers()
               self.wfile.write(json.dumps(books).encode())
           elif self.path.startswith('/books/'):
               try:
                   book_id = int(self.path.split('/')[2])
                   book = next((book for book in books if book['id'] == book_id), None)
                   if book:
                       self.send_response(200)
                       self.send_header('Content-type', 'application/json')
                       self.end_headers()
                       self.wfile.write(json.dumps(book).encode())
                   else:
                       self.send_response(404)
                       self.send_header('Content-type', 'application/json')
                       self.end_headers()
                       self.wfile.write(json.dumps({"message": "Book not found"}).encode())
               except ValueError:
                   self.send_response(400)
                   self.send_header('Content-type', 'application/json')
                   self.end_headers()
                   self.wfile.write(json.dumps({"message": "Invalid book ID"}).encode())
           else:
               self.send_response(404)
               self.send_header('Content-type', 'application/json')
               self.end_headers()
               self.wfile.write(json.dumps({"message": "Route not found"}).encode())
   
       def do_POST(self):
           if self.path == '/books':
               content_length = int(self.headers['Content-Length'])
               post_data = self.rfile.read(content_length)
               try:
                   new_book = json.loads(post_data.decode())
                   if "title" in new_book and "author" in new_book:
                       new_book['id'] = max(book['id'] for book in books) + 1 if books else 1
                       books.append(new_book)
                       self.send_response(201)
                       self.send_header('Content-type', 'application/json')
                       self.end_headers()
                       self.wfile.write(json.dumps(new_book).encode())
                   else:
                       self.send_response(400)
                       self.send_header('Content-type', 'application/json')
                       self.end_headers()
                       self.wfile.write(json.dumps({"message": "Title and author are required"}).encode())
               except json.JSONDecodeError:
                   self.send_response(400)
                   self.send_header('Content-type', 'application/json')
                   self.end_headers()
                   self.wfile.write(json.dumps({"message": "Invalid JSON"}).encode())
           else:
               self.send_response(404)
               self.send_header('Content-type', 'application/json')
               self.end_headers()
               self.wfile.write(json.dumps({"message": "Route not found"}).encode())
   
   def run(server_class=HTTPServer, handler_class=BooksHandler, port=8000):
       server_address = ('', port)
       httpd = server_class(server_address, handler_class)
       print(f'Starting httpd on port {port}...')
       httpd.serve_forever()
   
   if __name__ == "__main__":
       run()
