import numpy as np         # 引入 NumPy 庫，用於數值計算
import cv2                 # 引入 OpenCV 庫，用於影像處理
from datetime import datetime  # 引入 datetime 模組，用於獲取當前時間
import time                # 引入 time 模組，用於精確的時間計算

"""
防盜錄影系統
功能：監控畫面變化，當偵測到大幅度的畫面變化時，自動錄影10秒鐘
"""

# 初始化攝影機，使用默認攝影機（0 代表第一個攝影機）
cap = cv2.VideoCapture(0)

# 錄影參數設定
錄影持續時間 = 10          # 當畫面有變化時，錄影持續時間（秒）
width = 320                # 設定影片的寬度
height = 200               # 設定影片的高度
fps = 12.0                 # 設定影片的幀率（每秒幀數）

# 設定影片編碼格式
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 默認使用 XVID 編碼格式

# 檢查操作系統，並根據系統選擇不同的影片編碼格式和檔案擴展名
import platform
os = platform.system()
ext = '.avi'  # 預設擴展名為 .avi
if os == "Linux" or os == "Darwin":  # 如果系統為 Linux 或 Mac
    ext = '.mov'  # 使用 .mov 檔案格式
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 使用 MP4V 編碼格式


# 畫面變化偵測參數
lastAveImageDiff = 0       # 上一幀畫面的平均像素值，用於比較畫面變化
變化閾值 = 20              # 畫面變化閾值，超過此值才觸發錄影 0~255

# 錄影狀態控制
recording = False          # 當前是否正在錄影
錄影開始時間 = None        # 錄影開始的時間戳記
out = None                 # 影片寫入物件，初始化為 None

print("防盜錄影系統啟動中...")
print(f"錄影參數：寬度={width}, 高度={height}, 幀率={fps}, 錄影持續時間={錄影持續時間}秒")
print(f"畫面變化閾值：{變化閾值}")
print("按 'q' 或 'ESC' 鍵可退出程式\n")

# 進入影像捕捉循環
while cap.isOpened():
    ret, frame = cap.read()  # 從攝影機捕獲一幀影像
    if ret is True:          # 如果成功捕獲影像 
        frame = cv2.resize(frame, (width, height))  # 調整影像大小至指定尺寸

        # 計算當前畫面的平均像素值，用於偵測畫面變化
        # 將所有像素值相加，再除以像素總數，得到平均像素強度
        imageTotal = frame.sum()                    # 計算所有像素值的總和
        aveImageDiff = imageTotal / frame.size      # 計算平均像素值

        # 如果當前沒有在錄影，則檢查畫面是否有大幅度變化
        if recording == False:
            # 計算當前畫面與上一幀畫面的差異
            畫面差異 = abs(aveImageDiff - lastAveImageDiff)
            
            # 顯示當前畫面差異值（用於調試）
            print(f"畫面差異: {畫面差異:.2f} (閾值: {變化閾值})")
            
            # 如果畫面差異超過閾值，表示有大變化，開始錄影
            if 畫面差異 > 變化閾值:
                print(f"偵測到畫面大幅度變化！差異值: {畫面差異:.2f}，開始錄影...")
                
                # 更新上一幀的平均值
                lastAveImageDiff = aveImageDiff
                
                # 獲取當前時間，用於檔案命名
                now = datetime.now()
                dt_string = now.strftime("%Y%m%d%H%M%S")
                
                # 如果之前有影片寫入物件，先釋放它
                if out is not None:
                    out.release()
                
                # 創建新的影片寫入物件，以時間戳記作為檔名
                out = cv2.VideoWriter(dt_string + ext, fourcc, fps, (width, height))
                
                # 記錄錄影開始時間（使用 time.time() 獲取精確的時間戳）
                錄影開始時間 = time.time()
                
                # 設定錄影狀態為 True
                recording = True
                print(f"錄影檔案：{dt_string + ext}")
        else:
            # 如果正在錄影，更新上一幀的平均值（繼續追蹤畫面變化）
            lastAveImageDiff = aveImageDiff

        # 如果正在錄影，將當前幀寫入影片檔案
        if recording == True:
            out.write(frame)
            
            # 檢查錄影是否已超過指定持續時間（10秒）
            if time.time() - 錄影開始時間 >= 錄影持續時間:
                print(f"錄影已持續 {錄影持續時間} 秒，停止錄影")
                recording = False  # 停止錄影
                # 注意：out 物件在此不釋放，因為可能會再次錄影
                # 當下次開始錄影時會自動釋放並創建新的

        cv2.imshow('frame', frame)  # 顯示當前影像
    else:
        break  # 如果無法捕獲影像，退出循環

    # 等待按鍵輸入，計算等待時間以維持設定的幀率
    key = cv2.waitKey(int(1000/fps))  # 設置延遲時間，根據幀率計算
    if key == 27 or key == ord("q"):  # 如果按下 "q" 鍵 or ESC (27)
        print("\n程式結束")
        break                         # 退出循環

# 釋放資源
cap.release()            # 釋放攝影機資源
if out is not None:
    out.release()        # 釋放影片寫入物件
cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗
print("所有資源已釋放，程式結束")