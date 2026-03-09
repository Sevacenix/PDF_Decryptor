#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_ROOT="/tmp/pdf_decryptor_build"
VENV_DIR="/tmp/pdf_decryptor_build_venv"
PYTHON_BIN="${PYTHON_BIN:-/opt/homebrew/bin/python3.12}"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "未找到可用 Python: $PYTHON_BIN"
  echo "请先安装: brew install python@3.12 python-tk@3.12"
  exit 1
fi

echo "使用 Python: $PYTHON_BIN"
"$PYTHON_BIN" - <<'PY'
import tkinter as tk
r = tk.Tk()
r.withdraw()
r.destroy()
print("tkinter runtime ok")
PY

rm -rf "$BUILD_ROOT" "$VENV_DIR"
mkdir -p "$BUILD_ROOT" "$DIST_DIR"
cp "$PROJECT_ROOT/app.py" "$BUILD_ROOT/"
cp "$PROJECT_ROOT/requirements.txt" "$BUILD_ROOT/"

"$PYTHON_BIN" -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip >/dev/null
"$VENV_DIR/bin/pip" install -r "$BUILD_ROOT/requirements.txt" pyinstaller >/dev/null

cd "$BUILD_ROOT"
"$VENV_DIR/bin/python" -m PyInstaller --noconfirm --clean --windowed --name PDF_Decryptor app.py

# Keep old build for troubleshooting, publish fixed build to default name.
if [[ -d "$DIST_DIR/PDF_Decryptor.app" ]]; then
  rm -rf "$DIST_DIR/PDF_Decryptor-broken-system-python.app"
  mv "$DIST_DIR/PDF_Decryptor.app" "$DIST_DIR/PDF_Decryptor-broken-system-python.app"
fi

cp -R "$BUILD_ROOT/dist/PDF_Decryptor.app" "$DIST_DIR/PDF_Decryptor.app"
cp -R "$BUILD_ROOT/dist/PDF_Decryptor.app" "$DIST_DIR/PDF_Decryptor-fixed.app"

ditto -c -k --sequesterRsrc --keepParent \
  "$BUILD_ROOT/dist/PDF_Decryptor.app" \
  "$DIST_DIR/PDF_Decryptor-macOS-brew-fixed.zip"

echo "构建完成:"
echo "  $DIST_DIR/PDF_Decryptor.app"
echo "  $DIST_DIR/PDF_Decryptor-fixed.app"
echo "  $DIST_DIR/PDF_Decryptor-macOS-brew-fixed.zip"
