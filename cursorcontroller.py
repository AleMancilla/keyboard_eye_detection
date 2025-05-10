import cv2
import pyttsx3
import pyautogui
from ultralytics import YOLO
import time

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def getDirectionFromTop1(top1):
    direction_map = {
        0: 'abajo',
        1: 'arriba',
        2: 'centro',
        3: 'cerrado',
        4: 'derecha',
        5: 'izquierda'
    }
    return direction_map.get(top1, 'desconocido')

# Movimiento del cursor según dirección
def mover_cursor(direccion, step=30):  # puedes ajustar el step para mayor o menor velocidad
    x, y = pyautogui.position()
    if direccion == 'arriba':
        pyautogui.moveTo(x, y - step)
    elif direccion == 'abajo':
        pyautogui.moveTo(x, y + step)
    elif direccion == 'izquierda':
        pyautogui.moveTo(x - step, y)
    elif direccion == 'derecha':
        pyautogui.moveTo(x + step, y)

# Cargar modelo
modelo = YOLO("best3.pt")
cap = cv2.VideoCapture(0)

ultima_direccion = None
contador = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    resultados = modelo.predict(frame, save=False, show=True)
    top1 = resultados[0].probs.top1
    direccion = getDirectionFromTop1(top1)

    print("#####################")
    print(resultados[0].names)
    print(resultados[0].probs.data)
    print("#####################")

    # Decimos la dirección si cambió recientemente
    if direccion != ultima_direccion:
        ultima_direccion = direccion
        print(f"Dirección: {direccion}")
        speak(direccion)

    # Mover el cursor siempre que no sea centro ni cerrado
    if direccion not in ['centro', 'cerrado']:
        mover_cursor(direccion)

    cv2.imshow("Detección en tiempo real", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
