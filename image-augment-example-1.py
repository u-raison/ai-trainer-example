import cv2 
import numpy as np
#导入随机数模块
import random
#从pathlib模块中导入Patch类
import os
from pathlib import Path

#定义图片增强函数
def augment_image(img):

    """
    对【单张图片】做随机增强(只在内存里处理,不读写文件)

    参数:
        img: 已经用 cv2.imread 读好的图片(numpy 数组, 形状 高×宽×通道)
    返回:
        增强后的新图片(numpy 数组)

    处理顺序:
        1. 随机水平翻转   cv2.flip            按概率触发
        2. 随机旋转±15°   getRotationMatrix2D + warpAffine   每次都做
        3. 亮度/对比度    convertScaleAbs     每次都做
        4. 高斯噪声       np.random.normal + cv2.add   按概率触发

    考点: 组合多种增强方法,随机应用
    """

    # random.uniform(a, b) 的主要作用是在指定的两个数之间，随机生成一个经过均匀分布（Uniform Distribution）的浮点数
    # 1.生成一个0~1的随机数，如果随机数大于0.5就水平翻转（50%概率）
    if random.random()>0.9:
        
        # 用于对图像进行翻转（镜像）的函数
        #使用cv2.flip对图片水平翻转，img是要翻转的图片，1表示水平翻转，0表示垂直翻转，-1表示水平和垂直同时翻转
        img=cv2.flip(img,1)

    #随机旋转[-15°，15°],通过random.uniform随机生成-15到15之间的浮点数
    angle = random.uniform(-15,15)
    
    # img.shape 是一个用于获取图像形状和维度属性的元组（tuple）
    # 获取图片的高度和宽度，返回3个参数，img.shape[0]是高度，img.shape[1]是宽度，img.shape[2]是通道数
    h,w = img.shape[:2]
    
    
    #计算图片的中心点，并存在变量中.//是整除,结果是整数。通过宽、高整除2，获得中心点坐标位置
    center = (w// 2,h//2)
    
    # # cv2.getRotationMatrix2D() 函数的作用是计算图像绕指定点旋转和缩放的仿射变换矩阵（2×3 矩阵）
    # 创建旋转矩阵，以中心点center为旋转中心，angle是旋转角度，正数是逆时针，负数是顺时针，缩放比例，1.0 不缩放，0.5 缩小一半，2.0 放大一倍
    M = cv2.getRotationMatrix2D(center,angle,1.0)

    # 执行仿射变换;cv2.warpAffine() 的主要作用是对图像进行仿射变换（Affine Transformation）
    # 仿射变换是指在几何与图像处理中，对图像进行“线性变换”（如旋转、缩放、剪切/错切、反射）与“平移”的组合操作
    img = cv2.warpAffine(
        img,M,(w,h), # 传入图片img,矩阵M，宽和高，注意别反了
        flags = cv2.INTER_LINEAR, # 指定插值方式
        borderMode =cv2.BORDER_REFLECT #指定边界填充方式
    )
    
    
    # 3.亮度/对比度调整

    # 通过ramdom.uniform随机生成0.2~1.2的浮点数作为对比度系数，并存在变量alpha中,
    alpha = random.uniform(0.8,1.9)

    # 通过ramdom.uniform随机生成-30~30的浮点数作为
    beta = random.uniform(-30,20)

    # cv2.convertScaleAbs() 函数主要作用是对数组（图像）的每个元素依次执行：缩放（Scale）、取绝对值（Absolute）、转换成无符号 8 位类型（uint8，数值范围 0 ~ 255）
    # 通过cv2.convertScaleAbs调整图片的亮度和对比度,alpha是对比度，beta是亮度
    img = cv2.convertScaleAbs(img,alpha=alpha,beta=beta)

    # 4.（考点）生成随机数，大于0.7就添加高斯早上（30%概率）
    if random.random() >0.2:
        
        # np.random.nomal 用来从正态分布（也叫高斯分布或“钟形曲线”）中抽取随机数
        # 生成高斯噪声，第一个参数是均值，数据围绕哪个数波动；第二个参数是标准差，波动幅度，越大噪声越强；第三个是生成的数据形状
        # img.shape返回3个数，这里代入就是生成与图片同形状的浮点噪声（正负都有）
        # astype(np.uint8)是转换为无符号 8 位整数
        noise = np.random.normal(0,10,img.shape).astype(np.uint8)

        # 把高斯噪声添加到图片上；cv2.add用来叠加图片、调亮度、加噪声
        img =cv2.add(img,noise)

    return img



# 定义批量随机增强函数,传入输入目录、输出目录、增强比率为0.3，种子为42
def random_augment_images(input_dir,output_dir,aug_ratio=0.3, seed=42):

    """
    【批量】从图库随机抽取一部分图片,增强后保存到输出目录
    (本函数负责文件和流程,像素处理交给 augment_image 完成)

    参数:
        input_dir:  输入图片目录(会递归查找子文件夹)
        output_dir: 输出目录(不存在会自动创建)
        aug_ratio:  抽取比例, 如 0.3 表示抽 30% 的图片
        seed:       随机种子, 相同种子结果可复现
    返回:
        无(结果保存为 原名_aug_序号.后缀 的图片文件)

    流程:
        1. 设置随机种子         random.seed / np.random.seed
        2. 创建输出目录         Path.mkdir
        3. 遍历找出所有图片     os.walk + endswith(后缀元组)
        4. 随机抽样             random.sample(不重复)
        5. 逐张处理: 读取(imread) → 增强(augment_image) → 命名 → 保存(imwrite)
        6. 打印成功数量

    考试重点:
        1. 随机抽样 random.sample()
        2. 文件名处理 os.path.relpath / splitext / replace
        3. 支持多种图片格式
    """

    # 输出提示
    print("=" * 70)
    print("图像数据增强程序")
    print("=" * 70)

    # 步骤1： 设置 Python random 模块的随机种子,让 random.random/uniform/sample 的结果每次运行都一样(可复现)
    random.seed(seed)
    # 设置 numpy 的随机种子,让 np.random.normal(高斯噪声)的结果每次运行也一样
    np.random.seed(seed)

    # 步骤2： 创建输出目录（文件夹）
    Path(output_dir).mkdir(parents=True,exist_ok=True)

    # 输出提示
    print(f"输出目录{output_dir}")

    # 步骤3：获取所有图片文件,存所有支持的图片后缀名
    img_extensions = ('.jpg','.jpeg','.png','.bmp','.tiff')

    # 声明一个所有文件的空列表
    all_files=[]

    # 遍历输入文件夹，root表示当前遍历的文件夹路径，_表示当前文件夹下的子文件夹列表，files表示当前文件夹的文件列表
    # os.walk() 是 Python 中用于递归遍历文件夹（目录树）的内置方法
    for root,_,files in os.walk(input_dir):
        
        #调试语句，打印所有目录 
        #print(root)
        
        # 遍历当前文件夹下的每一个文件名
        for f in files:
            
            # 将文件名转换为小写，匹配文件名是否以img_extensions结尾的
            if f.lower().endswith(img_extensions):
                
                # 调试语句
                #print( f"{if}是图片文件")
                
                # 把图片的完整路径加入到列表中,join是把路径+文件名 拼接起来，这里的路径是相对路径
                all_files.append(os.path.join(root,f))
                
                # 调试语句，打印所有文件
                # print(all_files)

    # 判断是否没有找到任何图片，all_files[]为空是False，not False 则为True
    if not all_files:

        # 输出提示：
        print("错误: 未找到任何图片文件!")
        
        # 结束本函数
        return
    
    # 打印提示，通过len来查看列表的数量
    print(f"图库中共有{len(all_files)}张图片")


    # 步骤4，随机抽取指定比例
    # 计算需要增强的图片数量，用图片总数量乘以 设置的比例 aug_ratio=3，并转换为数值类型
    
    num_to_aug = int(len(all_files) * aug_ratio)
    print(num_to_aug)

    # 判断计算出的增强数量是否为0
    if num_to_aug == 0:
        
        # 保障至少有1张图片，使用min函数，在len(all_files)和1 两个数中，取最小的值为1
        num_to_aug = min(1,len(all_files))

    # random.sample() 的主要作用是从指定的序列或集合中随机抽取指定数量的不重复元素，并以列表（List）形式返回
    # 从所有图片里随机抽出 num_to_aug 张,存成列表
    selected_files = random.sample(all_files,num_to_aug)
    
    # 输出提示：抽取了num_to_aug张，aug_ratio * 100:.1f} 表示将比例乘以100后拼接“%”转换为百分比，保留1位小数点
    print(f"随机抽取{num_to_aug}张 ({aug_ratio * 100:.1f}%) 进行增强")
    print("=" * 70)
    

    # 步骤5，对每张图片进行增强

    # 声明遍历存成功处理的张数
    success_count = 0

    # 遍历所有被抽中的图片，idx默认返回索引号，这里指的是第几张图片，img_path是遍历selected_files列表中的数据，返回已选择的图片路径
    for idx,img_path in enumerate(selected_files,1):
        
        print(f"idx = {idx},im_path={img_path}")
        # 捕获异常
        try:

            # 读取图片
            img = cv2.imread(img_path)

            # 判断图片是否读取失败，如果img的值是None
            if img is None:

                # 打印提示，{idx}/{num_to_aug}表示总数的第几张是无效的，比如 5 / 10 ，10张中的第5张无效
                print(f"[{idx}/{num_to_aug}] 跳过无效图片：{img_path}")

                # 跳过本次循环，继续下一次循环
                continue

                # 调用单张图片增强函数，对当前图片进行随机增强，并将结果保存到遍历aug_img中        
            aug_img = augment_image(img)     
            
            # os.path.relpath求"路径img_path"相对于"起点目录input_dir"的相对路径,即把前面共同的目录去掉，这里返回最终是图片名称，如4.jpg            
            rel_path = os.path.relpath(img_path,input_dir)
            
            #print(f"rel_path : {rel_path}")

            # 图片处理后的新文件名：stem返回不带后缀的文件名
            # os.path.splitext将文件路径或文件名分割成“根目录/文件名（root）”与“扩展名（ext）”两部分，
            # 它返回一个元组(两个元素),第 1 个是点之前的部分,第 2 个是点和后缀。传入：'4.jpg'，返回('4', '.jpg')，'cat\\1.png'返回'cat\\1'
            # os.sep是当前系统的路径分隔符，Windows是\，通过os.path.splitext(rel_path)[0]获取第一个元素，例如：“4”，“cat\\1”，
            # 通过replace将当前系统路径分隔符替换为下划线，例如：cat\\1 替换后是cat_1
            stem = os.path.splitext(rel_path)[0].replace(os.sep,'_')

            # 以下是调试语句
            # print(os.path.splitext(rel_path))
            # print(os.path.splitext(rel_path)[0])
            # print(f"stem :{stem}")

            # ext是获取原图片img_path的扩展名 赋值给ext
            ext = os.path.splitext(img_path)[1]

            # 新文件名 = 上述得到的 stem + _aug_ + 序号（补零到 4 位）+ 后缀
            new_name = f"{stem}_aug_{idx:04d}{ext}"

            # 保存路径通过join拼接 = 输出目录 + 新文件名
            save_path = os.path.join(output_dir,new_name)
            
            # 调试语句
            #print(f"save_path is {save_path}")

            # 保存图片
            cv2.imwrite(save_path,aug_img) 

            # 调试语句
            # print(f"svae_path is {save_path}, aug_img is {aug_img}" )

            # 输出提示
            # os.path.basename从一个完整的路径字符串中，提取出最后一部分的文件名或目录（文件夹）名
            print(f"[{idx}/{num_to_aug}] {os.path.basename(img_path)} - >{new_name} ")

            # save_count 自增1
            success_count += 1
        
        # 捕获异常
        except Exception as e:

            # 打印信息
            print(f"[{idx} / {num_to_aug}] 处理失败 {img_path}")
            print(f"错误信息:{e}")

    # 步骤6:输出统计信息
    print("=" * 70)
    print(f"增强完成!成功处理{success_count} / {num_to_aug} 张图片")
    print(f"增强图片已保存至: {output_dir}")
    print("=" * 70)
    

# 定义演示各种增强方法的函数
def demo_augmentation_methods():

    """
    演示 7 种单独的增强方法(讲解用)

    做的事:
        在内存里造一张 200×300 的浅灰图,写上红字 Original,
        依次演示: 水平翻转、垂直翻转、旋转、亮度/对比度、高斯噪声、缩放、平移,
        并打印每种方法的用途和参数。

    说明:
        - 不读写任何图片文件
        - 不调用 augment_image
        - 目前没有 return, 结果只存在函数内部的变量里;
          想看效果, 需要打开 return 并用 imshow 显示    

    考点: 理解每种增强的作用和参数
    """

    print("\n" + "=" * 70)
    print("常用图形增强方法演示")
    print("=" * 70)

    # 创建一张测试图片
    # np.ones() 函数作用是创建一个指定形状（shape）和数据类型（dtype），且所有元素值都初始化为 1 的新数组：[1 1 1] [1 1 1]
    # (200,300,3) shape 形状:高 200 行，每行300个像素、3 个通道（每个像素3个值）。注意顺序是 高、宽、通道
    # 3 个通道在 OpenCV 里的顺序是 B(蓝)、G(绿)、R(红),不是 RGB。
    # dtype=np.uint8 每个数的类型是 0~255 的整数,图片就用这种类型
    # * 200 是列表做乘法，从[1,1,1] 变成 [200,200,200];即蓝=200、绿=200、红=200。三个值相等,就是偏亮的浅灰色,就是浅灰空白图

    img = np.ones((200,300,3),dtype = np.uint8) * 200
    
    # 调试语句 打印img返回值
    # print(f"img is : {img}")
    
    # 调用opencv的文字绘制函数

    # cv2.putText() 是 OpenCV 库中用于在图像或视频帧上绘制（添加）文本的核心函数
    cv2.putText(

        # 要添加文本的图片，添加的文字内容"Original"，文字左下角的位置,第一个是 x(向右),第二个是 y(向下)
        img,'Original',(50,100), 

        # cv2.FONT_HERSHEY_SIMPLEX 常量（字体类型标识符），其作用是指定在图像上绘制文字时使用“正常大小的无衬线字体"
        # 第二个“2” 是字体大小(缩放倍数)。1 约 27 像素高,0.5 约 14 像素,2 约 54 像素
        # 颜色,BGR 顺序,即蓝=0、绿=0、红=255,是红色
        # 最后的“2” 是线条粗细,单位是像素
        cv2.FONT_HERSHEY_SIMPLEX,2,(0,0,255),10
    )

    # 打印信息
    print("\n 1. 水平翻转函数 --> cv2.flip(img,1) ")
    # cv2.flip()函数执行图片水平翻转,1水平；flip = 翻转

    img_h_flip = cv2.flip(img,1)
    print("用途： 增加样本多样性，适用于无方向性的图像")

    # 打印信息
    print("\n 2. 垂直翻转函数 --> cv2.flip(img,0)")
    
    # 执行图片垂直翻转，0垂直
    img_v_flip = cv2.flip(img,0)
    print("用途： 模拟倒置场景")

    # 打印信息
    print("\n 3. 旋转函数 --> cv2.getRotationMatrix2D() + cv2.warpAffine()")

    # 声明变量存储旋转的角度数， angle = 角度
    angle = 30

    # 通过img.shape获得图片高宽，img.shape正常返回三个值对应宽度，高度，通道数，img.shape[:2]取前2个值就是宽度，高度
    # shape = 形状
    h,w = img.shape[:2]

    # 生成旋转矩阵，使用cv2.getRotationMatrix2D()函数,ratation=旋转，Matrix=矩阵
    # 创建旋转矩阵，以中心点(w//2、h//2是获得中心点位置)为旋转中心，angle是旋转角度，正数是逆时针，缩放比例，1.0 不缩放
    M = cv2.getRotationMatrix2D(( w //2, h//2),angle,1.0)
    
    # cv2.warpAffine()函数执行仿射变换，传入img图片，旋转矩阵M，(w,h) 是输出图片的大小,先宽后高,和 shape 的顺序相反
    # warp = 扭曲 affine = 仿射
    img_rotate = cv2.warpAffine(img, M, (w,h))

    print(f" 参数 angel={angle}° （正数逆时针，负数顺时针）")
    
    
    # 输出提示
    print(f"\n 4. 亮度/对比调整 --> cv2.convertScaleAbs")

    # cv2.convertScaleAbs()函数对图像数组的每个元素顺序执行三个操作：缩放（Scale）、取绝对值（Absolute value），并转换为无符号 8 位类型（uint8）
    # convertScaleAbs = convert(转换) + Scale(缩放) + Abs(绝对值)
    # img 是要传入的图片，alpha是对比度值，beta是亮度值
    img_bright = cv2.convertScaleAbs(img, alpha = 1.2,beta =30)

    # 输出提示
    print("  参数：alpha >1 增加对比对， beta > 0 增加亮度")


    print("\n 5. 高斯噪声 --> np.random.nomal()函数")

    # noise(噪声)
    # np.random.normal 用来从正态分布（也叫高斯分布或“钟形曲线”）中抽取随机数
    # 生成高斯噪声，第一个参数是均值，数据围绕哪个数波动；第二个参数是标准差，波动幅度，越大噪声越强；第三个是生成的数据形状
    # img.shape返回3个数，这里代入就是生成与图片同形状的浮点噪声（正负都有）
    # astype(np.uint8)是转换为无符号 8 位整数 
    # noise 返回的是一个和图片同样大小的数组，图片有多少个数值,它就有多少个随机数,这样才能一个对一个地相加。
    noise = np.random.normal(0,5,img.shape).astype(np.uint8)
    # 调试语句
    #print(f"noise is {noise}")

    # 把高斯噪声添加到图片上；cv2.add用来叠加图片、调亮度、加噪声
    img_noise = cv2.add(img, noise)
    
    
    # 输出提示
    print("\n 6. 缩放函数 --> cv2.resize()")
    
    # cv2.resize() 用于对图像进行缩放（大小变换）的函数，resize(调整大小)
    # img传入要缩放的图片，dsize 是输出的目标尺寸，给 None 表示不直接指定尺寸
    # fx 宽度(水平方向)的缩放比例为1.5倍，高度(垂直方向)的缩放比例为1.5倍
    # cv2.INTER_LINEAR  插值方式:放大后多出来的像素,怎么算出它们的颜色，
    # 图片放大后,像素变多了,新增的像素原本没有颜色,需要根据周围的像素估算。这种估算方法叫插值（interpolation）
    img_scaled = cv2.resize(
        img, None, fx = 1.5, fy = 1.5,
        interpolation = cv2.INTER_LINEAR 
    )

    # 输出提示
    print("参数： fx=1.5, fy=1.5 (放大倍数)")


    # 输出提示
    print("\n 7. 平移 --> cv2.warpAffine()")

    # np.flaot()将输入的数据（如数字、列表、元组或其他 NumPy 数组）转换成单精度浮点数（32位浮点数）类型
    # 创建的是一张 2 行 3 列的平移矩阵[[ 1.  0. 50.] [ 0.  1. 30.]],warpAffine 要求矩阵是小数类型
    # 前两列 [1,0] 和 [0,1] 这是"不旋转、不缩放"的部分(单位矩阵),保持原样
    # 第三列 50 和 30;平移量:第一行的 50 是 x 方向(水平)平移,第二行的 30 是 y 方向(垂直)平移
    M_trans = np.float32([[1,0,50] , [0,1,30]])

    # 调试语句
    print (f"M_trans is {M_trans}")

    # 仿射变换，img是传入的图片，M是平移矩阵，(w,h)是输出的大小，保存不变。  trans(转移)
    img_trans = cv2.warpAffine(img, M_trans, (w,h))

    print("参数：tx = 50, ty =30 (向右移动50像素，向下移动30像素)")

    
    print("\n" + "=" * 70)

    # 调试语句
    #return img, img_rotate, img_bright, img_noise, img_scaled, img_trans
    

def main():

    """主函数 - 使用示例"""

    #声明三个变量分别存输入图片文件夹路径，输出文件夹路径，抽取图片比例
    INPUT_DIR = "./images5"
    OUTPUT_DIR = "./augmented"
    AUG_RAITO =  0.3 

    # 调用演示各种增强方法的函数
    demo_augmentation_methods()

    # 输出提示
    print("\n" + "=" * 70)
    print("开始批量增强")
    print("=" * 70)

    # 通过os.path.exists()函数判断输入文件夹是否不存在
    if not os.path.exists(INPUT_DIR):

        # 输出提示
        print(f"输入目录不存在: {INPUT_DIR}")
        print(f"提示：请将图片放在 '{INPUT_DIR}'目录下 ")
        print('或修改代码中的 INPUT DIR 变量')

        # 通过os.makedirs()函数创建输入文件夹
        os.makedirs(INPUT_DIR,exsit_ok  = True)
        print(f" 已创建实例目录 ：{INPUT_DIR}")
        print("请添加图片后重新运行程序")
    
    else:
        # 调用批量增强图片函数
        random_augment_images(INPUT_DIR,OUTPUT_DIR,aug_ratio = AUG_RAITO)


# python程序主入口
if __name__ == '__main__':
    main()

#random_augment_images(input_dir=r'images5', output_dir='images_output')

# 调试语句

# orig, rot, bright, noise, scaled, trans = demo_augmentation_methods()

# names = ["原图", "旋转", "提亮", "高斯", "缩放", "平移"]
# imgs  = [orig, rot, bright, noise, scaled, trans]

# cells = []
# for name, im in zip(names, imgs):
#     im = cv2.resize(im, (300, 200))                  # 统一成宽300、高200,否则大小不同拼不起来
#     cv2.putText(im, name, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)    # 左上角写名字
#     cells.append(im)

# grid = np.vstack([np.hstack(cells[:3]), np.hstack(cells[3:])])   # 上面一行 3 张,下面一行 3 张
# cv2.imshow("demo", grid)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 显示图片，窗口名为img
#img = demo_augmentation_methods()
#cv2.imshow("demo", img)
# 等待按键，按任意按键继续，不加窗口会一闪而过
#cv2.waitKey(0)
# 关闭所有窗口
#cv2.destroyAllWindows
#demo_augmenttation_methods()