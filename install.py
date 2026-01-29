# install.py
from pathlib import Path
import zipfile
import time
import random
import shutil

from textual.app import App, ComposeResult, on
from textual.widgets import (
    Header, Footer, Static, Label, Button, Checkbox, ProgressBar,
    RichLog
)
from textual.containers import Horizontal, Center, Container
from textual.screen import Screen


class WelcomeScreen(Screen):
    """첫 화면: 설치 시작"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label(
                """
ArrowDOS v1.0 build5.20260129

설치 프로그램을 시작합니다...
                """.strip(),
                classes="title"
            ),
            Center(
                Static("잠시만 기다려 주십시오...", id="status"),
            ),
            id="welcome"
        )
        yield Footer()

    def on_mount(self) -> None:
        # 2초 후 자동으로 다음 화면으로 이동
        time.sleep(2.0)
        self.app.push_screen(ComponentSelectScreen())


class ComponentSelectScreen(Screen):
    """구성 요소 선택 화면"""

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("구성 요소 선택", classes="title"),
            Static("설치할 구성 요소를 선택하세요:", classes="subtitle"),
            Checkbox("앱 포함", value=False, id="include_apps"),
            Static(" "),
            Horizontal(
                Button("뒤로", id="back"),
                Button("설치 시작", variant="primary", id="install"),
            ),
            id="components"
        )
        yield Footer()

    @on(Button.Pressed, "#back")
    def go_back(self):
        self.app.pop_screen()

    @on(Button.Pressed, "#install")
    def start_install(self):
        include_apps = self.query_one("#include_apps", Checkbox).value
        self.app.push_screen(InstallProgressScreen(include_apps))


class InstallProgressScreen(Screen):
    def __init__(self, include_apps: bool):
        super().__init__()
        self.include_apps = include_apps

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Label("ArrowDOS 설치 중", classes="title"),
            Static("DISK1에 파일을 복사하고 있습니다...", classes="subtitle"),
            ProgressBar(id="pb", show_percentage=True, show_eta=False),
            RichLog(id="log", markup=True, highlight=False, max_lines=15),
            id="installing"
        )
        yield Footer()

    def on_mount(self) -> None:
        self.start_installation()

    def start_installation(self):
        log = self.query_one(RichLog)
        pb = self.query_one(ProgressBar)

        zip_path = Path("main.adi")
        extract_dir = Path("DISK1")

        extract_dir.mkdir(exist_ok=True)
        log.write(f"[white]설치 대상: {extract_dir.resolve()}[/white]")

        if not zip_path.is_file():
            log.write("[red]오류: 설치 이미지 파일이 없습니다.[/]")
            return

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                members = zf.infolist()
                total = len(members)
                count = 0

                for i, member in enumerate(members):
                    count += 1
                    percent = (count / total) * 100

                    fname = member.filename
                    is_dir = fname.endswith('/')
                    status_prefix = "[yellow]복사중[/yellow]" if not is_dir else "[yellow]폴더 생성중[/yellow]"

                    short = fname[:45] + "..." if len(fname) > 45 else fname
                    log.write(f"{status_prefix}: {short}")

                    zf.extract(member, path=extract_dir)

                    log.write(f"[green]완료[/green]: {short}")

                    pb.progress = percent

                    time.sleep(0.02 + random.uniform(0, 0.06))

            log.write("\n[bright_green]설치 완료![/bright_green]")
            log.write("[white]ArrowDOS v1.0 build5.20260129 설치가 성공적으로 완료되었습니다.[/]")

            if not self.include_apps:
                local_programs = extract_dir / "LOCAL-PROGRAMS"
                if local_programs.exists():
                    shutil.rmtree(local_programs)
                    log.write("[yellow]앱 포함 옵션 OFF: LOCAL-PROGRAMS 폴더 삭제 완료[/yellow]")

            log.write("[dim]DISK1 폴더에서 ArrowDOS를 실행할 수 있습니다.[/]")

        except Exception as e:
            log.write(f"[red]설치 오류: {str(e)}[/red]")


class ArrowDOSInstaller(App):
    CSS = """
    Screen {
        background: #000080;
    }

    Header, Footer {
        background: #000080;
        color: #ffffff;
    }

    .title {
        text-align: center;
        text-style: bold;
        color: white;
        margin: 1;
        padding: 1;
        background: #000040;
        border: tall #c0c0c0;
    }

    .subtitle {
        margin: 1 2;
        color: #c0c0c0;
        text-align: center;
    }

    Container {
        width: 80%;
        height: auto;
        margin: 1;
        background: #000000;
        border: tall #c0c0c0;
        padding: 1;
    }

    Checkbox {
        margin: 1 2;
        color: #ffffff;
    }

    Button {
        margin: 1 2;
        width: 20;
    }

    RichLog {
        height: 12;
        margin: 1;
        background: #000000;
        color: #c0c0c0;
        border: tall #808080;
    }

    ProgressBar {
        margin: 1 2;
        color: #00ff00;
        background: #000000;
    }

    Static {
        color: #c0c0c0;
    }
    """

    def compose(self) -> ComposeResult:
        yield WelcomeScreen()

    def on_mount(self) -> None:
        self.title = "ArrowDOS v1.0 build5.20260129 설치"


if __name__ == "__main__":
    app = ArrowDOSInstaller()
    app.run()