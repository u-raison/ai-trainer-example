import cv2
import inspect
print(inspect.getmembers(cv2, inspect.isfunction))   # 只列函数（C 扩展可能不全）
print(cv2.__file__)                                  # 找到包所在位置，可去 .pyi 里搜

# import os
# import cv2
# help(os.makedirs)                                         # 查参数
# cap = cv2.VideoCapture("video.mp4")                        # 创建视频读取对象
# print(type(cap.read()), len(cap.read())) 

inspect.getdoc(cv2)