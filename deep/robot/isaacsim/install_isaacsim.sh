#!/usr/bin/env bash
#
# Isaac Sim 6.0 설치 스크립트 (pip 방식)
# - Python 3.12 venv 를 사용해 Isaac Sim 을 설치한다.
# - 최신 Isaac Sim(6.0.x)은 Python 3.12(==3.12.*)를 요구한다. (5.0=3.11, 4.5=3.10)
#
# 사용법:   ./install_isaacsim.sh
#
set -euo pipefail

# ── 설정 ─────────────────────────────────────────────────────────────
ISAACSIM_VERSION="6.0.1.0"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/venv"
PYTHON_BIN="${PYTHON_BIN:-python3.12}"   # 필요시 PYTHON_BIN=python3.12 로 지정
# ─────────────────────────────────────────────────────────────────────

echo "== Isaac Sim ${ISAACSIM_VERSION} 설치 =="
echo "프로젝트: ${PROJECT_DIR}"
echo "venv    : ${VENV_DIR}"

# 1) venv 준비 (없으면 생성)
if [ ! -x "${VENV_DIR}/bin/python" ]; then
  echo "-- venv 생성 (${PYTHON_BIN})"
  "${PYTHON_BIN}" -m venv "${VENV_DIR}"
fi

# 2) Python 버전 확인 (3.12 필수)
source "${VENV_DIR}/bin/activate"
PYVER="$(python -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')"
if [ "${PYVER}" != "3.12" ]; then
  echo "!! Python ${PYVER} 감지 — Isaac Sim ${ISAACSIM_VERSION}은 3.12가 필요합니다." >&2
  echo "   venv 를 지우고 Python 3.12 로 다시 만드세요: rm -rf '${VENV_DIR}'" >&2
  exit 1
fi
echo "-- Python ${PYVER} OK"

# 3) pip 업그레이드
python -m pip install --upgrade pip

# 4) Isaac Sim 설치 (약 15GB 다운로드)
echo "-- isaacsim[all,extscache]==${ISAACSIM_VERSION} 설치 (수 GB, 시간 소요)"
pip install "isaacsim[all,extscache]==${ISAACSIM_VERSION}" \
  --extra-index-url https://pypi.nvidia.com

# 5) 설치 검증
echo "-- import 검증"
OMNI_KIT_ACCEPT_EULA=YES python -c "import isaacsim; print('isaacsim import OK')"

echo
echo "== 설치 완료 =="
echo "기동:  ./run_stream.sh"
