from pathlib import Path
import zipfile
import asyncio
import os
import sys
import subprocess

from textual.app import App, ComposeResult, on
from textual.widgets import (
    Static, Label, Button, ProgressBar, RichLog, Digits, RadioSet, RadioButton
)
from textual.containers import Horizontal, Center, Container, Vertical
from textual.screen import ModalScreen
from textual.events import MouseDown, MouseMove, MouseUp
from textual.binding import Binding


def get_exe_dir() -> Path:
    """실행 파일(또는 스크립트)이 위치한 디렉토리를 반환합니다."""
    if getattr(sys, "frozen", False):
        # PyInstaller 등으로 패키징된 경우
        return Path(sys.executable).parent
    else:
        # 일반 .py 스크립트로 실행된 경우
        return Path(__file__).parent


EXE_DIR = get_exe_dir()
os.chdir(EXE_DIR)  # 작업 디렉토리를 실행 파일 위치로 변경


class DraggableWin95(Container):
    """마우스 드래그로 이동 가능한 Windows 95 스타일 창"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dragging = False
        self.mouse_x = 0
        self.mouse_y = 0

    def on_mouse_down(self, event: MouseDown) -> None:
        if event.y < 2: 
            self.dragging = True
            self.capture_mouse()
            self.mouse_x = event.screen_x
            self.mouse_y = event.screen_y

    def on_mouse_move(self, event: MouseMove) -> None:
        if self.dragging:
            dx = event.screen_x - self.mouse_x
            dy = event.screen_y - self.mouse_y
            new_x = self.styles.offset.x.value + dx
            new_y = self.styles.offset.y.value + dy
            self.styles.offset = (new_x, new_y)
            self.mouse_x = event.screen_x
            self.mouse_y = event.screen_y

    def on_mouse_up(self, event: MouseUp) -> None:
        if self.dragging:
            self.dragging = False
            self.release_mouse()

class WelcomeScreen(ModalScreen):
    """1단계: 환영 화면"""
    def compose(self) -> ComposeResult:
        with DraggableWin95(id="welcome-box"):
            yield Label(" 🗔 ArrowDOS v1.0 Setup", classes="win-title")
            with Vertical(classes="content-area"):
                yield Label("ArrowDOS 설치 마법사", classes="main-heading")
                yield Static(
                    "ArrowDOS v1.0 설치 프로그램에 오신 것을 환영합니다.\n\n"
                    "이 프로그램은 사용자의 컴퓨터에 ArrowDOS를 설치합니다.\n"
                    "계속하시려면 [다음 >] 버튼을 눌러주십시오.",
                    classes="description"
                )
                with Center():
                    yield Digits("2026", id="year-bg")
            
            with Horizontal(classes="button-row"):
                yield Static("", classes="flex-spacer")
                yield Button("다음 >", variant="primary", id="next-to-select")
                yield Button("취소", id="exit")

    @on(Button.Pressed, "#next-to-select")
    def go_to_select(self):
        disk1_path = EXE_DIR / "DISK1"
        boot_path = disk1_path / "mainboot.py"
        if disk1_path.exists() and boot_path.exists():
            self.app.push_screen(AlreadyInstalledScreen())
        else:
            self.app.push_screen(VersionSelectScreen())

    @on(Button.Pressed, "#exit")
    def exit_app(self):
        self.app.exit()

class AlreadyInstalledScreen(ModalScreen):
    """DISK1이 이미 존재할 때: 실행 or 재설치 선택"""

    def compose(self) -> ComposeResult:
        with DraggableWin95(id="already-box"):
            yield Label(" 🗔 ArrowDOS - 이미 설치됨", classes="win-title")
            with Vertical(classes="content-area"):
                yield Label("설치된 버전이 감지되었습니다", classes="main-heading")
                yield Static(
                    f"경로: {EXE_DIR / 'DISK1'}\n\n"
                    "ArrowDOS가 이미 설치되어 있습니다.\n"
                    "실행하시겠습니까, 아니면 재설치하시겠습니까?",
                    classes="description"
                )
            with Horizontal(classes="button-row"):
                yield Static("", classes="flex-spacer")
                yield Button("▶ 실행", variant="primary", id="do-launch")
                yield Button("🔄 재설치", id="do-reinstall")
                yield Button("취소", id="exit")

    @on(Button.Pressed, "#do-launch")
    def launch(self):
        self.app.exit(result="LAUNCH")

    @on(Button.Pressed, "#do-reinstall")
    def reinstall(self):
        self.app.pop_screen()          # WelcomeScreen으로 돌아감
        self.app.push_screen(VersionSelectScreen())

    @on(Button.Pressed, "#exit")
    def cancel(self):
        self.app.exit()


class VersionSelectScreen(ModalScreen):
    """2단계: 버전 선택 화면"""
    def compose(self) -> ComposeResult:
        # 실행 파일 위치 기준으로 .adi 탐색
        self.adi_files = list(EXE_DIR.glob("*.adi"))
        
        with DraggableWin95(id="select-box"):
            yield Label(" 🗔 버전 선택 - ArrowDOS Setup", classes="win-title")
            with Vertical(classes="content-area"):
                yield Label("설치할 버전을 선택하십시오", classes="main-heading")
                
                if not self.adi_files:
                    yield Static(
                        f"⚠️ 설치 파일(.adi)을 찾을 수 없습니다.\n"
                        f"탐색 경로: {EXE_DIR}\n\n"
                        "데모 모드로 진행됩니다.",
                        classes="error-text"
                    )
                else:
                    yield Label(f"사용 가능한 패키지 목록: ({EXE_DIR})", classes="sub-heading")
                    with RadioSet(id="version-selector"):
                        for i, file in enumerate(self.adi_files):
                            yield RadioButton(file.stem, value=(i == 0), id=f"file_{i}")
                
                yield Static("\n버전을 선택한 후 [설치 시작]을 눌러주십시오.", classes="description")
            
            with Horizontal(classes="button-row"):
                yield Static("", classes="flex-spacer")
                yield Button("< 뒤로", id="back-to-welcome")
                yield Button("설치 시작", variant="primary", id="start-install")

    @on(Button.Pressed, "#back-to-welcome")
    def go_back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#start-install")
    def go_install(self):
        selected_file = None
        if hasattr(self, "adi_files") and self.adi_files:
            rs = self.query_one(RadioSet)
            if rs.pressed_index >= 0:
                selected_file = self.adi_files[rs.pressed_index]
        
        self.app.push_screen(InstallProgressScreen(selected_file))

class InstallProgressScreen(ModalScreen):
    """3단계: 실제 설치 진행 화면"""
    def __init__(self, target_file: Path = None):
        super().__init__()
        self.target_file = target_file

    def compose(self) -> ComposeResult:
        with DraggableWin95(id="install-box"):
            yield Label(" 🗔 ArrowDOS 설치 중...", classes="win-title")
            with Vertical(classes="content-area"):
                yield Label("설치 준비 중...", id="status-text")
                yield ProgressBar(id="pb", show_percentage=True, show_eta=False)
                yield RichLog(id="log", markup=True, highlight=True)
            with Horizontal(classes="button-row"):
                yield Static("", classes="flex-spacer")
                yield Button("마침", id="finish", disabled=True)

    def on_mount(self) -> None:
        self.run_worker(self.do_installation, thread=True)

    async def do_installation(self) -> None:
        log = self.query_one(RichLog)
        pb = self.query_one(ProgressBar)
        status = self.query_one("#status-text", Label)
        
        # 설치 대상 경로도 실행 파일 기준으로 설정
        self.base_path = EXE_DIR

        try:
            log.write("🚀 [bold white]설치 프로세스 시작...[/]")
            log.write(f"📂 설치 경로: [cyan]{self.base_path}[/]")
            
            if self.target_file is None or not self.target_file.is_file():
                log.write("[yellow]⚠️ 선택된 설치 파일이 없어 시뮬레이션을 진행합니다.[/]")
                sim_disk = self.base_path / "DISK1"
                sim_disk.mkdir(exist_ok=True)
                
                steps = ["시스템 커널 복사", "기본 명령어 구성", "레지스트리 설정", "정리 작업"]
                for i, step in enumerate(steps):
                    status.update(f"작업 중: {step}")
                    log.write(f"⚙️ {step}...")
                    await asyncio.sleep(0.5)
                    pb.advance(25)
                
                boot_script = sim_disk / "mainboot.py"
                with open(boot_script, "w", encoding="utf-8") as f:
                    f.write("import os\nprint('ArrowDOS 데모 모드 가동!')\ninput()")
            else:
                log.write(f"📦 [bold cyan]{self.target_file.name}[/] 분석 및 해제...")
                try:
                    with zipfile.ZipFile(self.target_file, 'r') as zf:
                        members = zf.infolist()
                        total = len(members)
                        
                        first_member = members[0].filename
                        if first_member.startswith("DISK1/"):
                            log.write("🔍 파일 구조 내 'DISK1' 폴더를 감지했습니다. 최상위에 바로 설치합니다.")
                            extract_target = self.base_path
                        else:
                            log.write("🔍 'DISK1' 폴더가 감지되지 않았습니다. 폴더를 생성하여 설치합니다.")
                            extract_target = self.base_path / "DISK1"
                            extract_target.mkdir(exist_ok=True)

                        for i, member in enumerate(members):
                            is_dir = member.is_dir() or member.filename.endswith('/')
                            status.update(f"추출 중: {member.filename}")
                            
                            zf.extract(member, path=extract_target)
                            
                            pb.progress = ((i + 1) / total) * 100
                            if is_dir:
                                log.write(f"  📁 {member.filename}")
                            else:
                                log.write(f"  📄 {member.filename}")
                                
                            await asyncio.sleep(0.01)
                            
                except (zipfile.BadZipFile, PermissionError) as e:
                    log.write(f"[red]❌ 오류 발생: {str(e)}[/]")
                    status.update("설치 실패")
                    return

            status.update("설치 완료!")
            log.write("\n[bright_green]✨ 설치가 성공적으로 끝났습니다![/]")
            self.query_one("#finish", Button).disabled = False

        except Exception as e:
            log.write(f"[red]❌ 예외 발생: {str(e)}[/]")
            status.update("시스템 오류")

    @on(Button.Pressed, "#finish")
    def finish(self):
        self.app.exit(result="LAUNCH")

class ArrowDOSInstaller(App):
    TITLE = "ArrowDOS Setup"
    BINDINGS = [Binding("q", "quit", "Quit")]

    CSS = """
    Screen {
        background: #008080;
        align: center middle;
    }

    DraggableWin95 {
        width: 70;
        height: 30;
        background: #c0c0c0;
        border: tall #ffffff;
        padding: 0;
    }

    .win-title {
        width: 100%;
        background: #000080;
        color: white;
        text-style: bold;
        padding: 0 1;
    }

    .content-area {
        height: 1fr;
        padding: 1 2;
        border: tall #808080;
        margin: 1;
        background: #c0c0c0;
        overflow-y: auto;
    }

    .main-heading {
        text-style: bold;
        margin-bottom: 1;
        color: black;
    }

    .sub-heading {
        color: #000080;
        text-style: bold;
        margin-top: 1;
    }

    .error-text {
        color: #ff0000;
        text-style: italic;
    }

    Static, Label {
        color: black;
    }

    #version-selector {
        background: #ffffff;
        border: tall #808080;
        margin: 1 0;
        padding: 0 1;
        color: black;
    }

    RadioButton {
        color: black;
    }

    #year-bg {
        color: #888888;
        margin-top: 1;
    }

    .button-row {
        height: 3;
        padding: 0 1;
        margin-bottom: 1;
    }

    .flex-spacer {
        width: 1fr;
    }

    Button {
        margin-left: 1;
        min-width: 14;
        background: #c0c0c0;
        color: black;
        border: tall #ffffff;
    }

    Button:hover {
        background: #d0d0d0;
    }

    RichLog {
        background: #000000;
        color: #00ff00;
        border: tall #808080;
        margin-top: 1;
        height: 1fr;
    }

    ProgressBar {
        width: 100%;
        margin: 1 0;
    }
    """

    def on_mount(self) -> None:
        self.push_screen(WelcomeScreen())

if __name__ == "__main__":
    app = ArrowDOSInstaller()
    result = app.run()

    boot_path = EXE_DIR / "DISK1" / "mainboot.py"

    if result in ("LAUNCH", str(boot_path)):
        # ── 터미널 완전 초기화 ──────────────────────────────────────────
        # 1) ANSI 이스케이프: 화면 지우기 + 커서 홈 + 속성 리셋
        sys.stdout.write("\033[2J\033[H\033[0m")
        sys.stdout.flush()

        # 2) Unix 계열: stty sane 으로 터미널 모드 복구
        if sys.platform != "win32":
            os.system("stty sane")

        # 3) Windows: cls
        else:
            os.system("cls")

        # ── mainboot.py 서브프로세스 실행 ──────────────────────────────
        subprocess.run([sys.executable, str(boot_path)])