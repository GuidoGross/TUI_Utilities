$ErrorActionPreference = "Stop"

chcp 65001 > $null
$utf8_encoding = New-Object System.Text.UTF8Encoding($false)
[Console]::InputEncoding = [Console]::OutputEncoding = $OutputEncoding = $utf8_encoding

$base_path = Get-Location

$escape = [char]27
$bold = "$escape[1m"
${/bold} = "$escape[22m"
$italic = "$escape[3m"
${/italic} = "$escape[23m"
$reset_style = "$escape[0m"

function separator {
    $width = $Host.UI.RawUI.WindowSize.Width
    if ($null -eq $width) { $width = 125 }
    $separator = "${bold}/" + ("-" * ($width - 3)) + "/${reset_style}"
    Write-Host $separator -ForegroundColor White
}

function main {
    $total_start_time = Get-Date
    Write-Host "${bold}${italic}Comenzando proceso de publicación y actualización...${reset_style}" -ForegroundColor White
    separator
    build_package
    upload_library_to_pypi
    delete_temporary_files
    update_library
    finish $total_start_time
}

function build_package {
    Write-Host "${bold}${italic}[1/4]${/italic} Construyendo paquete con build...${reset_style}" -ForegroundColor White
    $current_step_start_time = Get-Date
    python -m build
    $duration = (Get-Date) - $current_step_start_time
    Write-Host "${bold}Paquete construido en:${/bold} $($duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
    separator
}

function upload_library_to_pypi {
    Write-Host "${bold}${italic}[2/4]${/italic} Subiendo a PyPI con twine...${reset_style}" -ForegroundColor White
    $current_step_start_time = Get-Date
    twine upload dist/*
    $duration = (Get-Date) - $current_step_start_time
    Write-Host "${bold}Carga a PyPI completada en:${/bold} $($duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
    separator
}

function delete_temporary_files {
    Write-Host "${bold}${italic}[3/4]${/italic} Eliminando archivos temporales y residuos...${reset_style}" -ForegroundColor White
    $current_step_start_time = Get-Date
    $folders_to_delete = @("dist", "build")
    Get-ChildItem -Path $base_path -Filter "*.egg-info" -Directory | ForEach-Object { $folders_to_delete += $_.FullName }
    $folders_to_delete | ForEach-Object { if (Test-Path $_) { Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue } }
    $duration = (Get-Date) - $current_step_start_time
    Write-Host "${bold}Residuos eliminados en:${/bold} $($duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
    separator
}

function update_library {
    Write-Host "${bold}${italic}[4/4]${/italic} Actualizando tui_utilities localmente...${reset_style}" -ForegroundColor White
    $current_step_start_time = Get-Date
    pip install -U tui_utilities
    pip install -U tui_utilities
    $duration = (Get-Date) - $current_step_start_time
    Write-Host "${bold}Actualización completada en:${/bold} $($duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
    separator
}

function finish($total_start_time) {
    $total_duration = (Get-Date) - $total_start_time
    Write-Host "${bold}Proceso de publicación y actualización completado con éxito en:${/bold} $($total_duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
}

main