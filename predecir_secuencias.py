# predecir_secuencias.py - Predicción en tiempo real con modelo LSTM
# Captura secuencias de video con Holistic, predice gestos con un modelo LSTM y muestra el resultado en pantalla

import cv2
import time
import numpy as np
import pickle
import os
from collections import deque, Counter
from tensorflow.keras.models import load_model
from utils import (
    Config, initialize_holistic, setup_camera, 
    extract_holistic_landmarks, normalize_landmarks, validate_landmarks
)
from PIL import Image

# Carga los frames de un gif correspondiente a una clase reconocida
def reproducir_gif(ruta_gif):
    if not os.path.exists(ruta_gif):
        return None

    gif = Image.open(ruta_gif)
    frames = []
    try:
        while True:
            frame = gif.convert('RGB')
            frame = np.array(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, (300, 300))
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass
    return frames

def main():
    print("\n🔮 PREDICCIÓN EN TIEMPO REAL - MODO UNIFICADO")

    # Carga el modelo LSTM previamente entrenado y las etiquetas
    model = load_model(Config.MODEL_PATH)
    with open(Config.LABELS_PATH, 'rb') as f:
        etiquetas = pickle.load(f)

    # Inicializa cámara y Holistic
    cap = setup_camera()
    holistic = initialize_holistic()

    # Buffers para almacenar frames y resultados de predicción recientes
    buffer = deque(maxlen=Config.FRAMES_PER_SEQUENCE)
    pred_buffer = deque(maxlen=3)

    gesto_actual = ""
    ultimo_tiempo = 0
    frames_gif = []  # frames del gif asociado a la clase predicha
    gif_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        results = holistic.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        landmarks = extract_holistic_landmarks(results)
        landmarks = normalize_landmarks(landmarks)

        # Solo usamos frames válidos para predecir
        if validate_landmarks(landmarks):
            buffer.append(landmarks)

        # Cuando se completa el buffer de secuencia
        if len(buffer) == Config.FRAMES_PER_SEQUENCE:
            secuencia = np.array(buffer).reshape(1, Config.FRAMES_PER_SEQUENCE, Config.FEATURES)
            pred = model.predict(secuencia, verbose=0)[0]
            idx = np.argmax(pred)
            confianza = pred[idx]
            pred_buffer.append(idx)

            # Si la predicción es suficientemente confiable y consistente
            if confianza > 0.6 and pred_buffer.count(idx) >= 2:
                gesto_actual = etiquetas[idx]
                ultimo_tiempo = time.time()
                print(f"🎯 GESTO DETECTADO: {gesto_actual.upper()} (confianza: {confianza:.2f})")

                # Carga el gif de referencia de la clase detectada
                ruta_gif = os.path.join(Config.GIFS_DIR, f"{gesto_actual}.gif")
                frames_gif = reproducir_gif(ruta_gif)
                gif_idx = 0

            buffer.clear()

        # Muestra el gesto detectado en el frame principal
        if gesto_actual and (time.time() - ultimo_tiempo < 2.5):
            cv2.putText(frame, f"{gesto_actual.upper()}", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,255,0), 4)
        else:
            gesto_actual = ""
            frames_gif = []

        cv2.putText(frame, "'Q'=salir", (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200,200,200), 1)
        cv2.imshow("Reconocimiento de Señas (Holistic)", frame)

        # Ventana secundaria que reproduce el gif del gesto identificado
        if frames_gif:
            cv2.imshow("Ejemplo Identificado", frames_gif[gif_idx % len(frames_gif)])
            gif_idx += 1

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    # Libera recursos
    cap.release()
    cv2.destroyAllWindows()
    holistic.close()
    print("\n👋 Predicción finalizada.")

def predecir_desde_imagen(imagen):
    import mediapipe as mp
    import numpy as np
    from tensorflow.keras.models import load_model
    from utils import extract_holistic_landmarks, normalize_landmarks, validate_landmarks, Config

    mp_holistic = mp.solutions.holistic
    with mp_holistic.Holistic(static_image_mode=True) as holistic:
        frame = np.array(imagen.convert('RGB'))
        frame = frame[:, :, ::-1]  # RGB a BGR
        results = holistic.process(frame)
        landmarks = extract_holistic_landmarks(results)
        if not validate_landmarks(landmarks):
            return "sin_seña"
        landmarks_norm = normalize_landmarks(landmarks)
        # Repite el mismo vector 30 veces para simular una secuencia
        secuencia = np.array([landmarks_norm] * 30).reshape(1, 30, 147)
        modelo = load_model(Config.MODEL_PATH)
        etiquetas = np.load(Config.LABELS_PATH, allow_pickle=True)
        pred = modelo.predict(secuencia)
        clase_idx = np.argmax(pred)
        return etiquetas[clase_idx]

if __name__ == '__main__':
    main()