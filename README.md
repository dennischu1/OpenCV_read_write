## OpenCV Webcam 應用整合專案

這是一個基於 Python 與 OpenCV 的專案集錦，展示了從基本的攝影機錄影到進階的音訊同步、動態偵測及浮水印添加等多種實用功能。

🚀 功能特點
本倉庫包含四個核心腳本，分別對應不同的應用場景：

1. 音訊視訊同步錄製 (OpenCV\_WebCam\_Audio.py)

* 使用 threading 進行多執行緒處理，同時擷取影像與音訊。
* 整合 PyAudio 錄音與 MoviePy (2.x 版本) 進行後製合併。
* 自動處理音畫同步長度對齊。

2. 即時中文浮水印錄影 (OpenCV\_WebCam\_Watermark.py)

* 透過 PIL (Pillow) 解決 OpenCV 無法直接顯示中文字型的問題。
* 支援自定義字體 (.ttf) 與即時影像疊加。

3. 分段自動循環錄影 (OpenCV\_WebCam\_VideoRecording.py)

* 以時間戳記自動命名檔案。
* 設定固定時間間隔（如 100 秒）自動切割影片，適合長時間監控記錄。

4. 智慧防盜動態偵測錄影 (OpenCV\_WebCam\_MotionDetect.py)

* 動態演算法：計算相鄰幀的平均像素差異值。
* 觸發機制：當畫面變動超過閾值時，自動啟動 10 秒鐘的緊急錄影。
* 節省儲存空間，僅記錄關鍵畫面。

🛠️ 安裝環境
在執行腳本之前，請確保已安裝 Python 3.x 並執行以下指令安裝必要的函式庫：

Bash

pip install numpy opencv-python pyaudio moviepy Pillow
注意：

PyAudio 在某些系統上可能需要額外安裝 PortAudio 庫。

OpenCV\_WebCam\_Watermark.py 需要字體檔案（預設為 GenJyuuGothic-Light.ttf），請確保檔案路徑正確。

📂 檔案說明與使用

1. 影音同步錄製
   執行後會同時啟動麥克風與攝影機，按下 q 或 ESC 停止後，系統會自動將 test\_video.avi 與 test\_audio.wav 合併為最終檔案。
2. 中文浮水印
   此腳本展示了將 OpenCV 格式 (NumPy array) 轉換為 PIL 格式進行繪圖，再轉回 OpenCV 顯示的技術路徑。
3. 動態偵測
   這是一個簡易的「防盜系統」。當你不在電腦前且畫面發生移動時，它會記錄下當時的影像。你可以調整 變化閾值 來優化靈敏度。

💻 跨平台相容性
程式碼內建了作業系統判斷機制，會根據 Windows、Linux 或 macOS 自動切換影片編碼格式：

Windows: 使用 XVID 編碼 (.avi)

Linux / macOS: 使用 mp4v 編碼 (.mov)

📝 技術重點
影像處理：使用 cv2.resize 優化錄影效能。

多執行緒：解決 I/O 阻塞問題，確保錄音不卡頓。

MoviePy 2.x 更新：針對新版 moviepy 使用 with\_duration() 與 with\_audio() 替代舊版方法。

