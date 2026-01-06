import numpy as np         # 引入 NumPy 庫，用於數值計算
import cv2                 # 引入 OpenCV 庫，用於影像處理
from datetime import datetime  # 引入 datetime 模組，用於獲取當前時間

cap = cv2.VideoCapture(0)  # 初始化攝影機，使用默認攝影機
相差時間 = 100              # 設定每個影片檔案的時間間隔，以秒為單位
width = 320                # 設定影片的寬度
height = 200               # 設定影片的高度
ftp = 12.0                 # 設定影片的幀率

# 設定影片編碼格式
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 默認使用 XVID 編碼格式

# 檢查操作系統，並根據系統選擇不同的影片編碼格式和檔案擴展名
import platform
os = platform.system()
ext = '.avi'  # 預設擴展名為 .avi
if os == "Linux" or os == "Darwin":  # 如果系統為 Linux 或 Mac
    ext = '.mov'  # 使用 .mov 檔案格式
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 使用 MP4V 編碼格式


# 獲取當前日期和時間
now = datetime.now() 
# 格式化日期和時間為字串，用於影片檔名
dt_string = now.strftime("%Y%m%d%H%M%S")
print("date and time =", dt_string)  # 輸出格式化後的日期和時間 # 輸出當前時間
lastTiime = int(dt_string)           # 將當前時間轉換為整數，用於時間比較

# 創建影片寫入物件，使用當前時間作為檔名
out = cv2.VideoWriter(dt_string + ext, fourcc, ftp, (width, height))

# 進入影像捕捉循環
while cap.isOpened():
    ret, frame = cap.read()  # 從攝影機捕獲一幀影像
    if ret is True:          # 如果成功捕獲影像
        frame = cv2.resize(frame, (width, height))  # 調整影像大小
        out.write(frame)     # 將當前幀寫入影片檔案

        now = datetime.now()  # 獲取當前時間
        dt_string = now.strftime("%Y%m%d%H%M%S")  # 格式化當前時間
        currentTime = int(dt_string)  # 將格式化後的時間轉換為整數
        if currentTime > lastTiime + 相差時間:  # 如果當前時間超過上一個檔案時間 + 相差時間
            lastTiime = currentTime  # 更新 lastTiime
            out.release()            # 釋放當前影片寫入物件
            # 創建新影片寫入物件，以新時間作為檔名
            out = cv2.VideoWriter(dt_string + ext, fourcc, ftp, (width, height))

        cv2.imshow('frame', frame)  # 顯示當前影像
    else:
        break  # 如果無法捕獲影像，退出循環

    key = cv2.waitKey(int(1000/ftp))  # 設置延遲時間，根據幀率計算
    if  key==27 or key == ord("q"):               # 如果按下 "q" 鍵 or ESC
        break                         # 退出循環

# 釋放攝影機和影片寫入物件，關閉所有 OpenCV 視窗
cap.release()            # 釋放攝影機
out.release()            # 釋放影片寫入物件
cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗