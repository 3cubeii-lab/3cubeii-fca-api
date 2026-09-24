from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    if not video_id: 
        return jsonify({"error": "Missing video_id"}), 400
    
    try:
        # 獲取該影片所有可用的字幕清單
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        
        try:
            # 優先 1：尋找手動建立的英文或各區英文 (美式、英式、加式、澳式)
            transcript = transcript_list.find_transcript(['en', 'en-US', 'en-GB', 'en-CA', 'en-AU'])
        except:
            try:
                # 優先 2：如果沒有手動上傳的，嘗試尋找 YouTube AI 自動生成的英文
                transcript = transcript_list.find_generated_transcript(['en'])
            except:
                # 優先 3 (大絕招)：如果完全沒有英文，隨便抓一個現有語言，直接呼叫 YouTube 內建翻譯轉成英文！
                for t in transcript_list:
                    transcript = t.translate('en')
                    break
                    
        # 將找到的字幕陣列，組裝成一大串純文字
        transcript_data = transcript.fetch()
        text = " ".join([item['text'] for item in transcript_data])
        return jsonify({"transcript": text})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
