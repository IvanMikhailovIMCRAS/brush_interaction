import numpy as np


def mol_script(N1: int, N2: int, m: int, n: int, number: int) -> str:

    if number < 1:
        raise Exception("number must be >= 1")
    if N1 <= 0:
        raise Exception("N1 must be > 0")
    if N2 < 0:
        raise Exception("N2 must be >= 0")
    if N2 != 0:
        if N2 <= m or N2 % m != 0:
            raise Exception("N2 must be > m and N2 % m == 0")
    if m < 1:
        raise Exception("m must be >= 1")
    if n < 0:
        raise Exception("m must be >= 0")
    if N2 == 0:
        return f'(X{number})1(A{number}){N1-1}'
    elif n == 0:
        return f'(X{number})1(A{number}){N1-1}(B{number}){N2}'

    else:
        return f'(X{number})1(A{number}){N1-1}((B{number}){m}[(C{number}){n}]){N2//m-1}(B{number}){N2}'

if __name__ == '__main__':
    N1 = 10
    N2 = 8
    m = 4
    n = 10
    sigma = 0.1
    n_layer = 40
    theta = N1 + N2 + (N2 // m - 1) * n * sigma
    d_max = int((N1 + N2 + n) * 2)
    d_min = int(2 * theta) + 1
    print(d_max,
          d_min)
    with open('brush.in', 'w') as file1:
        file1.writelines(
    f"""
    lat : flat : n_layers : {d_min}
    lat : flat : geometry : flat
    lat : flat : lambda : 0.16666666666666666667
    lat : flat : lowerbound : surface
    lat : flat : upperbound : surface

    mon : solid1 : freedom : frozen
    mon : solid1 : frozen_range : upperbound
    mon : solid2 : freedom : frozen
    mon : solid2 : frozen_range : lowerbound
    mon : W : freedom : free
    mon : X1: freedom : pinned
    mon : X1 : pinned_range : 1
    mon : A1 : freedom : free
    mon : B1 : freedom : free
    mon : X2: freedom : pinned
    mon : X2 : pinned_range : {d_min}
    mon : A2 : freedom : free
    mon : B2 : freedom : free
    mon : C1 : freedom : free
    mon : C2 : freedom : free
    
    mol : solvent : composition : (W)1
    mol : solvent : freedom : solvent

    mol : pol1 : composition : {mol_script(N1, N2, m, n, 1)}
    mol : pol1 : freedom : restricted
    mol : pol1 : theta : {theta}

    mol : pol2 : composition : {mol_script(N1, N2, m, n, 2)}
    mol : pol2 : freedom : restricted
    mol : pol2 : theta : {theta}

    output : filename.pro : type : profiles
    output : filename.pro : template : profile.template

    output : filename.kal : type : kal
    output : filename.kal : template : kaleidagraph.template

    start
    
    """
        )
        for i in range (d_min+1, d_max+1):
            file1.writelines(
            f"""
            lat : flat : n_layers : {i}   
            mon : X2 : pinned_range : {i}

            start
            
            """
            )

