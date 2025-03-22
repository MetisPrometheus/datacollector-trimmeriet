# Data Collector - Trimmeriet

This repository automatically collects visitor count data and weather conditions every 15 minutes using GitHub Actions. It also tracks Norwegian holidays and vacation periods to enable richer data analysis.

## Data Collection

The system collects and stores:

- **Visitor counts**: Number of visitors at Trimmeriet
- **Weather data**: Temperature and weather conditions from the Norwegian Meteorological Institute
- **Holiday status**: All official Norwegian public holidays
- **Vacation periods**: Common Norwegian vacation and academic periods
- **Time information**: Timestamps with day/night distinction

## Data Structure

The CSV file (`data/visitor_counts.csv`) contains:

| Column             | Description                                            |
| ------------------ | ------------------------------------------------------ |
| timestamp          | Date and time (YYYY-MM-DD HH:MM:SS)                    |
| visitor_count      | Number of visitors                                     |
| temperature        | Temperature in °C                                      |
| weather_category   | Weather condition (clear, cloudy, rainy, snowy, foggy) |
| is_raining         | Whether it's raining (yes/no)                          |
| is_daytime         | Whether it's daytime (yes/no)                          |
| is_holiday         | Whether it's an official holiday (yes/no)              |
| is_vacation_period | Whether it's a common vacation period (yes/no)         |
| special_date_name  | Name of the holiday or vacation period, if applicable  |

## Special Periods Tracked

### Official Holidays

- New Year's Day (Nyttårsdag)
- Easter holidays (Påske)
- Labor Day (Arbeidernes dag)
- Constitution Day (Grunnlovsdag)
- Christmas holidays (Jul)
- And all other Norwegian public holidays

### Academic & Vacation Periods

- **Eksamensperiode (Exam Period)** - All of May through first week of June
- **Studentferie (Student Summer)** - June 8-30 and August 1-14
- **Fellesferie (Summer Vacation)** - All of July
- **Juleferie (Christmas Break)** - December 20 - January 2
- **Vinterferie (Winter Break)** - Week 8 (February)
- **Påskeferie (Easter Break)** - Week before/after Easter

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

## Using This Data

### In a Next.js App

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
            isHoliday: values[6] === "yes",
            isVacationPeriod: values[7] === "yes",
            specialDate: values[8],
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
            {item.isRaining ? " 🌧️" : ""}
            {item.isDaytime ? "☀️" : "🌙"}
            {item.isHoliday ? "🎉" : ""}
            {item.isVacationPeriod ? "✈️" : ""}
            {item.specialDate ? ` (${item.specialDate})` : ""}
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
- `enhanced_vacation_periods.py` - Tracks Norwegian holidays and vacation periods
- `scheduler.py` - Local continuous scheduler (runs every minute)
- `.github/workflows/visitor-tracker.yml` - GitHub Actions workflow that runs every 15 minutes
