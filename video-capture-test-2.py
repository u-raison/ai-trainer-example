import <1>
import os

def extract_frames(video_path, output_dir, interval=8, num_frame=6, start_frame=20):

    os.<2>(output_dir, <3>=True)

    print(f"当前已创建文件夹{output_dir}")

    cap = cv2.<4>(video_path)

    if not cap.<5>():
        print("视频无法正确打开")
        return

    fps = cap.<6>(cv2.CAP_PROP_FPS)
    total_frame = int(cap.get(cv2.<7>))
    print(f"当前视频的帧率为{fps}，视频一共有{total_frame}帧")

    frame_count = <8>
    saved_count = 0

    while saved_count < num_frame:

        ret, frame = cap.<9>()

        if not <10>:
            print(f"视频已结束或读取失败，仅截取了{saved_count}帧")
            break

        # 从 start_frame 开始，每隔 interval 帧保存一张
        if frame_count >= start_frame and (frame_count - start_frame) <11> interval == 0:

            filename = os.path.<12>(output_dir, f"{saved_count:<13>}.png")

            cv2.<14>(filename, frame)

            print(f"已保存第{frame_count}帧 -> 保存文件名为{filename}")

            saved_count += 1

        frame_count += 1

    cap.release()
    print("视频截帧已全部完成")


def main():
    extract_frames("video.mp4", "images4", interval=8, num_frame=6, start_frame=20)


if __name__ == "__main__":
    main()