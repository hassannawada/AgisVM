import queue
import requests
import threading

# Security injection signatures targeting application backend configurations
API_FAULT_PAYLOADS = [
    "' OR '1'='1' --",       # Classical Auth Bypass Signature
    "admin' --",             # Parameter Clamping Vector
    "<script>alert(1)</script>", # Cross-Site Script Structural Breakout
    "../../etc/passwd"       # Resource Breakout Payload
]

def fuzz_api_payload_structure(target_endpoint_url, active_session):
    """
    Simulates intelligent JSON body morphing by dynamically injecting security
    fault structures into standard programmatic payload maps.
    """
    print(f"      └── [API FUZZER ACTIVE]: Profiling parameter fault arrays against vector paths...")
    
    # Simulating a default captured schema structure representing a regular client API post request
    base_json_template = {"user_id": "test_guest", "auth_token": "active_session_token", "query": "default"}
    
    # Catching anomalous server states: 500 (Internal Server Error) or 503 (Service Unavailable)
    fault_trigger_statuses = [500, 503]
    
    for payload in API_FAULT_PAYLOADS:
        for target_parameter in base_json_template.keys():
            # Create a localized deep clone template copy to mutate arguments independently
            morphed_json_body = base_json_template.copy()
            morphed_json_body[target_parameter] = payload
            
            try:
                # Dispatching dynamic raw POST requests containing mutated structured parameters
                response = active_session.post(
                    target_endpoint_url, 
                    json=morphed_json_body, 
                    timeout=2.0
                )
                
                # Intercepting anomalous server error states (Internal Errors, Database Faults, Script Breaks)
                if response.status_code in fault_trigger_statuses:
                    print(f"          [!] FAULT VECTOR DISCOVERED: Parameter [{target_parameter}] leaked anomalous Status {response.status_code} on injection!")
            except requests.RequestException:
                pass

def api_worker_routine(target_url, api_queue, discovered_apis):
    """
    Isolated worker that probes endpoints and conditionally triggers structural data fuzzing routines.
    """
    session = requests.Session()
    valid_statuses = [200, 201, 202, 301, 302, 401, 403]
    
    while not api_queue.empty():
        try:
            endpoint = api_queue.get_nowait()
        except queue.Empty:
            break
            
        full_api_url = f"{target_url.rstrip('/')}/{endpoint}"
        
        try:
            headers = {"Accept": "application/json, text/plain, */*"}
            response = session.get(full_api_url, headers=headers, timeout=2.5, allow_redirects=False)
            
            content_type = response.headers.get("Content-Type", "").lower()
            status_code = response.status_code
            
            if status_code in valid_statuses:
                is_json = "json" in content_type or "xml" in content_type
                info_string = "JSON API" if is_json else "Standard Web Endpoint"
                
                print(f"  [+] API VECTOR FOUND: /{endpoint} (Status: {status_code} | Type: {info_string})")
                discovered_apis.append({
                    "endpoint": endpoint,
                    "status": status_code,
                    "is_programmatic": is_json
                })
                
                # CORE ENGINE UPGRADE: Trigger content parameter injection checks on the live target stream
                fuzz_api_payload_structure(full_api_url, session)
                
        except requests.RequestException:
            pass
        finally:
            api_queue.task_done()

def orchestrate_api_enumeration(target_url, wordlist_path="api_wordlist.txt", threads_count=4):
    print(f"\n[API ENGINE v2]: Launching data-injection & programmatic fuzzing on: {target_url}")
    
    api_queue = queue.Queue()
    discovered_apis = []
    
    try:
        with open(wordlist_path, "r") as f:
            for line in f:
                clean_line = line.strip()
                if clean_line and not clean_line.startswith("#"):
                    api_queue.put(clean_line)
    except FileNotFoundError:
        print(f"[-] API Engine Error: Wordlist matrix '{wordlist_path}' could not be located.")
        return []

    print(f"[API ENGINE]: Dispatched {api_queue.qsize()} endpoint profiles into task queue matrix.")
    
    workers_pool = []
    for _ in range(threads_count):
        worker = threading.Thread(
            target=api_worker_routine,
            args=(target_url, api_queue, discovered_apis)
        )
        worker.daemon = True
        workers_pool.append(worker)
        worker.start()
        
    api_queue.join()
    print(f"[API ENGINE COMPLETE]: Injection cycle wrapped up. Logged {len(discovered_apis)} API structures.")
    return discovered_apis

if __name__ == "__main__":
    test_endpoint = "http://localhost:5000"
    orchestrate_api_enumeration(test_endpoint)
