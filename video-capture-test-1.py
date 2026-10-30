import cv2   # 导入 OpenCV，用来读视频、存图片
import os    # 导入 os，用来创建文件夹、拼接路径

def extract_video_frames(video_path, output_dir, interval=10, num_frames=5):

    os.makedirs(output_dir,exist_ok=True )   # 创建输出文件夹；已存在也不报错

    print(f"输出目录已创建 {output_dir}")

    cap = cv2.VideoCapture(video_path)   # 创建视频读取对象

    if not cap.isOpened():           # 返回 True/False，打不开就提示并结束函数
      
        print("无法打开视频文件")
       
        return

    fps = cap.get(cv2.CAP_PROP_FPS)      # 获取视频帧率

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))   # 获取视频总帧数

    print(f"该视频的帧率是{fps}，总帧数为 {total_frames}")
    

    frame_count = 0   # 位置计数器：当前读到第几帧
    save_count = 0    # 进度计数器：已保存几张

    while save_count < num_frames:

        ret, frame = cap.read()    # 读下一帧：ret 是否成功，frame 是画面

        if not ret:
            print(f"视频读取完毕，一共读取了{save_count}帧")
            break

        if frame_count % interval == 0:   # 当前位置能被 interval 整除时才保存

            filename = os.path.join(output_dir, f"frame_{save_count:03d}.jpg")   # 拼接保存路径

            cv2.imwrite(filename, frame)   # 把这一帧画面写成图片文件

            print(f"已保存第{frame_count}帧， -> {filename}")

            save_count += 1

        else:
            print(f"跳过第{frame_count}帧")

        frame_count += 1

    cap.release()
    print(f"\n 截图完毕！共保存了{save_count}图片")


def main():
    video_path = "video.mp4"
    output_dir = "images"
    extract_video_frames(video_path, output_dir, interval=10, num_frames=5)


if __name__ == "__main__":
    print("=" * 60)
    print("=" * 60)
    main()
    print("视频截帧程序执行完毕！")