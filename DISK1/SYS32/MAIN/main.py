import sys,os,time,subprocess
from tqdm import tqdm
from pathlib import Path

dir=Path.cwd()

os.system('cls')

tmp=''
dv=False

def path_exists(path: str) -> bool:
    return os.path.exists(path) and os.path.isfile(path)
with open(os.path.join(dir, 'SYS32','osname.txt'), 'r', encoding='utf-8') as f:
    osname = [line.strip() for line in f.readlines()]
print("\033[32mArrow corp. Arrow DOS\033[34m-v1.0\033[0m")


for i in tqdm(range(100), desc="loading...\033[32m"):
    time.sleep(0.01)
print("\033[0m")
print('done.')
time.sleep(1)
os.system('cls')

if path_exists(f"{dir}\\Users\\User\\UserDATA.txt")==False:
    print("계정 생성 마법사를 불러오는 중 입니다...\n")
    time.sleep(1)
    tmp=os.path.join('SYS32','SYSdriver','UserMakeWizard','UserMakeWizard.py')
    subprocess.run([sys.executable,tmp])
    print("\n계정 설정이 완료되었습니다.")
    print('컴퓨터를 재부팅합니다.')
    time.sleep(2)
    subprocess.run([sys.executable,'mainboot.py'])
elif path_exists(f"{dir}\\Users\\User\\UserDATA.txt")==True:
    with open(os.path.join(dir, 'Users','User','UserDATA.txt'), 'r', encoding='utf-8') as f:
        userdata = [line.strip() for line in f.readlines()]
    print(f"{userdata[0]}님, 안녕하세요!")
    while True:
        tmp=input('비밀번호를 입력해주세요:')
        if tmp==userdata[1]:
            break
        else:
            print('비밀번호를 다시 입력해주세요')
    print('환영합니다...')
    time.sleep(1)
    os.system('cls')


    cmd=''
    cd='DISK1'
    while True:
        cmd=input(f'{cd} >')
        if cmd=='?':
            print('\033[32mArrowDOS\033[0m 도움말 정보를 로드하는 중...')
            time.sleep(1)
            print('? - 이 명령어는 \033[32mArrowDOS\033[0m의 기능(도움말)을 불러와주는 간단한 명령어입니다.')
            print('info - 이 명령어는 \033[32mArrowDOS\033[0m 시스템의 정보를 불러오는 명령어입니다.')
            print('dv() - 이 명령어는 ()안에 T아니면F를 쓰면 상황에 맞게 개발자 모드가 켜지고 꺼집니다.')
            if dv==True:
                print('regedit - *개발자 기능*이 DOS의 소스코드의 변수를 출력하고 수정합니다.')
            else:
                pass
            print('clr - 이 명령어는 터미널의 명령어 입력 내역을 모두 삭제 합니다.')
            print('account - 이 명령어는 신원을 확인하고 계정의 보안을 확인하는 명령어입니다.')
        elif cmd=='info':
            print('\033[32mArrowDOS\033[0m 시스템 정보를 로드하는 중...')
            time.sleep(1)
            print(f'ArrowDOS버전:{(osname[0])[8:]}')
            print(f'고급 정보:{osname[2]}')
            if dv==True:
                tmp=input('ArrowDOS의 소스코드를 확인하시겠습니까? (Y or N):')
                if tmp=='Y':
                    print('====================')
                    with open(os.path.join(dir, 'SYS32','MAIN','main.py'), 'r', encoding='utf-8') as f:
                        code = [line.strip() for line in f.readlines()]
                    for i in range(0,len(code)):
                        print(code[i])
                    print('====================')
                else:
                    pass
        elif cmd.startswith('dv(') and cmd.endswith(')'):
            if cmd[3:-1]=='T':
                dv=True
                print('개발자 모드가 켜졌습니다.')
            elif cmd[3:-1]=='F':
                dv=False
                print('개발자 모드가 꺼졌습니디.')
            else:
                print('dv(T) - 개발자 모드를 켭니다.')
                print('dv(F) - 개발자 모드를 끕니다.')
        elif cmd=='clr':
            os.system('cls')
        elif cmd=='account':
            print("계정 보안 프로그램을 불러오는 중 입니다...\n")
            time.sleep(1)
            dir=Path.cwd()
            tmp=os.path.join(dir,'SYS32','SYSdriver','UserManager','UserManager.py')
            subprocess.run([sys.executable,tmp])
        elif cmd=='regedit':
            if dv==True:
                while True:
                        print("\n변수 목록:")
                        print("-" * 35)
                        
                        vars_dict = {k: v for k, v in locals().items() 
                                    if not k.startswith(('_', 'var_edit'))}
                        
                        if not vars_dict:
                            print(" (변수 없음)")
                        else:
                            for k in sorted(vars_dict):
                                print(f" {k:>12} = {repr(vars_dict[k])}")
                        print("-" * 35)
                        
                        name = input("\n수정할 변수 (종료: q 또는 엔터): ").strip()
                        if not name or name.lower() in ('q', 'quit'):
                            print("종료\n")
                            break
                            
                        if name not in vars_dict:
                            print(f"→ {name} 변수 없음\n")
                            continue
                            
                        print(f"  현재: {repr(vars_dict[name])}")
                        value_str = input(f"  새 값: ").strip()
                        
                        if not value_str:
                            print("취소\n")
                            continue
                            
                        try:
                            new_val = eval(value_str, {"__builtins__": {}}, vars_dict)
                            locals()[name] = new_val
                            print(f"→ {name} = {repr(new_val)}\n")
                        except Exception as e:
                            print(f"오류: {e}")
                            print("예: 42, '텍스트', [1,2,3], None\n")
            else:
                print('개발자 기능입니다.')








        else:
            print(f"{cmd}는 유효한 경로나 파일, 응용 프로그램 단축이 아닙니다.\n도움말을 불러오시려면 ?를 입력해주세요.")
        