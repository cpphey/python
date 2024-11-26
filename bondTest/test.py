import QuantLib as ql
import datetime
import pandas as pd

# Load data from CSV
csv_data = pd.read_csv('bond_data.csv')

# Initialize an empty DataFrame to store the results
output_data = pd.DataFrame(columns=[
    'CUSIP', 'Yield to Maturity (YTM)', 'Simple Duration', 'Macaulay Duration', 'Modified Duration',
    'Effective Modified Duration', 'Effective Convexity', 'Convexity', 'Effective Yield',
    'Yield to Call (YTC)', 'Yield to Worst (YTW)', 'Credit Duration', 'Delta', 'Spread to Curve', 'Spread to Worst',
    'input_effective_mod_duration', 'input_duration_modified', 'input_duration_Macaulay', 'input_effective_convexity',
    'input_convexity', 'input_spread_duration', 'input_ytm', 'input_effective_yield'
])

def process_bond_data(row):
    global output_data
    # Assign inputs from CSV
    cusip = row['cusip']
    sec_id = row['sec_id']
    issue_date = ql.DateParser.parseFormatted(row['issue_date'], '%m/%d/%Y') if pd.notna(row['issue_date']) else None
    end_date = ql.DateParser.parseFormatted(row['end_date'], '%m/%d/%Y') if pd.notna(row['end_date']) else None
    coupon_rate = row['coupon_rate'] / 100 if pd.notna(row['coupon_rate']) else None
    price_mid = row['price_mid'] if pd.notna(row['price_mid']) else None
    price_high = row['price_high'] if pd.notna(row['price_high']) else None
    price_low = row['price_low'] if pd.notna(row['price_low']) else None
    settlement_days = row['settlement_days'] if pd.notna(row['settlement_days']) else None
    face_value = row['face_value'] if pd.notna(row['face_value']) else None
    bondCalendar = eval(row['bond_calendar']) if pd.notna(row['bond_calendar']) else None  # ql.UnitedStates.Settlement
    day_counter = eval(row['day_counter']) if pd.notna(row['day_counter']) else None  # ql.Thirty360.USA
    custom_date = row['custom_date'] if pd.notna(row['custom_date']) else None
    input_effective_mod_duration = row['input_effective_mod_duration'] if pd.notna(row['input_effective_mod_duration']) else None
    input_duration_modified = row['input_duration_modified'] if pd.notna(row['input_duration_modified']) else None
    input_duration_Macaulay = row['input_duration_Macaulay'] if pd.notna(row['input_duration_Macaulay']) else None
    input_effective_convexity = row['input_effective_convexity'] if pd.notna(row['input_effective_convexity']) else None
    input_convexity = row['input_convexity'] if pd.notna(row['input_convexity']) else None
    input_spread_duration = row['input_spread_duration'] if pd.notna(row['input_spread_duration']) else None
    input_ytm = row['input_ytm'] if pd.notna(row['input_ytm']) else None
    input_effective_yield = row['input_effective_yield'] if pd.notna(row['input_effective_yield']) else None

    call_date = ql.DateParser.parseFormatted(row['call_date'], '%m/%d/%Y') if pd.notna(row['call_date']) else None
    call_price = row['call_price'] if pd.notna(row['call_price']) else None
    spread = row['spread'] if pd.notna(row['spread']) else None
    shock_size = row['shock_size'] if pd.notna(row['shock_size']) else None
    benchmark_yield = row['benchmark_yield'] if pd.notna(row['benchmark_yield']) else None

    # Cusip
    print(f"Processing CUSIP: {cusip}")

    # Setup schedule and bond
    today = datetime.date.today()
    formatted_date = today.strftime('%m/%d/%Y') if custom_date is None else custom_date
    todays_date = ql.DateParser.parseFormatted(formatted_date, '%m/%d/%Y')
    print("Todays Date is: " + formatted_date)
    ql.Settings.instance().evaluationDate = todays_date

    # Schedule
    tenor = ql.Period(ql.Semiannual)
    convention = ql.Unadjusted
    terminationDateConvention = ql.Unadjusted
    DateGeneration_Rule = ql.DateGeneration.Backward
    endOfMonth = False
    schedule = ql.Schedule(issue_date, end_date, tenor, bondCalendar, convention, terminationDateConvention, DateGeneration_Rule, endOfMonth)

    # FixedRateBond
    paymentConvention = ql.Unadjusted
    bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter, paymentConvention)

    # Yield to Maturity (YTM)
    clean_price = price_mid
    ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual)
    print(f"Yield to Maturity (YTM): {ytm * 100:.8f}%")

    # Duration and Convexity
    yield_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual)

    # Calculate duration and convexity
    duration_simple = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Simple)
    duration_Macaulay = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Macaulay)
    duration_modified = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified)
    effective_mod_duration = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified) / (1 + ytm / 2)
    effective_convexity = ql.BondFunctions.convexity(bond, yield_rate) / (1 + ytm / 2)
    convexity = ql.BondFunctions.convexity(bond, yield_rate) / 100

    print(f"Simple Duration: {duration_simple:.8f}")
    print(f"Macaulay Duration: {duration_Macaulay:.8f}")
    print(f"Modified Duration: {duration_modified:.8f}")
    print(f"Effective Modified Duration: {effective_mod_duration:.8f}")
    print(f"Effective Convexity: {effective_convexity:.8f}")
    print(f"Convexity: {convexity:.8f}")

    # Effective Yield using QuantLib
    effective_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual).equivalentRate(day_counter, ql.Compounded, ql.Annual, todays_date, end_date).rate()
    effective_yield = effective_rate * 100
    print(f"Effective Yield (using QuantLib): {effective_yield:.8f}%")

    # Yield to Call (YTC) with Dummy Numbers
    ytc = None
    if call_date is not None:
        ytc = bond.bondYield(call_price, day_counter, ql.Compounded, ql.Semiannual, call_date)
        print(f"Yield to Call with dummy (YTC) on {call_date}: {ytc * 100:.8f}%")

    # Yield to Worst (YTW) with Dummy Numbers
    ytw = None
    if ytc is not None:
        ytw = min(ytm, ytc)
        print(f"Yield to Worst (YTW): {ytw * 100:.8f}%")

    # Credit Duration with Dummy Numbers
    yield_rate_with_spread = None
    credit_duration = None
    if spread is not None:
        yield_rate_with_spread = ql.InterestRate(ytm + spread, day_counter, ql.Compounded, ql.Semiannual)
        credit_duration = ql.BondFunctions.duration(bond, yield_rate_with_spread, ql.Duration.Modified)
        print(f"Credit Duration (with dummy spread of {spread * 100:.2f}%): {credit_duration:.8f}")

    # Delta with Dummy Numbers
    yield_rate_shocked = None
    delta = None
    if shock_size is not None:
        yield_rate_shocked = ql.InterestRate(ytm + shock_size, day_counter, ql.Compounded, ql.Semiannual)
        delta = (ql.BondFunctions.cleanPrice(bond, yield_rate_shocked) - ql.BondFunctions.cleanPrice(bond, yield_rate)) / shock_size
        print(f"Delta (with dummy shock of {shock_size * 100:.2f}%): {delta:.8f}")

    # Spread to Curve with Dummy Numbers
    spread_to_curve = None
    if benchmark_yield is not None:
        spread_to_curve = ytm - benchmark_yield
        print(f"Spread to Curve (with dummy benchmark yield of {benchmark_yield * 100:.2f}%): {spread_to_curve * 100:.8f}%")

    # Spread to Worst with Dummy Numbers
    spread_to_worst = None
    if benchmark_yield is not None and ytw is not None:
        spread_to_worst = ytw - benchmark_yield
        print(f"Spread to Worst (with dummy benchmark yield of {benchmark_yield * 100:.2f}%): {spread_to_worst * 100:.8f}%")

    # Append the results to the output DataFrame
    new_row = pd.DataFrame([{
        'CUSIP': cusip,
        'ytm': ytm * 100,
        'duration_simple': duration_simple,
        'duration_Macaulay': duration_Macaulay,
        'duration_modified': duration_modified,
        'effective_mod_duration': effective_mod_duration,
        'effective_convexity': effective_convexity,
        'convexity': convexity,
        'effective_yield': effective_yield,
        'ytc': ytc * 100 if ytc is not None else None,
        'ytw': ytw * 100 if ytw is not None else None,
        'credit_duration': credit_duration,
        'delta': delta,
        'spread_to_curve': spread_to_curve * 100 if spread_to_curve is not None else None,
        'spread_to_worst': spread_to_worst * 100 if spread_to_worst is not None else None,
        'input_effective_mod_duration': input_effective_mod_duration,
        'input_duration_modified': input_duration_modified,
        'input_duration_Macaulay': input_duration_Macaulay,
        'input_effective_convexity': input_effective_convexity,
        'input_convexity': input_convexity,
        'input_spread_duration': input_spread_duration,
        'input_ytm': input_ytm,
        'input_effective_yield': input_effective_yield,
        'formatted_date': formatted_date
    }])
    output_data = pd.concat([output_data, new_row], ignore_index=True)

# Iterate over each row in the CSV and process the bond data
for index, row in csv_data.iterrows():
    process_bond_data(row)

# Write the output to a CSV file
output_data.to_csv('processed_bond_data.csv', index=False)
