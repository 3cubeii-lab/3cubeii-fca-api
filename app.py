import traceback
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def fetch_youtube_subtitles():
    video_id = request.args.get('video_id')
    if not video_id: 
        return jsonify({"error": "Missing video_id"}), 400
    
    try:
        langs = ['en', 'en-US', 'en-GB', 'en-CA', 'en-AU']
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
        text = " ".join([item['text'] for item in transcript_data])
        return jsonify({"transcript": text})
        
    except Exception as e:
        error_msg = f"{str(e)} | Traceback: {traceback.format_exc()}"
        return jsonify({"error": error_msg}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
