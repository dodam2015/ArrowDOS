from tqdm import tqdm
import time
import time,os
from pathlib import Path

def usermake(dir: str, nadme: str, 추가모드=True):
    mode = 'a' if 추가모드 else 'w'
    with open(dir, mode, encoding='utf-8') as f:
        f.write(f"{nadme}\n")

for i in tqdm(range(100), desc="loading...\033[32m"):
    time.sleep(0.02)

print("설정할 하드 디스크 용량을 입력하세요.")
print("매번 부팅 마다 하드 디스크의 용량을 체크 합니다.")
print("최대 값은 32GB입니다.")
harddisk=34
while harddisk>=33:
    harddisk=int(input("설정할 하드 디스크 용량을 입력하세요(단위:GB): "))
print('설정이 완료되었습니다.')
print('감사합니다!')
print('파일 저장중...')

data_file = os.path.join(
    Path.cwd(),
    "SYS32", "OSHD.txt"
)

with open(data_file, 'w', encoding='utf-8') as gg:
    gg.write('')
gg.close
usermake(data_file,harddisk)