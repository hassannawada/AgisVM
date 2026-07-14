import queue
import requests
import threading
import uuid

def worker_thread_routine(target_url, path_queue, results_list, baseline_profile):
    """
    Thread worker that performs content-length filtering to eliminate 
    wildcard routing false positives in high-velocity directory scans.
    """
    session = requests.Session()
    
    # Target status codes we want to investigate: 200 (OK), 301/302 (Redirects), 403 (Forbidden)
    target_status_codes = [200, 301, 302, 403]
    
    while not path_queue.empty():
        try:
            path = path_queue.get_nowait()
        except queue.Empty:
            break
            
        fuzzed_url = f"{target_url.rstrip('/')}/{path}"
        
        try:
            # Using GET requests here to fully profile content body sizes
            response = session.get(fuzzed_url, timeout=2.5, allow_redirects=False)
            status_code = response.status_code
            content_length = len(response.content)
            
            if status_code in target_status_codes:
                # ANTI-FALSE POSITIVE FILTER: Skip if it behaves exactly like our non-existent baseline canary
                if status_code == baseline_profile["status"] and content_length == baseline_profile["length"]:
                    continue
                    
                print(f"  [+] PRODUCTION RESOURCE: /{path} (Status: {status_code} | Size: {content_length} bytes)")
                results_list.append({"path": path, "status": status_code, "length": content_length})
                
        except requests.RequestException:
            pass
        finally:
            path_queue.task_done()

def calibrate_false_positive_baseline(target_url):
    """
    Generates a unique random string signature request to profile 
    how the target infrastructure handles non-existent paths.
    """
    print("[*] Calibrating Anti-False Positive baseline signatures...")
    random_canary_path = f"aegis_{uuid.uuid4().hex[:10]}"
    canary_url = f"{target_url.rstrip('/')}/{random_canary_path}"
    
    try:
        response = requests.get(canary_url, timeout=3.0, allow_redirects=False)
        profile = {"status": response.status_code, "length": len(response.content)}
        print(f"    └── [CALIBRATION SUCCESS]: Non-Existent baseline profiles as Status {profile['status']} (Size: {profile['length']} bytes)")
        return profile
    except requests.RequestException:
        print("    └── [CALIBRATION WARNING]: Host connection failure. Defaulting to empty baseline maps.")
        return {"status": 404, "length": 0}

def orchestrate_directory_bruteforce(target_url, wordlist_file="wordlist.txt", max_threads=4):
    print(f"\n[DIRECTORY ENGINE v2]: Initializing signature-filtered directory auditing on: {target_url}")
    
    # Run the validation calibration check before launching the threads
    baseline_profile = calibrate_false_positive_baseline(target_url)
    
    path_queue = queue.Queue()
    discovered_resources = []
    
    try:
        with open(wordlist_file, "r") as f:
            for line in f:
                clean_line = line.strip()
                if clean_line and not clean_line.startswith("#"):
                    path_queue.put(clean_line)
    except FileNotFoundError:
        print(f"[-] Directory Engine Error: Local wordlist database '{wordlist_file}' not found.")
        return []

    print(f"[DIRECTORY ENGINE]: Spawning {max_threads} concurrent thread workers against tracking matrix...")

    thread_pool = []
    for _ in range(max_threads):
        worker = threading.Thread(
            target=worker_thread_routine, 
            args=(target_url, path_queue, discovered_resources, baseline_profile)
        )
        worker.daemon = True
        thread_pool.append(worker)
        worker.start()

    path_queue.join()
    print(f"[DIRECTORY ENGINE COMPLETE]: Filtered mapping finished. Found {len(discovered_resources)} verified assets.")
    return discovered_resources

if __name__ == "__main__":
    test_endpoint = "http://localhost:5000"
    orchestrate_directory_bruteforce(test_endpoint)
