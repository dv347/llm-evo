def evolve(in0):
    loopBreakConst = 200
    i0 = int()
    res0 = bool()
    res0 = True
    loopBreak = 0
    for i0 in range(1, len(in0)):
        if in0[i0] < in0[i0 - 1]:
            res0 = False
        if loopBreak > loopBreakConst:
            break
        loopBreak += 1
    return res0