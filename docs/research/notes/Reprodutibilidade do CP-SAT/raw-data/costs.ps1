# A: num_workers=1; B: tempo de relógio binárias on/off alternando; C: bancada com a configuração candidata.
$s = $PSScriptRoot
$env:PYTHONPATH = "C:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan-worktrees\fix-cpsat-reproducibility\src"
$py = "c:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan\.venv\Scripts\python.exe"
Set-Location $s
& $py repro.py --request large-house --reps 1 --mode topo --limit 20 --set num_workers=1 --label A-1worker > "$s\c01-A.jsonl"
foreach ($r in 1..2) {
  & $py repro.py --request large-house --reps 1 --mode topo --limit 1e9 --set max_num_deterministic_batches=6 --label B-binon-$r >> "$s\c02-B.jsonl"
  & $py repro.py --request large-house --reps 1 --mode topo --limit 1e9 --set max_num_deterministic_batches=6 --set share_binary_clauses=false --label B-binoff-$r >> "$s\c02-B.jsonl"
}
& $py bench.py --label cand-B6 --limit 1e9 --set max_num_deterministic_batches=6 --set share_binary_clauses=false > "$s\c03-C.jsonl" 2> "$s\c03-C.err"
"done"
