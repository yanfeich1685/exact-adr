from utils import rho_frac


def print_table(M):
    print('Exact rho(m, k):')
    for m in range(2, M + 1):
        cells = []
        for k in range(1, m + 1):
            nom, denom = rho_frac(m, k)
            cell = str(nom) + '/' + str(denom) if nom > denom else str(1)
            cells.append(cell)
        print(f'  m={m:2d}: ' + '  '.join(f'{c:>6}' for c in cells))
    print('\n')


if __name__ == '__main__':
    print_table(10)
