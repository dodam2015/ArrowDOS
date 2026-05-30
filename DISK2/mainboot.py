try:
    import sys,os,time,subprocess,traceback,datetime,base64
    from tqdm import tqdm
    from pathlib import Path
    dir=Path.cwd()
    os.system('cls')
    print('\033[0m')
    os.system('cls')
    parent_name=Path.cwd().name
    def path_exists(path: str) -> bool:
        return os.path.exists(path) and os.path.isfile(path)
    print("\033[32mArrowDOS 복구 매니저\033[34m-v1.0\033[0m")
    time.sleep(2)
    cmd=''
    cd=parent_name
    while True:
        cmd=input(f'{cd} >')
        if cmd=='?':
            print('\033[32mArrowDOS\033[0m 도움말 정보를 로드하는 중...')
            print('    ? - 이 명령어는 \033[32mArrowDOS 복구 매니저\033[0m의 기능(도움말)을 불러와주는 간단한 명령어입니다.')
            print('    bootmn - 부팅 매니저를 실행합니다.')
        elif cmd=='bootmn':
            print('그 외 디스크로 부팅합니다...')
            time.sleep(1)
            print('번호로 선택하세요:')
            dir2=Path.cwd().parent
            tmplist=[]
            tmp1=0
            for name in os.listdir(dir2):
                folder_path = os.path.join(dir2, name)
                if os.path.isdir(folder_path):
                    file_path = os.path.join(folder_path, "DISKINFO")
                    if os.path.isfile(file_path):
                        tmp1+=1
                        try:
                            with open(file_path, 'r', encoding='utf-8') as df:
                                disk_desc = df.readline().strip()
                        except:
                            disk_desc = name
                        print(f'     {tmp1}. {disk_desc} ({name})')
                        tmplist.append(name)
            
            if not tmplist:
                print("\033[31m부팅 가능한 디스크가 없습니다.\033[0m")
                time.sleep(1)
                continue
                
            tmp=int(input('번호: '))
            if 1 <= tmp <= len(tmplist):
                selected_folder = tmplist[tmp - 1]
                print('부팅 중...')
                time.sleep(1)
                os.system("cls")
                boot_path = os.path.join(dir2, selected_folder, 'mainboot.py')
                subprocess.run([sys.executable, boot_path])
                break
            else:
                print('선택한 번호가 목록에 없습니다.')
                time.sleep(1)


except(Exception,KeyboardInterrupt) as e:
    print(f'error: {str(e)}')