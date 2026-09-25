import math
import time
import itertools
import numpy as np

from gurobipy import GRB, quicksum
import gurobipy as gp

from utils import rho_decimal


def check_random_instances(m):
    tic = time.perf_counter()

    N_TRIALS = 200
    EPS = 1e-6
    MAX_COL_RATIO = 3
    MIN_VAL = 1e-2
    MAX_VAL = 10
    RANGE = MAX_VAL - MIN_VAL
    np.random.seed(1077)

    print('We compute the affine gap on random instances.\n'
          'The ADR is generic (no symmetric requirement).\n'
          f'For each (m, k) we generate {N_TRIALS} random instances.\n'
          'The gap is computed and compared to the exact formula.\n'
          f'Verification for m = {m}.')

    res = np.zeros((m + 1, N_TRIALS))

    for k in range(1, m + 1):
        exact_value = rho_decimal(m, k)
        for t in range(N_TRIALS):
            n = np.random.randint(m, MAX_COL_RATIO * m + 1)
            B = MIN_VAL + np.random.rand(m, n) * RANGE
            d = MIN_VAL + np.random.rand(n) * RANGE
            V = [np.zeros(m)]
            zeros = np.zeros(n)
            for r in range(1, k + 1):
                for S in itertools.combinations(range(m), r):
                    v = np.zeros(m)
                    v[list(S)] = 1.0
                    V.append(v)

            vcount = len(V)

            mfa = gp.Model()
            mfa.Params.OutputFlag = 0
            mfa.Params.FeasibilityTol = 1e-9
            mfa.Params.OptimalityTol = 1e-9
            mfa.Params.NumericFocus = 3

            y = {}
            for v in range(vcount):
                y[v] = mfa.addMVar(shape=n, vtype=GRB.CONTINUOUS, lb=0, ub=GRB.INFINITY)
            tau = mfa.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)

            mfa.setObjective(tau, GRB.MINIMIZE)

            for v in range(vcount):
                mfa.addConstr(B @ y[v] >= V[v])
                mfa.addConstr(d @ y[v] <= tau)

            mfa.optimize()

            maff = gp.Model()
            maff.Params.OutputFlag = 0
            maff.Params.FeasibilityTol = 1e-9
            maff.Params.OptimalityTol = 1e-9
            maff.Params.NumericFocus = 3

            p = maff.addMVar(shape=n, vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)
            Q = maff.addMVar(shape=(n, m), vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)
            ttt = maff.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)

            maff.setObjective(ttt, GRB.MINIMIZE)

            for v in range(vcount):
                maff.addConstr(B @ p + B @ Q @ V[v] >= V[v])
                maff.addConstr(p + Q @ V[v] >= zeros)
                maff.addConstr(d @ p + d @ Q @ V[v] <= ttt)

            maff.optimize()

            res[k, t] = maff.ObjVal / mfa.ObjVal
            if res[k, t] > exact_value * (1 + EPS):
                elapsed = time.perf_counter() - tic
                print(f'\nVerification failed at k = {k}.\n'
                      f'Exact value = {exact_value}, gap = {res[k, t]}.\n'
                      f'Time = {elapsed:.2f}.\n\n')

        gap_min = res[k, :].min()
        gap_max = res[k, :].max()
        elapsed = time.perf_counter() - tic
        print(f'k = {k}, gap min/max/worst = {gap_min:.6f}/{gap_max:.6f}/{exact_value:.6f}, time = {elapsed:.2f}')

    elapsed = time.perf_counter() - tic
    print(f'Verification succeeded at m = {m}.\n'
          f'Time = {elapsed:.2f}.\n\n')


if __name__ == '__main__':
    check_random_instances(8)
