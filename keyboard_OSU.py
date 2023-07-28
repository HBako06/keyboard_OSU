import cv2
import numpy as np
#import keyboard
#import pyautogui
#from pynput.keyboard import Controller
import time
import ctypes
import threading

# Definir algunas constantes necesarias para la simulación de teclas
VK_CODE = {
    'd': 0x44,
    'f': 0x46,
    'j': 0x4A,
    'k': 0x4B,
}

# Función para enviar una pulsación de tecla
def key_down(key):
    ctypes.windll.user32.keybd_event(VK_CODE[key], 0, 0, 0)

# Función para liberar una tecla presionada
def key_up(key):
    ctypes.windll.user32.keybd_event(VK_CODE[key], 0, 2, 0)

# Función para simular una pulsación de tecla
def press_key(key, duration):
    key_down(key)
    time.sleep(duration)
    key_up(key)
    
def dibujarBotones(img, collision):
    # Dividir la línea en 4 rectángulos con un espacio en medio
    y_bottom = 370
    y_top = 470

    x_left = 100
    x_right = 150
    
    print(collision)
    print(collision[0])
    print(collision[1])
    print(collision[2])
    print(collision[3])
    
    timequedoy = 0.3

    # Dibujar el rectángulo con relleno verde si hay colisión, de lo contrario, azul
    if collision[0]:
        cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (0, 255, 0), -1)
        press_key('d', 0.1)
        threading.Thread(target=press_key, args=('d',timequedoy)).start()
    else:
        cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (255, 0, 0), -1)
    # Dibujar el contorno negro
    cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (0, 0, 0), 2)

    x_left = 172
    x_right = 220
    # Dibujar el rectángulo con relleno verde si hay colisión, de lo contrario, azul
    if collision[1]:
        cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (0, 255, 0), -1)
        threading.Thread(target=press_key, args=('f', timequedoy)).start()
    else:
        cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (255, 0, 0), -1)
    # Dibujar el contorno negro
    cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (0, 0, 0), 2)

    x_left = 316
    x_right = 366
    # Dibujar el rectángulo con relleno verde si hay colisión, de lo contrario, azul
    if collision[2]:
        cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (0, 255, 0), -1)
        threading.Thread(target=press_key, args=('j', timequedoy)).start()
        #keyboard_controller.press('j')
    else:
        cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (255, 0, 0), -1)
    # Dibujar el contorno negro
    cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (0, 0, 0), 2)

    x_left = 381
    x_right = 431
    # Dibujar el rectángulo con relleno verde si hay colisión, de lo contrario, azul
    if collision[3]:
        cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (0, 255, 0), -1)
        threading.Thread(target=press_key, args=('k', timequedoy)).start()
        #keyboard_controller.press('k')
    else:
        cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (255, 0, 0), -1)
    # Dibujar el contorno negro
    cv2.rectangle(img, (x_left, y_top), (x_right, y_bottom), (0, 0, 0), 2)

def obtenerCoordenadas(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenadas: ({x}, {y})")

def main():
    wCam, hCam = 600, 400

    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    while (cap.isOpened()):
        ret, img = cap.read()
        img = cv2.flip(img, 1)

        if ret:
            imghsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            blancobajo = np.array([0, 0, 200], np.uint8)
            blancoalto = np.array([180, 30, 255], np.uint8)
            mascara = cv2.inRange(imghsv, blancobajo, blancoalto)

            contornos, _ = cv2.findContours(mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Inicializar una lista para rastrear si un botón está siendo presionado o no
            boton_presionado = [False, False, False, False]

            for c in contornos:
                area = cv2.contourArea(c)
                if 900 < area < 2000:
                    (x, y), radius = cv2.minEnclosingCircle(c)
                    center = (int(x), int(y))
                    radius = int(radius)
                    cv2.circle(img, center, radius, (0, 255, 0), -1)

                    # Verificar colisión del círculo con los rectángulos
                    x_left = [100, 172, 316, 381]
                    x_right = [150, 220, 366, 431]
                    y_top = 370
                    y_bottom = 470

                    for i in range(4):
                        if x_left[i] < int(x) < x_right[i] and y_top < int(y + radius) < y_bottom:
                            boton_presionado[i] = True

            dibujarBotones(img, boton_presionado)

            cv2.imshow('Video de entrada', img)

            if cv2.waitKey(1) == ord('q'):
                break
        else:
            break
        
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    cv2.namedWindow('Video de entrada')
    #cv2.setMouseCallback('Video de entrada', obtenerCoordenadas)
    main()