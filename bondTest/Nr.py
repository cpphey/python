import pandas as pd
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib.pyplot as plt
import logging

# Configure logging
logging.basicConfig(filename='Nr.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def convert_tenor_to_months(tenor):
    """
    Convert tenor strings (e.g., 'Spot', '1W', '1M', '1Y', '2Y5Y') to numeric values in months.
    """
    if tenor == "Spot":
        return 0  # Spot corresponds to 0 months
    elif tenor.endswith('W'):
        return int(tenor[:-1]) / 4  # Weeks converted to months (approximation: 4 weeks = 1 month)
    elif tenor.endswith('M'):
        return int(tenor[:-1])  # Months
    elif tenor.endswith('Y') and 'Y' not in tenor[:-1]:  # Single tenor like '1Y'
        return int(tenor[:-1]) * 12  # Years to months
    elif tenor.count('Y') == 2:  # Forward tenors like '2Y5Y' or '10Y5Y'
        parts = tenor.split('Y')
        start = int(parts[0]) * 12  # Start of the range in months
        end = int(parts[1]) * 12    # End of the range in months
        return (start, end)  # Return as a tuple (start, end)
    else:
        raise ValueError(f"Unsupported tenor format: {tenor}")

def process_fwd(df, output_dir="", is_first=True):
    """
    Process data for forward curves with '_fwd' in their curve_name.
    """
    logging.info("Processing forward curve: %s", df['curve_name'].iloc[0])

    # Convert tenor to start and end months
    ranges = df['tenor'].apply(convert_tenor_to_months)
    df = df.copy()  # Avoid SettingWithCopyWarning
    df['start_month'] = ranges.apply(lambda x: x[0] if isinstance(x, tuple) else x)
    df['end_month'] = ranges.apply(lambda x: x[1] if isinstance(x, tuple) else x)

    # Generate interpolated tenors and rates for the forward periods
    forward_data = []
    for _, row in df.iterrows():
        start = row['start_month']
        end = row['end_month']
        rate = row['rate']
        for tenor in range(start, end + 1):  # Forward tenors in 1-month intervals
            forward_data.append([row['curve_name'], tenor, rate])

    forward_df = pd.DataFrame(forward_data, columns=['curve_name', 'tenor', 'rate'])

    # Handle duplicate tenor values by averaging rates
    forward_df = forward_df.groupby('tenor', as_index=False).agg({
        'curve_name': 'first',  # Take the first curve name (all should be the same)
        'rate': 'mean'          # Average rates for duplicate tenors
    })

    # Save to input_converted.csv
    converted_input_file = f"{output_dir}input_converted.csv"
    if is_first:
        forward_df.to_csv(converted_input_file, index=False)
        logging.info("Created new input_converted.csv file")
    else:
        forward_df.to_csv(converted_input_file, index=False, mode='a', header=False)
        logging.info("Appended to input_converted.csv file")

    # Sort data and interpolate rates for output.csv
    fine_tenors = np.arange(forward_df['tenor'].min(), forward_df['tenor'].max() + 1, 1)
    spline = make_interp_spline(forward_df['tenor'], forward_df['rate'], k=3)
    fine_rates = spline(fine_tenors)

    output_df = pd.DataFrame({
        "curve_name": forward_df['curve_name'].iloc[0],
        "tenor": fine_tenors,
        "rate": fine_rates
    })

    # Save to output.csv
    output_file = f"{output_dir}output.csv"
    if is_first:
        output_df.to_csv(output_file, index=False)
        logging.info("Created new output.csv file")
    else:
        output_df.to_csv(output_file, index=False, mode='a', header=False)
        logging.info("Appended to output.csv file")

    # Plot
    logging.info("Plotting forward curve: %s", forward_df['curve_name'].iloc[0])
    plt.figure(figsize=(10, 6))
    plt.plot(forward_df['tenor'], forward_df['rate'], 'o', label="Original Data (Input)", markersize=8)
    plt.plot(output_df['tenor'], output_df['rate'], '-', label="Interpolated Data (1M intervals)")
    plt.xlabel("Tenor (Months)")
    plt.ylabel("Rate")
    plt.title(f"Forward Rates: {forward_df['curve_name'].iloc[0]}")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show(block=True)

def process_curve(df, output_dir="", is_first=True):
    """
    Generic function to process non-forward curves.
    """
    logging.info("Processing curve: %s", df['curve_name'].iloc[0])

    df = df.copy()  # Avoid SettingWithCopyWarning
    df.loc[:, 'tenor'] = df['tenor'].apply(convert_tenor_to_months)
    converted_input_file = f"{output_dir}input_converted.csv"
    if is_first:
        df.to_csv(converted_input_file, index=False)
        logging.info("Created new input_converted.csv file")
    else:
        df.to_csv(converted_input_file, index=False, mode='a', header=False)
        logging.info("Appended to input_converted.csv file")

    df = df.sort_values(by='tenor')
    fine_tenors = np.arange(min(df['tenor']), max(df['tenor']) + 1, 1)
    spline = make_interp_spline(df['tenor'], df['rate'], k=3)
    fine_rates = spline(fine_tenors)

    output_df = pd.DataFrame({
        "curve_name": df['curve_name'].iloc[0],
        "tenor": fine_tenors,
        "rate": fine_rates
    })

    output_file = f"{output_dir}output.csv"
    if is_first:
        output_df.to_csv(output_file, index=False)
        logging.info("Created new output.csv file")
    else:
        output_df.to_csv(output_file, index=False, mode='a', header=False)
        logging.info("Appended to output.csv file")

    # Plot
    logging.info("Plotting curve: %s", df['curve_name'].iloc[0])
    plt.figure(figsize=(10, 6))
    plt.plot(df['tenor'], df['rate'], 'o', label="Original Data (Input)", markersize=8)
    plt.plot(output_df['tenor'], output_df['rate'], '-', label="Interpolated Data (1M intervals)")
    plt.xlabel("Tenor (Months)")
    plt.ylabel("Rate")
    plt.title(f"Spot Rates: {df['curve_name'].iloc[0]}")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show(block=True)

def main():
    input_file = "input.csv"
    output_dir = ""

    logging.info("Starting processing of input file: %s", input_file)

    df = pd.read_csv(input_file)
    unique_curves = df['curve_name'].unique()
    is_first = True
    for curve in unique_curves:
        logging.info("Processing curve: %s", curve)
        curve_data = df[df['curve_name'] == curve]
        if '_fwd' in curve:
            process_fwd(curve_data, output_dir, is_first)
        else:
            process_curve(curve_data, output_dir, is_first)
        is_first = False

    logging.info("Completed processing of all curves")

if __name__ == "__main__":
    main()
