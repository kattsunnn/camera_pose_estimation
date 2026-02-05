
def xc_to_xw(xc, R, t):
    return R.T @ ( xc - t )

def xw_to_xc(xw, R, t):
    return R @ xw + t