import cv2
import os

def extract_video_frames(video_path,output_dir,interval=10,num_frames=5):

    os.makedirs(output_dir,exist_ok=True)

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        print("错误,暂时无法打开视频")
        
        return

    
    frame_count = 0 # 当前获取的帧
    saved_count = 0 # 已保存的图片数量


    while saved_count < num_frames:

        ret,frame = cap.read()

        if not ret:
           
           break

        if frame_count % interval == 0:

            filename = os.path.join(output_dir,f"{saved_count:03d}.jpg")

            cv2.imwrite(filename,frame)

            print(f"当前为第{frame_count}帧,当前已保存为{filename}")

            saved_count += 1

        else:

            print(f"当前为第{frame_count}帧，已跳过")
            
        frame_count += 1

    cap.release()
    
    print("截图完成")


if __name__ == "__main__":

    video_path = "video.mp4"

    output_dir = "images3"

    extract_video_frames(video_path,output_dir,interval=10,num_frames=5) 


