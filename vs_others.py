import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math

from utils import rho_decimal, bb_decimal, tws_decimal, beg_decimal


def vs_others():
    label_fontsize = 14
    title_fontsize = 18
    sns.set_theme(style='white')

    os.makedirs('figures', exist_ok=True)

    M_list = [8, 16, 32, 64]

    fig, axes = plt.subplots(2, 2, figsize=(16, 10), facecolor='white')
    axes = axes.flatten()

    for ax, M in zip(axes, M_list):
        ax.set_facecolor('white')

        m_coord = range(1, M + 1)
        rho_coord = [rho_decimal(M, k) for k in m_coord]
        bb_coord = [bb_decimal(M, k) for k in m_coord]
        tws_coord = [tws_decimal(M, k) for k in m_coord]
        beg_coord = [beg_decimal(M, k) for k in m_coord]

        ax.plot(
            m_coord,
            rho_coord,
            # marker='o',
            # markersize=3,
            linewidth=1.5,
            label=r'$\rho$',
        )

        ax.plot(
            m_coord,
            bb_coord,
            # marker='s',
            # markersize=3,
            linewidth=1.5,
            label=r'$\rho^{\mathrm{BB}}$',
        )

        ax.plot(
            m_coord,
            beg_coord,
            # marker='s',
            # markersize=3,
            linewidth=1.5,
            label=r'$\rho^{\mathrm{BEG}}$',
        )

        ax.plot(
            m_coord,
            tws_coord,
            # marker='s',
            # markersize=3,
            linewidth=1.5,
            label=r'$\rho^{\mathrm{TWS}}$',
        )

        ax.set_xlabel(r'$k$', fontsize=label_fontsize)
        ax.set_ylabel(r'$\rho$', fontsize=label_fontsize)
        ax.set_title(rf'$m = {M}$', fontsize=title_fontsize)
        ax.legend(fontsize=label_fontsize)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('figures/vs_known.pdf', format='pdf', bbox_inches='tight')
    plt.show()

    print('Figures are generated and saved.\n\n')


if __name__ == '__main__':
    vs_others()
