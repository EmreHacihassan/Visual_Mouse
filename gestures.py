import pyautogui
import math
import time

class GestureController:
    def __init__(self, mouse_controller):
        self.mouse_controller = mouse_controller
        self.last_gesture = None
        self.left_down = False
        self.right_down = False
        self.dragging = False
        self.last_click_time = 0

    def distance(self, lm1, lm2):
        return math.hypot(lm1.x - lm2.x, lm1.y - lm2.y)

    def handle_gestures(self, hand_landmarks, frame):
        thumb_tip = hand_landmarks.landmark[4]
        index_tip = hand_landmarks.landmark[8]
        middle_tip = hand_landmarks.landmark[12]

        # Sol tıklama (tek tık)
        if self.distance(thumb_tip, index_tip) < 0.05:
            if not self.left_down:
                now = time.time()
                # Çift tıklama kontrolü
                if now - self.last_click_time < 0.4:
                    pyautogui.doubleClick()
                    self.last_gesture = "Çift Tık"
                else:
                    pyautogui.mouseDown(button='left')
                    self.left_down = True
                    self.last_gesture = "Sol Tık (Basılı)"
                self.last_click_time = now
        else:
            if self.left_down:
                pyautogui.mouseUp(button='left')
                self.left_down = False

        # Sağ tıklama
        if self.distance(thumb_tip, middle_tip) < 0.05:
            if not self.right_down:
                pyautogui.mouseDown(button='right')
                self.right_down = True
                self.last_gesture = "Sağ Tık (Basılı)"
        else:
            if self.right_down:
                pyautogui.mouseUp(button='right')
                self.right_down = False

        # Drag (sürükle-bırak): işaret parmağı ve baş parmak uzun süre yakınsa
        if self.distance(thumb_tip, index_tip) < 0.05:
            if not self.dragging:
                pyautogui.mouseDown()
                self.dragging = True
                self.last_gesture = "Sürükle Başladı"
        else:
            if self.dragging:
                pyautogui.mouseUp()
                self.dragging = False
                self.last_gesture = "Sürükle Bitti"

        # Scroll: baş parmak ve orta parmak yakınsa, el yukarı/aşağı hareket ediyorsa
        # (Burada y koordinatındaki değişime bakabilirsiniz, örnek için basit bir mantık)
        # İleri düzey scroll için bir önceki y değerini saklayıp farkı kullanabilirsiniz.

        # Eğer başka gesture yoksa
        if not self.left_down and not self.right_down and not self.dragging:
            self.last_gesture = "Takip: Parmağı izliyor"