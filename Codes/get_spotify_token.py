import webbrowser
import urllib.parse
import http.server
import threading
import requests
import base64
import json

# =============================================
#   TADY DOPLŇ SVOJE ÚDAJE
# =============================================
CLIENT_ID     = "Zadej sem svoje ClientID z spotify dashboardu"
CLIENT_SECRET = "Sem tvuj Secret ID taky ze spotify dashboardu"
REDIRECT_URI  = "http://127.0.0.1:8888/callback"
# =============================================

SCOPE = "user-read-currently-playing user-read-playback-state user-modify-playback-state"

auth_code = None
server_done = threading.Event()

class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"""
                <html><body style='font-family:sans-serif;text-align:center;padding:50px'>
                <h2>&#10003; Hotovo! Refresh token byl ziskan.</h2>
                <p>Muzes zavrit toto okno a jit zpet do terminalu.</p>
                </body></html>
            """)
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Chyba: chybi authorization code")

        server_done.set()

    def log_message(self, format, *args):
        pass  # Potlac logovani

def main():
    print("\n=== Spotify Refresh Token Generator ===\n")

    # Krok 1: Spust lokalni server
    server = http.server.HTTPServer(("localhost", 8888), CallbackHandler)
    thread = threading.Thread(target=server.handle_request)
    thread.daemon = True
    thread.start()

    # Krok 2: Otevri Spotify autorizaci v prohlizeci
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
    }
    auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)
    print("Oteviru Spotify prihlaseni v prohlizeci...")
    webbrowser.open(auth_url)

    # Krok 3: Cekej na callback
    print("Cekam na prihlaseni... (prihlaste se ve webovem prohlizeci)")
    server_done.wait(timeout=120)

    if not auth_code:
        print("CHYBA: Neprisiel zadny authorization code. Zkus to znovu.")
        return

    # Krok 4: Vymena code za tokeny
    credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": REDIRECT_URI,
        },
        headers={
            "Authorization": f"Basic {credentials}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
    )

    if response.status_code != 200:
        print(f"CHYBA pri ziskavani tokenu: {response.text}")
        return

    tokens = response.json()
    refresh_token = tokens.get("refresh_token")

    print("\n" + "="*50)
    print("USPECH! Tady je tvuj Refresh Token:")
    print("="*50)
    print(f"\n{refresh_token}\n")
    print("="*50)
    print("Zkopiruj tento token a vloz ho do Arduino kodu.")
    print("NESDILEJ ho s nikym!\n")

    # Uloz token do souboru
    with open("refresh_token.txt", "w") as f:
        f.write(refresh_token)
    print("Token byl take ulozen do souboru: refresh_token.txt\n")

if __name__ == "__main__":
    main()

