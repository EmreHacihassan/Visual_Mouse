import sys
import cv2
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QWidget, QSlider, QComboBox, QMessageBox, QGroupBox, QFormLayout, QSpacerItem, QSizePolicy, QFrame
)
from PyQt5.QtCore import Qt, QTimer, QDateTime
from PyQt5.QtGui import QImage, QPixmap

from config import CAMERA_INDEX, FRAME_WIDTH, FRAME_HEIGHT, SHOW_DEBUG, MOUSE_SMOOTHING
from hand_tracker import HandTracker
from mouse_controller import MouseController
from gestures import GestureController

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Mouse")
        self.setGeometry(100, 100, 1400, 900)
        # [Önceki styleSheet kodları aynen kalacak...]
        self.setStyleSheet("""
            QMainWindow { 
                background: #1e1e2e;
            }
            QLabel, QGroupBox, QComboBox { 
                color: #cdd6f4;
                font-family: 'Segoe UI', 'Arial', sans-serif;
            }
            QGroupBox {
                background: rgba(49, 50, 68, 0.6);
                border: 2px solid #45475a;
                border-radius: 15px;
                padding: 15px;
                font-size: 16px;
            }
            QPushButton {
                background: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background: #b4befe;
            }
            QPushButton:disabled {
                background: #45475a;
                color: #6c7086;
            }
            QComboBox {
                background: #313244;
                border: 1px solid #45475a;
                border-radius: 8px;
                padding: 8px;
                min-width: 150px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
            QSlider::groove:horizontal {
                background: #45475a;
                height: 8px;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #89b4fa;
                width: 18px;
                margin: -5px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #b4befe;
            }
        """)

        # Ana widget ve layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        # Üst bilgi barı
        top_bar = QFrame()
        top_bar.setStyleSheet("""
            QFrame {
                background: rgba(49, 50, 68, 0.6);
                border-radius: 15px;
                padding: 10px;
            }
        """)
        top_layout = QHBoxLayout()
        top_bar.setLayout(top_layout)

        self.fps_label = QLabel("FPS: -")
        self.fps_label.setStyleSheet("color: #89b4fa; font-size: 18px; font-weight: bold;")
        top_layout.addWidget(self.fps_label)

        self.gesture_label = QLabel("Gesture: -")
        self.gesture_label.setStyleSheet("color: #f5c2e7; font-size: 18px; font-weight: bold; margin-left: 20px;")
        top_layout.addWidget(self.gesture_label)

        self.status_label = QLabel("Durum: Hazır")
        self.status_label.setStyleSheet("color: #a6e3a1; font-size: 18px; font-weight: bold; margin-left: 20px;")
        top_layout.addWidget(self.status_label)

        top_layout.addStretch()
        self.main_layout.addWidget(top_bar)

        # Orta bölüm (kamera ve kontroller)
        middle_layout = QHBoxLayout()
        self.main_layout.addLayout(middle_layout)

        # Kamera görüntüsü
        self.video_label = QLabel()
        self.video_label.setFixedSize(1000, 650)
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("""
            background: #11111b;
            border: 2px solid #313244;
            border-radius: 20px;
        """)
        middle_layout.addWidget(self.video_label)

        # Alt panel (ayarlar ve butonlar)
        bottom_layout = QHBoxLayout()
        self.main_layout.addLayout(bottom_layout)

        # Ayarlar grubu
        settings_group = QGroupBox("Ayarlar")
        settings_layout = QFormLayout()
        settings_group.setLayout(settings_layout)

        # Kamera seçimi
        self.camera_box = QComboBox()
        self.camera_box.addItem("Kamera 0")
        settings_layout.addRow("Kamera:", self.camera_box)

        # Çözünürlük seçimi
        self.resolution_box = QComboBox()
        self.resolution_box.addItems(["640x480", "800x600", "1280x720", "1920x1080"])
        settings_layout.addRow("Çözünürlük:", self.resolution_box)

        # Smoothing ayarı
        self.smooth_slider = QSlider(Qt.Horizontal)
        self.smooth_slider.setMinimum(0)
        self.smooth_slider.setMaximum(100)
        self.smooth_slider.setValue(1)
        settings_layout.addRow("Smoothing:", self.smooth_slider)

        # Gesture hassasiyeti
        self.gesture_slider = QSlider(Qt.Horizontal)
        self.gesture_slider.setMinimum(1)
        self.gesture_slider.setMaximum(10)
        self.gesture_slider.setValue(5)
        settings_layout.addRow("Hassasiyet:", self.gesture_slider)

        bottom_layout.addWidget(settings_group)

        # Butonlar grubu
        button_group = QFrame()
        button_group.setStyleSheet("""
            QFrame {
                background: rgba(49, 50, 68, 0.6);
                border: 2px solid #45475a;
                border-radius: 15px;
                padding: 15px;
            }
        """)
        button_layout = QVBoxLayout()
        button_group.setLayout(button_layout)

        self.start_button = QPushButton("▶ Başlat")
        self.start_button.setStyleSheet("background: #a6e3a1;")
        button_layout.addWidget(self.start_button)

        self.stop_button = QPushButton("⏹ Durdur")
        self.stop_button.setStyleSheet("background: #f38ba8;")
        self.stop_button.setEnabled(False)
        button_layout.addWidget(self.stop_button)

        self.help_button = QPushButton("？ Yardım")
        self.help_button.setStyleSheet("background: #fab387;")
        button_layout.addWidget(self.help_button)

        self.exit_button = QPushButton("✕ Çıkış")
        self.exit_button.setStyleSheet("background: #f38ba8;")
        button_layout.addWidget(self.exit_button)

        bottom_layout.addWidget(button_group)

        # Çerçeve ayarları
        self.boundary_margin = 0.1  # %10'luk margin

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Event bağlantıları
        self.start_button.clicked.connect(self.start_system)
        self.stop_button.clicked.connect(self.stop_system)
        self.exit_button.clicked.connect(self.close)
        self.help_button.clicked.connect(self.show_help)

        self.running = False

        # FPS ölçüm değişkenleri
        self._frame_count = 0
        self._last_fps_time = QDateTime.currentDateTime()
        self._current_fps = 0

    def draw_boundary_box(self, frame):
        h, w = frame.shape[:2]
        margin_ratio = self.boundary_margin
        
        # Çerçeve koordinatlarını hesapla
        x1 = int(w * margin_ratio)
        y1 = int(h * margin_ratio)
        x2 = int(w * (1 - margin_ratio))
        y2 = int(h * (1 - margin_ratio))
        
        # Çerçeveyi çiz (yarı saydam yeşil)
        overlay = frame.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        
        return (x1, y1, x2, y2)

    def start_system(self):
        cam_index = self.camera_box.currentIndex()
        res_text = self.resolution_box.currentText()
        width, height = map(int, res_text.split("x"))
        self.cap = cv2.VideoCapture(cam_index)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        smoothing_value = self.smooth_slider.value() / 100
        if smoothing_value < 0.01:
            smoothing_value = 0
        self.hand_tracker = HandTracker()
        self.mouse_controller = MouseController(camera_width=width, camera_height=height, smoothing=smoothing_value)
        self.gesture_controller = GestureController(self.mouse_controller)
        self.running = True
        self.status_label.setText("Durum: Aktif")
        self.gesture_label.setText("Gesture: -")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.timer.start(10)

    def stop_system(self):
        self.running = False
        self.timer.stop()
        if hasattr(self, 'cap') and self.cap:
            self.cap.release()
        self.video_label.clear()
        self.status_label.setText("Durum: Durduruldu")
        self.gesture_label.setText("Gesture: -")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_frame(self):
        if not self.running or not hasattr(self, 'cap') or not self.cap:
            return
        ret, frame = self.cap.read()
        if not ret:
            self.status_label.setText("Kamera görüntüsü alınamadı")
            return

        frame = cv2.flip(frame, 1)
        # Sınır çerçevesini çiz ve koordinatlarını al
        boundary_box = self.draw_boundary_box(frame)
        
        hand_result = self.hand_tracker.process(frame)
        if hand_result and isinstance(hand_result, tuple) and len(hand_result) == 3:
            x, y, hand_landmarks = hand_result
            
            # Gesture kontrolü ve mouse hareketi
            self.gesture_controller.handle_gestures(hand_landmarks, frame)
            self.mouse_controller.move_mouse(x, y, boundary_box)
            if SHOW_DEBUG:
                self.hand_tracker.draw_landmarks(frame, hand_result)

            # Çerçeveye göre durumu güncelle
            if self.is_within_boundary(x, y, boundary_box):
                self.status_label.setText("Durum: Aktif (İç Alan)")
            else:
                self.status_label.setText("Durum: Aktif (Dış Alan)")

        gesture_info = getattr(self.gesture_controller, "last_gesture", None)
        if gesture_info:
            self.gesture_label.setText(f"Gesture: {gesture_info}")
        else:
            self.gesture_label.setText("Gesture: -")

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qt_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image).scaled(self.video_label.width(), self.video_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.video_label.setPixmap(pixmap)

        # FPS ölçümü
        self._frame_count += 1
        now = QDateTime.currentDateTime()
        elapsed = self._last_fps_time.msecsTo(now)
        if elapsed >= 1000:
            self._current_fps = self._frame_count * 1000 // elapsed
            self.fps_label.setText(f"FPS: {self._current_fps}")
            self._frame_count = 0
            self._last_fps_time = now

    def is_within_boundary(self, x, y, boundary_box):
        x1, y1, x2, y2 = boundary_box
        return x1 <= x <= x2 and y1 <= y <= y2

    def show_help(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Yardım ve Kullanım Kılavuzu")
        msg.setText(
            "1. '▶ Başlat' ile sistemi başlatın.\n"
            "2. Yeşil çerçeve içinde el hareketleriniz fare imlecini kontrol eder.\n"
            "3. El çerçeve dışına çıksa bile, en yakın çerçeve noktasına göre imleç hareket eder.\n"
            "4. Ayarlar panelinden smoothing, çözünürlük ve gesture hassasiyetini değiştirebilirsiniz.\n"
            "5. '⏹ Durdur' ile sistemi durdurabilir, '✕ Çıkış' ile programı kapatabilirsiniz."
        )
        msg.setIcon(QMessageBox.Information)
        msg.exec_()

    def closeEvent(self, event):
        self.stop_system()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())