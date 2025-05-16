from flask import Flask, Response, abort
import streamlink

app = Flask(__name__)

@app.route('/stream/<channel>.m3u', methods=['GET'])
def get_twitch_m3u(channel):
    try:
        twitch_url = f"https://www.twitch.tv/{channel}"
        streams = streamlink.streams(twitch_url)

        if not streams:
            abort(404, description="Canale non trovato o non in streaming.")

        hls_url = streams.get("best").url  # Usa "worst", "best" o una qualità specifica

        # Costruiamo il contenuto del file M3U
        m3u_content = f"""#EXTM3U
#EXTINF:-1 tvg-name="{channel}" tvg-logo="https://static-cdn.jtvnw.net/previews-ttv/live_user_ {channel.lower()}-640x360.jpg" group-title="Twitch",{channel}
{hls_url}
"""

        # Restituiamo la risposta con il tipo MIME corretto e il download del file
        return Response(
            m3u_content,
            mimetype='application/x-mpegurl',
            headers={
                'Content-Disposition': f'attachment; filename={channel}.m3u'
            }
        )

    except Exception as e:
        abort(500, description=str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)