def remove_duplicates(file_path):
    lines = set()
    new_lines = []

    # 读取文件并检查重复内容
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line not in lines:
                lines.add(line)
                new_lines.append(line)

    # 将去重后的内容写回文件
    with open(file_path, 'w') as file:
        file.write('\n'.join(new_lines))


# 指定要检查重复内容的文件路径
file_path = 'TrueUser.txt'

# 调用函数进行重复内容检查和删除
remove_duplicates(file_path)
