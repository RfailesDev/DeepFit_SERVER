# backend/main.py

import eventlet
eventlet.monkey_patch()

import os
import base64
import cv2
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from pushup_counter import PushUpCounter
import json
from pyngrok import ngrok

app = Flask(__name__, static_folder='../frontend', template_folder='../frontend')
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# Инициализация PushUpCounter
counter = PushUpCounter()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('status', {'status': 'Connected to server'})

@socketio.on('image')
def handle_image(data):
    try:
        # Декодирование base64 изображения
        header, encoded = data.split(',', 1)
        decoded = base64.b64decode(encoded)
        np_data = np.frombuffer(decoded, np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        if frame is None:
            emit('result', {'status': 'error', 'message': 'Invalid image data'})
            return

        # Обработка кадра
        result = counter.process_frame(frame)

        # Формирование данных для отправки
        response = {
            'status': 'processing',
            'progress': result.get('count', 0),
            'landmarks': result.get('landmarks', []),
            'angles': result.get('angles', {}),
            'feedback': result.get('feedback', '')
        }

        # Отправка данных обратно клиенту
        emit('result', json.dumps(response))
    except Exception as e:
        print(f"Error processing frame: {e}")
        emit('result', {'status': 'error', 'message': str(e)})

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    # Открыть туннель ngrok
    public_url = ngrok.connect(5000)
    print(f"Public URL: {public_url}")

    # Запуск Flask-SocketIO сервера
    socketio.run(app, host='0.0.0.0', port=5000)