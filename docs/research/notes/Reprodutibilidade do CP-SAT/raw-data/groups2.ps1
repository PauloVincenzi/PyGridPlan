# BisseÃ§Ã£o no modelo nÂº 3 (repro2.py), cÃ³digo corrigido como base; 3 processos simultÃ¢neos por grupo.
param([string]$Prefix = "e01", [string[]]$Only = @())
$s = $PSScriptRoot
$env:PYTHONPATH = "C:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan-worktrees\fix-cpsat-reproducibility\src"
$py = "c:\Users\paulo\AREA_DE_TRABALHO\PyGridPlan\.venv\Scripts\python.exe"
Set-Location $s
$groups = [ordered]@{
  "R0base"   = ""
  "R1glue"   = "--set share_glue_clauses=false"
  "R2bounds" = "--set share_objective_bounds=false --set share_level_zero_bounds=false"
  "R3rins"   = "--set use_rins_lns=false"
  "R4all"    = "--set share_glue_clauses=false --set share_objective_bounds=false --set share_level_zero_bounds=false --set use_rins_lns=false"
  "R5nolns"  = "--set use_lns=false"
  "R6pool1"  = "--set solution_pool_size=1"
  "R8seq"    = "--set num_workers=1 --set max_deterministic_time=20"
  "R9nolnsbin" = "--set use_lns=false --set share_binary_clauses=true"
  "R10nolnsdt" = "--set use_lns=false --set max_num_deterministic_batches=0 --set max_deterministic_time=20"
}
foreach ($g in $groups.Keys) {
  if ($Only.Count -and $g -notin $Only) { continue }
  $ps = foreach ($i in 1..3) {
    Start-Process -FilePath $py -ArgumentList "repro2.py run --label $g-p$i $($groups[$g])" -RedirectStandardOutput "$s\$Prefix-$g-p$i.jsonl" -RedirectStandardError "$s\$Prefix-$g-p$i.err" -NoNewWindow -PassThru
  }
  $ps | Wait-Process
  foreach ($i in 1..3) {
    Get-Content "$s\$Prefix-$g-p$i.err" | Select-Object -Last 3
    Get-Content "$s\$Prefix-$g-p$i.jsonl" | ForEach-Object {
      $j = $_ | ConvertFrom-Json
      "{0,-12} total={1}s {2} model={3} obj={4} dtime={5} sol={6}" -f $j.label, $j.total, $j.status, $j.model, $j.obj, $j.dtime, $j.sol
    }
  }
}


