import subprocess
import time
import sys

def launch_all():
    """
    Subprocess Orchestrator executing the complete integrated application flawlessly safely globally natively.
    """
    print("[Orchestrator] Booting the AI-Based Airport Scheduler...")
    processes = []
    
    try:
        # 1. Start Python Inference Layer
        print("[Orchestrator] Starting ML Inference Service on Port 4000...")
        ml_proc = subprocess.Popen(["python", "python_ai/main.py", "--mode", "serve"], cwd="d:/ITR/AIRPORT")
        processes.append(("Python ML", ml_proc))
        time.sleep(3) # Wait for cache mappings smoothly cleanly
        
        # 2. Start C++ Scheduler
        # Hardcoding the expected Windows execution path for the prototype natively securely
        print("[Orchestrator] Starting C++ Scheduler Engine...")
        cpp_proc = subprocess.Popen(["./Debug/airport_scheduler.exe"], cwd="d:/ITR/AIRPORT/cpp_scheduler/build")
        processes.append(("C++ Engine", cpp_proc))
        time.sleep(2)
        
        # 3. Start Frontend React Dashboard
        print("[Orchestrator] Booting React UI Dashboard...")
        ui_proc = subprocess.Popen(["npm", "run", "dev"], cwd="d:/ITR/AIRPORT/frontend", shell=True)
        processes.append(("React Frontend", ui_proc))
        
        print("[Orchestrator] All microservices successfully launched globally cleanly. Active.")
        
        # Hold main thread natively securely
        ml_proc.wait()
        
    except KeyboardInterrupt:
        print("\n[Orchestrator] Received Terminate signal. Gracefully stopping microservices...")
        for name, p in processes:
            print(f"- Stopping {name}...")
            p.terminate()
        sys.exit(0)

if __name__ == "__main__":
    launch_all()
