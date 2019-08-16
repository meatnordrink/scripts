def parseArray(arr):
    """Takes as input a string that looks like an array and returns an array of values. The values in the array are not necessarily of the same type. The function attempts to eval() each value in the array; but if it fails, it leaves the unevaluated string in place."""
    cleaned = arr.replace(" ", "").replace("[", "").replace("]", "")
    vals = cleaned.split(",")

    for i in range(0, len(vals)):
        try:
            vals[i] = eval(vals[i])
        except:
            pass

    return vals

def parseNumericArray(arr):
    """Takes as input a string that looks like an array and returns an array of numeric values. Any value in the array that can't be evaluated is turned into a zero."""
    out = parseArray(arr)

    for i in range(0, len(out)):
        if isinstance(out[i], str):
            out[i] = 0

    return out