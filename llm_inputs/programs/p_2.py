def evolve(in0, in1, in2):
    res0 = bool()
    if (in0+in1==in2):
        res0 = True
    if (in0+in2==in1):
        res0 = True
    if (in1+in2==in0):
        res0 = True
    return res0