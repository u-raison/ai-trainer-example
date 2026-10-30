import cv2
import os

def extract_frames(video_path,output_dir,interval=8,num_frame=6):

    os.makedirs(output_dir,exist_ok=True)

    print(f"当前已创建文件夹{output_dir}")

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():

        print("视频无法正确打开")

        return 


    fps = cap.get(cv2.CAP_PROP_FPS)

    total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    print(f"当前视频的帧率为{fps},视频一共有{total_frame}帧")

    frame_count = 0

    saved_count = 0 


    while saved_count < num_frame :

        ret,frame  = cap.read()

        if not ret :

            print("视频已结束或读取失败，仅截取了{saved_count}帧")

            break

        if frame_count % interval == 0:

            filename = os.path.join(output_dir,f"{saved_count:3d}.jpg")

            cv2.imwrite(filename,frame)

            print(f"已保存第{frame_count}帧 -> 保存文件名为{filename}")

            saved_count +=1

        frame_count +=1

    cap.release()

    print("视频截帧已全部完成")


def main():

    video_file = "video.mp4"

    output_folder = "images4"

    extract_frames(video_file,output_folder,interval=8,num_frame=6)


if __name__ == "__main__":

    print("=" * 60)

    print("视频截帧程序")

    print("=" * 60)

    main()