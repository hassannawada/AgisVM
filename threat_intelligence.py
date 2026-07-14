import json
import os

class ThreatIntelFeedProcessor:
    """
    Ingests real-time CVE Threat Intelligence feeds and scales fuzzer arrays
    by dynamically injecting discovered indicators directly into target wordlists.
    """
    def __init__(self):
        self.cached_advisories = []
        self.extracted_payloads = []

    def load_mock_threat_feed_stream(self):
        """
        Simulates ingesting an external structured security feed streaming 
        newly released high-severity zero-day exploit paths.
        """
        print("\n[THREAT INTEL v2]: Connecting to live vulnerability advisory stream...")
        mock_feed_data = """
        [
            {
                "cve_id": "CVE-2026-9991",
                "target_type": "api",
                "exploit_vector": "api/v1/debug/leak_config",
                "severity": "CRITICAL"
            },
            {
                "cve_id": "CVE-2026-9992",
                "target_type": "directory",
                "exploit_vector": "private_backup.tar.gz",
                "severity": "HIGH"
            }
        ]
        """
        try:
            self.cached_advisories = json.loads(mock_feed_data)
            print(f"    └── [FEED SUCCESS]: Ingested {len(self.cached_advisories)} active threat updates.")
        except json.JSONDecodeError:
            print("    └── [FEED ERROR]: Failed parsing incoming threat metadata buffer.")

    def inject_signatures_to_disk_wordlists(self, target_type, exploit_vector):
        """
        Safely injects dynamic threat strings into physical file dictionaries 
        while avoiding duplication states.
        """
        filename = "api_wordlist.txt" if target_type == "api" else "wordlist.txt"
        
        # Check if the baseline target wordlist exists
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("")

        # Read current entries to prevent dirty file padding duplicates
        with open(filename, "r") as f:
            existing_entries = [line.strip() for line in f.readlines()]

        if exploit_vector not in existing_entries:
            with open(filename, "a") as f:
                f.write(f"\n{exploit_vector}")
            print(f"        [+] INJECTION SUCCESS: Loaded vector onto physical asset database: {filename}")
        else:
            print(f"        [-] Skip Check: Vector already synchronized inside {filename}")

    def parse_and_sync_signatures(self):
        """
        Extracts specific path indicators and triggers dynamic file updates.
        """
        print("[THREAT INTEL]: Extracting actionable indicators of compromise (IoCs)...")
        new_paths_extracted = []
        
        for advisory in self.cached_advisories:
            target_type = advisory.get("target_type")
            exploit_vector = advisory.get("exploit_vector")
            cve_reference = advisory.get("cve_id")
            
            if exploit_vector and target_type:
                print(f"    ├── [SIGNATURE DISCOVERED]: Syncing vector pathway: /{exploit_vector} ({cve_reference})")
                new_paths_extracted.append(exploit_vector)
                
                # Dynamic injection to disk scaling
                self.inject_signatures_to_disk_wordlists(target_type, exploit_vector)
                
        self.extracted_payloads = new_paths_extracted
        return new_paths_extracted

if __name__ == "__main__":
    # Ingest and execute live dynamic synchronization testing profiles
    intel_engine = ThreatIntelFeedProcessor()
    intel_engine.load_mock_threat_feed_stream()
    intel_engine.parse_and_sync_signatures()
