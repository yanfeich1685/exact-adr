import math
import time
from gurobipy import GRB, quicksum
import gurobipy as gp

from utils import rho_decimal


def check_four_var_lp(M):
    tic = time.perf_counter()
    print('We verify whether the four-variable program\n'
          'on the canonical instance produces the number in the exact formula.\n'
          f'Verification goes from m = 2 to {M}.\n'
          f'Total examinations = {(M + 2) * (M - 1) / 2:.0f}.')
    EPS = 1e-6
    max_dev = min_dev = 0

    val8 = []

    for m in range(2, M + 1):
        for k in range(1, m + 1):
            exact_value = rho_decimal(m, k)

            A = math.comb(m - 1, k - 1)
            B = math.comb(m - 2, k-2) if k >= 2 else 0
            C = math.comb(m - 2, k-1)
            D = math.comb(m - 1, k)
            N = math.comb(m, k)

            model = gp.Model()
            model.Params.OutputFlag = 0
            model.Params.FeasibilityTol = 1e-9
            # model.Params.IntFeasTol = 1e-9
            model.Params.OptimalityTol = 1e-9
            model.Params.NumericFocus = 3

            p = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)
            qp = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)
            qm = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)
            tau = model.addVar(vtype=GRB.CONTINUOUS, lb=-GRB.INFINITY, ub=GRB.INFINITY)

            model.setObjective(tau, GRB.MINIMIZE)

            for r in range(1, k + 1):
                model.addConstr(A * p + (A + (r - 1) * B) * qp + (r - 1) * C * qm >= 1)
            for r in range(0, k + 1):
                t_lb = max(0, k - m + r)
                for t in range(t_lb, r + 1):
                    model.addConstr(p + t * qp + (r - t) * qm >= 0)
                model.addConstr(tau >= N * p + r * A * qp + r * D * qm)

            model.optimize()

            dev = model.ObjVal - exact_value
            if dev > max_dev:
                max_dev = dev
            if dev < min_dev:
                min_dev = dev

            if abs(dev) > EPS:
                elapsed = time.perf_counter() - tic
                print(f'Verification failed for (m, k) = ({m}, {k}).\n'
                      f'Exact value = {exact_value}, LP value = {model.ObjVal}.\n'
                      f'Time = {elapsed:.2f}.\n\n')

                return

            if m == 8:
                val8.append(model.ObjVal)

    val8_round = [round(v, 6) for v in val8]
    elapsed = time.perf_counter() - tic
    print(f'Verification succeeded up to m = {M}.\n'
          f'Deviation range [{min_dev}, {max_dev}].\n'
          'The affine program gives the exact formula.\n'
          f'At m = 8: {val8_round}.'
          f'\nTime = {elapsed:.2f}.\n\n')


if __name__ == '__main__':
    check_four_var_lp(30)
