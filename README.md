# Aero Language

**A fast, fluid language built for lightweight systems and high-speed execution.**
_Aero lifts your code off the ground - fast compile, faster runtime._

---

## Installation
From PyPI (recommended)
```bash
pip install aero-lang
```
From source (development)
```bash
git clone https://github.com/Aero-Organization/aero-lang.git
cd aero-lang
pip install -e .
```

---

## Quick Start
Create `hello.aero`:
```aero
// Aero v0.0.2b example
name = "World"
version = "0.0.2b"

print("Hello,", name, "!")
print("Aero version:", version)
```
Run it:
```bash
aero hello.aero
```
Output:
```
Hello, World !
Aero version: 0.0.2b
```

---

## Syntax Examples
Variables & Assignment
```aero
counter = 100
pi = 3.14  // Note: only integers supported in v0.0.2b
message = "Lift off!"
```
Function Calls
```aero
print("Signle arg")
print("Multiple", "args", "supported")
```
Expressions
```aero
x = 5
y = 10
print("Sum:", x + y) // Output: Sun: 15
```
> "**NOTE**: v0.0.2b supports only **integers,** **strings,** `+`, `-`, and `print()`. Full expressions, loops, and conditionals coming in v0.0.3a!"

---
## CLI Usage
```bash
aero [file.aero]
```
Examples:
```bash
aero examples/hello.aero
aero my_script.aero
```

---
## Roadmap
| VERSION | FEATURES |
| ------- | -------- |
| v0.0.3a | `if`/`else`,`while`,booleans, comparisons |
| v0.0.4a | Functions (`fn`), return values |
| v0.1.0  | First stable preview (stdlib, file I/O) |
