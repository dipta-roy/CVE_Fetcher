#
#    CVE Info Fetcher (Python + CIRCL.lu API)
#    Author   : Dipta Roy
#    Version  : 1.1
#    Last Edit: 2025-08-15
#    Description: 
#        Python GUI tool that fetches CVE details (titles, descriptions, CVSS scores, etc.) from the CIRCL.lu API using a CSV input file, saving results to a timestamped CSV. 
#
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
import requests
import json
from datetime import datetime
import re
import time
from tenacity import retry, stop_after_attempt, wait_exponential
import pandas as pd

class CVEFetcherApp:
    def __init__(self, root):
        # Initialize the main window with a title and background color
        self.root = root
        self.root.title("CSV Info Fetcher v1.1")
        self.root.configure(bg="#F0F0F0")
        self.root.geometry("600x500")
        self.cancelled = False
        self.file_path = None

        # Create and configure the main label
        self.label = tk.Label(root, text="CSV Info Fetcher v1.1",
                              font=("TkDefaultFont", 12), bg="#F0F0F0")
        self.label.pack(pady=10)

        # Create a frame for buttons and pack it
        self.button_frame = tk.Frame(root, bg="#F0F0F0")
        self.button_frame.pack(pady=10)

        # Add buttons to the frame in a horizontal row
        self.select_button = tk.Button(self.button_frame, text="Select CSV File with CVE IDs", command=self.select_file,
                                      font=("TkDefaultFont", 10), padx=5)
        self.select_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel_processing,
                                      state="disabled", font=("TkDefaultFont", 10), padx=5)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(self.button_frame, text="Reset", command=self.reset_ui,
                                     font=("TkDefaultFont", 10), padx=5)
        self.reset_button.pack(side=tk.LEFT, padx=5)

        self.close_button = tk.Button(self.button_frame, text="Close", command=self.close_program,
                                     font=("TkDefaultFont", 10), padx=5)
        self.close_button.pack(side=tk.LEFT, padx=5)

        # Create and configure the status label
        self.status_label = tk.Label(root, text="Status: Waiting for file selection...", bg="#F0F0F0",
                                    font=("TkDefaultFont", 10))
        self.status_label.pack(pady=10)

        # Create and configure the progress bar
        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=5)

        # Create and configure the text box with increased height
        self.progress_text = tk.Text(root, height=15, width=60, font=("TkDefaultFont", 10))
        self.progress_text.pack(pady=10)

        # Add developer credit at the bottom
        self.developer_label = tk.Label(root, text="Developed by Dipta Roy", bg="#F0F0F0",
                                       font=("TkDefaultFont", 8))
        self.developer_label.pack(side=tk.BOTTOM, pady=5)

    def clean_description(self, description):
        # Clean description by removing excessive newlines and normalizing spaces
        if not description or description == 'N/A':
            return description
        return re.sub(r'\n+', ' ', description).strip()

    def is_valid_cve(self, cve_id):
        # Validate CVE ID format (CVE-YYYY-NNNN)
        return bool(re.match(r'^CVE-\d{4}-\d{4,}$', cve_id, re.IGNORECASE))

    def cancel_processing(self):
        # Set flag to cancel processing and update UI
        self.cancelled = True
        self.status_label.config(text="Status: Processing cancelled")
        self.cancel_button.config(state="disabled")
        self.select_button.config(state="normal")

    def reset_ui(self):
        # Reset UI to initial state
        self.file_path = None
        self.cancelled = False
        self.status_label.config(text="Status: Waiting for file selection...")
        self.progress_bar["value"] = 0
        self.progress_text.delete(1.0, tk.END)
        self.select_button.config(state="normal")
        self.cancel_button.config(state="disabled")

    def close_program(self):
        # Close the program
        self.root.destroy()

    def select_file(self):
        # Open file dialog to select CSV and start processing
        self.file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if self.file_path:
            self.status_label.config(text=f"Selected file: {self.file_path}")
            self.select_button.config(state="disabled")
            self.cancel_button.config(state="normal")
            self.progress_text.delete(1.0, tk.END)
            self.root.after(100, self.process_csv)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def fetch_cve(self, cve_id):
        # Fetch CVE details with retry logic
        response = requests.get(f"https://cve.circl.lu/api/cve/{cve_id}", timeout=10)
        response.raise_for_status()
        return response.json()

    def process_csv(self):
        # Process CSV file asynchronously using root.after
        try:
            # Validate CSV
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                if not headers:
                    raise ValueError("CSV file must contain at least one header")
                cve_ids = [row[0].strip().upper() for row in reader if row and self.is_valid_cve(row[0])]

            if not cve_ids:
                raise ValueError("No valid CVE IDs found in CSV")

            self.progress_text.insert(tk.END, f"Found {len(cve_ids)} valid CVE IDs to process...\n")
            self.progress_bar["maximum"] = len(cve_ids)
            self.progress_bar["value"] = 0
            self.root.update()

            # Prepare output (fixed to CSV)
            output_file = f"Output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            output_headers = headers + ['Title', 'Description', 'CVSS Score', 'Exploit Available', 'CWE', 'References']
            results = []

            def process_next_cve(index, cve_ids, results):
                if index >= len(cve_ids) or self.cancelled:
                    # Save results to CSV
                    if results:
                        with open(output_file, 'w', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file)
                            writer.writerow(output_headers)
                            writer.writerows(results)
                    self.progress_text.insert(tk.END, f"\nOutput saved to: {output_file}\n")
                    self.status_label.config(text="Status: Processing complete!")
                    self.cancel_button.config(state="disabled")
                    self.select_button.config(state="normal")
                    messagebox.showinfo("Success", f"CVE details saved to {output_file}")
                    return

                cve_id = cve_ids[index]
                status = "Success"
                try:
                    data = self.fetch_cve(cve_id)
                    if not data or "error" in data or not data.get("containers", {}).get("cna"):
                        status = "Not Found"
                        results.append([cve_id] + [''] * (len(headers) - 1) + ['Not Found', 'Not Found', 'N/A', 'No', 'None', 'None'])
                    else:
                        cna = data.get("containers", {}).get("cna", {})
                        title = cna.get('title', 'N/A')
                        description = self.clean_description(cna.get('descriptions', [{}])[0].get('value', 'N/A'))
                        cvss_score = 'N/A'
                        metrics = cna.get('metrics', [])
                        for metric in metrics:
                            cvss_data = metric.get('cvssV3_1', {})
                            if cvss_data.get('baseScore'):
                                cvss_score = str(cvss_data['baseScore'])
                                break
                        exploit_available = 'No'
                        adp = data.get("containers", {}).get("adp", [])
                        for entry in adp:
                            for metric in entry.get('metrics', []):
                                ssvc = metric.get('other', {}).get('content', {})
                                if ssvc.get('options', []):
                                    for option in ssvc['options']:
                                        if option.get('Exploitation') == 'active':
                                            exploit_available = 'Yes'
                                            break
                                if exploit_available == 'Yes':
                                    break
                            if exploit_available == 'Yes':
                                break
                        cwe = 'None'
                        problem_types = cna.get('problemTypes', [])
                        for pt in problem_types:
                            for desc in pt.get('descriptions', []):
                                if desc.get('cweId'):
                                    cwe = desc['cweId']
                                    break
                            if cwe != 'None':
                                break
                        references = ';'.join([ref.get('url', '') for ref in cna.get('references', []) if ref.get('url')])
                        if not references:
                            references = 'None'
                        results.append([cve_id] + [''] * (len(headers) - 1) + [title, description, cvss_score, exploit_available, cwe, references])

                except requests.RequestException as e:
                    status = f"Error: {str(e)}"
                    results.append([cve_id] + [''] * (len(headers) - 1) + ['Error', str(e), 'N/A', 'No', 'None', 'None'])

                self.progress_text.insert(tk.END, f"{index + 1}/{len(cve_ids)} {cve_id} -- {status}\n")
                self.progress_text.see(tk.END)
                if index % 2 == 0:  # Update progress bar every 2 iterations
                    self.progress_bar["value"] = index + 1
                    self.root.update()

                time.sleep(0.5)  # Respect API rate limits
                self.root.after(100, process_next_cve, index + 1, cve_ids, results)

            process_next_cve(0, cve_ids, results)

        except Exception as e:
            self.progress_text.insert(tk.END, f"Error: {str(e)}\n")
            self.status_label.config(text="Status: Error occurred")
            self.cancel_button.config(state="disabled")
            self.select_button.config(state="normal")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    # Start the main application
    root = tk.Tk()
    app = CVEFetcherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()