# Bu kod config.py içindir
# filepath: görüntü/config.py

# Kamera ve uygulama ayarları
CAMERA_INDEX = 0  # Varsayılan kamera
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# El algılama ayarları
MAX_NUM_HANDS = 1
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.6

# Mouse kontrol hassasiyeti
MOUSE_SMOOTHING = 0.2  # 0-1 arası, düşük değer daha yumuşak hareket

# Ekran çözünürlüğü (PyAutoGUI ile otomatik alınabilir, burada sabitlenebilir)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Hareket eşik değerleri
CLICK_THRESHOLD = 0.04  # Parmaklar arası mesafe oranı (tıklama için)
SCROLL_SENSITIVITY = 2  # Kaydırma hızı

# Diğer ayarlar
SHOW_DEBUG = True  # Debug pencerelerini göster