import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt


def convert_tenor_to_months(tenor):
    """
    Convert tenor strings (e.g., 'Spot', '1W', '1M', '1Y') to numeric values in months.
    """
    if tenor == "Spot":
        return 0  # Spot corresponds to 0 months
    elif tenor.endswith('W'):
        return int(tenor[:-1]) / 4  # Weeks converted to months (approximation: 4 weeks = 1 month)
    elif tenor.endswith('M'):
        return int(tenor[:-1])  # Months
    elif tenor.endswith('Y'):
        return int(tenor[:-1]) * 12  # Years to months
    else:
        raise ValueError(f"Unsupported tenor format: {tenor}")


def process_curve(df, output_dir="", is_first=True):
    """
    Generic function to process curve data for '_gov' and '_fx' curves.
    Writes fresh data for the first curve and appends data for subsequent curves.

    df: DataFrame containing curve data.
    output_dir: Directory to save the output files.
    is_first: Whether this is the first curve being processed.
    """
    # Modify tenor safely using .loc
    df.loc[:, 'tenor'] = df['tenor'].apply(convert_tenor_to_months)

    # Save the converted input data to input_converted.csv
    converted_input_file = f"{output_dir}input_converted.csv"
    if is_first:
        df.to_csv(converted_input_file, index=False)  # Fresh write
    else:
        df.to_csv(converted_input_file, index=False, mode='a', header=False)  # Append

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
    if is_first:
        output_df.to_csv(output_file, index=False)  # Fresh write
    else:
        output_df.to_csv(output_file, index=False, mode='a', header=False)  # Append

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
    plt.show(block=True)


def main():
    # Input file location
    input_file = "input.csv"  # Replace with the correct path if needed
    output_dir = ""  # Specify directory for outputs, default is current directory

    # Read input data
    df = pd.read_csv(input_file)

    # Process curves based on curve_name
    unique_curves = df['curve_name'].unique()
    is_first = True  # Track whether this is the first curve being processed
    for curve in unique_curves:
        curve_data = df[df['curve_name'] == curve]
        process_curve(curve_data, output_dir, is_first)
        is_first = False  # Subsequent curves will append to the files


if __name__ == "__main__":
    main()
