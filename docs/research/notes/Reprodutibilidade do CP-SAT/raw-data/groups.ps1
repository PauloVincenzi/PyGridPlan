# Roda grupos de configurações, cada um com 3 processos simultâneos, e resume a assinatura.
param([string]$Prefix = "r13", [string]$Request = "large-house", [string]$Mode = "topo")
$s = $PSScriptRoot
$env:PYTHONPATH = "C:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan-worktrees\fix-cpsat-reproducibility\src"
$py = "c:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan\.venv\Scripts\python.exe"
Set-Location $s
$groups = [ordered]@{
  "G3rins"    = "--limit 1e9 --set max_num_deterministic_batches=6 --set share_binary_clauses=false --set share_glue_clauses=false"
  "G4dtime"   = "--limit 20 --set use_rins_lns=false --set share_binary_clauses=false --set share_glue_clauses=false"
  "G5glue"    = "--limit 1e9 --set max_num_deterministic_batches=6 --set use_rins_lns=false --set share_glue_clauses=false"
  "G6binary"  = "--limit 1e9 --set max_num_deterministic_batches=6 --set use_rins_lns=false --set share_binary_clauses=false"
}
foreach ($g in $groups.Keys) {
  $ps = foreach ($i in 1..3) {
    Start-Process -FilePath $py -ArgumentList "repro.py --request $Request --reps 1 --mode $Mode $($groups[$g]) --label $g-p$i" -RedirectStandardOutput "$s\$Prefix-$g-p$i.jsonl" -NoNewWindow -PassThru
  }
  $ps | Wait-Process
  foreach ($i in 1..3) {
    Get-Content "$s\$Prefix-$g-p$i.jsonl" | ForEach-Object {
      $j = $_ | ConvertFrom-Json; $c = $j.calls[0]
      "{0} total={1}s obj={2} dtime={3} sol={4} plan={5} score={6}" -f $j.label, $j.total, $c.obj, $c.dtime, $c.sol, $j.plan, $j.score
    }
  }
}
