#!/usr/bin/env bash
# Uploads the project to ~/whosz/tarot/ over SFTP (curl). Credentials come from ~/.config/spooooky/sftp.env.
set -euo pipefail
. ~/.config/spooooky/sftp.env
cd "$(dirname "$0")/.."
base="sftp://$SFTP_HOST:$SFTP_PORT/$SFTP_DIR"
python3 tools/bump_version.py
python3 tools/build_sw.py
find index.html manifest.webmanifest sw.js licenses.txt .htaccess css js data img fonts audio -type f 2>/dev/null | while read -r f; do
  curl -sS --ftp-create-dirs -u "$SFTP_USER:$SFTP_PASS" -T "$f" "$base/$f"
  echo "ok $f"
done
