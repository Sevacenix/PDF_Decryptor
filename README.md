# PDF Decryptor

[![Release](https://img.shields.io/github/v/release/Sevacenix/PDF_Decryptor)](https://github.com/Sevacenix/PDF_Decryptor/releases)
[![License](https://img.shields.io/github/license/Sevacenix/PDF_Decryptor)](LICENSE)

A lightweight desktop utility for detecting and removing PDF passwords in batches.

[中文说明](README.zh-CN.md)

## Download

[Download the latest macOS build](https://github.com/Sevacenix/PDF_Decryptor/releases/latest/download/PDF_Decryptor-macOS.zip)
[Download the SHA-256 checksum](https://github.com/Sevacenix/PDF_Decryptor/releases/latest/download/PDF_Decryptor-macOS.zip.sha256)

## Preview

![PDF Decryptor preview](docs/assets/pdf-decryptor-preview.svg)

## Features

- Batch import PDF files or scan a folder for PDFs
- Detect whether each file is encrypted
- Decrypt multiple files with one password
- AES-encrypted PDF support
- Save decrypted files to a selected folder
- Flexible output naming with placeholder rules
- One-click original file name export
- Password visibility toggle
- Chinese and English UI support

## Quick Start

```bash
python3 -m pip install -r requirements.txt
python3 app.py
```

## Build macOS App

```bash
brew install python@3.12 python-tk@3.12
./scripts/build_macos_app.sh
```

## Install Notes

- macOS may ask you to confirm the app on first launch
- If that happens, right-click the app and choose `Open`
- Each release also includes a `.sha256` checksum file for verification

## Output Name Pattern

- `{name}`: original file name without extension
- `{index}`: file index with leading zeros, for example `001`
- `{date}`: current date in `YYYYMMDD`

If a file with the same name already exists in the output folder, the app appends `_1`, `_2`, and so on.

Suggested screenshots and release copy are prepared in [docs/GITHUB_RELEASE_COPY.md](docs/GITHUB_RELEASE_COPY.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
