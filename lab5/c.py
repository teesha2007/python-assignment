# main.py – run this file to do the whole project

from data_ingestion import load_and_merge_csv
from aggregation import (
    calculate_daily_totals,
    calculate_weekly_aggregates,
    building_wise_summary,
    building_weekly_average,
)
from models import BuildingManager
from visualization import create_dashboard
from report import (
    save_cleaned_data,
    save_building_summary,
    write_text_summary,
)


def main():
    # -------------------------
    # Task 1: Load and combine data
    # -------------------------
    df = load_and_merge_csv("data")

    if df is None:
        print("No data loaded. Exiting.")
        return

    print("\nFirst few rows of combined data:")
    print(df.head())

    # -------------------------
    # Task 2: Aggregations
    # -------------------------
    daily_totals = calculate_daily_totals(df)
    weekly_totals = calculate_weekly_aggregates(df)
    building_summary = building_wise_summary(df)
    weekly_building_avg = building_weekly_average(df)

    print("\nBuilding-wise summary:")
    print(building_summary)

    # -------------------------
    # Task 3: OOP Model
    # -------------------------
    manager = BuildingManager()
    manager.load_from_dataframe(df)
    print("\nOOP Building Reports:")
    manager.print_reports()

    # -------------------------
    # Task 4: Visualization
    # -------------------------
    create_dashboard(df, daily_totals, weekly_totals, weekly_building_avg)

    # -------------------------
    # Task 5: Save outputs
    # -------------------------
    save_cleaned_data(df)
    save_building_summary(building_summary)
    write_text_summary(df, building_summary, daily_totals, weekly_totals)

    print("\n Capstone pipeline completed successfully!")


if __name__ == "__main__":
    main()
