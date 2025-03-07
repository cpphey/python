import QuantLib as ql

# Define bond calendar (United Kingdom Settlement)
calendar = ql.UnitedKingdom(ql.UnitedKingdom.Settlement)

# Define key dates
trade_date = ql.Date(6, 3, 2024)   # March 6, 2024
coupon_date = ql.Date(15, 8, 2024)  # August 15, 2024

# Adjust dates to business days if necessary
trade_date = calendar.adjust(trade_date, ql.Following)
coupon_date = calendar.adjust(coupon_date, ql.Following)

# Define 30/360 ISMA day count convention
day_count = ql.Thirty360(ql.Thirty360.ISMA)

# Compute accrued days using 30/360 ISMA
accrued_days_30360 = day_count.dayCount(trade_date, coupon_date)

# Given values
coupon_payment = 57500  # Semi-annual coupon payment

# Accrued Interest Calculation (from March 6 to August 15)
accrued_interest_30360 = (coupon_payment * accrued_days_30360) / 360

print(f"Accrued Days (30/360 ISMA): {accrued_days_30360}")
print(f"Accrued Interest from March 6 to Aug 15 (30/360 ISMA): ${accrued_interest_30360:.2f}")
