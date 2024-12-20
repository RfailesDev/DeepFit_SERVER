# Подсчет отжиманий в реальном времени с MediaPipe и перспективной интеграцией PyTorch Transformer

Этот проект представляет собой веб-приложение, которое использует MediaPipe для подсчета отжиманий в реальном времени с помощью веб-камеры.  В настоящее время ведется исследовательская работа по интеграции модели на основе PyTorch Transformer для более точной классификации упражнений и подсчета подходов.

## Возможности

* **Подсчет отжиманий:** Приложение определяет и подсчитывает количество выполненных отжиманий.
* **Обратная связь в реальном времени:**  Предоставляет  обратную связь о форме выполнения упражнения, помогая пользователю поддерживать правильную технику. Сообщения "Go Up", "Go Down", "Keep Going" и "Bad Form. Correct Posture" помогают корректировать движения.
* **Визуализация ключевых точек:** Отображает ключевые точки тела, обнаруженные MediaPipe, на видеопотоке.
* **Прогресс-бар:**  Показывает процент выполнения текущего отжимания.
* **Простая установка и использование:**  Приложение легко настроить и запустить.
* **Кроссплатформенность:** Работает в любом современном веб-браузере, поддерживающем WebSockets и доступ к веб-камере.

## Технологии

* **Python:** Бэкенд на Python с использованием Flask и Flask-SocketIO.
* **MediaPipe:**  Обнаружение поз и ключевых точек тела.
* **PyTorch Transformer (в разработке):**  Планируется использовать для классификации упражнений и подсчета подходов.  В данный момент проводится исследование и разработка этой функциональности.
* **JavaScript, HTML, CSS:**  Фронтенд приложения.
* **WebSockets (Socket.IO):**  Двусторонняя связь между клиентом и сервером.
* **ngrok:**  Для создания туннеля к локальному серверу.

## Установка и запуск

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/ваш_репозиторий/pushup-counter.git
   ```

2. **Перейдите в директорию проекта:**
   ```bash
   cd pushup-counter/backend 
   ```

3. **Создайте виртуальное окружение (рекомендуется):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```

4. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Запустите сервер:**
   ```bash
   python main.py
   ```
   * Вам понадобится токен ngrok.  Замените плейсхолдер `"..."` в `main.py` на ваш актуальный токен.
   * Сервер запустится на порту 5000. ngrok создаст публичный URL, который вы сможете использовать для доступа к приложению.


## Как использовать

1. Откройте публичный URL, предоставленный ngrok, в вашем веб-браузере.
2. Нажмите кнопку "Activate Camera", чтобы разрешить доступ к вашей веб-камере.
3. Примите правильную позу для отжиманий.
4. Начните выполнять отжимания, следуя инструкциям на экране.

##  Планы развития и исследования

В настоящее время ведется активное исследование  возможностей использования архитектуры Transformer (PyTorch) для улучшения точности и функциональности приложения.  Цель исследования — создать модель, способную:

* **Классифицировать различные типы упражнений:** Автоматически определять, какое упражнение выполняет пользователь (отжимания, приседания, выпады и т.д.).
* **Точно подсчитывать подходы:**  Определять начало и конец каждого подхода для различных упражнений.
* **Улучшить распознавание формы:**  Более точно анализировать форму выполнения упражнений и предоставлять более детальную обратную связь.

Эта функциональность находится в стадии разработки и будет добавлена в будущих версиях приложения.
