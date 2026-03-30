import ensurepip
import subprocess
import sys
from pathlib import Path


def ensure_pip():
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "--version"], check=True, capture_output=True
        )
    except subprocess.CalledProcessError:
        print("pip not found, installing...")
        ensurepip.bootstrap(upgrade=True)
        print("pip installed!")


DEFAULT_PLATFORMS = ["win_amd64", "manylinux2014_x86_64"]


def pip_download_no_platform(
    packages: list[str],
    output_dir: Path,
    requirements: Path = None,
):
    """1단계: pure Python + 현재 OS wheel"""
    print("\n📦 [1/3] Downloading pure Python wheels & source distributions...")
    cmd = [sys.executable, "-m", "pip", "download", "-d", str(output_dir)]

    if requirements:
        cmd += ["-r", str(requirements)]

    cmd += list(packages)
    subprocess.run(cmd, check=True)


def pip_download_with_platform(
    packages: list[str],
    output_dir: Path,
    platforms: list[str],
    python_version: str = None,
    requirements: Path = None,
):
    """2~3단계: 플랫폼별 바이너리 wheel"""
    for i, platform in enumerate(platforms, start=2):
        print(f"\n🖥️  [{i}/{len(platforms) + 1}] Downloading for platform: {platform}")
        cmd = [sys.executable, "-m", "pip", "download", "-d", str(output_dir)]

        if requirements:
            cmd += ["-r", str(requirements)]

        cmd += list(packages)
        cmd += ["--platform", platform, "--only-binary=:all:"]

        if python_version:
            cmd += ["--python-version", python_version]

        subprocess.run(cmd, check=True)


def main():
    ensure_pip()

    try:
        import click
    except ImportError:
        subprocess.run([sys.executable, "-m", "pip", "install", "click"], check=True)
        import click

    @click.command()
    @click.argument("packages", nargs=-1, required=False)
    @click.option(
        "-r",
        "--requirements",
        default=None,
        type=click.Path(exists=True),
        help="requirements.txt 경로",
    )
    @click.option(
        "-o",
        "--output",
        default="./packages",
        show_default=True,
        help="다운로드 디렉토리",
    )
    @click.option(
        "-p",
        "--platform",
        "platforms",
        multiple=True,
        help="플랫폼 지정 (여러 개 가능). 미지정시 win_amd64 + manylinux2014_x86_64",
    )
    @click.option("-v", "--python-version", default=None, help="ex) 313, 314")
    @click.option(
        "--no-pure",
        is_flag=True,
        default=False,
        help="1단계(pure Python) 다운로드 건너뜀",
    )
    def cli(packages, requirements, output, platforms, python_version, no_pure):
        """pip wheel downloader"""

        if not packages and not requirements:
            raise click.UsageError(
                "패키지 이름 또는 --requirements 파일을 지정해주세요."
            )

        output_dir = Path(output)
        output_dir.mkdir(parents=True, exist_ok=True)

        resolved_platforms = list(platforms) if platforms else DEFAULT_PLATFORMS
        req_path = Path(requirements) if requirements else None

        print(f"🎯 Platforms: {', '.join(resolved_platforms)}")
        print(f"📁 Output: {output_dir}")

        # 1단계: pure Python
        if not no_pure:
            pip_download_no_platform(list(packages), output_dir, req_path)

        # 2~3단계: 플랫폼별 바이너리
        pip_download_with_platform(
            list(packages), output_dir, resolved_platforms, python_version, req_path
        )

        print("\n✅ Done!")

    cli()


if __name__ == "__main__":
    main()
