def evolve(in0):
    loopBreakConst = 200
    i0 = int()
    res0 = int()
    loopBreak = 0
    for i0 in range(len(in0)):
        if mod(i0, 2) == 0:
            res0 += in0[i0]
        if loopBreak > loopBreakConst:
            break
        loopBreak += 1
    return res0