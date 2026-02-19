import QuantLib as ql

# 00434CAC3
# Bond parameters
issue_date = ql.Date(26, 5, 2010)  # March 1, 2024
maturity_date = ql.Date(31, 12, 2042)  # March 1, 2027
coupon_rate = 0.07067  # 5% annual coupon
face_value = 1000000  # $1,000,000 face value
frequency = ql.Semiannual
calendar = ql.UnitedStates(ql.UnitedStates.GovernmentBond)
day_count = ql.ActualActual(ql.ActualActual.Bond)
settlement_days = 1

ql.Settings.instance().evaluationDate = ql.Date(11, 3, 2025)

# Long or Short First Coupon Logic
first_coupon_long = True  # Set to False for short first coupon
first_coupon_date = ql.Date(31, 12, 2010)  # Example first coupon date

if first_coupon_long:
    schedule = ql.Schedule(issue_date, maturity_date, ql.Period(frequency),
                           calendar, ql.Following, ql.Following,
                           ql.DateGeneration.Backward, True,
                           first_coupon_date)
else:
    schedule = ql.Schedule(issue_date, maturity_date, ql.Period(frequency),
                           calendar, ql.Following, ql.Following,
                           ql.DateGeneration.Backward, True,
                           first_coupon_date)

#------------------------------------------------------------------------------------------------------------------------------
# Sinking fund schedule (accrual-based)
sinking_fund_schedule = ql.CallabilitySchedule()
num_periods = len(schedule)
remaining_principal = face_value

for i in range(num_periods):
    sinking_date = schedule[i]
    if sinking_date > maturity_date:
        sinking_date = maturity_date

    # Accrue interest from last payment date
    if i > 0:
        last_payment_date = schedule[i - 1]
        accrued_interest = coupon_rate / frequency * remaining_principal * day_count.yearFraction(last_payment_date,
                                                                                                  sinking_date)
    else:
        accrued_interest = 0

    # Adjust sinking payment based on remaining principal + accrued interest
    sinking_payment = (remaining_principal / (num_periods - i)) + accrued_interest
    remaining_principal -= sinking_payment

    callability_price = ql.BondPrice(sinking_payment, ql.BondPrice.Clean)
    sinking_fund_schedule.append(
        ql.Callability(callability_price, ql.Callability.Call, sinking_date)
    )
#------------------------------------------------------------------------------------------------------------------------------
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

# # Print cash flows
# print("\nCash Flows:")
# for c in sinking_bond.cashflows():
#     print(f"{c.date()} - {c.amount():,.2f}")
#
# # Print sinking fund schedule
# print("\nSinking Fund Payments:")
# for s in sinking_fund_schedule:
#     print(f"{s.date()} - {s.price().amount():,.2f}")

print("\nCash Flows for 2025:")
for c in sinking_bond.cashflows():
    if c.date().year() in (2025, 2026):
        print(f"{c.date()} - {c.amount():,.2f}")

print("\nSinking Fund Payments for 2025:")
for s in sinking_fund_schedule:
    if s.date().year() in (2025, 2026):
        print(f"{s.date()} - {s.price().amount():,.2f}")

print(f" ")
# Yield to Maturity (YTM)
ytm = sinking_bond.bondYield(price, day_count, ql.Compounded, frequency)
print(f"Yield to Maturity (YTM): {ytm:.4%}")

# Macaulay Duration
macaulay_duration = ql.BondFunctions.duration(sinking_bond, ytm, day_count, ql.Compounded, frequency)
print(f"Macaulay Duration: {macaulay_duration:.4f}")

# Modified Duration
modified_duration = ql.BondFunctions.duration(sinking_bond, ytm, day_count, ql.Compounded, frequency, ql.Duration.Modified)
print(f"Modified Duration: {modified_duration:.4f}")
