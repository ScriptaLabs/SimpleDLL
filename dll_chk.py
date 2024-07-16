import psutil
import os
import sys

def chk(pid):
    try:
        process = psutil.Process(pid)
        dlls = process.memory_maps()
        
        print(f"DLLs attached to {pid}:")
        for dll in dlls:
            # Extract just the filename from the path
            dll_name = os.path.basename(dll.path)
            print(f"- {dll_name}")
        
        print(f"\nTotal DLLs: {len(dlls)}")
    
    except psutil.NoSuchProcess:
        print(f"No process found with PID {pid}")
    except psutil.AccessDenied:
        print(f"Access denied to process with PID {pid}. Try running the script as administrator.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python dll_chk.py <PID>")
        sys.exit(1)
    
    try:
        pid = int(sys.argv[1])
    except ValueError:
        print("PID must be a number")
        sys.exit(1)
    
    chk(pid)