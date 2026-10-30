import cv2 # 导入 OpenCV，用来读视频、存图片
import os # 导入 os，用来创建文件夹、拼接路径
"""

从一个视频中按间隔每10帧截取帧，并保存为图片。

"""
# 定义截帧函数
# video_path: 视频路径；output_dir: 图片保存目录
# interval: 每隔多少帧取一张；num_frames: 一共要保存几张图

def extract_video_frames(video_path,output_dir,interval=10,num_frames=5):
   
   os.makedirs(output_dir, exist_ok=True)  # 创建输出文件夹；exist_ok=True 表示已存在也不报错
   
   print(f"输出目录已创建 {output_dir}")  # 输出目录已创建
   
   cap = cv2.VideoCapture(video_path)     # 创建视频读取对象 cap（此时只是"打开"，还没读画面）

   if not cap.isOpened():        # 返回 True/False，打不开就提示并结束函数
      print("无法打开视频文件")    # 如果无法打开视频文件，打印错误信息并返回
      return 

   fps = cap.get(cv2.CAP_PROP_FPS)   # 获取视频帧率，仅用于显示信息

   total_frames= int((cap.get(cv2.CAP_PROP_FRAME_COUNT)))     # 获取视频总帧数
   
   print(f"该视频的帧率是{fps}，总帧数为 {total_frames}")    # 输出视频的帧率和总帧数

   frame_count = 0  # 位置计数器：当前读到第几帧，从 0 开始
   save_count = 0   # 进度计数器：已保存几张，从 0 开始

   while save_count < num_frames:    # 只要已保存数量 < 目标数量，就继续循环

      ret,frame  = cap.read()  #读下一帧：ret 表示是否成功，frame 是这一帧的画面

      if not ret :    # 读取失败说明视频结束了，提前退出循环
         
         print(f"视频读取完毕，一共读取了{save_count}帧")  
         
         break 

      if frame_count % interval == 0:  # 当前位置能被 interval 整除（0、10、20…）时才保存

         filename = os.path.join(output_dir,f"frame_{save_count:03d}.jpg")  # 拼出保存路径，如 images\frame_000.jpg（:03d 表示补零到3位）

         cv2.imwrite(filename,frame) #把这一帧画面写成图片文件
      
         print(f"已保存第{frame_count}帧， -> {filename}")  # 输出已保存帧数和文件名

         save_count +=1 # 已保存帧数加1
         
      else:
         print(f"跳过第{frame_count}帧")  # 输出已跳过帧数


      frame_count +=1  # 无论是否保存，位置都 +1（指向下一帧）

   cap.release()
   print(f"\n 截图完毕！共保存了{save_count}图片")  # 输出已保存的图片数


def main():

   video_path = "video.mp4"  # 视频文件路径（相对当前工作目录）
      
   output_dir = "images"    # 图片保存文件夹

   extract_video_frames(video_path,output_dir,interval=10,num_frames=5)  # 调用截帧函数，按间隔每10帧截取5张图片

      
# 程序主入口

if __name__ == "__main__":
   print ("=" * 60) #
   print ("=" * 60)
   main()  # 调用主函数
   print ("视频截帧程序执行完毕！")  
