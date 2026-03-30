# pip-wheel-kit

A simple CLI tool to download pip wheels for multiple platforms.

## Requirements

- Python 3.10+
- uv (recommended)

## Installation

```bash
uv sync
```

## Usage

### Basic

```bash
# Download specific packages
python main.py requests==2.31.0 numpy==1.26.0

# Download from requirements.txt
python main.py -r requirements.txt
```

### Options

| Option                 | Default                         | Description                 |
| ---------------------- | ------------------------------- | --------------------------- |
| `-r, --requirements`   | None                            | requirements.txt 경로       |
| `-o, --output`         | `./packages`                    | 다운로드 디렉토리           |
| `-p, --platform`       | win_amd64, manylinux2014_x86_64 | 플랫폼 지정 (여러 개 가능)  |
| `-v, --python-version` | None                            | Python 버전 (ex. 313)       |
| `--no-pure`            | False                           | pure Python 다운로드 건너뜀 |

### Examples

```bash
# 기본 실행 (3단계 자동: pure Python + win_amd64 + manylinux)
python main.py -r requirements.txt

# Python 버전 지정
python main.py -r requirements.txt -v 313

# 플랫폼 직접 지정
python main.py -r requirements.txt -p win_amd64

# 1단계(pure Python) 건너뜀
python main.py -r requirements.txt --no-pure

# 출력 디렉토리 지정
python main.py -r requirements.txt -o ./my-packages
```

## Download Stages

총 3단계로 다운로드가 진행됩니다.

1. **Pure Python & Source** - 플랫폼 무관 패키지
2. **Windows (win_amd64)** - Windows 바이너리 wheel
3. **Linux (manylinux2014_x86_64)** - Linux 바이너리 wheel
