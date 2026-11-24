cd /c/Users/paulo/AppData/Local/Temp/claude/d0e1a6539163643b/bbff36b0-54ae-4fba-a5ab-ca4993a4a967/scratchpad/w
one() { powershell -Command "'{0} load={1} python={2} freeMB={3}' -f '$1 $2', (Get-CimInstance Win32_Processor).LoadPercentage, @(Get-Process python* -EA SilentlyContinue).Count, [int]((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1024)" >> load.log
 PYTHONPATH=$(cygpath -w /c/Users/paulo/AppData/Local/Temp/claude/d0e1a6539163643b/bbff36b0-54ae-4fba-a5ab-ca4993a4a967/scratchpad/w/$2/src) /c/Users/paulo/AREA_DE_TRABALHO/PyGridPlan/.venv/Scripts/python hi.py bench.py $2 $(cygpath -w /c/Users/paulo/AppData/Local/Temp/claude/d0e1a6539163643b/bbff36b0-54ae-4fba-a5ab-ca4993a4a967/scratchpad/w/$2/tests/fixtures/requests) $1 >> bench.jsonl 2>> bench.err; }
one one-bedroom old; one one-bedroom new
one small-lot new; one small-lot old
one basic-program old; one basic-program new
one three-bedroom new; one three-bedroom old
one large-house old; one large-house new
one small-lot old; one small-lot new
one small-lot new; one small-lot old
