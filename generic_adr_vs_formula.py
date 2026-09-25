import math
import time
import itertools
import numpy as np

from gurobipy import GRB, quicksum
import gurobipy as gp

from utils import rho_decimal


def check_generic_adr(m):
    tic = time.perf_counter()
    print('We verify whether a generic ADR (no symmetric requirement)\n'
          'on the canonical instance produces the number in the exact formula.\n'
          f'Verification for m = {m}.')
    EPS = 1e-6
    max_dev = min_dev = 0

    val8 = []

    for k in range(1, m + 1):
        exact_value = rho_decimal(m, k)
        cmk = math.comb(m, k)

        cols = list(itertools.combinations(range(m), k))
        B = np.array([[1.0 if i in w else 0.0 for w in cols] for i in range(m)])
        d = np.ones(len(cols))
        V = [np.zeros(m)]
        zeros = np.zeros(cmk)
        for r in range(1, k + 1):
            for S in itertools.combinations(range(m), r):
                v = np.zeros(m)
                v[list(S)] = 1.0
                V.append(v)

        model = gp.Model()
        model.Params.OutputFlag = 0
        model.Params.FeasibilityTol = 1e-9
        model.Params.OptimalityTol = 1e-9
        model.Params.NumericFocus = 3

        p = model.addMVar(shape=cmk, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)
        Q = model.addMVar(shape=(cmk, m), vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)
        tau = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)

        model.setObjective(tau, GRB.MINIMIZE)

        for v in V:
            model.addConstr(B @ p + B @ Q @ v >= v)
            model.addConstr(p + Q @ v >= zeros)
            model.addConstr(d @ p + d @ Q @ v <= tau)

        model.optimize()

        dev = model.ObjVal - exact_value
        if dev > max_dev:
            max_dev = dev
        if dev < min_dev:
            min_dev = dev

        if abs(dev) > EPS:
            elapsed = time.perf_counter() - tic
            print(f'\nVerification failed at k = {k}.\n'
                  f'Exact value = {exact_value}, generic ADR value = {model.ObjVal}.\n'
                  f'Time = {elapsed:.2f}.\n\n')

            return

        val8.append(model.ObjVal)
        if k == 1:
            print('Pass:', end='')
        print(f' {k}', end='')
        if k == m:
            print()

    val8_round = [round(v, 6) for v in val8]
    elapsed = time.perf_counter() - tic
    print(f'Verification succeeded at m = {m}.\n'
          f'Deviation range [{min_dev}, {max_dev}].\n'
          'The generic ADR gives the exact formula.\n'
          f'At m = 8: {val8_round}.'
          f'Time = {elapsed:.2f}.\n\n')


if __name__ == '__main__':
    check_generic_adr(8)
