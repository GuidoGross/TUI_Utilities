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
    update_tlds_list
    build_package
    upload_library_to_pypi
    delete_temporary_files
    update_library
    finish $total_start_time
}

function update_tlds_list {
    Write-Host "${bold}${italic}[1/5]${/italic} Actualizando lista de TLDs...${reset_style}" -ForegroundColor White
    $current_step_start_time = Get-Date
    try {
        $url = "https://data.iana.org/TLD/tlds-alpha-by-domain.txt"
        $response = Invoke-RestMethod -Uri $url
        $lines = $response -split "`n" | Where-Object { $_.Trim() -ne "" }
        if ($lines.Count -gt 1) {
            $tlds = $lines[1..($lines.Count - 1)] | ForEach-Object { $_.Trim().ToLower() }
            $output_path = Join-Path $base_path "tui_utilities\_tlds\tlds.txt"
            $tlds -join "`n" | Out-File -FilePath $output_path -Encoding utf8 -NoNewline
        }
        $duration = (Get-Date) - $current_step_start_time
        Write-Host "${bold}Lista de TLDs actualizada en:${/bold} $($duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
    }
    catch {
        Write-Host "${bold}Error al actualizar la lista de TLDs:${/bold} $($_.Exception.Message)${reset_style}" -ForegroundColor Red
    }
    separator
}

function build_package {
    Write-Host "${bold}${italic}[2/5]${/italic} Construyendo paquete con build...${reset_style}" -ForegroundColor White
    $current_step_start_time = Get-Date
    python -m build
    $duration = (Get-Date) - $current_step_start_time
    Write-Host "${bold}Paquete construido en:${/bold} $($duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
    separator
}

function upload_library_to_pypi {
    Write-Host "${bold}${italic}[3/5]${/italic} Subiendo a PyPI con twine...${reset_style}" -ForegroundColor White
    $current_step_start_time = Get-Date
    twine upload dist/*
    $duration = (Get-Date) - $current_step_start_time
    Write-Host "${bold}Carga a PyPI completada en:${/bold} $($duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
    separator
}

function delete_temporary_files {
    Write-Host "${bold}${italic}[4/5]${/italic} Eliminando archivos temporales y residuos...${reset_style}" -ForegroundColor White
    $current_step_start_time = Get-Date
    $folders_to_delete = @("dist", "build")
    Get-ChildItem -Path $base_path -Filter "*.egg-info" -Directory | ForEach-Object { $folders_to_delete += $_.FullName }
    $folders_to_delete | ForEach-Object { if (Test-Path $_) { Remove-Item -Path $_ -Recurse -Force -ErrorAction SilentlyContinue } }
    $duration = (Get-Date) - $current_step_start_time
    Write-Host "${bold}Residuos eliminados en:${/bold} $($duration.TotalMilliseconds.ToString("N0", [cultureinfo]::GetCultureInfo("es-ES")))ms${reset_style}" -ForegroundColor Green
    separator
}

function update_library {
    Write-Host "${bold}${italic}[5/5]${/italic} Actualizando tui_utilities localmente...${reset_style}" -ForegroundColor White
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