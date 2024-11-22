import QuantLib as ql
import datetime

#p4
issue_date = ql.Date(28, 10, 2014)
end_date = ql.Date(1, 5, 2025)
coupon_rate = 0.05
price = 99.704
settlement_days = 0
face_value = 100.0
bondCalendar =  ql.UnitedStates(ql.UnitedStates.Settlement)
day_counter = ql.Thirty360(ql.Thirty360.USA)
#day_counter  = ql.ActualActual(ql.ActualActual.ISMA)@al

# Setup schedule and bond
custom_date = None #'2024-11-18'
today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d') if custom_date is None else custom_date
todays_date = ql.DateParser.parseFormatted(formatted_date, '%Y-%m-%d')
print("Todays Date is: "+formatted_date)
ql.Settings.instance().evaluationDate = todays_date

#Schedule
convention = ql.Unadjusted
terminationDateConvention = ql.Unadjusted
DateGeneration_Rule = ql.DateGeneration.Backward
endOfMonth = False
schedule = ql.Schedule(issue_date, end_date, ql.Period(ql.Semiannual),
                       bondCalendar , convention , terminationDateConvention ,
                       DateGeneration_Rule, endOfMonth)
#FixedRateBond
paymentConvention = ql.Unadjusted
bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter, paymentConvention )  #added ql.Unadjusted

# Yield to Maturity (YTM)
clean_price = price
ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual) #SimpleThenCompounded
print(f"Yield to Maturity (YTM): {ytm * 100:.8f}%")

# Duration and Convexity
#yield_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual)#SimpleThenCompounded
yield_rate = ql.InterestRate(ytm, day_counter, ql.CompoundedThenSimple, ql.Semiannual)

# Calculate duration and convexity
duration_simple = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Simple)
duration_modified = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified)
effective_mod_duration = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified) / (1 + ytm / 2)
effective_convexity = ql.BondFunctions.convexity(bond, yield_rate) / (1 + ytm / 2)
convexity = ql.BondFunctions.convexity(bond, yield_rate) / 100

print(f"Simple Duration: {duration_simple:.8f}")
print(f"Modified Duration: {duration_modified:.8f}")
print(f"Effective Modified Duration: {effective_mod_duration:.8f}")
print(f"Effective Convexity: {effective_convexity:.8f}")
print(f"Convexity: {convexity:.8f}")

# Effective Yield using QuantLib
effective_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual).equivalentRate(day_counter, ql.Compounded, ql.Annual, todays_date, end_date).rate()
print(f"Effective Yield (using QuantLib): {effective_rate * 100:.8f}%")

# Yield to Call (YTC) with Dummy Numbers
call_date = ql.Date(1, 5, 2023)  # Dummy call date
call_price = 100.0  # Call price at par
ytc = bond.bondYield(call_price, day_counter, ql.Compounded, ql.Semiannual, call_date)
print(f"Yield to Call (YTC) on {call_date}: {ytc * 100:.8f}%")

# Yield to Worst (YTW) with Dummy Numbers
ytw = min(ytm, ytc)  # Yield to worst is the minimum of YTM and YTC
print(f"Yield to Worst (YTW): {ytw * 100:.8f}%")

# Credit Duration with Dummy Numbers
spread = 0.01  # Dummy credit spread of 1%
yield_rate_with_spread = ql.InterestRate(ytm + spread, day_counter, ql.Compounded, ql.Semiannual)
credit_duration = ql.BondFunctions.duration(bond, yield_rate_with_spread, ql.Duration.Modified)
print(f"Credit Duration (with dummy spread of {spread * 100:.2f}%): {credit_duration:.8f}")

# Delta with Dummy Numbers
shock_size = 0.01  # Dummy interest rate shock of 1%
yield_rate_shocked = ql.InterestRate(ytm + shock_size, day_counter, ql.Compounded, ql.Semiannual)
delta = (ql.BondFunctions.cleanPrice(bond, yield_rate_shocked) - ql.BondFunctions.cleanPrice(bond, yield_rate)) / shock_size
print(f"Delta (with dummy shock of {shock_size * 100:.2f}%): {delta:.8f}")

# Spread to Curve with Dummy Numbers
benchmark_yield = 0.03  # Dummy benchmark yield of 3%
spread_to_curve = ytm - benchmark_yield
print(f"Spread to Curve (with dummy benchmark yield of {benchmark_yield * 100:.2f}%): {spread_to_curve * 100:.8f}%")

# Spread to Worst with Dummy Numbers
spread_to_worst = ytw - benchmark_yield
print(f"Spread to Worst (with dummy benchmark yield of {benchmark_yield * 100:.2f}%): {spread_to_worst * 100:.8f}%")
