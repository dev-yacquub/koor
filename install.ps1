# Koor Language Installer for Windows
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "   RAKIBAADDA LUUQADDA KOOR (INSTALLING KOOR)   " -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan

# 1. Rakib xirmada Python (pip install -e .)
Write-Host "`n[1/3] Rakibaya xirmada Koor..." -ForegroundColor Yellow
python -m pip install -e . --no-warn-script-location

# 2. Ku dar jidadka PATH-ka isticmaalaha (User PATH)
Write-Host "`n[2/3] Ku daraya Koor PATH-ka nidaamka..." -ForegroundColor Yellow
$currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
$koorDir = $PSScriptRoot
$pythonScripts = "$env:APPDATA\Python\Python314\Scripts"

$toAdd = @($pythonScripts, $koorDir)
$pathParts = @($currentPath -split ';' | Where-Object { $_ -ne "" })
$updated = $false

foreach ($folder in $toAdd) {
    if (Test-Path $folder) {
        if ($pathParts -notcontains $folder) {
            $pathParts += $folder
            $updated = $true
            Write-Host "   + Lagu daray PATH: $folder" -ForegroundColor Green
        } else {
            Write-Host "   = Horay ayuu ugu jiray PATH: $folder" -ForegroundColor DarkGray
        }
    }
}

if ($updated) {
    $newPath = ($pathParts -join ';') + ';'
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "   + PATH-ka isticmaalaha si guul leh ayaa loo cusboonaysiiyay!" -ForegroundColor Green
}

# 3. Hubi amarka koor
Write-Host "`n[3/3] Hubinta amarka 'koor'..." -ForegroundColor Yellow
$env:Path = "$koorDir;$pythonScripts;" + $env:Path

Write-Host "`n==================================================" -ForegroundColor Cyan
Write-Host "   HAMBALYO! KOOR WAA LA RAKIBAY GUUD AHAAN!   " -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "`nHadda waxaad terminal kasta (ama meel kasta) ka qori kartaa:" -ForegroundColor White
Write-Host "   koor run fayl.koor" -ForegroundColor Cyan
Write-Host "   koor repl" -ForegroundColor Cyan
Write-Host "   koor check fayl.koor" -ForegroundColor Cyan
Write-Host "`nFiiro gaar ah: Terminal-ka hadda kuu furan dib u fur si uu u aqoonsado." -ForegroundColor Yellow
