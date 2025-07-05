import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self, max_num_hands=1, detection_confidence=0.4, tracking_confidence=0.4):
        self.max_num_hands = max_num_hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=self.max_num_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        # Özel çizim stilleri tanımla
        self.landmark_style = {
            'color': (255, 255, 255),  # Beyaz noktalar
            'thickness': 2,
            'circle_radius': 2,
        }
        self.connection_style = {
            'color': (180, 180, 255),  # Açık mor çizgiler
            'thickness': 1
        }

    def process(self, frame):
        """
        El tespiti yapar ve işaret parmağı ucu ile orta boğumu arasında bir noktayı mouse pozisyonu olarak döndürür.
        Menzili uzatmak için oranı 1.4 olarak ayarladık (daha hızlı köşe erişimi).
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            h, w, _ = frame.shape
            tip = hand_landmarks.landmark[8]  # İşaret parmağı ucu
            mid = hand_landmarks.landmark[6]  # İşaret parmağı orta boğum
            ratio = 1.4  # Menzili daha da uzatır
            x = int((mid.x + (tip.x - mid.x) * ratio) * w)
            y = int((mid.y + (tip.y - mid.y) * ratio) * h)
            return x, y, hand_landmarks
        return None

    def draw_landmarks(self, frame, hand_result):
        """
        El landmarkları ve işaret parmağı ucunda kırmızı nokta çizer,
        modern ve şık bir görünüm sağlar
        """
        if hand_result and len(hand_result) == 3:
            _, _, hand_landmarks = hand_result
            h, w, _ = frame.shape

            # Yarı saydam overlay oluştur
            overlay = frame.copy()
            
            # Bağlantıları çiz (el iskeleti)
            for connection in self.mp_hands.HAND_CONNECTIONS:
                start_idx = connection[0]
                end_idx = connection[1]
                
                start_point = hand_landmarks.landmark[start_idx]
                end_point = hand_landmarks.landmark[end_idx]
                
                start_x = int(start_point.x * w)
                start_y = int(start_point.y * h)
                end_x = int(end_point.x * w)
                end_y = int(end_point.y * h)
                
                cv2.line(overlay, (start_x, start_y), (end_x, end_y),
                        self.connection_style['color'],
                        self.connection_style['thickness'])

            # Overlay'i ana frame ile birleştir
            cv2.addWeighted(overlay, 0.7, frame, 0.3, 0, frame)

            # Landmark noktalarını çiz
            for idx, landmark in enumerate(hand_landmarks.landmark):
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                
                # İşaret parmağı ucu için özel stil
                if idx == 8:  # İşaret parmağı ucu
                    # Ana kırmızı nokta
                    cv2.circle(frame, (x, y), 8, (0, 0, 255), -1)
                    # Parlaklık efekti
                    cv2.circle(frame, (x, y), 4, (255, 255, 255), -1)
                else:
                    # Diğer noktalar için beyaz nokta
                    cv2.circle(frame, (x, y),
                             self.landmark_style['circle_radius'],
                             self.landmark_style['color'],
                             self.landmark_style['thickness'])

    def release(self):
        """
        Kaynakları serbest bırak
        """
        if hasattr(self, 'hands'):
            self.hands.close()