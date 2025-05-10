from multiprocessing import Process, Queue
from teclado2 import start_virtual_keyboard
import time
import cv2
from ultralytics import YOLO
import pyttsx3

def speak(text, engine):
    engine.say(text)
    engine.runAndWait()

def procesar_parametro(param):
    return str(param)

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
    q = Queue()
    p = Process(target=start_virtual_keyboard, args=(q,))
    p.start()

    engine = pyttsx3.init()
    modelo = YOLO("best5.pt")
    cap = cv2.VideoCapture(0)

    estado_anterior = None

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        resultados = modelo.predict(frame, save=False, show=True)
        mirada = procesar_parametro(resultados[0].probs.top1)

        if mirada != estado_anterior:
            estado_anterior = mirada
            direccion = getDirection(mirada)
            print(f"Cambio de estado a: {direccion}")
            speak(direccion, engine)
            if mirada != '2':
                q.put(mirada)

        cv2.imshow("Detección en tiempo real", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
