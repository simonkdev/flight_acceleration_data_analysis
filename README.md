# Flight Acceleration Data Analysis

A small project where I played around with using **accelerometer data recorded on a phone during aircraft landing**. This project analyzes the acceleration patterns to extract meaningful insights about the flight phases.

---

## 📌 About

### Purpose
This project was created to experiment with:
- **Accelerometer data analysis** from a smartphone
- **Flight phase detection** (takeoff, landing)
- **Signal processing** techniques (smoothing, jerk calculation)
- **Visualization** of acceleration patterns

### Data Source
- **Device**: Smartphone accelerometer
- **Context**: Aircraft landing
- **Data Type**: 3-axis timestamped acceleration (X, Y, Z) + absolute acceleration

---
## ✨ Features

- **Data Smoothing**: Rolling mean with 12-sample window
- **Touchdown Detection**: Automatic identification of landing moment
- **Jerk Calculation**: Rate of change of acceleration
- **Roughness Scoring**: Quantitative landing quality assessment
- **Landing Grading**: Automatic score (0-10) based on acceleration and jerk for qualitative comparison
- **Visualization**: Multiple plot types for different analysis aspects

If you want to use your own recordings, just replace the data source file with your own and adjust the column names to the example. I used phyphox on my phone, aligned to the plane I was sitting in with screen-to-sky and top-to-front. 

---
## 🔧 Analysis Methodology

### Data Processing
1. **Raw Data**: Loaded from CSV (`tables/plane_landing.csv`)
2. **Smoothing**: 12-sample rolling mean applied to all acceleration channels
3. **Peak Detection**: Touchdown identified as maximum absolute acceleration
4. **Jerk Calculation**:
   - Jerk = Δacceleration / Δtime
   - Calculated for all 4 acceleration channels (X, Y, Z, absolute)
5. **Roughness Score**:
   - RMS of absolute jerk values after touchdown
   - Higher values indicate rougher landings
6. **Landing Grade**:
   - Formula: `10 - (roughness/max_accel)*3 - (avg_abs_jerk)*4`
   - Range: 0-10 (higher is smoother)

### Key Parameters
| Parameter | Value | Description |
|-----------|-------|-------------|
| `ROLLING_WINDOW` | 12 | Samples for rolling mean smoothing |
| `ZOOM_WINDOW_MIN` | 180 | Focus window start (seconds) |
| `ZOOM_WINDOW_MAX` | 220 | Focus window end (seconds) |

---
## 🚀 Usage

### Prerequisites
- Python 3.11+
- Devenv (recommended)

### Setup
```sh
git clone https://github.com/simonkdev/flight_acceleration_data_analysis
cd flight_acceleration_data_analysis
devenv shell
```

### Running the Analysis
```sh
python main.py
```
This will:
1. Load accelerometer data from `tables/plane_landing.csv`
2. Apply smoothing to all acceleration channels
3. Calculate jerk values
4. Detect touchdown time
5. Compute roughness score and landing grade
6. Generate and save all visualization plots to `images/`
7. Create a detailed report in `landing_report.md`

---
## 📊 Outputs

### Generated Files
| File | Description |
|------|-------------|
| `images/acceleration_scatterplots.png` | Raw acceleration data (all axes) |
| `images/smoothed_acceleration.png` | Smoothed acceleration (all axes) |
| `images/combination_plot.png` | Raw vs. smoothed comparison |
| `images/smoothed_and_jerk_plot.png` | Smoothed acceleration + jerk |
| `images/raw_smoothed_and_jerk_plot.png` | All data combined |
| `tables/smoothed_df.csv` | Smoothed acceleration data |
| `tables/jerkframe.csv` | Calculated jerk values |
| `landing_report.md` | Complete analysis report |

### Sample Report Metrics
| Metric | Example Value | Description |
|--------|---------------|-------------|
| Raw touchdown time | 197.77 s | Time of max raw acceleration |
| Smoothed touchdown time | 197.97 s | Time of max smoothed acceleration |
| Raw peak acceleration | 9.99 m/s² | Maximum raw absolute acceleration |
| Smoothed peak acceleration | 5.08 m/s² | Maximum smoothed absolute acceleration |
| Peak acceleration (g) | 0.52 g | Peak in g-units |
| Max absolute jerk | 40.18 m/s³ | Highest rate of acceleration change |
| Rollout roughness | 2.69 | RMS jerk after touchdown |
| Landing grade | 8.40 / 10 | Overall landing quality score |

---
## 📁 Project Structure

```
flight_acceleration_data_analysis/
├── main.py                      # Main analysis script
├── landing_report.md            # Generated analysis report
├── images/                     # Generated visualization plots
│   ├── acceleration_scatterplots.png
│   ├── smoothed_acceleration.png
│   ├── combination_plot.png
│   ├── smoothed_and_jerk_plot.png
│   └── raw_smoothed_and_jerk_plot.png
├── tables/                     # Data files
│   ├── Acceleration without g (3).xlsx
│   ├── plane_landing.csv        # Raw accelerometer data
│   ├── smoothed_df.csv         # Generated: smoothed data
│   └── jerkframe.csv           # Generated: jerk data
├── devenv.nix                  # Devenv packages
├── devenv.yaml                 # Devenv config
├── devenv.lock                 # Locked dependencies
└── .envrc                      # Direnv configuration
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Core analysis script with all processing logic |
| `landing_report.md` | Auto-generated report with metrics and interpretations |
| `tables/plane_landing.csv` | Raw accelerometer data from the flight |
| `tables/smoothed_df.csv` | Smoothed acceleration data (generated) |
| `tables/jerkframe.csv` | Jerk values (generated) |
| `images/*.png` | Visualization plots (generated) |

---
## 📜 License

This project is licensed under the **MIT License**.

Copyright (c) 2026 Simon Korten
