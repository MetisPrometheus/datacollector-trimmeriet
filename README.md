# Data Collector - Trimmeriet

This repository automatically collects visitor count data and weather conditions every 15 minutes using GitHub Actions. Data is stored in a CSV file for analysis.

## How It Works

1. GitHub Actions runs the Python script every 15 minutes
2. The script fetches the current visitor count from the website
3. Weather data is collected from the Norwegian Meteorological Institute (Yr)
4. All data is appended to a CSV file with timestamp
5. Changes are automatically committed to the repository

## Data File Structure

The CSV file (`data/visitor_counts.csv`) contains:

- timestamp - Date and time (YYYY-MM-DD HH:MM:SS)
- visitor_count - Number of visitors
- temperature - Temperature in °C
- weather_category - Weather condition (clear, cloudy, rainy, snowy, foggy)
- is_raining - Whether it's raining (yes/no)
- is_daytime - Whether it's daytime (yes/no)

## Running Locally

You can run the data collector in two ways:

### Option 1: Main Script (With Weather Data)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the collector once
python main.py
```

### Option 2: Continuous Local Scheduler

```bash
# Install dependencies
pip install requests beautifulsoup4 pandas psutil

# Run the scheduler (runs every minute)
python scheduler.py
```

The scheduler will collect visitor counts once per minute and save to a local CSV file. Press Ctrl+C to stop.

## Using This Data in Next.js

```javascript
// Example fetching the data in Next.js
import { useState, useEffect } from "react";

export default function VisitorStats() {
  const [visitorData, setVisitorData] = useState([]);

  useEffect(() => {
    async function fetchData() {
      const response = await fetch(
        "https://raw.githubusercontent.com/MetisPrometheus/datacollector-trimmeriet/main/data/visitor_counts.csv"
      );
      const csvText = await response.text();

      // Simple CSV parsing
      const rows = csvText.split("\n");
      const headers = rows[0].split(",");
      const data = rows
        .slice(1)
        .filter((row) => row.trim())
        .map((row) => {
          const values = row.split(",");
          return {
            timestamp: values[0],
            count: parseFloat(values[1]),
            temperature: parseFloat(values[2]),
            weather: values[3],
            isRaining: values[4] === "yes",
            isDaytime: values[5] === "yes",
          };
        });

      setVisitorData(data);
    }

    fetchData();
  }, []);

  return (
    <div>
      <h1>Visitor Count Data</h1>
      <ul>
        {visitorData.slice(-10).map((item, index) => (
          <li key={index}>
            {item.timestamp}: {item.count} visitors, {item.temperature}°C,{" "}
            {item.weather}
            {item.isRaining ? " (Raining)" : ""} {item.isDaytime ? "☀️" : "🌙"}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

## Files

- `main.py` - Main script that runs the collector
- `scraper.py` - Contains the visitor count fetching logic
- `weather.py` - Fetches weather data from Yr API
- `weather_simplifier.py` - Categorizes weather conditions
- `database.py` - Handles saving data to the CSV file
- `scheduler.py` - Local continuous scheduler (runs every minute)
- `.github/workflows/visitor-tracker.yml` - GitHub Actions workflow
