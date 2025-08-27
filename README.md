# 🤟 Lengua de Señas con MediaPipe Holistic - VERSIÓN UNIFICADA

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/Status-Activo-brightgreen.svg)
![Reconocimiento](https://img.shields.io/badge/Holistic-Hands%2C%20Face%2C%20Pose-orange.svg)
![Modelo](https://img.shields.io/badge/Modelo-Unificado--LSTM-red.svg)

## 🚀 Proyecto Unificado para Reconocimiento de Señas

Este sistema reconoce:
- Letras del abecedario (a-z)
- Números (0-9)

- Palabras simples
- Frases complejas

Todo utilizando **MediaPipe Holistic** + **LSTM** + una interfaz unificada de captura, entrenamiento y predicción.

---

## 📁 Estructura del Proyecto

```
proyecto_senas_holistic/
├── data/
│   └── secuencias/          # Secuencias .npy organizadas por clase
├── gifs/                    # GIFs de referencia visual por clase
├── models/                  # Modelo LSTM entrenado + etiquetas
├── utils.py                 # Funciones generales y configuración
├── capturar_secuencias.py  # Captura unificada
├── entrenar_modelo.py      # Entrenamiento LSTM
├── predecir_secuencias.py  # Predicción en tiempo real
├── main.py                 # Menú interactivo unificado
└── requirements.txt        # Dependencias necesarias
```

---

## ✨ Características Destacadas

- 🧠 **Un solo modelo LSTM** para todo tipo de señas
- 👐 **Detección completa**: manos, rostro, hombros
- 🎥 **Captura guiada** con mensajes en pantalla y visores
- 🎞️ **GIF de ejemplo** para cada clase (letra, número, frase)
- 🎯 **Predicción fluida** con ventana de resultado + referencia

---

## 🔧 Requisitos

- Python 3.10+
- Webcam
- MediaPipe + TensorFlow

### 📦 Instalación

```bash
pip install -r requirements.txt
```

**Dependencias incluidas:**

```
opencv-python        # Captura de video
mediapipe            # Detección Holistic (manos, rostro, cuerpo)
numpy                # Cálculos numéricos
tensorflow           # Modelo LSTM
scikit-learn         # División de datos y procesamiento
pillow               # Generación de GIFs
```

---

## 📸 Captura de Datos

```bash
python capturar_secuencias.py
```

- Ingresá una letra, número o frase.
- El sistema te guía para grabar 30 secuencias.
- Se genera automáticamente un `.gif` de referencia.

---

## 🧠 Entrenamiento del Modelo

```bash
python entrenar_modelo.py
```

- Entrena el modelo LSTM para todas las clases detectadas.
- Usa callbacks inteligentes: EarlyStopping y ReduceLROnPlateau.

---

## 🔍 Predicción en Tiempo Real

```bash
python predecir_secuencias.py
```

- Muestra el gesto identificado.
- Abre una ventana con el `.gif` correspondiente al gesto.
- Buffer inteligente para evitar fluctuaciones.

---

## 🧪 Menú Interactivo

```bash
python main.py
```

- 1. Capturar nuevas clases
- 2. Entrenar modelo
- 3. Ejecutar predicción
- 4. Salir

---

## 🧠 Modelo Unificado

- Arquitectura: LSTM (64 → 32) + BatchNorm + Dropout + Dense
- Entrenado con secuencias de 30 frames, 147 features (2 manos + hombros + rostro)
- Multi-clase: reconoce letras, números y frases

---

## 🎓 Ideal para

- Aprendizaje de **lengua de señas** con ejemplos visuales
- Proyectos educativos con de **lengua de señas**

---

## 📄 Licencia

Distribuido bajo la licencia MIT. Uso libre con fines educativos y de investigación.

---

## 👨‍💻 Autores

**Ricardo Leitón**  
📧 ricardo.leiton@gmail.com  
🐙 GitHub: [@ricardoleiton](https://github.com/ricardoleiton)

**Aldana Cáseres**  
📧 aldiicaseres@gmail.com  

**Priscila Tayura**  
📧 priscilatayura@gmail.com

**Gimena Perez**  
📧 gimeperez1991@gmail.com  

**Mayerly Quiroz**  
📧 mayerlyquiroz22@gmail.com  

**Nahuel Lozano**  
📧 lozano.nahuel88@gmail.com 

---