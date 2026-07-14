#[unsafe(no_mangle)]
pub extern "C" fn initialize_engine() -> i32 {
    println!("[RUST CORE]: Memory pipeline initialized successfully.");
    return 1;
}cargo build --release
#[unsafe(no_mangle)]
pub extern "C" fn initialize_engine() -> i32 {
    println!("[RUST CORE]: Memory pipeline initialized successfully.");
    return 1;
}

// ---- MONTH 2: WEEK 1 CODE START HERE ----

use std::os::raw::c_char;
use std::ffi::{CStr, CString};

#[unsafe(no_mangle)]
pub extern "C" fn analyze_traversal_payload(input: *const c_char) -> *mut c_char {
    if input.is_null() {
        return CString::new("Safe").unwrap().into_raw();
    }

    let c_str = unsafe { CStr::from_ptr(input) };
    let raw_payload = match c_str.to_str() {
        Ok(s) => s.to_string(),
        Err(_) => return CString::new("Error: Invalid UTF-8").unwrap().into_raw(),
    };

    let mut normalized = raw_payload.to_lowercase();
    normalized = normalized.replace("%2e", ".");
    normalized = normalized.replace("%2f", "/");
    normalized = normalized.replace("%5c", "\\");
    normalized = normalized.replace("\\", "/");

    if normalized.contains("../") || normalized.contains(".../") || normalized.contains("..//") {
        return CString::new("High: Traversal Sequence Bypass Detected").unwrap().into_raw();
    }

    if normalized.contains("/etc/") || normalized.contains("c:/windows/") || normalized.contains("boot.ini") {
        return CString::new("Critical: Targeted OS System File Exposure").unwrap().into_raw();
    }

    CString::new("Safe").unwrap().into_raw()
}

#[unsafe(no_mangle)]
pub extern "C" fn free_string(s: *mut c_char) {
    if !s.is_null() {
        unsafe { CString::from_raw(s); }
    }
}
