# Weather Data Analysis Script
# This program analyzes weather data from a CSV file.
# It cleans the data, calculates statistics, creates visualizations,
# groups data by seasons, and generates a summary report.

import os
import pandas as pd
import matplotlib.pyplot as plt

def load_data(file_path):
    """Load weather data from CSV file and show basic information."""
    print("Loading weather data...")
    df = pd.read_csv(file_path)
    print("Data loaded successfully!")
    print(f"Shape: {df.shape}")
    print("First few rows:")
    print(df.head())
    return df

def clean_data(df):
    """Clean the data by handling dates and missing values."""
    print("\nCleaning data...")

    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Remove rows with invalid dates
    df = df.dropna(subset=['Date'])

    # Fill missing numeric values with averages
    numeric_cols = ['Temperature', 'Rainfall', 'Humidity']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].mean())

    print(f"Data cleaned! Shape: {df.shape}")
    return df

def calculate_stats(df):
    """Calculate daily, monthly, and yearly statistics."""
    print("\nCalculating statistics...")

    # Set Date as index for time-based operations
    df_stats = df.set_index('Date')

    # Daily averages
    daily_stats = df_stats.resample('D').mean()

    # Monthly statistics
    monthly_stats = df_stats.resample('ME').agg(['mean', 'min', 'max', 'std'])

    # Yearly statistics
    yearly_stats = df_stats.resample('YE').agg(['mean', 'min', 'max', 'std'])

    print("Statistics calculated!")
    return {'daily': daily_stats, 'monthly': monthly_stats, 'yearly': yearly_stats}

def create_plots(df, output_dir="output"):
    """Create various plots from the weather data."""
    print("\nCreating plots...")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Temperature trend
    plt.figure(figsize=(10, 6))
    df_temp = df.set_index('Date').resample('D').mean()
    plt.plot(df_temp.index, df_temp['Temperature'], 'b-', linewidth=2)
    plt.title('Daily Temperature Trend', fontsize=14)
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{output_dir}/temperature_trend.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Monthly rainfall
    plt.figure(figsize=(10, 6))
    df_rain = df.set_index('Date').resample('ME')['Rainfall'].sum()
    plt.bar(range(len(df_rain)), df_rain.values, color='skyblue', edgecolor='navy')
    plt.title('Monthly Rainfall Totals', fontsize=14)
    plt.xlabel('Month')
    plt.ylabel('Rainfall (mm)')
    plt.xticks(range(len(df_rain)), [d.strftime('%Y-%m') for d in df_rain.index], rotation=45)
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{output_dir}/monthly_rainfall.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Humidity vs Temperature scatter plot
    plt.figure(figsize=(8, 6))
    plt.scatter(df['Temperature'], df['Humidity'], alpha=0.6, color='green', s=50)
    plt.title('Humidity vs Temperature', fontsize=14)
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Humidity (%)')
    plt.grid(True, alpha=0.3)
    plt.savefig(f"{output_dir}/humidity_temperature.png", dpi=300, bbox_inches='tight')
    plt.close()

    # Combined plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Temperature subplot
    ax1.plot(df_temp.index, df_temp['Temperature'], 'r-', linewidth=2)
    ax1.set_title('Temperature Trend')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Temperature (°C)')
    ax1.grid(True, alpha=0.3)

    # Rainfall subplot
    ax2.bar(range(len(df_rain)), df_rain.values, color='lightcoral', edgecolor='darkred')
    ax2.set_title('Monthly Rainfall')
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Rainfall (mm)')
    ax2.set_xticks(range(len(df_rain)))
    ax2.set_xticklabels([d.strftime('%Y-%m') for d in df_rain.index], rotation=45)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"{output_dir}/combined_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()

    print(f"Plots saved in {output_dir} folder!")

def analyze_by_season(df):
    """Group data by seasons and calculate statistics."""
    print("\nAnalyzing data by seasons...")

    # Add season column
    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Autumn'

    df_season = df.copy()
    df_season['Month'] = df_season['Date'].dt.month
    df_season['Season'] = df_season['Month'].apply(get_season)

    # Monthly stats
    monthly_stats = df_season.groupby('Month').agg({
        'Temperature': 'mean',
        'Rainfall': 'sum',
        'Humidity': 'mean'
    }).round(2)

    # Seasonal stats
    seasonal_stats = df_season.groupby('Season').agg({
        'Temperature': 'mean',
        'Rainfall': 'sum',
        'Humidity': 'mean'
    }).round(2)

    print("Monthly Statistics:")
    print(monthly_stats)
    print("\nSeasonal Statistics:")
    print(seasonal_stats)

    return monthly_stats, seasonal_stats

def save_results(df, stats, monthly_stats, seasonal_stats, output_dir="output"):
    """Save cleaned data and generate summary report."""
    print("\nSaving results...")

    os.makedirs(output_dir, exist_ok=True)

    # Save cleaned data
    df.to_csv(f"{output_dir}/cleaned_weather_data.csv", index=False)

    # Generate summary report
    with open(f"{output_dir}/weather_summary.txt", 'w') as f:
        f.write("WEATHER DATA ANALYSIS REPORT\n")
        f.write("=" * 40 + "\n\n")

        f.write("DATA OVERVIEW:\n")
        f.write(f"Total records: {len(df)}\n")
        f.write(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}\n\n")

        f.write("TEMPERATURE SUMMARY:\n")
        f.write(f"Average: {df['Temperature'].mean():.2f}°C\n")
        f.write(f"Maximum: {df['Temperature'].max():.2f}°C\n")
        f.write(f"Minimum: {df['Temperature'].min():.2f}°C\n\n")

        f.write("RAINFALL SUMMARY:\n")
        f.write(f"Total: {df['Rainfall'].sum():.2f} mm\n")
        f.write(f"Average daily: {df['Rainfall'].mean():.2f} mm\n")
        f.write(f"Wettest day: {df.loc[df['Rainfall'].idxmax(), 'Date'].date()} ({df['Rainfall'].max():.1f} mm)\n\n")

        f.write("MONTHLY ANALYSIS:\n")
        f.write(monthly_stats.to_string())
        f.write("\n\n")

        f.write("SEASONAL ANALYSIS:\n")
        f.write(seasonal_stats.to_string())
        f.write("\n\n")

        f.write("KEY INSIGHTS:\n")
        f.write("- Monitor temperature variations for climate patterns\n")
        f.write("- Track rainfall distribution for water resource planning\n")
        f.write("- Seasonal analysis helps in agricultural planning\n")
        f.write("- Humidity levels affect comfort and health considerations\n")

    print(f"Results saved in {output_dir} folder!")

def main():
    """Main function to run the weather analysis."""
    print("  WEATHER DATA ANALYSIS PROGRAM  ")
    print("=" * 40)

    # File path
    data_file = os.path.join("data", "weather.csv")

    # Step 1: Load data
    df = load_data(data_file)

    # Step 2: Clean data
    df = clean_data(df)

    # Step 3: Calculate statistics
    stats = calculate_stats(df)

    # Reset index for further processing
    df = df.reset_index()

    # Step 4: Create visualizations
    create_plots(df)

    # Step 5: Seasonal analysis
    monthly_stats, seasonal_stats = analyze_by_season(df)

    # Step 6: Save results
    save_results(df, stats, monthly_stats, seasonal_stats)

    print("\n✅ Analysis complete! Check the 'output' folder for results.")

if __name__ == "__main__":
    main()