from flask import Flask, Response, abort
import streamlink
import requests

app = Flask(__name__)

@app.route('/stream/<channel>.m3u8', methods=['GET'])
def get_m3u8(channel):
    try:
        # Costruiamo l'URL del canale Twitch
        twitch_url = f"https://www.twitch.tv/{channel}"

        # Cerchiamo gli stream disponibili con Streamlink
        streams = streamlink.streams(twitch_url)

        if not streams:
            abort(404, description="Canale non trovato o non in streaming.")

        # Prendiamo l'URL HLS (.m3u8)
        m3u8_url = streams.get("best").url  # puoi usare "worst" o una qualità specifica

        # Scarichiamo il contenuto del file .m3u8
        resp = requests.get(m3u8_url, stream=True)

        # Passiamo i headers utili e il contenuto del file .m3u8 al client
        headers = {
            "Content-Type": resp.headers.get("Content-Type", "application/vnd.apple.mpegurl"),
            "Content-Disposition": f"inline; filename={channel}.m3u8"
        }

        return Response(resp.iter_content(chunk_size=1024), headers=headers)

    except Exception as e:
        abort(500, description=str(e))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)