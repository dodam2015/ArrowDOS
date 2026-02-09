import sys, os, time, subprocess
from tqdm import tqdm
from pathlib import Path
import zipfile
dir=Path.cwd()
print("시스템 복원 지점 생성 중...")
try:
    timestamp = time.strftime("%Y%m%d-%H-%M-%S")
    zip_path = os.path.join(dir,'SYS32' ,'restore point',f"ArrowDOS_{timestamp}.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in dir.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(dir.parent)
                zf.write(file, arcname)
    
    print(f"시스템 복원 지점 설정 완료")
    print("시스템 복원 지점이 저장되었습니다.")
except Exception as e:
    print(f"시스템 복원 지점 설정 실패: {e}")