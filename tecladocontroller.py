from multiprocessing import Process, Queue, set_start_method
import time
import cv2
from ultralytics import YOLO
import pyttsx3
from HACKATHON.teclado import start_virtual_keyboard

# Función para decir texto en voz alta
def speak(text, engine):
    engine.say(text)
    engine.runAndWait()

# Convierte el valor de top1 a string
def procesar_parametro(param):
    return str(param)

# Traduce el índice a dirección
def getDirection(param):
    directions = {
        '0': 'abajo',
        '1': 'arriba',
        '2': 'centro',
        '3': 'cerrado',
        '4': 'derecha',
        '5': 'izquierda'
    }
    return directions.get(param, 'desconocido')

if __name__ == "__main__":
    # 🔧 Requerido en algunos sistemas operativos como macOS o Linux
    set_start_method("spawn")

    # 🧠 Cola de comunicación entre procesos
    q = Queue()

    # 🎹 Lanzar el teclado virtual en un proceso separado
    p = Process(target=start_virtual_keyboard, args=(q,))
    p.start()

    # 🗣️ Inicializar motor de voz
    engine = pyttsx3.init()

    # 🧠 Cargar modelo YOLO
    modelo = YOLO("best.pt")

    # 🎥 Captura de video
    cap = cv2.VideoCapture(0)

    estado_anterior = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 🔍 Detectar mirada
        resultados = modelo.predict(frame, save=False, show=True)
        mirada = procesar_parametro(resultados[0].probs.top1)

        if mirada != estado_anterior:
            estado_anterior = mirada
            direccion = getDirection(mirada)
            print(f"Cambio de estado a: {direccion}")
            speak(direccion, engine)

            if mirada != '2':  # ignorar "centro"
                q.put(mirada)

        # Mostrar la cámara
        cv2.imshow("Detección en tiempo real", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 🧹 Cleanup
    cap.release()
    cv2.destroyAllWindows()
    p.terminate()
