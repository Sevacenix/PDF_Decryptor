# PDF Decryptor

A lightweight desktop utility for detecting and removing PDF passwords in batches.

[中文说明](README.zh-CN.md)

## Overview

PDF Decryptor is a small GUI tool built with `tkinter` and `pypdf`. It is designed for people who need a simple desktop workflow instead of command-line scripts.

## Features

- Batch import PDF files or scan a folder for PDFs
- Detect whether each file is encrypted
- Decrypt multiple files with one password
- Save output files to a selected folder
- Customize output file names with placeholders
- Use the original file name with one click
- Show or hide the password while typing
- Chinese and English interface support
- AES-encrypted PDF support

## Interface Language

The app now supports both Chinese and English.

- It automatically defaults to Chinese on Chinese systems and English otherwise
- You can switch the UI language directly inside the app
- You can also start it in English with `python3 app.py --lang en`

## Requirements

```bash
python3 -m pip install -r requirements.txt
```

## Run

```bash
python3 app.py
```

## Build macOS App

For macOS packaging, use the Homebrew Python runtime instead of the system Python runtime:

```bash
brew install python@3.12 python-tk@3.12
./scripts/build_macos_app.sh
```

The build script generates a macOS app and a release zip under `dist/`.

## Output Name Pattern

Supported placeholders:

- `{name}`: original file name without extension
- `{index}`: file index with leading zeros, for example `001`
- `{date}`: current date in `YYYYMMDD`

Examples:

- `{name}_decrypted`
- `{date}_{index}_{name}`
- `{name}`

If a file with the same name already exists in the output folder, the app appends `_1`, `_2`, and so on.

## GitHub Release Assets

Suggested release asset:

- `PDF_Decryptor-macOS-brew-fixed.zip`

Suggested screenshots and release copy are prepared in [docs/GITHUB_RELEASE_COPY.md](docs/GITHUB_RELEASE_COPY.md).

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
