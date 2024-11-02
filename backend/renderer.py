# renderer.py

import cv2


class Renderer:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw_annotations(self, frame, data):
        """
        Рисует аннотации на кадре на основе переданных данных.

        :param frame: Исходный кадр изображения.
        :param data: Словарь с данными для отрисовки.
        :return: Аннотированный кадр.
        """
        # Отрисовка ключевых точек
        if data['landmarks']:
            for lm in data['landmarks']:
                cv2.circle(frame, (lm[1], lm[2]), 5, (255, 0, 0), cv2.FILLED)

        # Отрисовка прогресса отжиманий
        if 'angles' in data and data['angles']:
            elbow_angle = data['angles'].get('elbow', 0)
            pushup_success_percentage = int(np.interp(elbow_angle, (90, 160), (0, 100)))
            pushup_progress_bar = int(np.interp(elbow_angle, (90, 160), (380, 50)))

            cv2.rectangle(frame, (580, 50), (600, 380), (0, 255, 0), 3)
            cv2.rectangle(frame, (580, pushup_progress_bar), (600, 380), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, f'{pushup_success_percentage}%', (565, 430),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

        # Отображение счёта отжиманий
        cv2.rectangle(frame, (0, 380), (100, 480), (0, 255, 0), cv2.FILLED)
        cv2.putText(frame, str(int(data['count'])), (25, 455),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        # Отображение обратной связи
        cv2.rectangle(frame, (500, 0), (640, 40), (255, 255, 255), cv2.FILLED)
        cv2.putText(frame, data['feedback'], (500, 40),
                    cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

        return frame