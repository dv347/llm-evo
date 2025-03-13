def evolve(in0):
    loopBreakConst = 200
    f0 = float()
    res0 = []
    loopBreak = 0
    for f0 in in0:
        if f0 == abs(f0):
            res0.append(f0)
        if loopBreak > loopBreakConst:
            break
        loopBreak += 1
    return res0