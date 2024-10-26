import json
from datetime import datetime, time

# 缓存字典
cache = {}
file_cache = './clock_cache.json'


# 将数据写入JSON文件
def write_to_json_file(data):
    with open(file_cache, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# 从JSON文件读取数据
def read_from_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


# 从缓存读取数据
def read_with_json_cache(file_path):
    if file_path in cache:
        return cache[file_path]

    data = read_from_json_file(file_path)
    cache[file_path] = data
    return data


# 示例：写入和读取JSON
data = {'name': 'Alice', 'age': 30}
face_time = datetime.strptime("10/26/2024 11:51:43", "%m/%d/%Y %H:%M:%S")

data["mock"] = "10/26/2024 11:51:43"

# 写入数据到JSON文件
write_to_json_file(data)

# 读取数据，从文件或缓存中获取
print("First read (from file): ", read_with_json_cache(file_cache))
print("Second read (from cache): ", read_with_json_cache(file_cache))
