# 🛡️ CVE Info Fetcher (Windows GUI + CIRCL.lu API)

This is a PowerShell-based Windows Forms application that reads a list of CVE IDs from a CSV file, fetches detailed vulnerability data from the [CIRCL.lu CVE API](https://cve.circl.lu/api/), and writes the enriched results into a new CSV file.

## 💡 Features

- ✅ Simple GUI to select input CSV and define output file
- 🌐 Uses CIRCL.lu public API to fetch CVE details
- 📊 Real-time progress bar during processing
- 📁 Outputs include:
  - CVE ID
  - Title
  - Description
  - CVSS Score
  - Exploit Availability
  - Data Source

## 🗂️ Input File Format

The input CSV should have a header row and a column titled `CVE_ID`:

```csv
CVE_ID
CVE-2024-47730
CVE-2023-25610
...
```

## 🧪 Output Example

```CVE_ID,Title,Description
CVE-2024-47730,Crypto Error Injection,In the Linux kernel...
```

## ▶️ How to Run

**Option 1: Double Click (GUI Launch)**
Save the script as `CVE_Fetcher_UI.ps1`

Open command prompt and enter `powershell.exe -ExecutionPolicy Bypass -File "C:\Path\To\CVE_Fetcher_UI.ps1"`

**Option 2: Run via .bat file**
You can automate script launch with a .bat file:

```bat
@echo off
powershell.exe -ExecutionPolicy Bypass -File "C:\Path\To\CVE_Fetcher_UI.ps1"
pause
```
Replace `C:\Path\To\CVE_Fetcher_UI.ps1` with the actual path to the script file.

Save this as `launch_cve_tool.bat` and double-click to launch.

Change `C:\Path\To\` in the above options to your current directory where the script is saved.

## 📦 Dependencies

Works on Windows 10/11

Requires PowerShell 5.1 or later (default in modern Windows)

No external modules required. Internet access is necessary to query the CIRCL.lu API.

## 📋 License

This project is provided under the MIT License. Use it, tweak it, and build on it.