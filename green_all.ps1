$base = "c:\Users\FERDINAND JR\Downloads\actbayan-main (3)\actbayan-main"

$colorMap = [ordered]@{
    'rgba(139, 0, 0, 0.15)' = 'rgba(22, 101, 52, 0.15)'
    'rgba(139,0,0,0.15)'    = 'rgba(22,101,52,0.15)'
    'rgba(139, 0, 0, 0.08)' = 'rgba(22, 101, 52, 0.08)'
    'rgba(139,0,0,0.08)'    = 'rgba(22,101,52,0.08)'
    '#6b0000'               = '#052e16'
    '#a30000'               = '#14532d'
    '#a00000'               = '#14532d'
    '#8b0000'               = '#166534'
    '#b91c1c'               = '#16a34a'
    '#dc2626'               = '#22c55e'
}

$files = @(
    "templates\lgu.html",
    "templates\lgu_map.html",
    "templates\lgu_analytics.html",
    "templates\lgu_announcements.html",
    "templates\lgu_notif.html",
    "templates\lgu_verifications.html",
    "templates\admin.html",
    "templates\admin_base.html",
    "templates\admin_reports.html",
    "templates\admin_login_attempts.html",
    "static\style.css"
)

$totalChanges = 0

foreach ($relPath in $files) {
    $fullPath = Join-Path $base $relPath
    if (-not (Test-Path $fullPath)) { Write-Host "SKIP: $relPath"; continue }

    $content = Get-Content $fullPath -Raw -Encoding UTF8
    $fileChanges = 0

    foreach ($from in $colorMap.Keys) {
        $to = $colorMap[$from]
        $count = ([regex]::Matches($content, [regex]::Escape($from))).Count
        if ($count -gt 0) {
            $content = $content.Replace($from, $to)
            $fileChanges += $count
            Write-Host "  $relPath : '$from' -> '$to' ($count)"
        }
    }

    if ($fileChanges -gt 0) {
        [System.IO.File]::WriteAllText($fullPath, $content, [System.Text.Encoding]::UTF8)
        Write-Host "  SAVED $relPath ($fileChanges changes)"
        $totalChanges += $fileChanges
    } else {
        Write-Host "  NO CHANGE: $relPath"
    }
}

Write-Host ""
Write-Host "=== Total: $totalChanges replacements ==="
