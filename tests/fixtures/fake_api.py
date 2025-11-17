# tests/fixtures/fake_api.py

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading

class FakeJulesAPIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/v1alpha/sources":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"sources": [{"name": "source1"}]}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/v1alpha/sessions":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"id": "fake_session_id"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

class FakeJulesAPI:
    def __init__(self, port=8000):
        self.port = port
        self.server = HTTPServer(("", port), FakeJulesAPIHandler)
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.daemon = True

    def start(self):
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()

def start_fake_api(port=8000):
    api = FakeJulesAPI(port=port)
    api.start()
    return api
