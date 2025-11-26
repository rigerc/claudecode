---
name: rust-developer
description: Use when writing Rust code, debugging issues, reviewing pull requests, or implementing CLI tools. Covers error handling, file I/O safety, performance, and best practices.
tags: [rust, development, debugging, cli, performance, io, safety]
---

# Rust Developer Guide

Comprehensive Rust development guidelines covering error handling, file I/O safety, performance, and common pitfalls.

## Quick Start

**New Rust project:**
```bash
cargo new rust_project
cd rust_project
cargo add tokio serde anyhow
```

**Error handling pattern:**
```rust
use anyhow::{Result, anyhow};

fn process_data() -> Result<String> {
    // Processing logic
    Ok(result)
}
```

## Expert Guidance

- **Error Handling**: Result<T> and anyhow for proper error propagation
- **File I/O**: Safe file operations and error handling
- **CLI Tools**: Command-line argument parsing and output
- **Performance**: Memory management and algorithmic efficiency
- **Testing**: Unit tests and integration testing
- **Code Review**: Common patterns and best practices

## Progressive Disclosure

Level 2 provides core patterns. Level 3+ contains detailed implementation guides and testing strategies.