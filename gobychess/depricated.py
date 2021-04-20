#!/usr/bin/env python3

def blocker_computation(square, blockers_opposite, blockers_own, direction):
    collision_opposite = table[direction][square] & blockers_opposite
    collision_own = table[direction][square] & blockers_own
    if direction in ['east', 'north east', 'north', 'north west']:
        idx_opposite = bit_scan1(collision_opposite) if bit_scan1(collision_opposite) else 66
        idx_own = bit_scan1(collision_own) if bit_scan1(collision_own) else 66
    if direction in ['west', 'south west', 'south', 'south east']:
        idx_opposite = reverse_bit_scan1(collision_opposite) if reverse_bit_scan1(collision_opposite) else 66
        idx_own = reverse_bit_scan1(collision_own) if reverse_bit_scan1(collision_own) else 66

    # print("=====================")
    # print_bitboard(collision_opposite)
    # print("=====================")
    # print_bitboard(collision_own)
    # print("=====================")
    # print(idx_opposite)
    # print(idx_own)

    if idx_opposite == 66 and idx_own == 66:
        blocked = xmpz(0b0000000000000000000000000000000000000000000000000000000000000000)
    elif idx_opposite < idx_own:
        idx = idx_opposite
        blocked = table[direction][idx]
        # print("opp: " + str(idx))
    else:
        idx = idx_own - 1
        blocked = table[direction][idx]
        # print("own" + str(idx))

    blocked = (1 << 64) - 1 - blocked
    movement = table[direction][square] & blocked
    return movement
