import cv2
import os

def extract_video_frames(video_path,output_dir,interval=10,num_frames=5):
    
    os.makedirs(output_dir,exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        
        print("错误,无法打开视频文件")
        
        return

    frame_count = 0 
    saved_count = 0

    while saved_count < num_frames:

        ret,frame =cap.read()

        if not ret:
            print(f"无法读取帧,当前仅截取了{save_count}张图片")
            break

        if frame_count % interval == 0:

            filename = os.path.join(output_dir,f"frame{saved_count:03d}.jpg")

            cv2.imwrite(filename,frame)

            print(f"当前第{frame_count}帧, 已保存为文件名{filename}")
            

            saved_count += 1
            
        else:
            
            print(f"跳过了第{frame_count}帧")

        frame_count += 1 

    cap.release()

print("完成全部截图")

video_path = "video.mp4"
output_dir = "images2"
extract_video_frames(video_path,output_dir,interval=10,num_frames=5)

