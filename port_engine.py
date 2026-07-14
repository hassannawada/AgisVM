import asyncio
import socket
import sys
from urllib.parse import urlparse

# Service mapping signature index
SERVICE_SIGNATURES = {
    b"SSH": "Secure Shell Protocol (SSH)",
    b"HTTP": "Hypertext Transfer Protocol (HTTP)",
    b"Werkzeug": "Python Flask Development Server (Werkzeug)",
    b"MySQL": "MySQL Database Server"
}

async def grab_service_banner(reader, writer):
    """
    Extracts service identity signatures from raw socket connections.
    """
    try:
        writer.write(b"HEAD / HTTP/1.1\r\nHost: localhost\r\n\r\n")
        await writer.drain()
        
        banner_bytes = await asyncio.wait_for(reader.read(1024), timeout=1.5)
        if not banner_bytes:
            return "Unknown System Protocol (Null Buffer)"
            
        for signature, service_name in SERVICE_SIGNATURES.items():
            if signature in banner_bytes:
                return service_name
                
        if b"8.0." in banner_bytes or b"mysql" in banner_bytes.lower():
            return "MySQL Database Server"
            
        readable_banner = "".join([chr(b) if 32 <= b < 127 else "" for b in banner_bytes[:30]])
        return f"Active Target Profile | Signature: {readable_banner.strip()}"
    except Exception:
        return "Unidentified Infrastructure Port"

async def audit_single_socket(target_host, target_port, timeout_seconds=1.5):
    """
    Asynchronously probes a single port and catches Windows connection noise safely.
    """
    try:
        conn = asyncio.open_connection(target_host, target_port)
        reader, writer = await asyncio.wait_for(conn, timeout=timeout_seconds)
        
        print(f"  [+] DISCOVERY ALERT: Port {target_port} is OPEN.")
        service_banner = await grab_service_banner(reader, writer)
        
        try:
            writer.close()
            await writer.wait_closed()
        except Exception:
            pass # Suppresses Windows Proactor WinError 10054 noise completely
            
        return {"port": target_port, "service": service_banner}
    except Exception:
        return None

async def orchestrate_infrastructure_scan(target_url, port_range_list):
    print(f"\n[PORT ENGINE v2]: Starting raw socket & protocol profiling on: {target_url}")
    
    parsed_domain = urlparse(target_url).netloc
    if ":" in parsed_domain:
        target_host = parsed_domain.split(":")[0]
    else:
        target_host = parsed_domain if parsed_domain else urlparse(target_url).path

    if not target_host or target_host == "localhost":
        target_host = "127.0.0.1"

    print(f"[PORT ENGINE]: Scheduling {len(port_range_list)} concurrent socket verification workers...")

    async_tasks = [audit_single_socket(target_host, port) for port in port_range_list]
    
    loop = asyncio.get_running_loop()
    def handler(loop, context):
        pass # Drops socket reset anomalies silently on Windows systems
    loop.set_exception_handler(handler)
    
    scan_results = await asyncio.gather(*async_tasks, return_exceptions=True)
    active_vectors = [res for res in scan_results if isinstance(res, dict) and res is not None]
    
    print(f"[PORT ENGINE COMPLETE]: Resource mapping complete. Discovered {len(active_vectors)} active nodes.")
    return active_vectors
