1. Repository'i klonlayın:
```bash
git clone https://github.com/EmreHacihassan/Visual__Mouse.git
cd Visual_Mouse
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı başlatın:
```bash
python gui_main.py

bu proje fiziksel mouse yerine el hareketlerini mouse olarak kullanmanıza olanak tanır 

işaret parmağı ile baş parmağını birleştirmek sol tık 
orta parmak ile işaret parmağı birleştirmmek sol tıktır 

gui_main.py dosyasında projeyi çalıştırın 








# Visual Mouse - El Hareketleriyle Fare Kontrolü

## 🛠 Sürüm Gereksinimleri

Bu proje aşağıdaki spesifik sürümlerle test edilmiş ve çalıştığı doğrulanmıştır:

### Temel Gereksinimler
- Python 3.10
- Windows 10/11 (64-bit)

### Python Paketleri
```bash
mediapipe==0.10.5
protobuf==3.20.3
numpy==1.22.0
opencv-python==4.8.1.78
PyQt5==5.15.9
pyautogui==0.9.54
```

### Ek Bağımlılıklar
- Visual C++ Redistributable 2019 veya üzeri
- Çalışan bir webcam

## ⚠️ Önemli Notlar

1. **MediaPipe Sürümü**: 
   - 0.10.5 sürümü özellikle el takibi için optimize edilmiştir
   - DLL hatalarını önlemek için tam olarak bu sürümü kullanın

2. **NumPy Sürümü**:
   - 1.22.0 sürümü MediaPipe ile en uyumlu sürümdür
   - Daha yüksek sürümler uyumluluk sorunlarına yol açabilir

3. **Protobuf Sürümü**:
   - 3.20.3 sürümü MediaPipe ile uyumlu çalışmaktadır
   - Farklı sürümler DLL hatalarına neden olabilir

## 🔧 Kurulum Sırası

1. Visual C++ Redistributable yükleyin
2. Python 3.10 kurun
3. Paketleri tam olarak bu sırayla yükleyin:
```bash
pip install numpy==1.22.0
pip install protobuf==3.20.3
pip install mediapipe==0.10.5
pip install opencv-python==4.8.1.78
pip install PyQt5==5.15.9
pip install pyautogui==0.9.54
```

## 🐛 Bilinen Sürüm Sorunları ve Çözümleri

1. **MediaPipe DLL Hatası**:
   - Visual C++ Redistributable'ı yeniden yükleyin
   - Paketleri verilen sırayla yükleyin

2. **NumPy Uyumluluk Sorunu**:
   - Eğer farklı bir NumPy sürümü yüklüyse, önce kaldırın:
   ```bash
   pip uninstall numpy
   pip install numpy==1.22.0
   ```

3. **Protobuf Çakışması**:
   - Tüm protobuf sürümlerini kaldırın:
   ```bash
   pip uninstall protobuf
   pip install protobuf==3.20.3
   ```

Bu sürümler birbiriyle uyumlu çalışacak şekilde test edilmiştir. Farklı sürümler kullanmak beklenmedik sorunlara yol açabilir.
