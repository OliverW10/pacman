import ctypes
import pathlib
import time

file_dir = pathlib.Path(__file__).parent.resolve()
print(file_dir)
module = ctypes.CDLL(f"{file_dir}/evaluate.so")
module.testFunc.argtypes = [ctypes.c_int]
start_time = time.perf_counter()
ret = module.testFunc(3)
print((time.perf_counter()-start_time)*1000)
print(ret)
