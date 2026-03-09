# PDF 解密器

一个轻量级桌面工具，用来批量检测 PDF 是否加密，并在输入密码后批量去除密码。

[English README](README.md)

## 项目简介

PDF Decryptor 基于 `tkinter` 和 `pypdf` 开发，面向不想使用命令行脚本的普通用户，提供直接可用的图形界面解密流程。

## 功能特性

- 支持批量导入 PDF 文件，也支持按文件夹扫描
- 自动检测每个 PDF 是否已加密
- 输入一次密码后批量解密多个文件
- 输出到指定目录
- 支持自定义输出文件名格式
- 一键使用原文件名输出
- 支持显示或隐藏密码输入内容
- 支持中文和英文界面
- 支持 AES 加密 PDF

## 界面语言

应用现在支持中英双语。

- 中文系统默认显示中文，其他系统默认显示英文
- 可以在应用界面里直接切换语言
- 也可以通过 `python3 app.py --lang en` 直接启动英文界面

## 安装依赖

```bash
python3 -m pip install -r requirements.txt
```

## 运行程序

```bash
python3 app.py
```

## 打包 macOS 应用

在 macOS 上打包时，建议使用 Homebrew 的 Python 运行时，不要使用系统自带 Python：

```bash
brew install python@3.12 python-tk@3.12
./scripts/build_macos_app.sh
```

打包产物会输出到 `dist/` 目录。

## 文件名格式

支持的占位符：

- `{name}`：原文件名（不含扩展名）
- `{index}`：三位序号，例如 `001`
- `{date}`：当前日期，格式为 `YYYYMMDD`

示例：

- `{name}_decrypted`
- `{date}_{index}_{name}`
- `{name}`

如果输出目录中存在同名文件，程序会自动追加 `_1`、`_2` 避免覆盖。

## GitHub 发布建议

推荐上传的 Release 资产：

- `PDF_Decryptor-macOS-brew-fixed.zip`

仓库描述、功能介绍和发布文案已整理在 [docs/GITHUB_RELEASE_COPY.md](docs/GITHUB_RELEASE_COPY.md)。

## 许可证

本项目采用 MIT License，详情见 [LICENSE](LICENSE)。
