# entrenar_modelo.py - Entrena el modelo LSTM para reconocer señas usando secuencias
# Este script recorre las carpetas de secuencias por clase, entrena una red LSTM y guarda el modelo y etiquetas

import os
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, BatchNormalization
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from utils import Config, create_directories

# Carga todas las secuencias de datos y etiquetas desde la carpeta data/secuencias/
def cargar_datos():
    X, y = [], []
    etiquetas = sorted(os.listdir(Config.SEQUENCES_DIR))  # Cada carpeta es una clase

    for idx, clase in enumerate(etiquetas):
        carpeta_clase = os.path.join(Config.SEQUENCES_DIR, clase)
        for archivo in os.listdir(carpeta_clase):
            if archivo.endswith('.npy'):
                ruta = os.path.join(carpeta_clase, archivo)
                secuencia = np.load(ruta)
                X.append(secuencia)
                y.append(idx)

    return np.array(X), np.array(y), etiquetas

# Define y construye el modelo LSTM para secuencias de landmarks
def construir_modelo(input_shape, num_clases):
    modelo = Sequential()
    modelo.add(LSTM(64, return_sequences=True, input_shape=input_shape))
    modelo.add(BatchNormalization())
    modelo.add(LSTM(32))
    modelo.add(Dropout(0.3))
    modelo.add(Dense(64, activation='relu'))
    modelo.add(Dense(num_clases, activation='softmax'))
    modelo.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return modelo

def main():
    print("📥 Cargando datos de entrenamiento...")
    X, y, etiquetas = cargar_datos()
    print(f"🔤 Clases encontradas: {etiquetas}")
    print(f"📊 Total de muestras: {len(X)}")

    # Divide los datos en entrenamiento y validación
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

    print("🧠 Construyendo modelo LSTM...")
    modelo = construir_modelo((Config.FRAMES_PER_SEQUENCE, Config.FEATURES), len(etiquetas))

    # Callbacks para detener el entrenamiento si no mejora o ajustar el learning rate
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5)

    print("🚀 Entrenando modelo...")
    modelo.fit(X_train, y_train, epochs=100, validation_data=(X_val, y_val),
               callbacks=[early_stop, reduce_lr], batch_size=16)

    create_directories([Config.MODELS_DIR])

    # Guarda el modelo y las etiquetas
    modelo.save(Config.MODEL_PATH)
    with open(Config.LABELS_PATH, 'wb') as f:
        pickle.dump(etiquetas, f)

    print(f"✅ Modelo guardado en {Config.MODEL_PATH}")
    print(f"✅ Etiquetas guardadas en {Config.LABELS_PATH}")

if __name__ == "__main__":
    main()