import blpapi
from blpapi import Request, SessionOptions, Session

CUSIP = "YOUR_CUSIP_HERE"
FIELDS = ["yld_ytm_bid", "yld_ytm_mid", "yld_ytm_ask"]

# Bloomberg server host and port
HOST = "localhost"
PORT = 8194

def get_yield_for_custom_price(price):
    # Setup session options
    sessionOptions = SessionOptions()
    sessionOptions.setServerHost(HOST)
    sessionOptions.setServerPort(PORT)

    # Create a session
    session = Session(sessionOptions)

    # Start the session
    if not session.start():
        print("Failed to start session.")
        return

    # Open the service to request data
    if not session.openService("//blp/refdata"):
        print("Failed to open //blp/refdata service.")
        return

    # Obtain the reference data service
    refDataService = session.getService("//blp/refdata")

    # Create the request
    request = refDataService.createRequest("ReferenceDataRequest")
    request.getElement("securities").appendValue("CUSIP:" + CUSIP)
    for field in FIELDS:
        request.getElement("fields").appendValue(field)

    # Add overrides to use the custom price
    overrides = request.getElement("overrides")
    override = overrides.appendElement()
    override.setElement("fieldId", "PX_LAST")
    override.setElement("value", price)

    # Send the request
    session.sendRequest(request)

    # Process received events
    while True:
        # We will timeout after 10 seconds to avoid indefinite waiting
        ev = session.nextEvent(10000)
        for msg in ev:
            if ev.eventType() == blpapi.Event.RESPONSE or ev.eventType() == blpapi.Event.PARTIAL_RESPONSE:
                # Print the result
                securityDataArray = msg.getElement("securityData")
                for securityData in securityDataArray.values():
                    security = securityData.getElement("security").getValue()
                    fieldData = securityData.getElement("fieldData")
                    yld_ytm_bid = fieldData.getElementAsFloat("yld_ytm_bid") if fieldData.hasElement("yld_ytm_bid") else None
                    yld_ytm_mid = fieldData.getElementAsFloat("yld_ytm_mid") if fieldData.hasElement("yld_ytm_mid") else None
                    yld_ytm_ask = fieldData.getElementAsFloat("yld_ytm_ask") if fieldData.hasElement("yld_ytm_ask") else None
                    print(f"CUSIP: {security}")
                    print(f"Yield to Maturity (Bid) for Custom Price ({price}): {yld_ytm_bid}")
                    print(f"Yield to Maturity (Mid) for Custom Price ({price}): {yld_ytm_mid}")
                    print(f"Yield to Maturity (Ask) for Custom Price ({price}): {yld_ytm_ask}")

        if ev.eventType() == blpapi.Event.RESPONSE:
            # Response event signals end of the response
            break

if __name__ == "__main__":
    # Example usage of get_yield_for_custom_price function
    custom_price = 100.5
    get_yield_for_custom_price(custom_price)
