from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from os import environ
import requests
import shutil
import string
import random

hostName = "localhost"
serverPort = 8080

auth_uri = "https://auth.viarezo.fr"
auth_token_uri = auth_uri + "/oauth/token"
auth_authorize_uri = auth_uri + "/oauth/authorize"

redirect_uri = "http://localhost:8080"
client_id = environ["CLIENT_ID"]
client_secret = environ["CLIENT_SECRET"]
response_type = "code"
scope = "default"
grant_type = "authorization_code"

file = "kitten.jpg"


class MyServer(BaseHTTPRequestHandler):

    def get_credentials(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/jpeg')
        self.end_headers()
        with open(file, 'rb') as content:
            shutil.copyfileobj(content, self.wfile)

    def go_login(self):
        global last_state
        last_state = ''.join(random.choice(string.ascii_letters) for _ in range(10))
        data = {
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "response_type": response_type,
            "state": last_state,
            "scope": scope
        }
        oauth_path = auth_authorize_uri + "/?"
        def param_formater(key): return f"{key}={data[key]}"
        oauth_path += "&".join(list(map(param_formater, data)))
        self.send_response(302)
        self.send_header("Location", oauth_path)
        self.end_headers()

    def go_check_creds(self, code, state):
        if state != last_state:
            self.send_response(400)
            return
        data = {
            "grant_type": grant_type,
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        get_token = requests.post(
            f"{auth_token_uri}", headers=headers, data=data)
        print(get_token.status_code)
        if get_token.status_code == 200:
            self.get_credentials()
        else:
            self.go_login()

    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        if not params:
            self.go_login()
        if "code" in params and "state" in params:
            self.go_check_creds(params['code'][0], params['state'][0])


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
