// backend/static/script.js

$(document).ready(function() {
    const video = document.getElementById('video');
    const overlay = document.getElementById('overlay');
    const ctx = overlay.getContext('2d');
    const feedback = $('#feedback');
    const countDisplay = $('#count');
    const progressBar = $('#progress');
    const activateButton = $('#activate-camera');
    const videoContainer = $('.video-container');
    const statusContainer = $('.status');

    let socket;

    // Функция для инициализации Socket.IO и захвата видео
    function initializeApp() {
        // Подключение к WebSocket серверу
        socket = io.connect();

        socket.on('connect', function() {
            console.log('Подключено к серверу');
        });

        socket.on('status', function(data) {
            console.log(data.status);
        });

        socket.on('result', function(data) {
            try {
                // Если данные уже объект
                const parsedData = data;

                if(parsedData.status === 'processing') {
                    // Обновление обратной связи и счётчика
                    feedback.text(parsedData.feedback);
                    countDisplay.text(parsedData.count);

                    // Изменение цвета обратной связи в зависимости от состояния
                    if(parsedData.feedback.startsWith("Go Up") || parsedData.feedback.startsWith("Go Down")) {
                        feedback.css('color', 'green');
                    } else if(parsedData.feedback.startsWith("Bad")) {
                        feedback.css('color', 'red');
                    } else if(parsedData.feedback.startsWith("Keep")) {
                        feedback.css('color', 'orange');
                    } else {
                        feedback.css('color', 'black');
                    }

                    // Вычисление процента успешности на основе углов
                    const elbowAngle = parsedData.angles.elbow || 0;
                    const pushupSuccessPercentage = Math.min(Math.max(((elbowAngle - 90) / 70) * 100, 0), 100);
                    progressBar.css('width', `${pushupSuccessPercentage}%`);

                    // Масштабирование координат ключевых точек
                    const scaleX = overlay.width / parsedData.frame_width;
                    const scaleY = overlay.height / parsedData.frame_height;
                    const adjustedLandmarks = parsedData.landmarks.map(lm => ({
                        id: lm[0],
                        x: lm[1] * scaleX,
                        y: lm[2] * scaleY
                    }));

                    // Отрисовка аннотаций
                    drawAnnotations(adjustedLandmarks);
                }

            } catch (e) {
                console.error('Ошибка при обработке данных:', e);
            }
        });

        socket.on('disconnect', function() {
            console.log('Отключено от сервера');
        });

        // Захват видео с веб-камеры с заданными ограничениями
        navigator.mediaDevices.getUserMedia({
            video: {
                width: { ideal: 640 },
                height: { ideal: 480 }
            },
            audio: false
        })
            .then(function(stream) {
                video.srcObject = stream;
                video.play();
                // Настройка размера канваса после загрузки видео
                video.onloadedmetadata = function() {
                    overlay.width = video.videoWidth;
                    overlay.height = video.videoHeight;
                    // Запуск отправки кадров
                    sendFrames();
                };
            })
            .catch(function(err) {
                console.log("Ошибка доступа к камере: " + err);
                alert("Не удалось получить доступ к камере. Пожалуйста, попробуйте еще раз.");
            });

        // Отображение видео и статуса
        videoContainer.show();
        statusContainer.show();
        activateButton.hide();
    }

    // Функция для отправки кадров на сервер
    function sendFrames() {
        const FPS = 10; // Частота отправки кадров

        setInterval(function() {
            // Создание временного канваса для захвата кадра
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = video.videoWidth;
            tempCanvas.height = video.videoHeight;
            const tempCtx = tempCanvas.getContext('2d');
            tempCtx.drawImage(video, 0, 0, tempCanvas.width, tempCanvas.height);
            const dataURL = tempCanvas.toDataURL('image/jpeg');

            // Отправка изображения через WebSocket
            if (socket.connected) {
                socket.emit('image', dataURL);
            }
        }, 1000 / FPS);
    }

    // Функция для отрисовки аннотаций
    function drawAnnotations(landmarks) {
        // Очистка канваса
        ctx.clearRect(0, 0, overlay.width, overlay.height);

        if (landmarks && landmarks.length > 0) {
            // Преобразование списка ключевых точек в объект для удобства доступа
            const lm = {};
            landmarks.forEach(point => {
                lm[point.id] = {x: point.x, y: point.y};
            });

            // Нарисовать линии по связям Mediapipe
            const connections = [
                [11, 13], [13, 15],  // Левая рука
                [12, 14], [14, 16],  // Правая рука
                [11, 23], [12, 24],  // Туловище
                [23, 25], [24, 26],  // Ноги
                [11, 12],             // Шея между плечами
                [23, 24],             // Туловище горизонтально
                [25, 26]              // Ноги горизонтально
                // Добавьте другие связи по необходимости
            ];

            connections.forEach(pair => {
                const [start, end] = pair;
                if (lm[start] && lm[end]) {
                    ctx.beginPath();
                    ctx.moveTo(lm[start].x, lm[start].y);
                    ctx.lineTo(lm[end].x, lm[end].y);
                    ctx.strokeStyle = 'blue';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                }
            });

            // Нарисовать круги на ключевых точках
            for (const id in lm) {
                const x = lm[id].x;
                const y = lm[id].y;
                ctx.beginPath();
                ctx.arc(x, y, 5, 0, 2 * Math.PI);
                ctx.fillStyle = 'red';
                ctx.fill();
            }
        }
    }

    // Обработчик нажатия на кнопку "Activate Camera"
    activateButton.on('click', function() {
        initializeApp();
    });
});