<#
    CVE Info Fetcher (Windows GUI + CIRCL.lu API)
    Author   : Dipta Roy
    Version  : 1.0
    Last Edit: 2025-08-02
    Description:
        PowerShell-based GUI tool to fetch CVE details from https://cve.circl.lu/api/
        using a CSV input with a column named CVE_ID. The output is saved in a new CSV file.
#>

# Load required .NET assemblies
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Create the main form
$form = New-Object System.Windows.Forms.Form
$form.Text = "CVE Fetcher"
$form.Size = New-Object System.Drawing.Size(500,300)
$form.StartPosition = "CenterScreen"

# File Dialogs
$openFileDialog = New-Object System.Windows.Forms.OpenFileDialog
$saveFileDialog = New-Object System.Windows.Forms.SaveFileDialog
$saveFileDialog.Filter = "CSV files (*.csv)|*.csv"

# Label for input file
$label1 = New-Object System.Windows.Forms.Label
$label1.Text = "Input CSV (with CVE_ID column):"
$label1.Location = '10,20'
$label1.AutoSize = $true
$form.Controls.Add($label1)

# Label for input file
$textBoxInput = New-Object System.Windows.Forms.TextBox
$textBoxInput.Size = '300,20'
$textBoxInput.Location = '10,40'
$form.Controls.Add($textBoxInput)

# Browse button for input file
$buttonBrowse = New-Object System.Windows.Forms.Button
$buttonBrowse.Text = "Browse"
$buttonBrowse.Location = '320,38'
$buttonBrowse.Add_Click({
    if ($openFileDialog.ShowDialog() -eq "OK") {
        $textBoxInput.Text = $openFileDialog.FileName
    }
})
$form.Controls.Add($buttonBrowse)

# Label for output file
$label2 = New-Object System.Windows.Forms.Label
$label2.Text = "Output CSV file name:"
$label2.Location = '10,70'
$label2.AutoSize = $true
$form.Controls.Add($label2)

# Output file textbox
$textBoxOutput = New-Object System.Windows.Forms.TextBox
$textBoxOutput.Size = '300,20'
$textBoxOutput.Location = '10,90'
$form.Controls.Add($textBoxOutput)

# Save As button for output file
$buttonSave = New-Object System.Windows.Forms.Button
$buttonSave.Text = "Save As"
$buttonSave.Location = '320,88'
$buttonSave.Add_Click({
    if ($saveFileDialog.ShowDialog() -eq "OK") {
        $textBoxOutput.Text = $saveFileDialog.FileName
    }
})
$form.Controls.Add($buttonSave)

# Progress bar to indicate processing
$progressBar = New-Object System.Windows.Forms.ProgressBar
$progressBar.Location = '10,130'
$progressBar.Size = '450,20'
$form.Controls.Add($progressBar)

# Status label
$statusLabel = New-Object System.Windows.Forms.Label
$statusLabel.Location = '10,160'
$statusLabel.Size = '450,20'
$form.Controls.Add($statusLabel)

# Start Fetch button
$buttonStart = New-Object System.Windows.Forms.Button
$buttonStart.Text = "Start Fetch"
$buttonStart.Location = '10,200'
$form.Controls.Add($buttonStart)

# Start button logic
$buttonStart.Add_Click({
    $inputFile = $textBoxInput.Text
    $outputFile = $textBoxOutput.Text
	
	# Check for valid input file
    if (-not (Test-Path $inputFile)) {
        [System.Windows.Forms.MessageBox]::Show("Input file not found!")
        return
    }

    $cveList = Import-Csv $inputFile
    $total = $cveList.Count
	if ($total -eq 0) {
		[System.Windows.Forms.MessageBox]::Show("No CVE IDs found in the input file.")
		return
	}
    $results = @()

    $progressBar.Value = 0
    $i = 0

    foreach ($row in $cveList) {
        $cveId = $row.CVE_ID.Trim()
        $statusLabel.Text = "Fetching $cveId..."
        $form.Refresh()

        $url = "https://cve.circl.lu/api/cve/$cveId"

        try {
            $response = Invoke-RestMethod -Uri $url -Method Get -ErrorAction Stop
            $container = $response.containers.cna

            $title = $container.title
            $description = ($container.descriptions | Where-Object { $_.lang -eq 'en' }).value
            $cvss = ($container.metrics | Where-Object { $_.cvssV3 }).cvssV3.baseScore
            $exploit = "Unknown"

            if ($null -eq $cvss) { $cvss = "N/A" }
            if ($null -eq $title) { $title = "No Title Found" }
            if ($null -eq $description) { $description = "No Description Found" }

            $results += [PSCustomObject]@{
                CVE_ID = $cveId
                Title = $title
                Description = $description
            }
        } catch {
            $results += [PSCustomObject]@{
                CVE_ID = $cveId
                Title = "Error"
                Description = "Failed to fetch"
            }
        }

        $i++
        $progressBar.Value = [math]::Round(($i / $total) * 100)
    }
	# Export results to CSV
    $results | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8
    [System.Windows.Forms.MessageBox]::Show("Done! Output saved to $outputFile")
    $statusLabel.Text = "Completed!"
})

# Show form
$form.Add_Shown({ $form.Activate() })
[void]$form.ShowDialog()