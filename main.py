# Bu kod main.py içindir
# filepath: g/main.py

import cv2
from config import (
    CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, SHOW_DEBUG
)
from hand_tracker import HandTracker
from mouse_controller import MouseController
from gestures import GestureController

def main():
    # Kamera başlat
    cap = cv2.VideoCapture(CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # Yardımcı sınıfları başlat
    hand_tracker = HandTracker()
    mouse_controller = MouseController()
    gesture_controller = GestureController(mouse_controller)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Kamera görüntüsü alınamadı.")
            break

        frame = cv2.flip(frame, 1)  # Aynalama (ayna efekti) burada yapılır

        # El tespiti ve işaretleme
        hand_landmarks = hand_tracker.process(frame)
        if hand_landmarks:
            gesture_controller.handle_gestures(hand_landmarks, frame)

        # Debug için el noktalarını göster
        if SHOW_DEBUG and hand_landmarks:
            hand_tracker.draw_landmarks(frame, hand_landmarks)

        cv2.imshow("El ile Fare Kontrolü", frame)
        if cv2.waitKey(1) & 0xFF == 27:  # ESC ile çık
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()