#!/usr/bin/env bash
# Đăng bài blog đến hạn lên suoncaykhonglo.vn.
# Chạy tự động mỗi ngày bằng Task Scheduler (tác vụ "BepKhoi-DangBai").
# Chạy tay: mở Git Bash rồi gõ  bash /c/SEODALATNOW/bep-khoi/tools/dang-bai.sh

REPO="/c/SEODALATNOW/bep-khoi"
LOG="$REPO/tools/dang-bai.log"
PY="/c/Users/HP/AppData/Local/Programs/Python/Python311/python.exe"
export PATH="/mingw64/bin:/usr/bin:/c/Program Files/Git/cmd:$PATH"

log() { echo "$(date '+%Y-%m-%d %H:%M:%S') $1" >> "$LOG"; }

cd "$REPO" || exit 1
# Máy vừa bật thì mạng có thể chưa sẵn sàng: chờ tối đa 10 phút
for i in $(seq 1 30); do
  curl -s -o /dev/null -m 10 https://github.com && break
  [ "$i" = 1 ] && log "Chua co mang, cho ket noi..."
  sleep 20
done
# Lấy về thay đổi mới trên GitHub (nếu có) trước khi đăng
git pull -q --ff-only >> "$LOG" 2>&1 || log "Canh bao: git pull khong thanh cong, van tiep tuc"
"$PY" -X utf8 tools/dang_bai.py
