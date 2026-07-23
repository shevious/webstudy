#!/usr/bin/env bash
#
# Isaac Sim WebRTC 스트리밍 서버 기동 스크립트 (헤드리스)
# Mac 등 원격 클라이언트에서 WebRTC Streaming Client 로 접속해 사용한다.
#
# 사용법:
#   ./run_stream.sh                 # 아래 기본값으로 기동 (GPU 3번 사용)
#   PUBLIC_IP=1.2.3.4 ./run_stream.sh
#   CUDA_VISIBLE_DEVICES=1 ./run_stream.sh
#   ./run_stream.sh --bg            # 백그라운드로 기동, 로그는 stream.log
#
# 중요:
#   - 공유기 포트포워딩은 반드시 1:1 동일 포트로 (WebRTC 요구사항).
#       TCP  SIGNAL_PORT(외부) -> 192.168.2.74 SIGNAL_PORT(내부)
#       UDP  STREAM_PORT(외부) -> 192.168.2.74 STREAM_PORT(내부)
#   - PUBLIC_IP 를 공인 IP 로 설정해야 원격에서 검은 화면이 안 뜬다.
#   - TCP 만 열면 안 되고 UDP(미디어)도 반드시 열려 있어야 한다.
#
set -euo pipefail

# ── 설정 (환경변수로 덮어쓰기 가능) ──────────────────────────────────
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${PROJECT_DIR}/venv"
PUBLIC_IP="${PUBLIC_IP:-192.168.2.48}"   # 공인 IP (sw112.iptime.org)
SIGNAL_PORT="${SIGNAL_PORT:-49101}"        # WebRTC 시그널링 (TCP)
STREAM_PORT="${STREAM_PORT:-47999}"        # WebRTC 미디어    (UDP)
LOG_FILE="${LOG_FILE:-${PROJECT_DIR}/stream.log}"
CUDA_VISIBLE_DEVICES="${CUDA_VISIBLE_DEVICES:-3}"  # 사용할 GPU 인덱스
# ─────────────────────────────────────────────────────────────────────

if [ ! -x "${VENV_DIR}/bin/python" ]; then
  echo "!! venv 가 없습니다: ${VENV_DIR}" >&2
  echo "   먼저 ./install_isaacsim.sh 를 실행하세요." >&2
  exit 1
fi

# 기존 스트리밍 서버가 떠 있으면 종료
if pgrep -f "isaacsim.exp.full.streaming" >/dev/null; then
  echo "-- 기존 스트리밍 서버 종료"
  pkill -f "isaacsim.exp.full.streaming" || true
  sleep 3
  pkill -9 -f "isaacsim.exp.full.streaming" 2>/dev/null || true
  sleep 1
fi

echo "== Isaac Sim WebRTC 스트리밍 기동 =="
echo "  publicIp   : ${PUBLIC_IP}"
echo "  signalPort : ${SIGNAL_PORT} (TCP)"
echo "  streamPort : ${STREAM_PORT} (UDP)"
echo "  GPU        : ${CUDA_VISIBLE_DEVICES}"
echo "  로그       : ${LOG_FILE}"
echo "  클라이언트 : Server IP=${PUBLIC_IP} (또는 sw112.iptime.org), 포트 ${SIGNAL_PORT}"
echo

source "${VENV_DIR}/bin/activate"

CMD=(isaacsim isaacsim.exp.full.streaming --no-window
  "--/exts/omni.kit.livestream.app/primaryStream/publicIp=${PUBLIC_IP}"
  "--/exts/omni.kit.livestream.app/primaryStream/signalPort=${SIGNAL_PORT}"
  "--/exts/omni.kit.livestream.app/primaryStream/streamPort=${STREAM_PORT}")

export OMNI_KIT_ACCEPT_EULA=YES
export CUDA_VISIBLE_DEVICES

if [ "${1:-}" = "--bg" ]; then
  nohup "${CMD[@]}" > "${LOG_FILE}" 2>&1 &
  echo "-- 백그라운드 기동 (PID $!). 로그: tail -f ${LOG_FILE}"
  echo "   포트 확인: ss -tln | grep ${SIGNAL_PORT}"
else
  exec "${CMD[@]}"
fi
