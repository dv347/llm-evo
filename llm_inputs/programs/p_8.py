def evolve(in0):
    loopBreakConst = 200
    f0 = float()
    res0 = int()
    loopBreak = 0
    for f0 in in0:
        res0 += 1
        if loopBreak > loopBreakConst:
            break
        loopBreak += 1
    return res0