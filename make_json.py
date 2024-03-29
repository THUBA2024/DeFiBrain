import json

# 替换下面的路径为你的txt文件路径
txt_file_path = '1.txt'
json_file_path = '1.json'

# 读取文本文件
with open(txt_file_path, 'r') as file:
    # 假设每一行就是一个JSON对象，去除尾部的逗号（如果有的话）
    json_lines = [line.rstrip(',\n') for line in file]

# 将每行转换成JSON对象，并将所有对象保存到一个列表中
json_objects = [json.loads(line) for line in json_lines]

# 将列表保存到JSON文件
with open(json_file_path, 'w') as json_file:
    json.dump(json_objects, json_file, indent=4)

print(f'JSON数据已保存到{json_file_path}')