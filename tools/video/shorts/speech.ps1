param([Parameter(Mandatory=$true)][string]$InputJson, [Parameter(Mandatory=$true)][string]$OutputDirectory, [string]$Voice = 'Microsoft Hanhan Desktop')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$shortsInput = Get-Content -LiteralPath $InputJson -Raw -Encoding UTF8 | ConvertFrom-Json
$shortsSynth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
  $shortsSynth.SelectVoice($Voice)
  $shortsSynth.Rate = 1
  $shortsIndex = 0
  foreach ($shortsPhrase in $shortsInput) {
    $shortsPath = Join-Path $OutputDirectory ('{0:d3}.wav' -f $shortsIndex)
    $shortsSynth.SetOutputToWaveFile($shortsPath)
    $shortsSynth.Speak([string]$shortsPhrase)
    $shortsSynth.SetOutputToNull()
    $shortsIndex++
  }
} finally { $shortsSynth.Dispose() }
