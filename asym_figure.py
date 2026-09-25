import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

from utils import rho_decimal


def asym_figure():
    label_fontsize = 14
    title_fontsize = 18
    sns.set_theme(style='white')

    os.makedirs('figures', exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5), facecolor='white')

    ax1 = axes[0]
    ax1.set_facecolor('white')

    k_list = range(1, 7)
    m_coord = range(2, 51)
    rho_coord_fixed = {}
    for k in k_list:
        rho_coord_fixed[k] = [1 if k > m else rho_decimal(m, k) for m in m_coord]

    for k in k_list:
        ax1.plot(
            m_coord,
            rho_coord_fixed[k],
            markersize=3,
            linewidth=1.5,
            label=f'k = {k}',
        )

    ax1.set_xlabel(r'$m$', fontsize=label_fontsize)
    ax1.set_ylabel(r'$\rho(m, k)$', fontsize=label_fontsize)
    ax1.set_title(r'Fixed budget', fontsize=title_fontsize)
    ax1.legend(fontsize=label_fontsize)
    ax1.grid(True, alpha=0.3)

    ax2 = axes[1]
    ax2.set_facecolor('white')

    m_list = [4, 8, 16, 32, 64]
    alpha_coord = {}
    rho_coord_proportional = {}

    for m in m_list:
        budget_list = np.linspace(1, m, m)
        rho_list = [rho_decimal(m, k) for k in budget_list]
        alpha_coord[m] = budget_list / m
        rho_coord_proportional[m] = rho_list

    color_map = {}

    for m in m_list:
        line, = ax2.plot(
            alpha_coord[m],
            rho_coord_proportional[m],
            linewidth=1.5,
            label=f'm = {m}',
        )
        color_map[m] = line.get_color()

    alpha_asym = np.linspace(0.001, 1.0, 500)
    rho_asym = 1.0 / alpha_asym
    ax2.plot(
        alpha_asym,
        rho_asym,
        linestyle='--',
        color='black',
        linewidth=1.2,
        label=r'$1 / \alpha$',
    )

    peak = {}
    for m in m_list:
        floor = math.floor(math.sqrt(m))
        ceil = floor + 1
        floor_rho = rho_decimal(m, floor)
        ceil_rho = rho_decimal(m, ceil)
        peak[m] = [ceil / m, ceil_rho] if floor_rho < ceil_rho else [floor / m, floor_rho]

    for m in m_list:
        ax2.plot(
            peak[m][0],
            peak[m][1],
            marker='*',
            markersize=15,
            color=color_map[m],
        )

    ax2.set_xlabel(r'$\alpha = k / m$', fontsize=label_fontsize)
    ax2.set_ylabel(r'$\rho(m, k)$', fontsize=label_fontsize)
    ax2.set_title(r'Proportional growth', fontsize=title_fontsize)
    ax2.legend(fontsize=label_fontsize)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0.8, 5.2)

    plt.tight_layout()
    plt.savefig('figures/asymptotic.pdf', format='pdf', bbox_inches='tight')
    plt.show()

    print('Figures are generated and saved.\n\n')


if __name__ == '__main__':
    asym_figure()
