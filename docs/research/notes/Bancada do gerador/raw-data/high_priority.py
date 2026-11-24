"""Roda o bench.py em prioridade alta e sem economia de energia (EcoQoS) neste processo."""
import ctypes, runpy, sys
k = ctypes.WinDLL("kernel32", use_last_error=True)
k.GetCurrentProcess.restype = ctypes.c_void_p
h = ctypes.c_void_p(k.GetCurrentProcess())
assert k.SetPriorityClass(h, 0x80)  # HIGH_PRIORITY_CLASS
state = (ctypes.c_ulong * 3)(1, 1, 0)  # PROCESS_POWER_THROTTLING: controla EXECUTION_SPEED, desligado
assert k.SetProcessInformation(h, 4, ctypes.byref(state), ctypes.sizeof(state)), ctypes.get_last_error()
sys.argv = sys.argv[1:]
runpy.run_path(sys.argv[0], run_name="__main__")
