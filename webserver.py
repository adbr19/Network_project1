from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

tasklist = ['Task 1', 'Task 2', 'Task 3']
authenticated = False

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global authenticated
        if not authenticated:
            self.send_response(200)
            self.send_header('content-type', 'text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Login</h1>'
            output += '<form method="POST" enctype="multipart/form-data" action="/login">'
            output += '<label for="username">Username:</label>'
            output += '<input type="text" id="username" name="username"><br>'
            output += '<label for="password">Password:</label>'
            output += '<input type="password" id="password" name="password"><br>'
            output += '<input type="submit" value="Login">'
            output += '</form>'
            output += '</body></html>'
            self.wfile.write(output.encode())
        else:
            if self.path.endswith('tasklist'):
                self.send_response(200) # ok
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += '<h1>Task List</h1>'
                output += '<h3><a href="/tasklist/new">Add New Task</a></h3>'
                for task in tasklist:
                    output += task 
                    output += '<a/ href = "tasklist/%s/remove">Delete</a>' % task
                    output += '</br>'
                output += '</body></html>'
                self.wfile.write(output.encode())

            if self.path.endswith('/new'):
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()
                
                output = ''
                output += '<html><body>'
                output += '<h1>Add New Task</h1>'

                output += '<form method = "POST" enctype = "multipart/form-data" action="/tasklist/new">'
                output += '<input name = "task" type = "text" placeholder="Add new task">'
                output += '<input type ="submit" value = "Add">'
                output += '</form>'
                output += '</body></html>'

                self.wfile.write(output.encode())

            if self.path.endswith('/remove'):
                listIDPath = self.path.split('/')[2]
                print(listIDPath)
                self.send_response(200)
                self.send_header('content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += '<h1>Delete task: %s</h1>' % listIDPath.replace('%20', ' ')
                output += '<form method ="POST" enctype = "multipart/form-data" action = "/tasklist/%s/remove">' % listIDPath
                output += '<input type = "submit" value = "Remove"></form>'
                output += '<a href = "/tasklist">Cancel</a>'

                output += '</body></html>'
                self.wfile.write(output.encode())  # Corrected 'endcode()' to 'encode()'

    def do_POST(self):
        global authenticated
        if self.path.endswith('/login'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                username = fields.get('username')
                password = fields.get('password')
                if username[0] == 'username' and password[0] == 'password':
                    authenticated = True

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()
        elif self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('Content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                new_task = fields.get('task')
                tasklist.append(new_task[0])

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()
        
        elif self.path.endswith('/remove'):
            listIDPath =self.path.split('/')[2]
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                list_item = listIDPath.replace('%20', ' ')
                tasklist.remove(list_item)

            self.send_response(301)
            self.send_header('content-type', 'text/html')
            self.send_header('Location', '/tasklist')
            self.end_headers()

def main():
    PORT = 9000
    server_address = ('localhost', PORT)
    server = HTTPServer(server_address, requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()




