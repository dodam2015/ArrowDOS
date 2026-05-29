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

    def path_exists(path: str) -> bool:
        return os.path.exists(path) and os.path.isfile(path)


    def harddisk():
        bytes = sum(f.stat().st_size for f in dir.rglob('*') if f.is_file())

        # 2. 적절한 단위로 변환해서 출력
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024

    if path_exists(f"{dir}\\SYS32\\OSHD.txt")==True:
        with open(os.path.join(dir, 'SYS32','OSHD.txt'), 'r', encoding='utf-8') as f:
            OSHD = [line.strip() for line in f.readlines()]
        bytes_size = sum(f.stat().st_size for f in dir.rglob('*') if f.is_file())
        
        # 2. Byte를 GB 단위로 변환 (출력용이나 다른 곳에 쓰실 때 활용)
        dir_gb = bytes_size / (1024 ** 3)

        # 3. 크기 비교 (Byte 단위로 직접 계산해서 정확하게 비교)
        if bytes_size > float(OSHD[0]) * (1024 ** 3):
            print('디스크 용량 초과!')
            print('정상적으로 실행되지 않다면 시스템 복구 모드를 사용하세요!')
            time.sleep(2)
            args = [sys.executable, os.path.join(dir,'mainboot.py')]
            subprocess.run(args)
        else:
            pass
        print(f'하드 디스크 용량: {OSHD[0]}GB / {harddisk()} 사용됨.')
    else:
        pass

    def guiboot():
        subprocess.run([sys.executable, os.path.join(dir,'SYS32','SYSF','-guiboot-','main.py')])
        os.system('cls')

    tmp=''
    dv=False
    pygame.mixer.init()

    with open(os.path.join(dir, 'SYS32','osname.txt'), 'r', encoding='utf-8') as f:
        osname = [line.strip() for line in f.readlines()]
    def sound(a):
        a=os.path.join('SYS32','Sounds',a)
        pygame.mixer.music.load(a)   # 파일 경로 넣기
        pygame.mixer.music.play()
    def clock():
        now = datetime.now(timezone.utc) + timedelta(hours=9)
        ampm = "오전" if now.hour < 12 else "오후"
        # 12시간제 표시를 위해 %I 사용
        return now.strftime(f"%Y년%m월%d일 {ampm}%I시%M분%S초").replace(" 0", " ")
#시작


    if osname[2][-1]=='s':
        print('프리릴리즈 버전에서는 ArrowDOS의 여러 신기능을 테스트할 수 있고')
        print('문제점을 개선할 수 있습니다.')
        print('개발자 이메일: dodam2015no1@naver.com')
    time.sleep(2)
    with open(os.path.join(dir, 'SYS32','SYSF','guiboot.arsys'), 'r', encoding='utf-8') as f:
        bootmn = f.readline().strip()

    if bootmn[0]=='t':
        guiboot()
    elif bootmn[0]=='f':
            print("\033[32mArrow corp. Arrow DOS\033[34m-v1.0\033[0m")
            for i in tqdm(range(100), desc="loading...\033[32m"):
                time.sleep(0.02)
            print("\033[0m")
            print('done.')
            time.sleep(1)
            os.system('cls')
            sound('start.mp3')



    msg=[]
    msg.append('ArrowDOS가 실행되었습니다!')

    def logon():
        with open(os.path.join(dir, 'SYS32','SYSF','dftuser.arsys'), 'r', encoding='utf-8') as f:
            dftusr = [line.strip() for line in f.readlines()]
        if path_exists(f"{dir}\\Users\\{dftusr[0]}\\UserDATA.txt")==False:
            print("OOBE에 진입 중 입니다...\n")
            time.sleep(2)
            print("PC 기본 설정 마법사를 실행합니다.")
            time.sleep(1)
            tmp=os.path.join('SYS32','SYSdriver','PCMakeWizard','PCMakeWizard.py')
            subprocess.run([sys.executable,tmp])
            print("\nPC 기본 설정이 완료되었습니다.")
            time.sleep(1)
            print("계정 생성 마법사를 실행합니다.")
            time.sleep(1)
            tmp=os.path.join('SYS32','SYSdriver','UserMakeWizard','UserMakeWizard.py')
            subprocess.run([sys.executable,tmp])
            print("\n계정 설정이 완료되었습니다.")
            print('컴퓨터를 재부팅합니다.')
            time.sleep(2)
            subprocess.run([sys.executable,'mainboot.py'])
        elif path_exists(f"{dir}\\Users\\{dftusr[0]}\\UserDATA.txt")==True:
            with open(os.path.join(dir, 'Users',dftusr[0],'UserDATA.txt'), 'r', encoding='utf-8') as f:
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
    date_str = osname[5]
    TARGET_YEAR   = int(date_str[0:4])# 앞에서 4글자 (2026)
    TARGET_MONTH  = int(date_str[4:6])# 그 다음 2글자 (03)
    TARGET_DAY    = int(date_str[6:8])# 그 다음 2글자 (15)
    TARGET_HOUR = 18
    TARGET_MINUTE = 32
    TARGET_SECOND = 15


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
        msg.append(f'프리릴리즈 버전입니다! 이 프리릴리즈 마지막 지원 날짜는 {TARGET_YEAR}년 {TARGET_MONTH}월 {TARGET_DAY}일 {TARGET_HOUR}시 {TARGET_MINUTE}분 {TARGET_SECOND}초까지 입니다. 새로운 ArrowDOS버전을 미리 테스트 해보세요.')
    logon()
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
            print('    ctpl - 제어판을 엽니다.')
            print('    logout - 로그아웃 합니다.')
            print('    credit - 도움을 주신 개발자들을 출력합니다.')
            print('    curnel(명령어) - 커널 모드에 접근합니다.')
        elif cmd=='info':
            print('\033[32mArrowDOS\033[0m 시스템 정보를 로드하는 중...')
            time.sleep(1)
            if osname[2][-1]=='s':
                print(f'    베타 버전 참가 중 (프리릴리즈)')
                print(f'    ArrowDOS버전:{(osname[0])[8:]} - \033[33m\033[1m{osname[3]}\033[0m,{osname[4]}')
                print(f'    마지막 업데이트 날짜:{osname[2][-9:-1]}')
                print(f'    프릴리리즈 지원:{TARGET_YEAR}년{TARGET_MONTH}월{TARGET_DAY}일{TARGET_HOUR}시{TARGET_MINUTE}분 까지')
            elif osname[2][-1]=='p':
                print(f'    정식 버전 (릴리즈)')
                print(f'    ArrowDOS버전:{(osname[0])[8:]} - \033[33m\033[1m{osname[3]}\033[0m,{osname[4]}')
                print(f'    마지막 업데이트 날짜:{osname[2][-9:-1]}')
                print(f'    \033[33m\033[1m{osname[3]}\033[0m 지원:{TARGET_YEAR}년{TARGET_MONTH}월{TARGET_DAY}일{TARGET_HOUR}시{TARGET_MINUTE}분 까지')
            else:
                print('    무단 복제본 또는 수정된 버전. 사기에 조심하세요.')
            print(f'하드 디스크 용량: {OSHD[0]}GB / {harddisk()} 사용됨.')
        elif cmd=='clr':
            os.system('cls')
        elif cmd=='account':
            print("계정 보안 프로그램을 불러오는 중 입니다...\n")
            time.sleep(1)
            tmp=os.path.join(dir,'SYS32','SYSdriver','UserManager','UserManager.py')
            subprocess.run([sys.executable,tmp])
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
        elif cmd=='rst' or cmd=='restart':
            print('ArrowDOS를 다시 시작 합니다... 취소하려면 3초 안에 ctrl + c를 눌러주세요...')
            try:
                sound('end.mp3')
                time.sleep(3)
                subprocess.run([sys.executable,'mainboot.py'])
            except KeyboardInterrupt:
                print('취소되었습니다.')
        elif cmd=='rst.d':
            sound('end.mp3')
            subprocess.run([sys.executable,'mainboot.py'],)
        elif cmd=='sht':
            print('ArrowDOS를 전원을 종료 합니다... 취소하려면 3초 안에 ctrl + c를 눌러주세요...')
            try:
                sound('end.mp3')
                time.sleep(3)
                quit()
            except KeyboardInterrupt:
                print('취소되었습니다.')
        elif cmd=='time':
            # 수정: datetime.datetime 대신 datetime 사용 및 오전/오후 포맷팅 적용
            print(clock())
        elif cmd=='controlpanel' or cmd=='ctpl':
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
        elif cmd=='logout':
            os.system('cls')
            logon()
        elif cmd=='credit':
            print('도움을 주신 분들')
            print('원작자:')
            print('    호기심소년 (ArrowCorp)')
            print('그 외:')
            print('    Gemini AI')
        elif cmd.startswith('curnel(') and cmd.endswith(')'):
            print('-----사용자 계정 컨트롤-----')
            print(f'{cmd[7:-1]}이 (가) 사용자의 ArrowDOS를 변경할 수 있도록 허용하시겠습니까? (y or n)')
            tmp=''
            tmp=input('선택하세요: ')
            if tmp=='y':
                args = [sys.executable, os.path.join(dir,'SYS32','SYSdriver','curnel',cmd[7:-1],'main.py')]
                subprocess.run(args)
                sound('info.mp3')
            else:
                print('취소되었습니다.')
                sound('error.mp3')
        else:
            sound('error.mp3')
            print(f"{cmd}는 유효한 경로나 파일, 응용 프로그램 단축이 아닙니다.\n도움말을 불러오시려면 ?를 입력해주세요.")

except(Exception,KeyboardInterrupt) as e:
    args = [sys.executable, os.path.join(dir,'SYS32','BSOD','main.py'), str(e)]
    subprocess.run(args)