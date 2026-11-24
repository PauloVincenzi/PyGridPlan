$s = $PSScriptRoot
$py = "c:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan\.venv\Scripts\python.exe"
Set-Location $s
foreach ($r in "one-bedroom","small-lot","basic-program","three-bedroom","large-house") {
  $env:PYTHONPATH = "$s\old\src"
  & $py bench.py --label antes-alt --requests $r >> "$s\h01-antes-alt.jsonl" 2>> "$s\h01.err"
  $env:PYTHONPATH = "C:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan-worktrees\fix-cpsat-reproducibility\src"
  & $py bench.py --label depois-alt --requests $r >> "$s\h02-depois-alt.jsonl" 2>> "$s\h02.err"
}
"done"
