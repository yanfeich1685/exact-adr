from asym_figure import asym_figure
from vs_others import vs_others
from print_table import print_table
from four_var_lp_vs_formula import check_four_var_lp
from generic_adr_vs_formula import check_generic_adr
from random_instances import check_random_instances


def main():
    asym_figure()
    vs_others()
    print_table(10)
    check_four_var_lp(30)
    check_generic_adr(8)
    check_random_instances(8)


if __name__ == '__main__':
    main()
