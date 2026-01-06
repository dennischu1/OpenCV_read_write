import numpy as np  # 引入 NumPy 庫，用於數值計算
import cv2  # 引入 OpenCV 庫，用於影像處理       
from PIL import ImageFont, ImageDraw, Image  # 從 PIL 中引入字體、繪圖、圖像模組

fontpath = "GenJyuuGothic-Light.ttf"  # 指定字體文件的路徑，這裡使用的是 GenJyuuGothic-Light 字體
font = ImageFont.truetype(fontpath, 32)  # 設定字體及大小為 32

# 初始化攝影機
cap = cv2.VideoCapture(0)

# 設定影像的寬度、高度及幀率（fps）
width = 640
height = 480
fps = 12.0

# 設定儲存影片的檔名及編碼格式 內定適用 windows
filename = "watermark.avi"
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 編碼格式（Windows）

# 檢查作業系統類型，針對不同系統使用不同的影片編碼格式
import platform
os = platform.system()
print(os)
if os == "Linux" or os == "Darwin":  # 如果是 Linux 或 Mac 系統
    filename = "watermark.mov"  # 使用 .mov 檔案格式
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 使用 MP4V 編碼格式（小寫）

# 初始化影片寫入物件，設定儲存的影片參數
out = cv2.VideoWriter(filename, fourcc, fps, (width, height))

# 開始捕捉影片
while cap.isOpened():
    ret, frame = cap.read()  # 從攝影機捕獲一幀影像
    if ret is True:          # 如果成功捕獲影像
        frame = cv2.resize(frame, (width, height))  # 調整影像大小為指定的寬度和高度
        # 加上浮水印
        img=frame
        img_pil = Image.fromarray(img)  # 將 NumPy 圖像轉換為 PIL 圖像
        draw = ImageDraw.Draw(img_pil)  # 創建繪圖對象
        # 繪製中文 "OpenCV練習" 到圖像上，使用綠色填充文字
        draw.text((10, 10), "OpenCV練習", font=font, fill=(125, 125,125))
        img = np.array(img_pil)  # 將 PIL 圖像轉換回 NumPy 陣列
        frame=img

        
        out.write(frame)     # 將當前幀寫入影片檔案
        cv2.imshow('frame', frame)  # 顯示當前幀
    else:
        break  # 如果捕獲影像失敗，退出循環

    key = cv2.waitKey(int(1000/fps))  # 根據 fps 設定延遲，以每秒顯示幀數控制播放速度
    if key == 27:  # 如果按下 ESC 鍵
        break  # 退出循環

# 釋放攝影機及影片寫入物件，並關閉所有 OpenCV 的視窗
cap.release()
out.release()         # 關閉 影片寫入 
cv2.destroyAllWindows()
