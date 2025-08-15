# 🛡️ CVE Info Fetcher 

Tool to fetch CVE details from online APIs based on a list of CVE IDs. Supports both Python (GUI) and PowerShell (Console) implementations.

![CVE Fetcher Screenshot](https://raw.githubusercontent.com/dipta-roy/CVE_Fetcher/refs/heads/main/screenshot.png)
![CVE Fetcher Screenshot](https://raw.githubusercontent.com/dipta-roy/CVE_Fetcher/refs/heads/main/Python_Screenshot.png)

## 💡 Features

- Fetch CVE details such as Title, Description, CVSS Score, Exploit Availability, CWE, and References.
- Input CVE IDs from a CSV or TXT file.
- Save results to a timestamped CSV file.
- Two options to run:
  - **Python GUI Tool** (interactive interface)
  - **PowerShell Script** (command-line based)

## 🗂️ Input File Format

The input CSV should have a header row and a column titled `CVE_ID`:

```csv
CVE_ID
CVE-2024-47730
CVE-2023-25610
...
```

## Prerequisites

### For Python Program
1. **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
2. Install required Python libraries:
   ```bash
   pip install requests pandas tenacity
   ```
3. Internet connection (fetches data from the [CIRCL.lu CVE API](https://cve.circl.lu/api)).

### For PowerShell Program
1. Windows PowerShell 5.1+ (or PowerShell Core 7+)
2. Internet connection (fetches data from [endoflife.date](https://endoflife.date/api) or CIRCL.lu API depending on script).


## Python Program – CVE Info Fetcher (GUI)

### File:
`CVE_Info_Fetcher.py`

### How to Run:
1. Save your CVE IDs in a CSV file.
   - First column: `CVE-YYYY-NNNN` format
   - Example:
     ```
     CVE-ID
     CVE-2024-12345
     CVE-2023-54321
     ```
2. Open a terminal in the folder containing `CVE_Info_Fetcher.py`.
3. Run:
   ```bash
   python CVE_Info_Fetcher.py
   ```
4. In the GUI:
   - Click **"Select CSV File with CVE IDs"**
   - Wait while it processes each CVE
   - Output file will be saved as `output_YYYYMMDD_HHMMSS.csv`.
   
## PowerShell Program – CVE Fetcher (Console) 

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


## Notes
- The Python version provides a progress bar, live status updates, and a Cancel option.
- The PowerShell version is simpler but runs directly in the terminal.
- Make sure your CSV files follow the correct format for best results.

## 📋 License

This project is provided under the MIT License. Use it, tweak it, and build on it.

## Author

- **Name:** Dipta Roy
- **Version:** 1.1
- **Last Updated:** August 15, 2025