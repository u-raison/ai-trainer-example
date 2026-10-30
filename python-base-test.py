import os
import shutil
from pathlib import Path
set = {1,2,3}

num1=10
num2=3

result = num1//num2
result2= num1**num2
print(result,result2)

list1=[1,2,3]
print(list1[2])
list1.append(4)
print(list1)
list1.remove(4)
print(list1)

def add(a,b):

    return a+b

# 获得当前路径
now_path = (os.getcwd())
print(now_path)

#列出所有文件夹及文件
file_list=os.listdir()
print(file_list)

print(os.path.basename(now_path))

name,ext = os.path.splitext('config.conf')
print(name,ext)


print(Path.cwd())
p = Path(r"C:\\Users\\LIURS\\Desktop\\ai-train\\images5\\Dalian.jpg")
print(p)
print(p.name)
print(p.stem)
print(p.suffix)
print(p.parent)
print(p.parents)
print(p.exists())
print(p.is_file())
print(p.is_dir())
print(p.is_absolute())

shutil.copy("1.png","copy1.png")
shutil.copy2("1.png","copy2.png")
shutil.move("copy.png",r"images5")
#shutil.copy("./images","./images6")