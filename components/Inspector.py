import json
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from urllib.parse import urlparse, parse_qs

class Inspector:
    def __init__(self):
        self.journal = {}
        self.history = {}
        
        # Automatically start server on a free port
        # self.server, self.port = self._start_server()
        # print(f"Server started on port {self.port}")

    # Journal Functions
    def track(self, instance_name, var_name, value):
        instance_key = f"{instance_name}"
        var_key = f"{var_name}"

        if instance_key not in self.journal:
            self.journal[instance_key] = {}

        if var_key not in self.journal[instance_key] or self.journal[instance_key][var_key] != value:
            self.journal[instance_key][var_key] = value

    def trackHistory(self, instance_name, history_id, obj):
        if instance_name not in self.history:
            self.history[instance_name] = []
            
        obj["history_id"] = history_id
        obj["_instance"] = instance_name
        self.history[instance_name].append(obj)

    def log(self):
        with open('history.csv', 'w') as f:
            f.write('hs,sp,ul,r,mu,ul-mu\n')
            for obj in self.history['Sourjya']:
                f.write(f"{obj['hs']},{obj['sp']},{obj['ul']},{obj['r']},{obj['mu']},{obj['ul-mu']}\n")
            
            for obj in self.history['Sayan']:
                f.write(f"{obj['hs']},{obj['sp']},{obj['ul']},{obj['r']},{obj['mu']},{obj['ul-mu']}\n")
        # with open('journal_full.json', 'w') as f:
        #     json.dump({
        #         "journal": self.journal,
        #         "history": self.history,
        #     }, f)

    # Server Functions
    def _start_server(self):
        # Find a free port by creating a socket, binding it to a random port, and retrieving the port number
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        
        # Start HTTP server on the free port
        handler = self._create_request_handler()
        server = HTTPServer(('localhost', port), handler)
        
        # Run the server in a separate thread
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        
        return server, port

    def joinAndLog(self, instances):
        fields = instances
        dumpObj = []
                        
        if len(fields) == 2 and fields[0] in self.history and fields[1] in self.history:
            field1 = self.history[fields[0]]
            field2 = self.history[fields[1]]
            joined_lists = []

            # Perform join based on matching `history_id`
            for entry1 in field1:
                # Find matching entry in field2 by `history_id`
                matches = [entry2 for entry2 in field2 if entry2.get("history_id") == entry1.get("history_id")]
                if matches:
                    # Append both matched entries to a sub-list
                    for entry2 in matches:
                        joined_lists.append([entry1, entry2])

            dumpObj = joined_lists

        with open(f'history_join_{instances[0]}_{instances[1]}.json', 'w') as f:
            json.dump(dumpObj, f)


    def stop_server(self):
        if self.server:
            self.server.shutdown()
            print("Server stopped")

    def _create_request_handler(self):
        inspector = self  # Capture the instance in the closure

        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                query_components = parse_qs(urlparse(self.path).query)
                response_data = {}

                # Check if a 'query' parameter is provided
                if 'query' in query_components:
                    query = query_components['query'][0]
                    
                    # Split the query into main parts
                    query_parts = query.split(',')

                    # Check for 'history.join' query format
                    if query_parts[0] == "history.join" and len(query_parts) > 1:
                        # Extract fields to join, e.g., "Sayan-Sourjya"
                        fields = query_parts[1].split('-')
                        
                        if len(fields) == 2 and fields[0] in inspector.history and fields[1] in inspector.history:
                            field1 = inspector.history[fields[0]]
                            field2 = inspector.history[fields[1]]
                            joined_lists = []

                            # Perform join based on matching `history_id`
                            for entry1 in field1:
                                # Find matching entry in field2 by `history_id`
                                matches = [entry2 for entry2 in field2 if entry2.get("history_id") == entry1.get("history_id")]
                                if matches:
                                    # Append both matched entries to a sub-list
                                    for entry2 in matches:
                                        joined_lists.append([entry1, entry2])

                            response_data = joined_lists
                        else:
                            response_data = {"error": "Invalid fields in join query."}
                    elif query == "journal":
                        response_data = inspector.journal
                    elif query == "history":
                        response_data = inspector.history
                    else:
                        response_data = {"error": "Invalid query. Use 'journal', 'history', or 'history.join,field1-field2'."}
                else:
                    response_data = {"error": "No query parameter provided."}

                # Send the JSON response
                self._send_json_response(response_data)

            def _send_json_response(self, data, status=200):
                self.send_response(status)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode("utf-8"))

        return RequestHandler



# You can now access the server via:
# http://localhost:<free_port>?query=journal to get journal data
# http://localhost:<free_port>?query=history to get history data

# Remember to stop the server when done
# inspector.stop_server()
