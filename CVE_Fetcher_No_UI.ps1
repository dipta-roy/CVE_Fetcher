# Input and output file paths
$inputFile = "cve.csv"
$outputFile = "cve_output.csv"

# Read input CSV
$cveList = Import-Csv -Path $inputFile
$results = @()

# Loop over each CVE
for ($i = 0; $i -lt $cveList.Count; $i++) {
    $cveId = $cveList[$i].CVE_ID

    # Show progress
    $percentComplete = [math]::Round(($i / $cveList.Count) * 100)
    Write-Progress -Activity "Processing CVEs" -Status "$cveId ($($i + 1)/$($cveList.Count))" -PercentComplete $percentComplete

    try {
        $url = "https://cve.circl.lu/api/cve/$cveId"
        $response = Invoke-RestMethod -Uri $url -UseBasicParsing -ErrorAction Stop

        $container = $response.containers.cna

        # Title
        $title = "No Title Found"
        if ($container -and $container.title) {
            $title = $container.title
        }

        # Description
        $description = "No Description Found"
        if ($container -and $container.descriptions) {
            foreach ($desc in $container.descriptions) {
                if ($desc.lang -eq "en") {
                    $description = $desc.value
                    break
                }
            }
        }

        # CVSS
        $cvss = "N/A"
        if ($container -and $container.metrics) {
            foreach ($metric in $container.metrics) {
                if ($metric.cvssV3 -and $metric.cvssV3.baseScore) {
                    $cvss = $metric.cvssV3.baseScore
                    break
                } elseif ($metric.cvssV2 -and $metric.cvssV2.baseScore) {
                    $cvss = $metric.cvssV2.baseScore
                }
            }
        }

        # Exploit availability
        $exploitAvailable = "Unknown"
        if ($container -and $container.exploit -and $container.exploit.available) {
            $exploitAvailable = $container.exploit.available
        }

        # Add result
        $results += [PSCustomObject]@{
            CVE_ID           = $cveId
            Title            = $title
            Description      = $description
        }

    } catch {
        Write-Warning "$cveId failed: $($_.Exception.Message)"
        $results += [PSCustomObject]@{
            CVE_ID           = $cveId
            Title            = "Error"
            Description      = "Error"
        }
    }
}

# Export to CSV
$results | Export-Csv -Path $outputFile -NoTypeInformation -Encoding UTF8
Write-Host "Done. Output saved to $outputFile"
