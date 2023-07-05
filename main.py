import whisper
import os

from flask import *
from flask_cors import CORS


# Gets audio file and converts it to text
def SpeechToTextMessege(Path):
    fileSize = (os.stat(Path).st_size) / (1024 * 1024)

    language_whisper = "hebrew"
    options = dict(language=language_whisper, beam_size=5, best_of=5)
    transcribe_options = dict(task="transcribe", **options)
    translate_options = dict(task="translate", **options)

    if fileSize > 72:
        return None
    else:
        if fileSize <= 39:
            model = whisper.load_model("tiny")
            result = model.transcribe(Path, **transcribe_options)
        else:
            model = whisper.load_model("base")
            result = model.transcribe(Path, **transcribe_options)
    return result["text"]


app = Flask(__name__)
CORS(app)


@app.route('/')
def main():
    print("run server")
    return render_template("index.html")


@app.route('/upload', methods=['POST'])
def upload():
    print("Function called successfully")
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'})

        f = request.files['file']
        save_path = r'C:\Users\AI\Desktop\server\saves\\' + f.name
        f.save(save_path)
        speech = SpeechToTextMessege(save_path)
        os.remove(save_path)
        print(speech)
        return jsonify({'text': speech})


if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0')
