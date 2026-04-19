#!/usr/bin/env python3
"""
Barsys AI Knowledge Graph — web server + Anthropic API proxy.

Hosted mode  (ANTHROPIC_API_KEY env var set):
  Everyone who opens the URL gets AI search automatically. No key prompt.

Local mode (no env var):
  Users enter their own Anthropic API key in the UI.
"""
import http.server, json, urllib.request, urllib.error, os, threading, time, webbrowser

PORT       = int(os.environ.get('PORT', 8765))
DIR        = os.path.dirname(os.path.abspath(__file__))
SERVER_KEY = os.environ.get('ANTHROPIC_API_KEY', '')
IS_HOSTED  = bool(SERVER_KEY)


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIR, **kw)

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def do_GET(self):
        if self.path in ('/', '/index.html'):
            # Serve the knowledge graph as root
            self.path = '/index.html'
            super().do_GET()
        elif self.path == '/health':
            self._json({'hasKey': IS_HOSTED, 'version': '2.0'})
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/anthropic':
            self._proxy()
        else:
            self.send_error(404)

    def _cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Api-Key')

    def _json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self._cors()
        self.end_headers()
        self.wfile.write(body)

    def _proxy(self):
        length = int(self.headers.get('Content-Length', 0))
        body   = self.rfile.read(length)
        # Server key takes priority; fall back to client-provided key
        key    = SERVER_KEY or self.headers.get('X-Api-Key', '')
        if not key:
            self._json({'error': {'message': 'No API key configured. Set ANTHROPIC_API_KEY env var or enter a key in the UI.'}}, 400)
            return
        req = urllib.request.Request(
            'https://api.anthropic.com/v1/messages',
            data=body,
            headers={
                'Content-Type':      'application/json',
                'x-api-key':         key,
                'anthropic-version': '2023-06-01',
            },
            method='POST'
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                resp_data = r.read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self._cors()
                self.end_headers()
                self.wfile.write(resp_data)
        except urllib.error.HTTPError as e:
            resp_data = e.read()
            self.send_response(e.code)
            self.send_header('Content-Type', 'application/json')
            self._cors()
            self.end_headers()
            self.wfile.write(resp_data)

    def log_message(self, fmt, *args):
        # Clean request logging
        if args:
            print(f'  {self.address_string()}  {args[0]}')


if IS_HOSTED:
    print(f'Hosted mode  |  ANTHROPIC_API_KEY set  |  port {PORT}')
else:
    print(f'Local mode   |  No server key  |  http://localhost:{PORT}')
    print('  Users must enter their own API key in the UI.')
    def _open_browser():
        time.sleep(0.9)
        webbrowser.open(f'http://localhost:{PORT}/')
    threading.Thread(target=_open_browser, daemon=True).start()

print('Starting server...\n')
with http.server.HTTPServer(('0.0.0.0', PORT), Handler) as srv:
    srv.serve_forever()
