import QuantLib as ql

# Bond parameters
issue_date = ql.Date(26, 5, 2010)  # March 1, 2024
maturity_date = ql.Date(1, 3, 2048)  # March 1, 2027
coupon_rate = 0.04232  # 5% annual coupon
face_value = 1000000  # $1,000,000 face value
frequency = ql.Semiannual
calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
day_count = ql.Thirty360(ql.Thirty360.BondBasis)
settlement_days = 1

ql.Settings.instance().evaluationDate = ql.Date(7, 3, 2025)

# Long or Short First Coupon Logic
first_coupon_date = ql.Date(31, 12, 2010)  # Example first coupon date

if first_coupon_date:
    schedule = ql.Schedule(issue_date, maturity_date, ql.Period(frequency),
                           calendar, ql.Following, ql.Following,
                           ql.DateGeneration.Backward, True,
                           first_coupon_date)

else:
    schedule = ql.Schedule(issue_date, maturity_date, ql.Period(frequency),
                           calendar, ql.Following, ql.Following,
                           ql.DateGeneration.Backward, True)

# Sinking fund schedule (6 equal payments over 3 years)
sinking_fund_schedule = ql.CallabilitySchedule()
sinking_payment = face_value / 6  # 6 payments over 3 years

sinking_date = issue_date
for i in range(6):
    sinking_date = calendar.advance(sinking_date, 6, ql.Months)
    if sinking_date > maturity_date:
        sinking_date = maturity_date
    callability_price = ql.BondPrice(sinking_payment, ql.BondPrice.Clean)
    sinking_fund_schedule.append(
        ql.Callability(callability_price, ql.Callability.Call, sinking_date)
    )

# Create sinking fund bond
sinking_bond = ql.CallableFixedRateBond(
    settlement_days, face_value, schedule, [coupon_rate],
    day_count, ql.Following, 0.0, issue_date,  # Set redemption to 0
    sinking_fund_schedule
)

# Set pricing engine (Hull-White model + tree)
rate = 0.03
vol = 0.01
term_structure = ql.FlatForward(issue_date, ql.QuoteHandle(ql.SimpleQuote(rate)),
                                day_count, ql.Compounded, frequency)
ts_handle = ql.YieldTermStructureHandle(term_structure)
model = ql.HullWhite(ts_handle, 0.03, vol)
engine = ql.TreeCallableFixedRateBondEngine(model, 40)

# Attach engine to bond
sinking_bond.setPricingEngine(engine)

# Bond price
price = sinking_bond.cleanPrice()
print(f"Bond Price: {price:.2f}")

# Print cash flows
print("\nCash Flows:")
for c in sinking_bond.cashflows():
    print(f"{c.date()} - {c.amount():,.2f}")

# Print sinking fund schedule
print("\nSinking Fund Payments:")
for s in sinking_fund_schedule:
    print(f"{s.date()} - {s.price().amount():,.2f}")
