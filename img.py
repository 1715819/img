import os
import requests
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# === 配置 ===
LINK_FILE = "links.txt"       # 链接列表
SAVE_FOLDER = "images"        # 图片保存目录
MAX_WORKERS = 8               # 最大线程数
DELAY_BETWEEN_ROUNDS = 20      # 每轮间的等待时间（秒）

# 支持的图片扩展名（通过 content-type 判断）
EXT_MAP = {
    'image/jpeg': '.jpg',
    'image/png': '.png',
    'image/webp': '.webp',
    'image/gif': '.gif',
    'image/bmp': '.bmp',
    'image/svg+xml': '.svg',
    'image/tiff': '.tiff'
}

# 创建保存目录（如果不存在）
os.makedirs(SAVE_FOLDER, exist_ok=True)

# 获取当前编号（从已有文件中提取最大编号）
def get_next_index():
    existing = [f for f in os.listdir(SAVE_FOLDER) if '.' in f]
    nums = []
    for name in existing:
        try:
            num = int(os.path.splitext(name)[0])
            nums.append(num)
        except:
            continue
    return max(nums) + 1 if nums else 1

# 下载函数
def download_image(index_url):
    index, url = index_url
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '').split(';')[0]
        ext = EXT_MAP.get(content_type, '.jpg')
        filename = f"{index}{ext}"
        path = os.path.join(SAVE_FOLDER, filename)

        with open(path, 'wb') as f:
            f.write(response.content)

        print(f"[✓] 下载成功: {filename}")
    except Exception as e:
        print(f"[×] 下载失败: {url}，原因: {e}")

# === 主循环 ===
counter = get_next_index()

while True:
    # 读取链接
    try:
        with open(LINK_FILE, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[×] 无法读取链接文件: {e}")
        time.sleep(DELAY_BETWEEN_ROUNDS)
        continue

    if not links:
        print("链接列表为空，等待中...")
        time.sleep(DELAY_BETWEEN_ROUNDS)
        continue

    indexed_links = [(counter + i, url) for i, url in enumerate(links)]

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        executor.map(download_image, indexed_links)

    counter += len(links)

    print(f"--- 本轮完成，下载 {len(links)} 张，等待 {DELAY_BETWEEN_ROUNDS} 秒 ---\n")
    time.sleep(DELAY_BETWEEN_ROUNDS)
