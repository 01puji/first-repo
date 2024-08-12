# 파일 내용 읽기
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

 # 파일에 데이터 쓰기
def write_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

# UTF-8 인코딩된 데이터를 십진수로 변환
def encode_to_decimal(data):
    return ' '.join(str(ord(char)) for char in data)

 # 10진수 데이터를 원래 UTF-8 문자열로 변환
def decode_from_decimal(data):
    return ''.join(chr(int(num)) for num in data.split())

# 인코딩 과정
# 파이썬 코드 파일 읽기
python_code = read_file('voice_chatbot.py')

# 코드를 십진수로 변환
encoded_code = encode_to_decimal(python_code)

# 파일에 십진수 표시 저장
write_file('encoded_voice_chatbot.txt', encoded_code)

print("파이썬 코드가 십진법으로 변환되어 encoded_voice_chatbot.txt에 저장되었습니다")

# 디코딩 과정
# 파일에서 십진수 문자열 읽기
encoded_code = read_file('encoded_voice_chatbot.txt')

# 파이썬 코드로 십진수 문자열을 디코딩
decoded_code = decode_from_decimal(encoded_code)

# 디코딩된 파이썬 코드를 새 파일에 저장
write_file('decoded_voice_chatbot.py', decoded_code)

print("10진수 문자열이 파이썬 코드로 디코딩되어 decoded_voice_chatbot.py 에 저장되었습니다")

