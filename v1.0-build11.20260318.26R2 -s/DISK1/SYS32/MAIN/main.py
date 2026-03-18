try:
    import sys,os,time,subprocess,traceback,base64,keyboard
    from playsound import playsound
    from tqdm import tqdm
    from pathlib import Path

    from datetime import datetime, timedelta, timezone
    from zoneinfo import ZoneInfo

    import pygame
    dir=Path.cwd()
    os.system('cls')

    tmp=''
    dv=False
    pygame.mixer.init()
    def path_exists(path: str) -> bool:
        return os.path.exists(path) and os.path.isfile(path)
    with open(os.path.join(dir, 'SYS32','osname.txt'), 'r', encoding='utf-8') as f:
        osname = [line.strip() for line in f.readlines()]
    def sound(a):
        a=os.path.join('SYS32','Sounds',a)
        pygame.mixer.music.load(a)   # 파일 경로 넣기
        pygame.mixer.music.play()
    print("\033[32mArrow corp. Arrow DOS\033[34m-v1.0\033[0m")


    for i in tqdm(range(100), desc="loading...\033[32m"):

        time.sleep(0.02)
    print("\033[0m")
    print('done.')
    msg=[]
    msg.append('ArrowDOS가 실행되었습니다!')
    time.sleep(1)
    os.system('cls')
    sound('start.mp3')



    def log_error(exc_type, exc_value, exc_tb):
        now = datetime.now()
        date = now.strftime("%Y%m%d")
        ampm = now.strftime("%p").replace("AM", "오전").replace("PM", "오후")
        time_str = now.strftime("%I-%M-%S")
        filename = dir.path.join(dir,'SYS32','LOG',f"{date}-{ampm}{time_str}.txt")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"시간: {now:%Y-%m-%d %H:%M:%S}\n")
            f.write(f"오류: {exc_type.__name__} - {exc_value}\n\n")
            traceback.print_exception(exc_type, exc_value, exc_tb, file=f)


    sys.excepthook = log_error


    #업데이트 제한 설정
    TARGET_YEAR = 2026
    TARGET_MONTH = 4
    TARGET_DAY = 18
    TARGET_HOUR = 0
    TARGET_MINUTE = 0
    TARGET_SECOND = 0
    SCRIPT_PATH = os.path.join(dir,'SYS32','SYSdriver','support_end','support_end.py')
    
    # 수정: 상단에서 datetime 클래스를 직접 import했으므로 datetime()으로 바로 호출
    target_naive = datetime(TARGET_YEAR, TARGET_MONTH, TARGET_DAY,
                            TARGET_HOUR, TARGET_MINUTE, TARGET_SECOND)
    target = target_naive.replace(tzinfo=timezone(timedelta(hours=9)))

    # 수정: datetime.datetime.now() 대신 datetime.now() 사용
    now_kst = datetime.now(timezone.utc) + timedelta(hours=9)

    if now_kst >= target:
        try:
            sound('error.mp3')
            subprocess.run(["python", SCRIPT_PATH], check=True)
            print("보안 업데이트 등을 받으려면 업데이트를 하세요...")
            msg.append('ArrowDOS의 지원 기간이 끝났습니다.')
            time.sleep(2)
        except Exception as e:
            print("??? 실패:", e)
    if osname[2][-1]=='s':
        msg.append(f'프리릴리즈 버전입니다! 이 프리릴리즈 마지막 지원 날짜는 {TARGET_YEAR}년 {TARGET_MONTH}월 {TARGET_DAY}일 {TARGET_HOUR}시 {TARGET_MINUTE}분 {TARGET_SECOND}까지 입니다. 새로운 ArrowDOS버전을 미리 테스트 해보세요.')
    


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
        sound('info.mp3')
        print('환영합니다...')
        time.sleep(1)
        os.system('cls')


        cmd=''
        cd='DISK1'
        while True:
            try:
                cmd=input(f'{cd} >')
            except(KeyboardInterrupt):
                cmd=''
                print('ArrowDOS를 전원을 종료 합니다... 취소하려면 3초 안에 ctrl + c를 눌러주세요...')
                try:
                    time.sleep(3)
                    quit()
                except KeyboardInterrupt:
                    print('취소되었습니다.')
            if cmd=='?' or cmd=='hlp':
                print('\033[32mArrowDOS\033[0m 도움말 정보를 로드하는 중...')
                time.sleep(1)
                print('    ? - 이 명령어는 \033[32mArrowDOS\033[0m의 기능(도움말)을 불러와주는 간단한 명령어입니다.')
                print('    hlp - 이 명령어는 \033[32mArrowDOS\033[0m의 기능(도움말)을 불러와주는 간단한 명령어입니다.')
                print('    info - 이 명령어는 \033[32mArrowDOS\033[0m 시스템의 정보를 불러오는 명령어입니다.')
                print('    dv(T) - 개발자 모드가 켜집니다.')
                print('    dv(F) - 개발자 모드가 꺼집니다.')
                if dv==True:
                    print('regedit - *개발자 기능*이 DOS의 소스코드의 변수를 출력하고 수정합니다.')
                else:
                    pass
                print('    clr - 이 명령어는 터미널의 명령어 입력 내역을 모두 삭제 합니다.')
                print('    account - 이 명령어는 신원을 확인하고 계정의 보안을 확인하는 명령어입니다.')
                print('    apps - 앱을 확인합니다.')
                print('    restart - ArrowDOS를 다시시작 합니다.')
                print('    rst - ArrowDOS를 다시시작 합니다.')
                print('    rst.d - ArrowDOS를 강제 다시시작 합니다.')
                print('    sht - ArrowDOS의 시스템을 종료합니다.')
                print('    time - 시간을 표시합니다.')
                print('    msg - 알림을 표시합니다.')
                print('    msgd - 알림을 삭제합니다.')
                print('    msgp - 알림을 추가합니다.')
                print('    diskmgr - 디스크 매니저를 실행합니다.')
            elif cmd=='info':
                print('\033[32mArrowDOS\033[0m 시스템 정보를 로드하는 중...')
                time.sleep(1)
                if osname[2][-1]=='s':
                    print(f'베타 버전 참가 중 (프리릴리즈)')
                    print(f'ArrowDOS버전:{(osname[0])[8:]} - \033[33m\033[1m{osname[3]}\033[0m,{osname[4]}')
                    print(f'마지막 업데이트 날짜:{osname[2][-9:-1]}')
                    print(f'프릴리리즈 지원:{TARGET_YEAR}년{TARGET_MONTH}월{TARGET_DAY}일{TARGET_HOUR}시{TARGET_MINUTE}분 까지')
                elif osname[2][-1]=='p':
                    print(f'정식 버전 (릴리즈)')
                    print(f'ArrowDOS버전:{(osname[0])[8:]} - \033[33m\033[1m{osname[3]}\033[0m,{osname[4]}')
                    print(f'마지막 업데이트 날짜:{osname[2][-9:-1]}')
                    print(f'\033[33m\033[1m{osname[3]}\033[0m 지원:{TARGET_YEAR}년{TARGET_MONTH}월{TARGET_DAY}일{TARGET_HOUR}시{TARGET_MINUTE}분 까지')
                else:
                    print('무단 복제본 또는 수정된 버전. 사기에 조심하세요.')
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
                tmp=os.path.join(dir,'SYS32','SYSdriver','UserManager','UserManager.py')
                subprocess.run([sys.executable,tmp])
            elif cmd=='regedit':
                if dv==True:
                    while True:
                            print("\n변수 목록:")
                            print("-" * 35)

                            vars_dict = {k: v for k, v in locals().items() 
                                        if not k.startswith(('_', 'var_edit')) and k != 'vars_dict'}

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
            elif cmd=='apps':
                print("앱을 불러오는 중 입니다...\n")
                time.sleep(1)   
                # 대상 경로
                base_dir = os.path.join(dir, 'LOCAL-PROGRAMS')

                # 폴더가 실제로 존재하는지 확인
                if not os.path.isdir(base_dir):
                    print(f"경로가 존재하지 않습니다: {base_dir}")
                    exit()

                # base_dir 안의 모든 **폴더**만 가져오기
                folders = [
                    d for d in os.listdir(base_dir)
                    if os.path.isdir(os.path.join(base_dir, d))
                ]

                if not folders:
                    print(f"{base_dir} 안에 폴더가 없습니다.")
                    exit()

                print(f"\n{base_dir} 안의 프로젝트 목록:")
                for i, folder in enumerate(folders, 1):
                    print(f"{i:2d}. {folder}")

                try:
                    choice = int(input("\n실행할 폴더 번호 (0 = 종료): "))

                    if choice == 0:
                        print("종료합니다.")
                    elif 1 <= choice <= len(folders):
                        selected = folders[choice - 1]
                        main_path = os.path.join(base_dir, selected, "main.py")

                        if os.path.isfile(main_path):
                            print(f"\n→ {selected} 실행 중...\n")
                            os.system('cls')
                            subprocess.run(["python", main_path], check=True)
                            time.sleep(1)
                            print('프로그램 종료!')
                            time.sleep(1)
                            os.system('cls')
                        else:
                            print(f"오류: {selected} 폴더에 main.py 파일이 없습니다.")
                    else:
                        print("잘못된 번호입니다.")

                except ValueError:
                    print("숫자를 입력해 주세요.")
            elif cmd=='restart':
                print('ArrowDOS를 다시 시작 합니다... 취소하려면 3초 안에 ctrl + c를 눌러주세요...')
                try:
                    time.sleep(3)
                    subprocess.run([sys.executable,'mainboot.py'])
                except KeyboardInterrupt:
                    print('취소되었습니다.')
            elif cmd=='rst':
                print('ArrowDOS를 다시 시작 합니다... 취소하려면 3초 안에 ctrl + c를 눌러주세요...')
                try:
                    time.sleep(3)
                    subprocess.run([sys.executable,'mainboot.py'])
                except KeyboardInterrupt:
                    print('취소되었습니다.')
            elif cmd=='rst.d':
                subprocess.run([sys.executable,'mainboot.py'],)
            elif cmd=='sht':
                print('ArrowDOS를 전원을 종료 합니다... 취소하려면 3초 안에 ctrl + c를 눌러주세요...')
                try:
                    time.sleep(3)
                    quit()
                except KeyboardInterrupt:
                    print('취소되었습니다.')
            elif cmd=='time':
                # 수정: datetime.datetime 대신 datetime 사용 및 오전/오후 포맷팅 적용
                now = datetime.now(timezone.utc) + timedelta(hours=9)
                ampm = "오전" if now.hour < 12 else "오후"
                # 12시간제 표시를 위해 %I 사용
                print(now.strftime(f"%Y년%m월%d일 {ampm}%I시%M분%S초").replace(" 0", " "))
            elif cmd=='controlpanel' or cmd=='crpl':
                print("제어판을 불러오는 중 입니다...\n")
                time.sleep(1)
                tmp=os.path.join(dir,'SYS32','SYSdriver','controlpanel','controlpanel.py')
                subprocess.run([sys.executable,tmp])
            elif cmd=='msg':
                print('현재 쌀여 있는 알림 메시지:')
                for i in range(0,len(msg)):
                    print(f'    {i}번째 메시지: {msg[i]}')
            elif cmd=='msgd':
                tmp=input('정말로 모든 메시지를 삭제할까요?(y,n)')
                if tmp=='y':
                    msg=[]
                    print('삭제되었습니다.')
                elif tmp=='n':
                    print('취소되었습니다.')
                else:
                    print('취소되었습니다.')
            elif cmd=='msgp':
                tmp=input('추가할 메시지를 입력하세요:')
                msg.append(tmp)
                print('메시지가 추가되었습니다!')
            elif cmd=='diskmgr':
                print("디스크 매니저를 불러오는 중 입니다...\n")
                time.sleep(1)
                tmp=os.path.join(dir,'LOCAL-PROGRAMS','diskmgr','main.py')
                subprocess.run([sys.executable,tmp])

            else:
                sound('error.mp3')
                print(f"{cmd}는 유효한 경로나 파일, 응용 프로그램 단축이 아닙니다.\n도움말을 불러오시려면 ?를 입력해주세요.")

except(Exception,KeyboardInterrupt) as e:
    try:
        print("\033[44m\033[97m")
        os.system('cls')
        print('BLUE_SCREEN')
        print('DOS-error')
        print(f'TARGET: {osname[0][:8]}')
        tb_text = traceback.format_exc()
        tb_base64 = base64.b64encode(tb_text.encode('utf-8')).decode('ascii')
        print('-' * 50)
        for i in range(0, len(tb_base64), 50):
            print(tb_base64[i:i+50])
        print('-' * 50)
        print(f'ERROR_MSG: {e}')
        bsodrsttim=5
        print(f'ERR: ARROWDOS_RESTART IN {bsodrsttim}S')
        time.sleep(bsodrsttim)
        subprocess.run([sys.executable,'mainboot.py'])
    except(Exception,KeyboardInterrupt):
        subprocess.run([sys.executable,'mainboot.py'])