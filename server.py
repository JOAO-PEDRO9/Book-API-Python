import json
   from http.server import HTTPServer, BaseHTTPRequestHandler
   import traceback
   import re  # Importe o módulo re para lidar com padrões de URL
   
   # Dados iniciais dos livros
   books = [
       {"id": 1, "title": "1984", "author": "George Orwell"},
       {"id": 2, "title": "Brave New World", "author": "Aldous Huxley"}
   ]
   
   class BooksHandler(BaseHTTPRequestHandler):
   
       def send_json_response(self, data, status_code):
           """Helper function to send JSON responses."""
           self.send_response(status_code)
           self.send_header('Content-type', 'application/json')
           self.end_headers()
           self.wfile.write(json.dumps(data).encode())
   
       def do_GET(self):
           """Handles GET requests."""
           print(f"GET request to: {self.path}")
           try:
               if self.path == '/books':
                   self.send_json_response(books, 200)
               else:
                   match = re.match(r'/books/(\d+)', self.path)  # Use regex para extrair o ID
                   if match:
                       try:
                           book_id = int(match.group(1))
                           book = next((b for b in books if b['id'] == book_id), None)
                           if book:
                               self.send_json_response(book, 200)
                           else:
                               self.send_json_response({"message": "Book not found"}, 404)
                       except ValueError:
                           self.send_json_response({"message": "Invalid book ID"}, 400)
                   else:
                       self.send_json_response({"message": "Route not found"}, 404)
           except Exception:
               error_message = traceback.format_exc()
               print(error_message)  # Log the full traceback
               self.send_json_response({"message": "Internal Server Error"}, 500)
   
       def do_POST(self):
           """Handles POST requests."""
           print(f"POST request to: {self.path}")
           try:
               if self.path == '/books':
                   content_length = int(self.headers['Content-Length'])
                   post_data = self.rfile.read(content_length)
                   print(f"Received data: {post_data.decode()}")  # Log received data
                   try:
                       new_book = json.loads(post_data.decode())
                       if "title" in new_book and "author" in new_book:
                           new_book['id'] = max(b['id'] for b in books) + 1 if books else 1
                           books.append(new_book)
                           self.send_json_response(new_book, 201)
                       else:
                           self.send_json_response({"message": "Title and author are required"}, 400)
                   except json.JSONDecodeError:
                       self.send_json_response({"message": "Invalid JSON"}, 400)
               else:
                   self.send_json_response({"message": "Route not found"}, 404)
           except Exception:
               error_message = traceback.format_exc()
               print(error_message)  # Log the full traceback
               self.send_json_response({"message": "Internal Server Error"}, 500)
   
   def run(server_class=HTTPServer, handler_class=BooksHandler, port=8000):
       """Starts the server."""
       try:
           server_address = ('', port)
           httpd = server_class(server_address, handler_class)
           print(f'Starting httpd on port {port}...')
           httpd.serve_forever()
       except Exception:
           error_message = traceback.format_exc()
           print(error_message)  # Log the full traceback
   
   if __name__ == "__main__":
       run()
