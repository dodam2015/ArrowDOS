import time
import pygame
import sys
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.progress import Progress, BarColumn, TextColumn
from rich.live import Live
from rich.table import Table
console = Console()
def play_sound():
    try:
        pygame.mixer.init()
        # 파일이 없을 경우를 대비해 예외 처리
        pygame.mixer.music.load('start.mp3')
        pygame.mixer.music.play()
    except Exception:
        pass
def make_layout():
    layout = Layout()
    # 화면을 상(header), 중(main), 하(footer)로 분할
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
        Layout(name="footer", size=3),
    )
    # 중간 부분을 왼쪽 메뉴(side)와 본문(body)으로 분할
    layout["main"].split_row(
        Layout(name="side", size=22),
        Layout(name="body", ratio=1),
    )
    return layout
def boot_arrow_dos():
    layout = make_layout()
    
    # 헤더 설정
    layout["header"].update(Panel(Align.center("[bold white]ArrowDos GUI Environment v1.0[/]"), style="white on blue"))
    
    # 사이드바 설정 (간단한 메뉴 테이블)
    menu_table = Table.grid(padding=1)
    menu_table.add_column(style="cyan")
    menu_table.add_row("📂 System")
    menu_table.add_row("💾 Files")
    menu_table.add_row("🌐 Network")
    menu_table.add_row("⚙️ Settings")
    layout["side"].update(Panel(menu_table, title="[bold]Menu[/]", border_style="bright_blue"))
    # 푸터 설정 (오류 났던 textAlign 대신 Align.center 사용)
    layout["footer"].update(Panel(Align.center("F1: Help | F10: Exit | [yellow]System Status: Booting...[/]"), border_style="white"))
    play_sound()
    with Live(layout, refresh_per_second=12, screen=True):
        # 1단계: 커널 및 시스템 드라이버 로드 시뮬레이션
        boot_log = "[green]OK[/] Kernel Loaded\n[green]OK[/] File System Mounted\n[green]OK[/] Audio Driver: start.mp3 playing..."
        layout["body"].update(Panel(boot_log, title="Boot Console", border_style="green"))
        time.sleep(1.5)
        # 2단계: GUI 로딩 프로그레스 바
        progress = Progress(
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=None),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        )
        task = progress.add_task("Loading Interface...", total=100)
        
        layout["body"].update(Panel(Align.center(progress, vertical="middle"), title="System Loading"))
        while not progress.finished:
            progress.update(task, advance=1.5)
            time.sleep(0.04)
        # 3단계: 최종 부팅 완료 화면
        success_msg = "\n\n[bold green]WELCOME TO ARROWDOS[/]\n\n[white]The terminal GUI is now active and ready.[/]"
        layout["body"].update(Panel(Align.center(success_msg, vertical="middle"), border_style="bright_magenta", title="Desktop"))
        layout["footer"].update(Panel(Align.center("[bold black on green] SYSTEM ONLINE [/]"), border_style="green"))
        
        # 잠시 결과를 볼 수 있게 대기
        time.sleep(3)
if __name__ == "__main__":
    boot_arrow_dos()