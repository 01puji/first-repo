def read_file(file_path):
    """读取文件内容"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path, data):
    """将数据写入文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

def encode_to_decimal(data):
    """将UTF-8编码的数据转换为十进制表示"""
    return ' '.join(str(ord(char)) for char in data)

def decode_from_decimal(data):
    """将十进制表示的数据解码回原始UTF-8字符串"""
    return ''.join(chr(int(num)) for num in data.split())

# 编码过程
# 读取Python代码文件
python_code = read_file('voice_chatbot.py')

# 将代码转换为十进制表示
encoded_code = encode_to_decimal(python_code)

# 将十进制表示保存到文件
write_file('encoded_voice_chatbot.txt', encoded_code)

print("Python代码已转换为十进制表示并保存到 encoded_voice_chatbot.txt")

# 解码过程
# 从文件读取十进制字符串
encoded_code = read_file('encoded_voice_chatbot.txt')

# 将十进制字符串解码回Python代码
decoded_code = decode_from_decimal(encoded_code)

# 将解码后的Python代码保存到新文件
write_file('decoded_voice_chatbot.py', decoded_code)

print("十进制字符串已解码回Python代码并保存到 decoded_voice_chatbot.py")
