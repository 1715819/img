import os
from PIL import Image

def is_image_valid(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()  # 检查图片是否损坏
        return True
    except Exception:
        return False

def clean_broken_images(folder):
    removed_files = []
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        if os.path.isfile(file_path):
            if not is_image_valid(file_path):
                print(f"删除损坏图片: {file_path}")
                os.remove(file_path)
                removed_files.append(file_path)
    return removed_files

if __name__ == "__main__":
    images_folder = "images"
    removed = clean_broken_images(images_folder)
    print(f"总共删除了 {len(removed)} 个损坏的图片文件。")
