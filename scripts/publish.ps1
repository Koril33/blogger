param([string]$TokenFile = 'pypi-token.txt')
$ErrorActionPreference = 'Stop'
$releaseRoot = Split-Path -Parent $PSScriptRoot
$projectText = Get-Content -Raw -LiteralPath (Join-Path $releaseRoot 'pyproject.toml')
$releaseVersion = [regex]::Match($projectText, '(?m)^version\s*=\s*"([^"]+)"').Groups[1].Value
if (-not $releaseVersion) { throw 'Cannot read release version' }
$releaseArtifacts = @(
    (Join-Path $releaseRoot "dist/djhx_blogger-$releaseVersion-py3-none-any.whl"),
    (Join-Path $releaseRoot "dist/djhx_blogger-$releaseVersion.tar.gz")
)
foreach ($releaseArtifact in $releaseArtifacts) {
    if (-not (Test-Path -LiteralPath $releaseArtifact -PathType Leaf)) { throw "Missing artifact: $releaseArtifact" }
}
$releaseTokenPath = if ([System.IO.Path]::IsPathRooted($TokenFile)) { $TokenFile } else { Join-Path $releaseRoot $TokenFile }
$priorPublishToken = $env:UV_PUBLISH_TOKEN
try {
    $env:UV_PUBLISH_TOKEN = (Get-Content -Raw -LiteralPath $releaseTokenPath).Trim()
    if (-not $env:UV_PUBLISH_TOKEN.StartsWith('pypi-')) { throw 'Invalid PyPI token format' }
    & uv publish --publish-url https://upload.pypi.org/legacy/ @releaseArtifacts
    if ($LASTEXITCODE -ne 0) { throw "PyPI publish failed with exit code $LASTEXITCODE" }
} finally {
    $env:UV_PUBLISH_TOKEN = $priorPublishToken
}
