param(
    [string]$PythonExe = "py -3.12",
    [string]$AppVersion = "1.0.3"
)

$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$DistDir = Join-Path $ProjectRoot "dist"
$BuildRoot = Join-Path $env:TEMP "pdf_decryptor_build_windows"
$VenvDir = Join-Path $env:TEMP "pdf_decryptor_build_windows_venv"
$IconPath = Join-Path $ProjectRoot "assets\PDF_Decryptor.ico"

function Invoke-Python {
    param(
        [string]$Command
    )

    Invoke-Expression "$PythonExe $Command"
}

Write-Host "Using Python launcher: $PythonExe"
Invoke-Python '-c "import tkinter; print(\"tkinter runtime ok\")"'

if (Test-Path $BuildRoot) {
    Remove-Item $BuildRoot -Recurse -Force
}
if (Test-Path $VenvDir) {
    Remove-Item $VenvDir -Recurse -Force
}

New-Item -ItemType Directory -Force -Path $BuildRoot | Out-Null
New-Item -ItemType Directory -Force -Path $DistDir | Out-Null

Copy-Item (Join-Path $ProjectRoot "app.py") $BuildRoot
Copy-Item (Join-Path $ProjectRoot "requirements.txt") $BuildRoot

Invoke-Python "-m venv `"$VenvDir`""

$VenvPython = Join-Path $VenvDir "Scripts\python.exe"
$PyInstallerArgs = @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--windowed",
    "--name", "PDF_Decryptor"
)

& $VenvPython -m pip install --upgrade pip | Out-Null
& $VenvPython -m pip install -r (Join-Path $BuildRoot "requirements.txt") pyinstaller | Out-Null

if (Test-Path $IconPath) {
    $PyInstallerArgs += @("--icon", $IconPath)
}

$VersionFile = Join-Path $BuildRoot "windows_version_info.txt"
$VersionParts = $AppVersion.Split(".")
while ($VersionParts.Count -lt 4) {
    $VersionParts += "0"
}
$VersionTuple = $VersionParts -join ", "

$VersionInfo = @"
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=($VersionTuple),
    prodvers=($VersionTuple),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', 'Sevacenix'),
          StringStruct('FileDescription', 'PDF_Decryptor'),
          StringStruct('FileVersion', '$AppVersion'),
          StringStruct('InternalName', 'PDF_Decryptor'),
          StringStruct('OriginalFilename', 'PDF_Decryptor.exe'),
          StringStruct('ProductName', 'PDF_Decryptor'),
          StringStruct('ProductVersion', '$AppVersion')
        ]
      )
    ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
"@

Set-Content -Path $VersionFile -Value $VersionInfo -Encoding ASCII
$PyInstallerArgs += @("--version-file", $VersionFile, "app.py")

Push-Location $BuildRoot
try {
    & $VenvPython @PyInstallerArgs
}
finally {
    Pop-Location
}

$OutputFolder = Join-Path $BuildRoot "dist\PDF_Decryptor"
$ZipPath = Join-Path $DistDir "PDF_Decryptor-windows.zip"
$HashPath = Join-Path $DistDir "PDF_Decryptor-windows.zip.sha256"

if (Test-Path $ZipPath) {
    Remove-Item $ZipPath -Force
}
if (Test-Path $HashPath) {
    Remove-Item $HashPath -Force
}

Compress-Archive -Path $OutputFolder -DestinationPath $ZipPath -Force
$Hash = (Get-FileHash -Algorithm SHA256 $ZipPath).Hash.ToLower()
Set-Content -Path $HashPath -Value "$Hash *PDF_Decryptor-windows.zip" -Encoding ASCII

Write-Host "Build completed:"
Write-Host "  $ZipPath"
Write-Host "  $HashPath"
