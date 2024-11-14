import QuantLib as ql
import datetime



#Input data
# issue_date = ql.Date(26, 11, 2024)
# end_date = ql.Date(1, 12, 2032)
# coupon_rate = 0.06875
# price = 100.86951
# settlement_days = 2
# face_value = 100.0

issue_date = ql.Date(1, 11, 2024)
end_date = ql.Date(3, 6, 2030)
coupon_rate = 0.04513
price = 100.171
settlement_days = 2
face_value = 100.0

# issue_date = ql.Date(1, 11, 2024)
# end_date = ql.Date(1, 11, 2031)
# coupon_rate = 0.06625
# price = 101.0625
# settlement_days = 2
# face_value = 100.0


# Setup schedule and bond
today = datetime.date.today()
formatted_date = today.strftime('%Y-%m-%d')
todays_date = ql.DateParser.parseFormatted(formatted_date, '%Y-%m-%d')
print("Todays Date is: "+formatted_date)
ql.Settings.instance().evaluationDate = todays_date

schedule = ql.Schedule(issue_date, end_date, ql.Period(ql.Semiannual),
                       ql.NullCalendar(), ql.Unadjusted, ql.Unadjusted,
                       ql.DateGeneration.Backward, False)

day_counter = ql.Thirty360(ql.Thirty360.USA)
bond = ql.FixedRateBond(settlement_days, face_value, schedule, [coupon_rate], day_counter)

# Yield to Maturity (YTM)
clean_price = price
ytm = bond.bondYield(clean_price, day_counter, ql.Compounded, ql.Semiannual)
print(f"Yield to Maturity (YTM): {ytm * 100:.2f}%")

# Duration and Convexity

yield_rate = ql.InterestRate(ytm, day_counter, ql.Compounded, ql.Semiannual)

# Calculate duration and convexity
duration_simple = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Simple)
duration_modified = ql.BondFunctions.duration(bond, yield_rate, ql.Duration.Modified)
convexity = ql.BondFunctions.convexity(bond, yield_rate) / 100

print(f"Simple Duration: {duration_simple:.8f}")
#print(f"Modified Duration: {duration_modified:.8f}")
print(f"Convexity: {convexity:.8f}")
