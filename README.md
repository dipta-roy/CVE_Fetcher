# 🛡️ CVE Info Fetcher

A tool to fetch CVE details from the CIRCL.lu CVE API using a list of CVE IDs. Supports both Python (GUI) and PowerShell (Console) implementations.

## ✨ Features

- Fetches CVE details: Title, Description, CVSS Score, Exploit Availability, CWE, and References.
- Accepts input from CSV or TXT files.
- Saves results to a timestamped CSV file (`output_YYYYMMDD_HHMMSS.csv`).
- Two implementations:
  - **Python GUI**: Interactive interface with progress bar and cancel option.
  - **PowerShell Script**: Command-line based with simple Windows GUI.

## 📝 Input File Format

The input CSV must have a header row with a `CVE_ID` column:

```csv
CVE_ID
CVE-2024-47730
CVE-2023-25610
```

## 🛠️ Prerequisites

### Python Program
- Python 3.8+ ([Download](https://www.python.org/downloads/))
- Required libraries: `requests`, `pandas`, `tenacity`
- Internet connection (uses CIRCL.lu CVE API)

### PowerShell Program
- Windows PowerShell 5.1+ or PowerShell Core 7+
- Internet connection (uses CIRCL.lu CVE API)

## 🚀 Installation

### Python Program
1. Install Python dependencies:
   ```bash
   pip install requests pandas tenacity
   ```
2. Download `CVE_Info_Fetcher.py` from the repository.

### PowerShell Program
1. Download `CVE_Fetcher_UI.ps1` from the repository.
2. Ensure PowerShell execution policy allows script execution:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass
   ```

## ▶️ Usage

### Python Program (GUI)
1. Prepare a CSV file with CVE IDs (see [Input File Format](#input-file-format)).
2. Run the script:
   ```bash
   python CVE_Info_Fetcher.py
   ```
3. In the GUI:
   - Click "Select CSV File with CVE IDs".
   - Monitor progress via the progress bar.
   - Output is saved as `output_YYYYMMDD_HHMMSS.csv`.

### PowerShell Program (Console)
#### Option 1: Direct Launch
1. Prepare a CSV file with CVE IDs.
2. Run the script:
   ```powershell
   powershell.exe -ExecutionPolicy Bypass -File "path\to\CVE_Fetcher_UI.ps1"
   ```
3. Select the CSV file via the GUI prompt.
4. Output is saved as `output_YYYYMMDD_HHMMSS.csv`.

#### Option 2: Batch File Launch
1. Create a `.bat` file (e.g., `launch_cve_tool.bat`):
   ```batch
   @echo off
   powershell.exe -ExecutionPolicy Bypass -File "path\to\CVE_Fetcher_UI.ps1"
   pause
   ```
2. Double-click the `.bat` file to run.

## ⚠️ Troubleshooting

- **Invalid CSV format**: Ensure the CSV has a `CVE_ID` header and valid CVE IDs (e.g., `CVE-YYYY-NNNN`).
- **API errors**: Verify internet connectivity and CIRCL.lu API availability.
- **PowerShell script blocked**: Run `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass` in PowerShell.
- **Python dependencies missing**: Reinstall dependencies using `pip install requests pandas tenacity`.

## 🔳 Screenshots

![CVE Fetcher Screenshot](https://raw.githubusercontent.com/dipta-roy/CVE_Fetcher/refs/heads/main/screenshot.png)
![CVE Fetcher Screenshot](https://raw.githubusercontent.com/dipta-roy/CVE_Fetcher/refs/heads/main/Python_Screenshot.png)

## 📋 License

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute.

## 👨‍💻 Author

- **Name**: Dipta Roy
- **Version**: 1.1
- **Last Updated**: August 15, 2025