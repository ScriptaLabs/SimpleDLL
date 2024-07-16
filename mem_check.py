import psutil
import ctypes

def mem_check():
    # virtual mem info
    mem = psutil.virtual_memory()
     #TEMPLATE BY PSUTIL MEMORY TOOLBOX
    print("Virtual Memory Information:")
    print(f"Total: {mem.total / (1024 ** 3):.2f} GB")
    print(f"Available: {mem.available / (1024 ** 3):.2f} GB")
    print(f"Used: {mem.used / (1024 ** 3):.2f} GB")
    print(f"Free: {mem.free / (1024 ** 3):.2f} GB")
    print(f"Percent used: {mem.percent}%")
    
    # Get page file information
    kernel32 = ctypes.windll.kernel32
    c_ulong = ctypes.c_ulong

    class MEMORYSTATUSEX(ctypes.Structure):
        _fields_ = [
            ("dwLength", c_ulong),
            ("dwMemoryLoad", c_ulong),
            ("ullTotalPhys", ctypes.c_ulonglong),
            ("ullAvailPhys", ctypes.c_ulonglong),
            ("ullTotalPageFile", ctypes.c_ulonglong),
            ("ullAvailPageFile", ctypes.c_ulonglong),
            ("ullTotalVirtual", ctypes.c_ulonglong),
            ("ullAvailVirtual", ctypes.c_ulonglong),
            ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
        ]

    memoryStatus = MEMORYSTATUSEX()
    memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
    kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))

    print("\nPage File Information:")
    print(f"Total: {memoryStatus.ullTotalPageFile / (1024 ** 3):.2f} GB")
    print(f"Available: {memoryStatus.ullAvailPageFile / (1024 ** 3):.2f} GB")
    print(f"Used: {(memoryStatus.ullTotalPageFile - memoryStatus.ullAvailPageFile) / (1024 ** 3):.2f} GB")
    print(f"Percent used: {(1 - memoryStatus.ullAvailPageFile / memoryStatus.ullTotalPageFile) * 100:.2f}%")

if __name__ == "__main__":
    mem_check()