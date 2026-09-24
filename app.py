from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    if not video_id: 
        return jsonify({"error": "Missing video_id"}), 400
    
    try:
        # 💡 核心手術：退回最穩定的語法，並賦予它尋找多區英文與「自動生成字幕」的能力
        langs = ['en', 'en-US', 'en-GB', 'en-CA', 'en-AU']
        transcript_data = YouTubeTranscriptApi.get_transcript(video_id, languages=langs)
        
        # 將找到的字幕陣列，組裝成一大串純文字
        text = " ".join([item['text'] for item in transcript_data])
        return jsonify({"transcript": text})
        
    except Exception as e:
        # 如果真的完全沒有任何英文字幕，將錯誤回傳給 WordPress
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
