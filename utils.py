# utils.py - Proyecto Holistic Unificado para Lengua de Señas

import os
import cv2
import numpy as np
import mediapipe as mp
import platform

# ==== CONFIGURACIÓN CENTRAL ====
class Config:
    # Carpetas para almacenar secuencias, modelos y gifs
    SEQUENCES_DIR = "data/secuencias"
    MODELS_DIR = "models"
    GIFS_DIR = "gifs"

    # Parámetros de captura
    FRAMES_PER_SEQUENCE = 30  # Cantidad de frames por cada secuencia
    SEQUENCES_PER_CLASS = 30  # Cuántas secuencias se capturan por clase

    # Cantidad total de características (features) por frame
    FEATURES = 147  # 2 manos (21x3x2 = 126), 2 hombros (2x3 = 6), rostro (5x3 = 15)

    # Rutas de salida del modelo y etiquetas
    MODEL_PATH = os.path.join(MODELS_DIR, "modelo_lstm.h5")
    LABELS_PATH = os.path.join(MODELS_DIR, "etiquetas.pkl")

    # Parámetros de configuración de MediaPipe Holistic
    DETECTION_CONFIDENCE = 0.7
    TRACKING_CONFIDENCE = 0.5
    MODEL_COMPLEXITY = 1

# ==== UTILIDADES GENERALES ====

def print_system_info():
    """Imprime información del sistema y la configuración del proyecto."""
    print("===============================")
    print(" Lengua de Señas - Holistic")
    print("===============================")
    print(f"Sistema: {platform.system()} {platform.release()}")
    print(f"Python: {platform.python_version()}")
    print(f"Landmarks: {Config.FEATURES} por frame")
    print(f"Frames por secuencia: {Config.FRAMES_PER_SEQUENCE}")
    print("===============================")

def create_directories(paths):
    """Crea las carpetas necesarias si no existen."""
    for path in paths:
        os.makedirs(path, exist_ok=True)

def initialize_holistic():
    """
    Inicializa el modelo Holistic de MediaPipe con los parámetros definidos en la configuración.
    Devuelve el objeto de seguimiento corporal completo.
    """
    return mp.solutions.holistic.Holistic(
        static_image_mode=False,
        model_complexity=Config.MODEL_COMPLEXITY,
        min_detection_confidence=Config.DETECTION_CONFIDENCE,
        min_tracking_confidence=Config.TRACKING_CONFIDENCE
    )

def setup_camera(index=0, width=1280, height=720):
    """
    Configura la cámara web con el índice y resolución especificados.
    Retorna el objeto de captura de OpenCV.
    """
    cap = cv2.VideoCapture(index)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    return cap

# ==== PROCESAMIENTO DE LANDMARKS ====

def extract_holistic_landmarks(results):
    """
    Extrae los landmarks relevantes del resultado de MediaPipe:
    - 2 manos (126 valores)
    - 2 hombros (6 valores)
    - 5 puntos del rostro (15 valores)
    Total: 147 valores por frame.
    """
    data = []

    # Manos (izquierda y derecha)
    for hand in [results.left_hand_landmarks, results.right_hand_landmarks]:
        if hand:
            for lm in hand.landmark:
                data.extend([lm.x, lm.y, lm.z])
        else:
            data.extend([0] * 63)  # 21 puntos * 3 coordenadas

    # Hombros (pose landmarks: índice 11 y 12)
    if results.pose_landmarks:
        for idx in [11, 12]:
            lm = results.pose_landmarks.landmark[idx]
            data.extend([lm.x, lm.y, lm.z])
    else:
        data.extend([0] * 6)

    # Puntos del rostro: nariz, ojos, boca
    if results.face_landmarks:
        for idx in [1, 33, 263, 61, 291]:
            lm = results.face_landmarks.landmark[idx]
            data.extend([lm.x, lm.y, lm.z])
    else:
        data.extend([0] * 15)

    return np.array(data)

def normalize_landmarks(landmarks):
    """
    Normaliza los landmarks para que sean independientes de la posición y tamaño del cuerpo.
    - Centra el conjunto en el punto medio
    - Escala dividiendo por la distancia máxima a ese centro
    """
    if landmarks is None or len(landmarks) != Config.FEATURES:
        return landmarks

    reshaped = landmarks.reshape(-1, 3)
    center = np.mean(reshaped, axis=0)
    reshaped -= center
    scale = np.max(np.linalg.norm(reshaped, axis=1))
    if scale > 0:
        reshaped /= scale
    return reshaped.flatten()

def validate_landmarks(landmarks):
    """
    Verifica si los landmarks extraídos son válidos:
    - Tiene longitud correcta
    - No está completamente en cero
    - No contiene NaN ni infinitos
    """
    if landmarks is None or len(landmarks) != Config.FEATURES:
        return False
    if np.allclose(landmarks, 0):
        return False
    if np.any(np.isnan(landmarks)) or np.any(np.isinf(landmarks)):
        return False
    return True
