from __future__ import annotations

import argparse
import locale
import os
import shutil
import webbrowser
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from pypdf import PdfReader, PdfWriter
from pypdf.errors import DependencyError

APP_NAME = "Batch PDF Decryptor"
APP_VERSION = "1.0.4"
REPOSITORY_URL = "https://github.com/Sevacenix/PDF_Decryptor"

LANGUAGE_NAMES = {
    "zh-CN": "中文",
    "en": "English",
}

TRANSLATIONS = {
    "zh-CN": {
        "app_title": "批量 PDF 解密与命名工具",
        "language": "界面语言",
        "add_pdf": "批量添加 PDF",
        "add_folder": "添加文件夹",
        "remove_selected": "移除选中",
        "clear_list": "清空列表",
        "redetect": "重新检测",
        "col_index": "#",
        "col_file": "文件路径",
        "col_encrypted": "已加密",
        "col_status": "状态",
        "settings": "解密设置",
        "output_dir": "输出目录",
        "choose_dir": "选择目录",
        "filename_pattern": "文件名格式",
        "use_original_name": "使用原文件名",
        "pattern_help": "可用占位符: {name} 原文件名, {index} 序号(001), {date} 日期(YYYYMMDD)",
        "password": "解密密码",
        "show_password": "显示密码",
        "copy_plain": "未加密文件也复制到输出目录",
        "start_decrypt": "开始批量解密",
        "pdf_files": "PDF 文件",
        "all_files": "所有文件",
        "pick_pdf_files": "选择 PDF 文件",
        "pick_pdf_folder": "选择包含 PDF 的文件夹",
        "pick_output_dir": "选择输出目录",
        "dialog_notice": "提示",
        "dialog_error": "错误",
        "dialog_complete": "完成",
        "dialog_about": "关于",
        "summary_loaded": "共 {total} 个文件，其中加密文件 {encrypted} 个。",
        "summary_no_new_files": "没有新增文件，可能是重复文件或非 PDF 文件。",
        "complete_result": "处理完成: 成功 {success}，失败 {failed}，跳过 {skipped}。",
        "warn_add_files": "请先添加 PDF 文件。",
        "warn_output_dir": "请先设置输出目录。",
        "warn_empty_pattern": "文件名格式不能为空。",
        "warn_need_password": "检测到加密文件，请输入密码后再解密。",
        "warn_no_pdf_in_folder": "该文件夹中没有 .pdf 文件。",
        "error_pattern": "文件名格式错误",
        "error_dir": "目录错误",
        "error_create_dir": "无法创建输出目录: {error}",
        "status_detected": "已检测",
        "status_detection_failed": "检测失败: {error}",
        "status_naming_failed": "命名失败: {error}",
        "status_skip_unknown": "跳过: 无法判断是否加密",
        "status_plain_copied": "未加密，已复制 -> {filename}",
        "status_copy_failed": "复制失败: {error}",
        "status_plain_skipped": "未加密，已跳过",
        "status_decrypt_done": "解密完成 -> {filename}",
        "status_decrypt_failed": "解密失败: {error}",
        "error_wrong_password": "密码错误或该文件不支持当前解密方式",
        "error_missing_aes_dependency": "缺少 AES 解密依赖 cryptography，请升级到修复版程序后重试",
        "error_missing_dependency": "缺少依赖: {error}",
        "error_unknown_placeholder": "未知占位符: {error}",
        "error_empty_filename": "文件名格式生成了空文件名",
        "enc_yes": "是",
        "enc_no": "否",
        "enc_unknown": "未知",
        "menu_app": "应用",
        "menu_about": "关于 Batch PDF Decryptor",
        "menu_open_repo": "打开 GitHub 仓库",
        "menu_quit": "退出",
        "about_body": "Batch PDF Decryptor\n版本 {version}\n\n一个面向批量处理的桌面 PDF 工具。\n支持批量检测加密状态、输入一次密码后批量解密，并按规则批量命名输出。\n支持 AES 解密和中英双语界面。\n\n仓库地址:\n{url}",
    },
    "en": {
        "app_title": "Batch PDF Decryptor",
        "language": "Language",
        "add_pdf": "Add PDF Files",
        "add_folder": "Add Folder",
        "remove_selected": "Remove Selected",
        "clear_list": "Clear List",
        "redetect": "Detect Again",
        "col_index": "#",
        "col_file": "File Path",
        "col_encrypted": "Encrypted",
        "col_status": "Status",
        "settings": "Decrypt Settings",
        "output_dir": "Output Folder",
        "choose_dir": "Choose Folder",
        "filename_pattern": "File Name Pattern",
        "use_original_name": "Use Original Name",
        "pattern_help": "Placeholders: {name} original file name, {index} sequence (001), {date} date (YYYYMMDD)",
        "password": "Password",
        "show_password": "Show password",
        "copy_plain": "Copy unencrypted files to the output folder too",
        "start_decrypt": "Start Batch Decrypt",
        "pdf_files": "PDF Files",
        "all_files": "All Files",
        "pick_pdf_files": "Choose PDF files",
        "pick_pdf_folder": "Choose a folder containing PDFs",
        "pick_output_dir": "Choose output folder",
        "dialog_notice": "Notice",
        "dialog_error": "Error",
        "dialog_complete": "Completed",
        "dialog_about": "About",
        "summary_loaded": "{total} files loaded, {encrypted} encrypted.",
        "summary_no_new_files": "No new files were added. They may already exist in the list or not be PDFs.",
        "complete_result": "Finished: {success} succeeded, {failed} failed, {skipped} skipped.",
        "warn_add_files": "Add PDF files first.",
        "warn_output_dir": "Choose an output folder first.",
        "warn_empty_pattern": "The file name pattern cannot be empty.",
        "warn_need_password": "Encrypted files were detected. Enter the password before decrypting.",
        "warn_no_pdf_in_folder": "No .pdf files were found in this folder.",
        "error_pattern": "Invalid file name pattern",
        "error_dir": "Folder error",
        "error_create_dir": "Failed to create the output folder: {error}",
        "status_detected": "Detected",
        "status_detection_failed": "Detection failed: {error}",
        "status_naming_failed": "Naming failed: {error}",
        "status_skip_unknown": "Skipped: unable to determine encryption status",
        "status_plain_copied": "Not encrypted, copied -> {filename}",
        "status_copy_failed": "Copy failed: {error}",
        "status_plain_skipped": "Not encrypted, skipped",
        "status_decrypt_done": "Decrypted -> {filename}",
        "status_decrypt_failed": "Decrypt failed: {error}",
        "error_wrong_password": "Wrong password or unsupported decryption method for this file",
        "error_missing_aes_dependency": "Missing AES decryption dependency: cryptography. Use the fixed build and try again.",
        "error_missing_dependency": "Missing dependency: {error}",
        "error_unknown_placeholder": "Unknown placeholder: {error}",
        "error_empty_filename": "The file name pattern produced an empty file name",
        "enc_yes": "Yes",
        "enc_no": "No",
        "enc_unknown": "Unknown",
        "menu_app": "App",
        "menu_about": "About Batch PDF Decryptor",
        "menu_open_repo": "Open GitHub Repository",
        "menu_quit": "Quit",
        "about_body": "Batch PDF Decryptor\nVersion {version}\n\nA desktop utility focused on batch PDF decryption and batch output naming.\nDetect encrypted PDFs, decrypt multiple files with one password, and export them with flexible naming rules.\nSupports AES decryption and a bilingual Chinese-English UI.\n\nRepository:\n{url}",
    },
}


def detect_default_language() -> str:
    candidates = [
        locale.getlocale()[0],
        os.environ.get("LC_ALL"),
        os.environ.get("LANG"),
    ]
    for candidate in candidates:
        if isinstance(candidate, str) and candidate.lower().startswith("zh"):
            return "zh-CN"
    return "en"


@dataclass
class PdfTaskItem:
    path: Path
    encrypted: bool | None
    status_key: str = "status_detected"
    status_context: dict[str, str] = field(default_factory=dict)


class PdfDecryptorApp(tk.Tk):
    def __init__(self, language: str | None = None) -> None:
        super().__init__()
        self.geometry("1080x680")
        self.minsize(960, 560)

        self.items: list[PdfTaskItem] = []
        self.language_code = language if language in TRANSLATIONS else detect_default_language()
        self.output_dir_var = tk.StringVar(value=str(Path.cwd() / "output"))
        self.pattern_var = tk.StringVar(value="{name}_decrypted")
        self.password_var = tk.StringVar()
        self.show_password_var = tk.BooleanVar(value=False)
        self.copy_plain_var = tk.BooleanVar(value=False)
        self.summary_var = tk.StringVar()
        self.language_display_var = tk.StringVar(value=LANGUAGE_NAMES[self.language_code])

        self.tree: ttk.Treeview | None = None
        self.password_entry: ttk.Entry | None = None
        self._build_ui()
        self.refresh_table()

    def t(self, key: str, **kwargs: object) -> str:
        text = TRANSLATIONS[self.language_code][key]
        return text.format(**kwargs) if kwargs else text

    def _build_ui(self) -> None:
        for child in self.winfo_children():
            child.destroy()

        self.title(self.t("app_title"))
        self._build_menu()
        root = ttk.Frame(self, padding=12)
        root.pack(fill="both", expand=True)

        top_bar = ttk.Frame(root)
        top_bar.pack(fill="x")

        ttk.Button(top_bar, text=self.t("add_pdf"), command=self.add_files).pack(side="left")
        ttk.Button(top_bar, text=self.t("add_folder"), command=self.add_folder).pack(
            side="left", padx=8
        )
        ttk.Button(top_bar, text=self.t("remove_selected"), command=self.remove_selected).pack(
            side="left"
        )
        ttk.Button(top_bar, text=self.t("clear_list"), command=self.clear_files).pack(
            side="left", padx=8
        )
        ttk.Button(top_bar, text=self.t("redetect"), command=self.redetect_all).pack(side="left")

        language_frame = ttk.Frame(top_bar)
        language_frame.pack(side="right")
        ttk.Label(language_frame, text=self.t("language")).pack(side="left", padx=(0, 8))
        language_combo = ttk.Combobox(
            language_frame,
            state="readonly",
            width=10,
            textvariable=self.language_display_var,
            values=[LANGUAGE_NAMES["zh-CN"], LANGUAGE_NAMES["en"]],
        )
        language_combo.pack(side="left")
        language_combo.bind("<<ComboboxSelected>>", self.change_language)

        table_frame = ttk.Frame(root)
        table_frame.pack(fill="both", expand=True, pady=(12, 10))

        columns = ("index", "file", "encrypted", "status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        self.tree.heading("index", text=self.t("col_index"))
        self.tree.heading("file", text=self.t("col_file"))
        self.tree.heading("encrypted", text=self.t("col_encrypted"))
        self.tree.heading("status", text=self.t("col_status"))

        self.tree.column("index", width=48, minwidth=48, stretch=False, anchor="center")
        self.tree.column("file", width=560, minwidth=320)
        self.tree.column("encrypted", width=90, minwidth=90, stretch=False, anchor="center")
        self.tree.column("status", width=360, minwidth=240)

        vbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        vbar.pack(side="right", fill="y")

        settings = ttk.LabelFrame(root, text=self.t("settings"), padding=10)
        settings.pack(fill="x")
        settings.columnconfigure(1, weight=1)

        ttk.Label(settings, text=self.t("output_dir")).grid(row=0, column=0, sticky="w")
        ttk.Entry(settings, textvariable=self.output_dir_var).grid(
            row=0, column=1, sticky="ew", padx=(8, 8)
        )
        ttk.Button(settings, text=self.t("choose_dir"), command=self.select_output_dir).grid(
            row=0, column=2
        )

        ttk.Label(settings, text=self.t("filename_pattern")).grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )
        pattern_row = ttk.Frame(settings)
        pattern_row.grid(row=1, column=1, sticky="ew", padx=(8, 8), pady=(10, 0))
        pattern_row.columnconfigure(0, weight=1)
        ttk.Entry(pattern_row, textvariable=self.pattern_var).grid(row=0, column=0, sticky="ew")
        ttk.Button(
            pattern_row, text=self.t("use_original_name"), command=self.use_original_filename
        ).grid(row=0, column=1, padx=(8, 0))
        ttk.Label(settings, text=self.t("pattern_help")).grid(
            row=1, column=2, sticky="w", pady=(10, 0)
        )

        ttk.Label(settings, text=self.t("password")).grid(row=2, column=0, sticky="w", pady=(10, 0))
        self.password_entry = ttk.Entry(settings, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=2, column=1, sticky="ew", padx=(8, 8), pady=(10, 0))

        password_options = ttk.Frame(settings)
        password_options.grid(row=2, column=2, sticky="w", pady=(10, 0))
        ttk.Checkbutton(
            password_options,
            text=self.t("show_password"),
            variable=self.show_password_var,
            command=self.toggle_password_visibility,
        ).pack(anchor="w")
        ttk.Checkbutton(
            password_options,
            text=self.t("copy_plain"),
            variable=self.copy_plain_var,
        ).pack(anchor="w", pady=(4, 0))

        ttk.Button(settings, text=self.t("start_decrypt"), command=self.decrypt_all).grid(
            row=3, column=2, sticky="e", pady=(12, 0)
        )

        ttk.Label(root, textvariable=self.summary_var).pack(anchor="w", pady=(10, 0))

    def change_language(self, _event: tk.Event | None = None) -> None:
        reverse_names = {name: code for code, name in LANGUAGE_NAMES.items()}
        selected_name = self.language_display_var.get()
        self.language_code = reverse_names.get(selected_name, self.language_code)
        self._build_ui()
        self.refresh_table()

    def _build_menu(self) -> None:
        menubar = tk.Menu(self)
        app_menu = tk.Menu(menubar, tearoff=0)
        app_menu.add_command(label=self.t("menu_about"), command=self.show_about)
        app_menu.add_command(label=self.t("menu_open_repo"), command=self.open_repository)
        app_menu.add_separator()
        app_menu.add_command(label=self.t("menu_quit"), command=self.quit)
        menubar.add_cascade(label=self.t("menu_app"), menu=app_menu)
        self.configure(menu=menubar)

    def set_status(self, item: PdfTaskItem, key: str, **context: object) -> None:
        item.status_key = key
        item.status_context = {k: str(v) for k, v in context.items()}

    def show_about(self) -> None:
        messagebox.showinfo(
            self.t("dialog_about"),
            self.t("about_body", version=APP_VERSION, url=REPOSITORY_URL),
        )

    @staticmethod
    def open_repository() -> None:
        webbrowser.open(REPOSITORY_URL)

    def status_text(self, item: PdfTaskItem) -> str:
        return self.t(item.status_key, **item.status_context) if item.status_key else ""

    def add_files(self) -> None:
        selected = filedialog.askopenfilenames(
            title=self.t("pick_pdf_files"),
            filetypes=[(self.t("pdf_files"), "*.pdf"), (self.t("all_files"), "*.*")],
        )
        if not selected:
            return
        self._append_paths([Path(path) for path in selected])

    def add_folder(self) -> None:
        folder = filedialog.askdirectory(title=self.t("pick_pdf_folder"))
        if not folder:
            return
        pdfs = sorted(Path(folder).glob("*.pdf"))
        if not pdfs:
            messagebox.showinfo(self.t("dialog_notice"), self.t("warn_no_pdf_in_folder"))
            return
        self._append_paths(pdfs)

    def _append_paths(self, paths: list[Path]) -> None:
        existing = {item.path.resolve() for item in self.items}
        added = 0

        for raw_path in paths:
            if raw_path.suffix.lower() != ".pdf":
                continue
            path = raw_path.expanduser().resolve()
            if path in existing:
                continue
            encrypted, status_key, status_context = self.detect_encryption(path)
            self.items.append(
                PdfTaskItem(
                    path=path,
                    encrypted=encrypted,
                    status_key=status_key,
                    status_context=status_context,
                )
            )
            existing.add(path)
            added += 1

        self.refresh_table()
        if added == 0:
            self.summary_var.set(self.t("summary_no_new_files"))

    def detect_encryption(self, pdf_path: Path) -> tuple[bool | None, str, dict[str, str]]:
        try:
            reader = PdfReader(str(pdf_path), strict=False)
            return reader.is_encrypted, "status_detected", {}
        except Exception as exc:
            return None, "status_detection_failed", {"error": str(exc)}

    def redetect_all(self) -> None:
        for item in self.items:
            encrypted, status_key, status_context = self.detect_encryption(item.path)
            item.encrypted = encrypted
            item.status_key = status_key
            item.status_context = status_context
        self.refresh_table()

    def remove_selected(self) -> None:
        if self.tree is None:
            return
        selected_rows = sorted((int(row_id) for row_id in self.tree.selection()), reverse=True)
        for row_index in selected_rows:
            del self.items[row_index]
        self.refresh_table()

    def clear_files(self) -> None:
        self.items.clear()
        self.refresh_table()

    def select_output_dir(self) -> None:
        selected = filedialog.askdirectory(title=self.t("pick_output_dir"))
        if selected:
            self.output_dir_var.set(selected)

    def use_original_filename(self) -> None:
        self.pattern_var.set("{name}")

    def toggle_password_visibility(self) -> None:
        if self.password_entry is None:
            return
        self.password_entry.configure(show="" if self.show_password_var.get() else "*")

    def refresh_table(self) -> None:
        if self.tree is None:
            return

        self.tree.delete(*self.tree.get_children())
        encrypted_count = 0

        for index, item in enumerate(self.items, start=1):
            if item.encrypted:
                encrypted_count += 1
            self.tree.insert(
                "",
                "end",
                iid=str(index - 1),
                values=(
                    index,
                    str(item.path),
                    self.encryption_text(item.encrypted),
                    self.status_text(item),
                ),
            )

        self.summary_var.set(
            self.t("summary_loaded", total=len(self.items), encrypted=encrypted_count)
        )

    def encryption_text(self, encrypted: bool | None) -> str:
        if encrypted is True:
            return self.t("enc_yes")
        if encrypted is False:
            return self.t("enc_no")
        return self.t("enc_unknown")

    def decrypt_all(self) -> None:
        if not self.items:
            messagebox.showwarning(self.t("dialog_notice"), self.t("warn_add_files"))
            return

        output_dir_raw = self.output_dir_var.get().strip()
        if not output_dir_raw:
            messagebox.showwarning(self.t("dialog_notice"), self.t("warn_output_dir"))
            return

        pattern = self.pattern_var.get().strip()
        if not pattern:
            messagebox.showwarning(self.t("dialog_notice"), self.t("warn_empty_pattern"))
            return

        try:
            self.format_output_stem(pattern=pattern, original_name="demo", index=1)
        except ValueError as exc:
            messagebox.showerror(self.t("error_pattern"), str(exc))
            return

        output_dir = Path(output_dir_raw).expanduser()
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            messagebox.showerror(self.t("error_dir"), self.t("error_create_dir", error=exc))
            return

        password = self.password_var.get()
        encrypted_exists = any(item.encrypted for item in self.items)
        if encrypted_exists and password == "":
            messagebox.showwarning(self.t("dialog_notice"), self.t("warn_need_password"))
            return

        success = 0
        failed = 0
        skipped = 0

        for index, item in enumerate(self.items, start=1):
            try:
                output_stem = self.format_output_stem(pattern, item.path.stem, index)
                output_file = self.ensure_unique(output_dir / f"{output_stem}.pdf")
            except ValueError as exc:
                self.set_status(item, "status_naming_failed", error=exc)
                failed += 1
                continue

            if item.encrypted is None:
                self.set_status(item, "status_skip_unknown")
                skipped += 1
                continue

            if item.encrypted is False:
                if self.copy_plain_var.get():
                    try:
                        shutil.copy2(item.path, output_file)
                        self.set_status(item, "status_plain_copied", filename=output_file.name)
                        success += 1
                    except OSError as exc:
                        self.set_status(item, "status_copy_failed", error=exc)
                        failed += 1
                else:
                    self.set_status(item, "status_plain_skipped")
                    skipped += 1
                continue

            ok, error = self.decrypt_one(item.path, output_file, password)
            if ok:
                self.set_status(item, "status_decrypt_done", filename=output_file.name)
                success += 1
            else:
                self.set_status(item, "status_decrypt_failed", error=error)
                failed += 1

        self.refresh_table()
        result_text = self.t(
            "complete_result", success=success, failed=failed, skipped=skipped
        )
        self.summary_var.set(result_text)
        messagebox.showinfo(self.t("dialog_complete"), result_text)

    def decrypt_one(self, src_file: Path, dst_file: Path, password: str) -> tuple[bool, str]:
        try:
            reader = PdfReader(str(src_file), strict=False)
            if reader.is_encrypted and reader.decrypt(password) == 0:
                return False, self.t("error_wrong_password")

            writer = PdfWriter()
            for page in reader.pages:
                writer.add_page(page)

            with dst_file.open("wb") as output_stream:
                writer.write(output_stream)
            return True, ""
        except DependencyError as exc:
            error_text = str(exc)
            if "cryptography" in error_text and "AES" in error_text:
                return False, self.t("error_missing_aes_dependency")
            return False, self.t("error_missing_dependency", error=error_text)
        except Exception as exc:
            return False, str(exc)

    def format_output_stem(self, pattern: str, original_name: str, index: int) -> str:
        date_str = datetime.now().strftime("%Y%m%d")
        try:
            stem = pattern.format(name=original_name, index=f"{index:03d}", date=date_str)
        except KeyError as exc:
            raise ValueError(self.t("error_unknown_placeholder", error=exc)) from exc

        stem = stem.strip()
        if not stem:
            raise ValueError(self.t("error_empty_filename"))

        invalid_chars = '/\\:*?"<>|'
        for char in invalid_chars:
            stem = stem.replace(char, "_")
        return stem

    @staticmethod
    def ensure_unique(path: Path) -> Path:
        if not path.exists():
            return path
        counter = 1
        while True:
            candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
            if not candidate.exists():
                return candidate
            counter += 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Batch PDF Decryptor")
    parser.add_argument("--lang", choices=sorted(TRANSLATIONS.keys()))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    app = PdfDecryptorApp(language=args.lang)
    app.mainloop()


if __name__ == "__main__":
    main()
