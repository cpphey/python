import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt


def convert_tenor_to_months(tenor):
    """
    Convert tenor strings (e.g., '1M', '6M', '1Y') to numeric values in months.
    """
    if tenor.endswith('M'):
        return int(tenor[:-1])  # Remove 'M' and convert to integer
    elif tenor.endswith('Y'):
        return int(tenor[:-1]) * 12  # Remove 'Y' and multiply by 12
    else:
        raise ValueError(f"Unsupported tenor format: {tenor}")


def process_gov(df, output_dir=""):
    """
    Process data for curves with the '_gov' suffix in their name.

    df: DataFrame containing the curve data.
    output_dir: Directory to save the output files (default is current directory).
    """
    # Convert tenor column to months
    df['tenor'] = df['tenor'].apply(convert_tenor_to_months)

    # Save the converted input data to input_converted.csv
    converted_input_file = f"{output_dir}input_converted.csv"
    df.to_csv(converted_input_file, index=False)

    # Sort data by tenor to ensure proper interpolation
    df = df.sort_values(by='tenor')

    # Create a finer grid for interpolation in 1-month intervals
    fine_tenors = np.arange(min(df['tenor']), max(df['tenor']) + 1, 1)  # 1-month intervals

    # Perform cubic spline interpolation
    spline = make_interp_spline(df['tenor'], df['rate'], k=3)
    fine_rates = spline(fine_tenors)

    # Prepare the output DataFrame
    output_df = pd.DataFrame({
        "curve_name": df['curve_name'].iloc[0],  # Apply the curve name
        "tenor": fine_tenors,  # Keep as months
        "rate": fine_rates
    })

    # Save the interpolated data to output.csv
    output_file = f"{output_dir}output.csv"
    output_df.to_csv(output_file, index=False)

    # Plot both the original input data and the interpolated data
    plt.figure(figsize=(10, 6))

    # Original data points
    plt.plot(df['tenor'], df['rate'], 'o', label="Original Data (Input)", markersize=8)

    # Interpolated curve
    plt.plot(output_df['tenor'], output_df['rate'], '-', label="Interpolated Data (1M intervals)")

    # Labels, title, and legend
    plt.xlabel("Tenor (Months)")
    plt.ylabel("Rate")
    plt.title(f"Spot Rates: {df['curve_name'].iloc[0]} - Input vs. Interpolated (1M Intervals)")
    plt.legend()
    plt.grid()
    plt.tight_layout()

    # Ensure plot is shown
    plt.show(block=True)  # Force the plot to display


def main():
    # Input file location
    input_file = "input.csv"  # Replace with the correct path if needed
    output_dir = ""  # Specify directory for outputs, default is current directory

    # Read input data
    df = pd.read_csv(input_file)

    # Check for '_gov' in curve_name and process accordingly
    if '_gov' in df['curve_name'].iloc[0]:
        process_gov(df, output_dir)


if __name__ == "__main__":
    main()
