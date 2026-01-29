import time,subprocess,sys,os
from pathlib import Path
os.system('cls')
parent_name=Path.cwd().name
print("\033[32mArrowDOS부팅매니저\033[34m-v1.0.7\033[0m")
time.sleep(2)
if parent_name=='DISK1':
    pass
else:
    print('사용자의 arrowDOS에서 문제점을 발견했습니다.')
    print('컴퓨터를 재부팅합니다.' )
    for i in range(0,4096):
        print('err: 58424')
    subprocess.run([sys.executable,'mainboot.py'])
print("사용하실 부팅 모드를 선택하세요.")
print("1.\033[36m일반 모드\033[0m")
print("2.\033[33m안전 모드\033[0m")
print("3.\033[31mDOS모드\033[0m")
while True:
    try:

        bootmod=int(input("번호를 입력하세요:"))
    except(KeyboardInterrupt):
        print("KeyboardInterrupt - Program interrupted by user.")
        time.sleep(2)
        cmd=''
        os.system("cls")
        print("일반 모드로 부팅하려면 bootmod=1 을 입력해 주세요.")
        while True:
            cmd=input(f'{parent_name}>')
            if cmd=='bootmod=1':
                bootmod=1
                break
            else:
                print(f"{cmd}는 유효한 경로나 파일, 응용 프로그램 단축이 아닙니다.")
    if bootmod==1:
        print("\033[36m일반 모드\033[0m를 선택하셨습니다.")
        print("\033[33m2\033[m초 후에 \033[36m일반 모드\033[0m로 진입합니다.")
        time.sleep(2)
        os.system("cls")
        subprocess.run([sys.executable, "SYS32/MAIN/main.py"])
        break
    elif bootmod==2:
        print("\033[33m안전 모드\033[0m를 선택하셨습니다.")
        print("\033[33m2\033[m초 후에 \033[33m안전 모드\033[0m로 진입합니다.")
        time.sleep(2)
        os.system("cls")
        print('구현되지 않았습니다.')
    elif bootmod==3:
        print("\033[31mDOS모드\033[0m를 선택하셨습니다.")
        print("\033[33m2\033[m초 후에 \033[31mDOS모드\033[0m로 진입합니다.")
        time.sleep(2)
        os.system("cls")
        print('구현되지 않았습니다.')
    else:
        print('입력한 번호를 재확인 하고 다시 입력해주세요.')
        print(f'입력한 번호는: {bootmod}입니다.')