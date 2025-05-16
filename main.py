from flask import Flask, redirect
import requests

app = Flask(__name__)

CLIENT_ID = "INSERISCI_IL_TUO_CLIENT_ID"
CLIENT_SECRET = "INSERISCI_IL_TUO_CLIENT_SECRET"

access_token = None

def get_access_token():
    global access_token
    if access_token is None:
        url = "https://id.twitch.tv/oauth2/token"
        params = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        }
        resp = requests.post(url, params=params)
        resp.raise_for_status()
        access_token = resp.json()["access_token"]
    return access_token

def get_stream_url(channel_name):
    token = get_access_token()
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {token}"
    }

    url = f"https://api.twitch.tv/helix/streams?user_login={channel_name}"
    resp = requests.get(url, headers=headers)
    data = resp.json()["data"]

    if not data:
        return None

    return f"https://usher.ttvnw.net/api/channel/hls/{channel_name}.m3u8"

@app.route("/stream/twitch/<channel>")
def twitch_proxy(channel):
    m3u8_url = get_stream_url(channel)
    if not m3u8_url:
        return "Channel is offline", 404
    return redirect(m3u8_url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
