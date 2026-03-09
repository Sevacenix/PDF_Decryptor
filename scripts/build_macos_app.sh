#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_DIR="$PROJECT_ROOT/dist"
BUILD_ROOT="/tmp/pdf_decryptor_build"
VENV_DIR="/tmp/pdf_decryptor_build_venv"
PYTHON_BIN="${PYTHON_BIN:-/opt/homebrew/bin/python3.12}"
APP_VERSION="${APP_VERSION:-1.0.1}"

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

INFO_PLIST="$BUILD_ROOT/dist/PDF_Decryptor.app/Contents/Info.plist"
set_plist_value() {
  local key="$1"
  local type="$2"
  local value="$3"

  if /usr/libexec/PlistBuddy -c "Print :$key" "$INFO_PLIST" >/dev/null 2>&1; then
    /usr/libexec/PlistBuddy -c "Set :$key $value" "$INFO_PLIST"
  else
    /usr/libexec/PlistBuddy -c "Add :$key $type $value" "$INFO_PLIST"
  fi
}

set_plist_value "CFBundleShortVersionString" "string" "$APP_VERSION"
set_plist_value "CFBundleVersion" "string" "$APP_VERSION"
set_plist_value "CFBundleIdentifier" "string" "com.sevacenix.pdfdecryptor"

# Keep old build for troubleshooting, publish fixed build to default name.
if [[ -d "$DIST_DIR/PDF_Decryptor.app" ]]; then
  rm -rf "$DIST_DIR/PDF_Decryptor-broken-system-python.app"
  mv "$DIST_DIR/PDF_Decryptor.app" "$DIST_DIR/PDF_Decryptor-broken-system-python.app"
fi

cp -R "$BUILD_ROOT/dist/PDF_Decryptor.app" "$DIST_DIR/PDF_Decryptor.app"
cp -R "$BUILD_ROOT/dist/PDF_Decryptor.app" "$DIST_DIR/PDF_Decryptor-fixed.app"

ditto -c -k --sequesterRsrc --keepParent \
  "$BUILD_ROOT/dist/PDF_Decryptor.app" \
  "$DIST_DIR/PDF_Decryptor-macOS.zip"

echo "构建完成:"
echo "  $DIST_DIR/PDF_Decryptor.app"
echo "  $DIST_DIR/PDF_Decryptor-fixed.app"
echo "  $DIST_DIR/PDF_Decryptor-macOS.zip"
