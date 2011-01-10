import math

def formatAmount(val, prec=3, lowest=0, highest=0):
    """
    Add suffix to value, transform value to match new suffix and round it.

    Keyword arguments:
    val -- value to process
    prec -- precision of final number (number of significant positions to show)
    lowest -- lowest order for suffixizing
    highest -- highest order for suffixizing
    """
    if val is None:
        result = ""
    else:
        # Separate value to mantissa and suffix
        mantissa, suffix = suffixizeAmount(val, lowest, highest)
        # Round mantissa and add suffix
        newMantissa = processAmount(mantissa, prec)
        result = u"{0}{1}".format(newMantissa, suffix)
    return result

def suffixizeAmount(val, lowest=-6, highest=9):
    """
    Add suffix to value and transform value to match new suffix.

    Keyword arguments:
    val -- value to process
    lowest -- lowest order for suffixizing
    highest -- highest order for suffixizing

    Suffixes below lowest and above highest orders won't be used.
    """
    if abs(val) >= 1000 and highest >= 3:
        suffixmap = {3 : "k", 6 : "M", 9 : "B"}
        # Start from highest possible suffix
        for key in sorted(suffixmap, reverse = True):
            # Find first suitable suffix and check if it's not above highest order
            if val >= 10**key and key <= highest:
                return val/float(10**key), suffixmap[key]
    # Take numbers between 0 and 1, and matching/below highest possible negative suffix
    elif abs(val) < 1 and val != 0 and lowest <= -3:
        suffixmap = {-6 : u'\u03bc', -3 : "m"}
        # Start from lowest possible suffix
        for key in sorted(suffixmap, reverse = False):
            # Check if mantissa with next suffix is in range [1, 1000)
            # Here we assume that each next order is greater than previous by 3
            if val < 10**(key+3) and key >= lowest:
                return val/float(10**key), suffixmap[key]
    # If no suitable suffixes are found within given order borders, or value
    # is already within [1, 1000) boundaries, just return rounded value with no suffix
    else:
        return val, ""

def processAmount(val, prec=3):
    """
    Round number and return as string.

    Keyword arguments:
    val -- value to round
    prec -- precision of final number (number of significant positions to show)

    Integer numbers are not rounded, only fractional part.
    """
    if val == 0: # Logarithm is not defined for zero
        return "0"

    roundFactor = int(prec - math.ceil(math.log10(abs(val))))
    # But we don't want to round integers
    if roundFactor < 0: roundFactor = 0
    val = round(val, roundFactor)
    # Strip trailing zero for integers and convert to string
    result = str(val)[-2:] == '.0' and str(val)[:-2] or str(val)
    return result