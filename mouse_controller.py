import pyautogui

class MouseController:
    def __init__(self, camera_width=640, camera_height=480, smoothing=0.01):
        self.screen_width, self.screen_height = pyautogui.size()
        self.camera_width = camera_width
        self.camera_height = camera_height
        self.smoothing = smoothing
        self.prev_x = None
        self.prev_y = None

    def update_camera_resolution(self, width, height):
        self.camera_width = width
        self.camera_height = height

    def clamp_to_boundary(self, x, y, boundary_box):
        x1, y1, x2, y2 = boundary_box
        
        # Eğer el çerçeve dışına çıkarsa, en yakın çerçeve noktasına kısıtla
        clamped_x = max(x1, min(x2, x))
        clamped_y = max(y1, min(y2, y))
        
        # Çerçeve içindeki pozisyonu 0-1 aralığına normalize et
        norm_x = (clamped_x - x1) / (x2 - x1)
        norm_y = (clamped_y - y1) / (y2 - y1)
        
        return norm_x, norm_y

    def move_mouse(self, x, y, boundary_box):
        # El pozisyonunu çerçeveye göre normalize et
        norm_x, norm_y = self.clamp_to_boundary(x, y, boundary_box)
        
        # Normalize edilmiş koordinatları ekran koordinatlarına çevir
        screen_x = int(norm_x * self.screen_width)
        screen_y = int(norm_y * self.screen_height)
        
        # Ekran sınırları içinde tut
        screen_x = max(0, min(self.screen_width - 1, screen_x))
        screen_y = max(0, min(self.screen_height - 1, screen_y))
        
        # Smoothing (yumuşatma) uygula
        if self.smoothing > 0 and self.prev_x is not None and self.prev_y is not None:
            # Mevcut ve hedef pozisyon arasında yumuşak geçiş
            screen_x = int(self.prev_x + (screen_x - self.prev_x) * self.smoothing)
            screen_y = int(self.prev_y + (screen_y - self.prev_y) * self.smoothing)
        
        # Mouse'u hareket ettir
        pyautogui.moveTo(screen_x, screen_y)
        
        # Önceki pozisyonu kaydet
        self.prev_x = screen_x
        self.prev_y = screen_y