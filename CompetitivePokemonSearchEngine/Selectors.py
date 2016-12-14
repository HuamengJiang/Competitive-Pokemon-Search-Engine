# The file where predicates using damage calc are defined

# currently not functional programming

def OHKO(move, offender, defender):
    return NHKO(offender, defender)

def NHKO(n, move, offender, defender):
    if n == 0:
        return defender.faints()

    damage = calc(move, offender, defender)
    # damage = move.calc(offender, defender)
    defender.useItem()
    if defender.faints():
        return True

    return NHKO(n-1, move, offender, defender)
