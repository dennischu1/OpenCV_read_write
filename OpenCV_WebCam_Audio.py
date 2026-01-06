import numpy as np  # 引入 NumPy 庫，用於數值計算
import cv2  # 引入 OpenCV 庫，用於影像處理
import pyaudio  # 引入 PyAudio 庫，用於音頻錄製
import wave  # 引入 wave 庫，用於保存音頻檔案
import threading  # 引入 threading 庫，用於多線程處理
#from moviepy.editor import VideoFileClip, AudioFileClip  # 引入 moviepy，用於合併視訊和音頻
from moviepy import VideoFileClip, AudioFileClip
print(VideoFileClip)
print(AudioFileClip)


# 音頻錄製參數
CHUNK = 1024  # 音頻緩衝區大小
FORMAT = pyaudio.paInt16  # 音頻格式：16位整數
CHANNELS = 1  # 單聲道
RATE = 44100  # 採樣率：44.1kHz

# 全局變量用於控制錄製
audio_frames = []  # 存儲音頻數據
is_recording = True  # 錄製狀態標誌

# 音頻錄製函數（在獨立線程中運行）
def record_audio():
    global audio_frames, is_recording
    audio = pyaudio.PyAudio()  # 初始化 PyAudio
    
    # 打開音頻流
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
    
    print("開始錄製音頻...")
    audio_frames = []  # 重置音頻緩衝區
    
    # 錄製音頻循環
    while is_recording:
        data = stream.read(CHUNK)
        audio_frames.append(data)
    
    # 停止並關閉音頻流
    stream.stop_stream()
    stream.close()
    audio.terminate()
    print("音頻錄製完成")

cap = cv2.VideoCapture(0)  # 初始化攝影機，使用默認攝影機
width = 320                # 設定影片的寬度
height = 200               # 設定影片的高度
ftp = 12.0                 # 設定影片的幀率

# 設定影片編碼格式    # 如果系統為 Windows 
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 默認使用 XVID 編碼格式

# 檢查操作系統，並根據系統選擇不同的影片編碼格式和檔案擴展名
import platform
os = platform.system()
ext = '.avi'  # 預設擴展名為 .avi
if os == "Linux" or os == "Darwin":  # 如果系統為 Linux 或 Mac
    ext = '.mov'  # 使用 .mov 檔案格式
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 使用 MP4V 編碼格式

# 設定檔案名稱
video_filename = "test_video" + ext  # 臨時視頻檔案名稱
audio_filename = "test_audio.wav"  # 臨時音頻檔案名稱
final_filename = "test" + ext  # 最終合併後的檔案名稱
    
# 創建影片寫入物件
out = cv2.VideoWriter(video_filename, fourcc, ftp, (width, height))

# 啟動音頻錄製線程
audio_thread = threading.Thread(target=record_audio)
audio_thread.start()

print("開始錄製（按 'q' 或 ESC 鍵停止）...")

# 進入影像捕捉循環
while cap.isOpened():
    ret, frame = cap.read()  # 從攝影機捕獲一幀影像
    if frame is not None:          # 如果成功捕獲影像
        frame = cv2.resize(frame, (width, height))  # 調整影像大小
        out.write(frame)     # 將當前幀寫入影片檔案
        cv2.imshow('frame', frame)  # 顯示當前影像

    key = cv2.waitKey(int(1000/ftp))  # 設置延遲時間，根據幀率計算
    if key == 27 or key == ord("q"):  # 如果按下 "q" 鍵 or ESC
        is_recording = False  # 停止音頻錄製
        break  # 退出循環

cap.release()            # 釋放攝影機
out.release()            # 釋放影片寫入物件
cv2.destroyAllWindows()  # 關閉所有 OpenCV 視窗

# 等待音頻錄製線程完成
audio_thread.join()

# 保存音頻檔案
print("保存音頻檔案...")
audio_temp = pyaudio.PyAudio()
wf = wave.open(audio_filename, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(audio_temp.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(audio_frames))
wf.close()
audio_temp.terminate()

# 合併視頻和音頻
print("正在合併視頻和音頻...")
try:
    video = VideoFileClip(video_filename)
    audio = AudioFileClip(audio_filename)
    
    # 確保音頻和視頻長度一致
    # if audio.duration > video.duration:
    #     audio = audio.subclip(0, video.duration)  #AudioFileClip.subclip() 在moviepy 2.x已被移除 
    # elif video.duration > audio.duration:         #改成使用 with_duration() / with_start() / with_end()
    #     video = video.subclip(0, audio.duration)

    min_duration = min(video.duration, audio.duration)

    video = video.with_duration(min_duration)
    audio = audio.with_duration(min_duration)
    
    # 合併音頻到視頻
    #final_video = video.set_audio(audio)
    final_video = video.with_audio(audio)
    
    # 輸出最終檔案
    final_video.write_videofile(final_filename, codec='libx264', audio_codec='aac')
    
    # 清理臨時檔案
    video.close()
    audio.close()
    final_video.close()
    
    import os
    os.remove(video_filename)  # 刪除臨時視頻檔案
    os.remove(audio_filename)  # 刪除臨時音頻檔案
    
    print(f"完成！最終檔案已保存為: {final_filename}")
except Exception as e:
    print(f"合併時發生錯誤: {e}")
    print(f"視頻檔案已保存為: {video_filename}")
    print(f"音頻檔案已保存為: {audio_filename}")