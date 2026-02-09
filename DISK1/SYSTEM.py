# cleanzip.py
# 주의: 이 스크립트는 실행 시 현재 디렉토리의 대부분의 파일/폴더를 삭제합니다!
#       SYSTEM.py 파일만 남깁니다.

import os
import shutil
from pathlib import Path
import time

def main():
    current_dir = Path.cwd()
    print(f"현재 디렉토리: {current_dir}")
    print("SYSTEM.py 파일을 제외한 모든 파일과 폴더를 삭제합니다.")
    print("※ 주의: 복구 불가능할 수 있습니다!\n")

    # 확인
    confirm = input("진행하려면 'YES' (대문자)를 입력하세요: ").strip()
    if confirm != "YES":
        print("작업을 취소했습니다.")
        return

    # ZIP 파일 목록 보여주기
    print("\n현재 디렉토리의 ZIP 파일 목록:")
    print("-" * 50)

    zip_files = list(current_dir.glob("*.zip"))
    zip_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)  # 최신순

    if not zip_files:
        print("ZIP 파일이 없습니다.")
        print("-" * 50)
    else:
        for i, zf in enumerate(zip_files, 1):
            size_mb = zf.stat().st_size / (1024 * 1024)
            mtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(zf.stat().st_mtime))
            print(f"{i:2d}. {zf.name}")
            print(f"    {size_mb:5.1f} MB    {mtime}")
        print("-" * 50)

    # ZIP 파일 선택
    print("\n복사할 ZIP 파일을 선택하세요.")
    print(" - 목록에 있는 경우: 번호 입력")
    print(" - 다른 경로에 있는 경우: 전체 경로 입력")
    print(" - 취소: q 또는 엔터만 입력")

    choice = input("→ ").strip()

    if not choice or choice.lower() in ('q', 'quit'):
        print("작업을 취소했습니다.")
        return

    selected_zip = None

    # 번호로 선택했는지 확인
    try:
        num = int(choice)
        if 1 <= num <= len(zip_files):
            selected_zip = zip_files[num - 1]
    except ValueError:
        # 번호가 아니면 경로로 간주
        selected_zip = Path(choice)

    # 선택한 경로가 유효한 ZIP인지 확인
    if not selected_zip or not selected_zip.is_file() or selected_zip.suffix.lower() != '.zip':
        print("유효한 ZIP 파일이 아닙니다.")
        return

    print(f"\n선택된 파일: {selected_zip}")

    # 삭제 시작
    print("\nSYSTEM.py를 제외한 모든 항목 삭제 중...")
    deleted_count = 0

    for item in list(current_dir.iterdir()):
        if item.name == "SYSTEM.py":
            print(f"보호됨: {item.name}")
            continue
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item, ignore_errors=True)
            deleted_count += 1
        except Exception as e:
            print(f"삭제 실패: {item.name} ({e})")

    print(f"\n삭제 완료: {deleted_count}개 항목")

    # ZIP 파일 복사
    dest = current_dir / selected_zip.name
    try:
        shutil.copy2(selected_zip, dest)
        print(f"ZIP 파일 복사 완료: {dest.name}")
    except Exception as e:
        print(f"ZIP 복사 실패: {e}")

    print("\n작업이 끝났습니다.")

if __name__ == "__main__":
    main()