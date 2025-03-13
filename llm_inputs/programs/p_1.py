def evolve(in0, in1, in2):
    f0 = float(); f1 = float(); f2 = float()
    b0 = bool(); b1 = bool(); b2 = bool()
    res0 = bool()
    f0 = in0*in0
    f1 = in1*in1
    f2 = in2*in2
    b0 = f0 == f1 + f2
    b1 = f1 == f0 + f2
    b2 = f2 == f0 + f1
    res0 = b0 or b1 or b2
    return res0