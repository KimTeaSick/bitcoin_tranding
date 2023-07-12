#!/bin/bash

# 프로세스 이름
process_name="trailingStop.py"

# 프로세스 실행 여부 확인 함수
check_process_running() {
    process_count=$(ps aux | grep -v grep | grep "$process_name" | wc -l)
    if [ $process_count -eq 0 ]; then
        return 1
    else
        return 0
    fi
}

# 특정 프로세스가 실행되지 않을 때 재실행하는 함수
restart_process() {
    echo "프로세스를 다시 시작합니다."
    # 프로세스 실행 명령어를 여기에 작성
    # 예: python your_script.py
    nohup /bin/python3 /data/4season/bitcoin_trading_back/trailingStop/trailingStop.py &
}
if check_process_running; then
    echo "프로세스가 실행 중입니다."
else
    restart_process
fi
