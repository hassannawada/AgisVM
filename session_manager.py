import datetime
import hashlib
import json
import uuid

class TenantScanContext:
    """
    Encapsulates isolated tracking matrices for single deployment targets,
    fortified with real-time SHA-256 cryptographic integrity checksums.
    """
    def __init__(self, target_url):
        self.workspace_id = str(uuid.uuid4())[:8]
        self.target_url = target_url
        self.initialization_time = datetime.datetime.now()
        
        # Isolated container boundaries for tracking state findings privately
        self.discovered_ports = []
        self.discovered_paths = []
        
        # Initializing the baseline structural security hash tracker
        self.state_integrity_checksum = ""
        self._recompute_integrity_digest()
        
        print(f"\n[SESSION ENGINE v2]: Spawning cryptographically secured container for job ID: [{self.workspace_id}]")
        print(f"    └── Target: {self.target_url}")

    def _recompute_integrity_digest(self):
        """
        Internal cryptographic helper that hashes volatile memory states to enforce data protection.
        """
        raw_state_data = {
            "id": self.workspace_id,
            "target": self.target_url,
            "ports": list(self.discovered_ports),
            "paths": list(self.discovered_paths)
        }
        serialized_state = json.dumps(raw_state_data, sort_keys=True).encode('utf-8')
        return hashlib.sha256(serialized_state).hexdigest()

    def update_integrity(self):
        """
        Locks the current state digest on authorized modifications.
        """
        self.state_integrity_checksum = self._recompute_integrity_digest()

    def log_port_finding(self, port_number, service_name):
        self.discovered_ports.append({"port": port_number, "service": service_name})
        self.update_integrity()
        
    def log_path_finding(self, path, status_code):
        self.discovered_paths.append({"path": path, "status": status_code})
        self.update_integrity()

    def verify_runtime_integrity(self):
        """
        Evaluates the active data array against the stored tracking digest to detect unauthorized changes.
        """
        current_calculated = self._recompute_integrity_digest()
        return current_calculated == self.state_integrity_checksum
        
    def compile_session_summary(self):
        """
        Extracts structural point-in-time metrics alongside the active cryptographic integrity hash.
        """
        return {
            "workspace_id": self.workspace_id,
            "target": self.target_url,
            "integrity_hash": self.state_integrity_checksum,
            "metrics": {
                "ports_found": len(self.discovered_ports),
                "paths_found": len(self.discovered_paths)
            }
        }

if __name__ == "__main__":
    # Test checking simulation verifying automated cryptographic tamper tracking
    tenant_secure = TenantScanContext("http://localhost:5000")
    
    # 1. Log a valid network data finding through authorized channel
    tenant_secure.log_port_finding(5000, "Flask Lab")
    saved_checksum = tenant_secure.state_integrity_checksum
    print(f"    ├── Initial State Hash Check: {saved_checksum[:16]}...")
    print(f"    ├── Active State Integrity Verified: {tenant_secure.verify_runtime_integrity()}")
    
    # 2. Simulate an unauthorized background data injection bypassing secure channels
    print("\n[*] Simulating unauthorized memory modification attack vector...")
    tenant_secure.discovered_ports.append({"port": 9999, "service": "HACHED_INJECTED_VECTOR"})
    
    # Evaluation check - Must catch the alteration because saved_checksum won't match new computed data
    is_tampered = not tenant_secure.verify_runtime_integrity()
    print(f"    └── [🚨 INTEGRITY REPORT]: Data Tampering Detected? {is_tampered}")
