# backend/pushup_counter.py

import cv2
import mediapipe as mp
import numpy as np
from collections import deque
from utils import set_pose_parameters, calculate_angle, LM_DICT
import os


# Если вы используете DeepFitClassifier, импортируйте его здесь.
# from DeepFit.DeepFitClassifier import DeepFitClassifier

class PushUpCounter:
    def __init__(self, deepfit_model_path='DeepFit/deepfit_classifier_v3.tflite'):
        # Инициализация параметров позы
        params = set_pose_parameters()
        (mode, complexity, smooth_landmarks, enable_segmentation,
         smooth_segmentation, detectionCon, trackCon, mpPose) = params
        self.pose = mpPose.Pose(
            static_image_mode=mode,
            model_complexity=complexity,
            smooth_landmarks=smooth_landmarks,
            enable_segmentation=enable_segmentation,
            smooth_segmentation=smooth_segmentation,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

        # Инициализация классификатора DeepFit (опционально)
        if os.path.exists(deepfit_model_path):
            # self.classifier = DeepFitClassifier(deepfit_model_path)
            self.classifier = None  # Замените на инициализацию вашего классификатора
            print(f"Классификатор DeepFit загружен по пути: {deepfit_model_path}")
        else:
            self.classifier = None
            print(f"Классификатор DeepFit не найден по пути: {deepfit_model_path}")

        # Инициализация счетчиков
        self.reset_counters()

    def reset_counters(self):
        self.count = 0
        self.direction = 0
        self.form = 0
        self.feedback = "Bad Form. Correct Posture."
        self.frame_queue = deque(maxlen=250)

    def process_frame(self, frame):
        """
        Обрабатывает один кадр и обновляет счетчики.
        Возвращает информацию для фронтенда.

        :param frame: Полученный кадр в формате BGR
        :return: Словарь с данными
        """
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)
        landmark_list = self.get_position(results, frame.shape[0], frame.shape[1])

        data = {
            'landmarks': landmark_list,
            'angles': {},
            'feedback': self.feedback,
            'count': self.count
        }

        if landmark_list:
            # Расчёт углов
            shoulder = self.get_landmark(landmark_list, 11)  # Левая рука
            elbow = self.get_landmark(landmark_list, 13)
            wrist = self.get_landmark(landmark_list, 15)
            hip = self.get_landmark(landmark_list, 23)
            knee = self.get_landmark(landmark_list, 25)  # Левое колено

            if shoulder and elbow and wrist and hip and knee:
                elbow_angle = calculate_angle(
                    (shoulder[1], shoulder[2]),
                    (elbow[1], elbow[2]),
                    (wrist[1], wrist[2])
                )
                shoulder_angle = calculate_angle(
                    (elbow[1], elbow[2]),
                    (shoulder[1], shoulder[2]),
                    (hip[1], hip[2])
                )
                hip_angle = calculate_angle(
                    (shoulder[1], shoulder[2]),
                    (hip[1], hip[2]),
                    (knee[1], knee[2])
                )

                data['angles'] = {
                    'elbow': elbow_angle,
                    'shoulder': shoulder_angle,
                    'hip': hip_angle
                }

                # Подсчёт отжиманий
                self.update_counters(elbow_angle, shoulder_angle, hip_angle)
                data['feedback'] = self.feedback
                data['count'] = self.count

        return data

    def get_position(self, results, height, width):
        """
        Извлекает координаты ключевых точек.

        :param results: Результаты обработки Mediapipe Pose
        :param height: Высота кадра
        :param width: Ширина кадра
        :return: Список ключевых точек
        """
        landmark_list = []
        if results.pose_landmarks:
            for id, lm in enumerate(results.pose_landmarks.landmark):
                px, py = int(lm.x * width), int(lm.y * height)
                landmark_list.append([id, px, py])
        return landmark_list

    def get_landmark(self, landmark_list, landmark_id):
        """
        Получает координаты конкретной ключевой точки.

        :param landmark_list: Список ключевых точек
        :param landmark_id: ID ключевой точки
        :return: Список [id, x, y] или None
        """
        for lm in landmark_list:
            if lm[0] == landmark_id:
                return lm
        return None

    def update_counters(self, elbow_angle, shoulder_angle, hip_angle):
        """
        Обновляет счетчики отжиманий на основе углов.

        :param elbow_angle: Угол в локте
        :param shoulder_angle: Угол в плече
        :param hip_angle: Угол в бедре
        """
        # Логирование углов для отладки
        print(f"Elbow Angle: {elbow_angle:.2f}, Shoulder Angle: {shoulder_angle:.2f}, Hip Angle: {hip_angle:.2f}")

        # Интерполяция угла локтя для прогресс-бара и процента успешности
        pushup_success_percentage = np.interp(elbow_angle, (90, 160), (0, 100))
        pushup_success_percentage = int(pushup_success_percentage)  # Округление для отправки клиенту

        # Проверка начальной формы
        if elbow_angle > 160 and shoulder_angle > 40 and hip_angle > 160:
            self.form = 1
        else:
            self.form = 0

        # Полный цикл выполнения отжиманий
        if self.form == 1:
            if pushup_success_percentage <= 10:
                if elbow_angle <= 90 and hip_angle > 160:
                    if self.direction == 0:
                        self.count += 0.5
                        self.direction = 1
                    self.feedback = "Go Up"
                else:
                    self.feedback = "Bad Form. Correct Posture."
            elif pushup_success_percentage >= 90:
                if elbow_angle > 160 and shoulder_angle > 20 and hip_angle > 160:
                    if self.direction == 1:
                        self.count += 0.5
                        self.direction = 0
                    self.feedback = "Go Down"
                else:
                    self.feedback = "Bad Form. Correct Posture."
            else:
                self.feedback = "Keep Going"
        else:
            self.feedback = "Bad Form. Correct Posture."

        # Логирование состояния счётчика для отладки
        print(f"Count: {self.count}, Direction: {self.direction}, Feedback: {self.feedback}")