param([Parameter(Mandatory=$true)][string]$Manifest, [int]$Rate = 0, [string]$Voice = 'Microsoft Hanhan Desktop')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$videoSpeech = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
  $videoSpeech.SelectVoice($Voice)
  $videoSpeech.Rate = $Rate
  $videoSpeech.Volume = 100
  $videoUnits = Get-Content -LiteralPath $Manifest -Raw -Encoding UTF8 | ConvertFrom-Json
  $videoFormat = New-Object System.Speech.AudioFormat.SpeechAudioFormatInfo(24000, [System.Speech.AudioFormat.AudioBitsPerSample]::Sixteen, [System.Speech.AudioFormat.AudioChannel]::Mono)
  foreach ($videoUnit in $videoUnits) {
    if (Test-Path -LiteralPath $videoUnit.path) { continue }
    $videoSpeech.SetOutputToWaveFile($videoUnit.path, $videoFormat)
    $videoSpeech.Speak($videoUnit.text)
    $videoSpeech.SetOutputToNull()
  }
} finally { $videoSpeech.Dispose() }
