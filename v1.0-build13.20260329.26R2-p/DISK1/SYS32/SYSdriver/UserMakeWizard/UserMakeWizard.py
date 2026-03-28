import time,os
from pathlib import Path
name=''
password=''



def usermake(dir: str, nadme: str, pw: str,추가모드=True):
    mode = 'a' if 추가모드 else 'w'
    with open(dir, mode, encoding='utf-8') as f:
        f.write(f"{nadme}\n")
        f.write(f"{pw}\n")

print('계정 생성 마법사에 오신 것을 환영합니다!')
time.sleep(2)
print('저는 계정 생성을 돕는 돋보기라고 합니다.')
time.sleep(2)
print('지금 부터 시작 하겠습니다!')
time.sleep(2)
print('당신의 이름이 저는 궁금합니다!')
print('이름이나 닉네임을 입력해주세요.')
name=input(':')
print(f'감사합니다! {name}님.')
print('당신의 계정을 지켜줄 강력한 비밀번호를 입력하세요!')
print('강력한 비밀번호를 입력해주세요')
password=input(':')
print('감사합니다!')
print('파일 저장중...')


data_file = os.path.join(
    Path.cwd(),
    "Users", "User", "UserDATA.txt"
)

with open(data_file, 'w', encoding='utf-8') as gg:
    gg.write('')
gg.close
usermake(data_file,name,password)