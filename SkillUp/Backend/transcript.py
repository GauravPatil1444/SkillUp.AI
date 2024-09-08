from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import json
import json5
import os
from dotenv import load_dotenv

load_dotenv()

KEY = os.getenv("KEY")

def transcript(videoID):
    result = ''
    txtlist = []
    status = True
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(videoID)
        transcript = transcript_list.find_transcript(['hi', 'en'])
        translated_transcript = transcript.translate('en')
        result = translated_transcript.fetch()
        for txt in range(len(result)):
            txtlist.append(result[txt]['text'])

    except:
        status = False

    # print(result)
    data = ' '.join(txtlist)
    # print(data)
    if status:
        genai.configure(api_key=KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        format = {
            "question": "What is the capital of France?",
            "options": ["Paris", "London", "Berlin", "Rome"],
            "correctAnswer": "Paris"
        }
        prompt = f"This is youtube video transcript use this to make MCQ quiz in this format {format} here's the transcript : {data}"
        response = model.generate_content(prompt)
        response = response.text
        # print(response.text)
        cleaned_str = response.replace("```json", "")
        cleaned_str = response.replace("```", "")
        newstr = cleaned_str[4:]
        json_data = json.dumps(newstr,indent=2)
        # print(type(json_data))
        json_data = json.loads(json_data)
        # print(type(json_data))
        data = json5.loads(json_data)
        # print(type(data))
        return data
    else:
        return 404 