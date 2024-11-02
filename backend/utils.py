# backend/utils.py

import mediapipe as mp
import math

# Словарь для сопоставления ключевых точек от Mediapipe с моделью классификатора
LM_DICT = {
    0: 0, 1: 10, 2: 12, 3: 14, 4: 16, 5: 11, 6: 13, 7: 15,
    8: 24, 9: 26, 10: 28, 11: 23, 12: 25, 13: 27,
    14: 5, 15: 2, 16: 8, 17: 7,
}


def set_pose_parameters():
    mode = False
    complexity = 1
    smooth_landmarks = True
    enable_segmentation = False
    smooth_segmentation = True
    detectionCon = 0.5
    trackCon = 0.5
    mpPose = mp.solutions.pose
    return mode, complexity, smooth_landmarks, enable_segmentation, smooth_segmentation, detectionCon, trackCon, mpPose


def calculate_angle(point1, point2, point3):
    """
    Вычисляет угол между тремя точками.

    :param point1: Координаты первой точки (x1, y1)
    :param point2: Координаты второй точки (x2, y2)
    :param point3: Координаты третьей точки (x3, y3)
    :return: Угол в градусах
    """
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3

    angle = math.degrees(
        math.atan2(y3 - y2, x3 - x2) -
        math.atan2(y1 - y2, x1 - x2)
    )

    # Корректировка угла
    if angle < 0:
        angle += 360
    if angle > 180:
        angle = 360 - angle
    return angle