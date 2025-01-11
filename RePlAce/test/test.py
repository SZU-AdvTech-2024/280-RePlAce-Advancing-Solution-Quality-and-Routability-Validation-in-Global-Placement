import glob
from PIL import Image
import numpy as np

def create_nine_grid(image_dir, output_path, interval=None):
    # 获取所有图片文件并排序
    image_files = sorted(glob.glob(f"{image_dir}/*.jpg"))
    total_images = len(image_files)
    
    if interval is None:
        # 自动计算间隔，选择首、尾和中间的图片
        indices = [0]  # 第一张
        step = (total_images - 1) // 8  # 平均分配其余8张
        for i in range(1, 8):
            indices.append(i * step)
        indices.append(total_images - 1)  # 最后一张
    else:
        # 使用指定间隔
        indices = list(range(0, total_images, interval))[:9]
    
    # 读取第一张图片来获取尺寸
    first_img = Image.open(image_files[0])
    img_width, img_height = first_img.size
    
    # 创建新图片（3x3网格）
    grid_width = img_width * 3
    grid_height = img_height * 3
    grid_image = Image.new('RGB', (grid_width, grid_height), 'white')
    
    # 填充九宫格
    for idx, img_idx in enumerate(indices):
        if img_idx >= total_images:
            break
            
        # 计算在九宫格中的位置
        row = idx // 3
        col = idx % 3
        
        # 打开并粘贴图片
        img = Image.open(image_files[img_idx])
        grid_image.paste(img, (col * img_width, row * img_height))
        
        # 在图片上添加迭代次数标签
        from PIL import ImageDraw, ImageFont
        draw = ImageDraw.Draw(grid_image)
        iteration = img_idx  # 或从文件名中提取迭代次数
        draw.text((col * img_width + 10, row * img_height + 10), 
                 f'Iteration {iteration}', 
                 fill='black')
    
    # 保存结果
    grid_image.save(output_path)
    print(f"Nine-grid image saved to {output_path}")

# 使用示例
image_dir = "/home/lizichao/RePlAce/test/output/etc/gcd/experiment001/cell"
output_path = "/home/lizichao/RePlAce/test/placement_nine_grid.png"

# 方式1：自动计算间隔
create_nine_grid(image_dir, "auto_interval_grid.jpg")

# 方式2：指定间隔（比如每隔40张图片选一张）
create_nine_grid(image_dir, "fixed_interval_grid.jpg", interval=40)
