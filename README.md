# Project AgisVM

Project Type: Hybrid Automated Malware Analysis and Vulnerability Scanner
Core Technologies: Python (High-Level Orchestrator) and Rust (Low-Level Secure VM Engine)

## System Architecture and 9-Phase Pipeline

AgisVM replaces legacy sequential network scanning by routing data packets through an asynchronous 9-Phase Master Orchestration Lifecycle:

1. Threat Intelligence Feed Ingestion: Real-time JSON/YAML CVE advisory streams parse and dynamically mutate attack dictionaries on-disk.
2. Multi-Tenant Isolation Envelope: Instantiates a cryptographically unique runtime tracking context (TenantScanContext) to enforce data-pool barriers.
3. Rust Native Handshake: Crosses the Foreign Function Interface (FFI) boundary to verify pipeline integrity using raw pointers.
4. Asynchronous Socket Probe: Dispatches non-blocking raw TCP SYN parallel workers to catalog target network openings.
5. Threaded Baseline Fuzzer: Utilizes synchronized workers to discover hidden directories against predictive wordlists.
6. API Structure Morphing: Modifies active JSON schemas to map unhandled server faults on programmatic routes.
7. Vulnerability Audit Matrix: Evaluates target endpoints against specialized modules (SQLi, Blind SQLi, XSS, Path Traversal).
8. Automated Exploit Exfiltration: Simulates safe read-only payload vectors to confirm vulnerabilities through verifiable FLAG string captures.
9. Unified Reporting Pipeline: Exports forensic metrics into structural JSON backups and HTML dashboards.


## Feature Breakdown and Core Modules

### Low-Level Rust Core Engine (aegis_core)
- GIL Bypass: Avoids Python Global Interpreter Lock (GIL) by porting continuous file analytics down to native machine code binaries (.dll / .so).
- FFI Boundary Safety: Implements explicit pointer tracking wrapped in null-checks to eliminate OS-level segmentation faults.

### Advanced Scanning Matrix
- Timing-Based Blind SQLi: Uses passive performance profiling to track database engine thread latency down to the millisecond, bypassing error-silent endpoints.
- Reflected XSS Auditor: Maps document templates for raw, unencoded payload echoes using standalone, circular-import-protected modules.
- Dual-Platform Path Traversal: Mutates multi-vector string arrays using both POSIX (../) and Windows (..\) platform breakout variations.
- Anti-False Positive Calibration: Injects a random canary path sequence prior to execution to establish an application response baseline, filtering out structural wildcard router behaviors.

### Enterprise-Grade Resilience
- Tamper-Evident State Hashing: Recomputes volatile memory objects continuously into an active SHA-256 digest stream to detect background variable injection attacks.
- Windows Proactor Patching: Deploys a global exception tracker to capture abrupt remote network disconnect warnings, silencing traceback logs gracefully.


## Tech Stack

Component | Technology
--- | ---
High-Level Orchestrator | Python 3.10+ (Asyncio, Ctypes, Flask, BeautifulSoup, Requests)
Low-Level Subsystem | Rust (Cargo, C-FFI Architecture, System Toolchain)
Sandboxing Environment | Docker Desktop, WSL 2 (Ubuntu Kernel Core)
IDE and Tooling | VS Code, Microsoft C++ Build Tools (link.exe), Git


## Getting Started

### Prerequisites
- Python v3.10+
- Rustup and Cargo
- Microsoft C++ Build Tools (For Windows hosts compiling .dll runtimes)

### Installation and Compilation

1. Clone the repository and submodules:
   ```bash
   git clone https://github.com
   cd AgisVM
   ```

2. Compile the Native Rust Core Binary:
   ```bash
   cd aegis_backend
   cargo build --release
   ```
   This outputs a highly optimized aegis_backend.dll (Windows) or aegis_backend.so (Linux) compiled dynamic utility library.

3. Configure the Master Python Orchestrator:
   Return to the root folder, configure your localized environment variables, and verify that the compiled Rust library is placed correctly within the project tree path:
   ```bash
   cd ..
   pip install -r requirements.txt
   ```

4. Initialize the Simulated Target Laboratory:
   Spin up the local micro-service test target to confirm diagnostic telemetry reporting loops:
   ```bash
   python vulnerable_app.py
   ```
   The target web server will run locally at http://localhost:5000.

5. Execute the Comprehensive 9-Phase Master Suite:
   ```bash
   python orchestrator.py --target http://localhost:5000
   ```


## Reporting and Dashboards

AgisVM generates universal, standalone audit logs out-of-the-box:
- Machine-Readable: Automated backups write persistent JSON states directly to report_tenant_id.json.
- Executive Presentation: HTML user interface dashboards map out attack metrics alongside pre-formatted remediation code blocks, strictly configured with universal UTF-8 character mapping to preserve diagnostic visual indicators cleanly across both Unix and Windows host systems.


## Development Milestones and Version Registry

- Phase 1 (Month 1-2): Core FFI Pipeline Handshake, HTML Crawler, SQLi/XSS Base Implementations. Commit: f70de4e
- Phase 2 (Month 3-5): Asyncio Raw Sockets Port Scanner, Multi-Threaded Canary Directory Worker Queues, API Data Fuzzer.
- Phase 3 (Month 6-8): Multi-Tenant Isolation Space Engine, Cryptographic Data Vault SHA Hashing Core.
- Phase 4 (Month 9-10): Live Threat Intelligence Parser Streaming, Executive HTML Visual Systems, Architecture Lock.


## Contributing

1. Fork the Project Repository.
2. Build your local tracking branch:
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. Commit your system changes:
   ```bash
   git commit -m "Add some AmazingFeature"
   ```
4. Push upstream:
   ```bash
   git push origin feature/AmazingFeature
   ```
5. Open a formal Pull Request review thread.


## Authors and Contact

- Hassan Ali - Lead Security Software Architect - hassanalich5616@gmail.com
- Project Link: https://github.com/hassannawada/AgisVM
