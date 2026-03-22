import time,os
from pathlib import Path
print('계정의 보안을 확인합니다...')
time.sleep(1)
tmp=''
tmp=input('보안을 위해 계정의 비밀번호를 입력해주세요:')
dir=Path.cwd()

with open(os.path.join(dir, 'SYS32','SYSF','dftuser.arsys'), 'r', encoding='utf-8') as f:
    dftusr = [line.strip() for line in f.readlines()]

with open(os.path.join(dir, 'Users',dftusr[0],'UserDATA.txt'), 'r', encoding='utf-8') as f:
    userdata = [line.strip() for line in f.readlines()]
if tmp==userdata[1]:
    print('신원 일치 확인 완료..')
    time.sleep(1)
    print(f'계정 이름:{userdata[0]}')
    print(f'계정 비밀번호:{userdata[1]}')
    print('보안을 위해 3초 후 프로그램이 종료됩니다.')
    time.sleep(3)
    os.system('cls')