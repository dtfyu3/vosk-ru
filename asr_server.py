from vosk import Model, KaldiRecognizer
import soundfile as sf
import json
import os
import uuid
import numpy as np
from flask import Flask, request, jsonify

# Инициализация модели
model_path = "/models/vosk-ru"
if not os.path.exists(os.path.join(model_path, "conf/mfcc.conf")):
    print(f"Модель не найдена по пути: {model_path}")
    sys.exit(1)

model = Model(model_path)

def transcribe_audio(audio_path):
    try:
        data, samplerate = sf.read(audio_path, dtype='int16')
        print(f"Аудио: {samplerate}Hz, каналов: {data.shape[1] if len(data.shape) > 1 else 1}")  
        max_amplitude = np.max(np.abs(data))
        print(f"Макс. амплитуда: {max_amplitude:.4f}")
        if max_amplitude < 100:
            return {"Аудио слишком тихое"}, 400
        rec = KaldiRecognizer(model, samplerate)
        rec.SetWords(True)
        results = []
        for block in sf.blocks(audio_path, blocksize=4000, dtype='int16'):
            if rec.AcceptWaveform(block.tobytes()):
                results.append(json.loads(rec.Result()))
        
        final = json.loads(rec.FinalResult())
        text =  final.get("text", "").strip() or " ".join(r.get("text", "") for r in results)
        if not text:
            return {"error":"Не удалось распознать речь"},400
        return {"text":text},200
    
    except Exception as e:
        return {f"Ошибка обработки: {e}"}, 500

app = Flask(__name__)

@app.route('/')
def hello():
    return "Server is alive"

@app.route('/transcribe', methods=['POST'])
def handle_audio():
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file"}), 400
    
    audio = request.files['audio']
    temp_file = f"/tmp/audio_{uuid.uuid4()}.wav"
    
    try:
        audio.save(temp_file)
        if os.path.getsize(temp_file) == 0:
            return jsonify({"error": "Empty audio file"}), 400
            
        response,status = transcribe_audio(temp_file)
        return jsonify(response), status, {'Content-Type': 'application/json; charset=utf-8'}
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)