#!/bin/bash

INPUT_FILE=$1

# 입력 없으면 에러
if [ -z "$INPUT_FILE" ]; then
  echo "Usage: $0 <docker-compose.yml 경로>"
  exit 1
fi

# 이 스크립트가 있는 디렉토리
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# update_compose.py 호출
python3 "$SCRIPT_DIR/update_compose.py" "$1"