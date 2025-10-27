import numpy as np
from math import factorial
from typing import List, Sequence, Tuple


def f(x: np.ndarray) -> np.ndarray:
    """Target function from variant 4."""
    value = 2 * x ** 3 - 4 * x
    return np.sign(value) * np.abs(value) ** (1 / 5)


# ---------------------------------------------------------------------------
# Interpolation helpers
# ---------------------------------------------------------------------------

def lagrange_polynomial(xs: Sequence[float], ys: Sequence[float]) -> np.poly1d:
    """Return the Lagrange interpolation polynomial as ``numpy.poly1d``."""
    poly = np.poly1d(0.0)
    for i, (x_i, y_i) in enumerate(zip(xs, ys)):
        basis = np.poly1d([1.0])
        denom = 1.0
        for j, x_j in enumerate(xs):
            if i == j:
                continue
            basis *= np.poly1d([1.0, -x_j])
            denom *= (x_i - x_j)
        poly += basis * (y_i / denom)
    return poly


def lagrange_value(x: float, xs: Sequence[float], ys: Sequence[float]) -> float:
    """Evaluate the Lagrange interpolation polynomial in the barycentric form."""
    total = 0.0
    for i, (x_i, y_i) in enumerate(zip(xs, ys)):
        term = y_i
        for j, x_j in enumerate(xs):
            if i == j:
                continue
            term *= (x - x_j) / (x_i - x_j)
        total += term
    return total


def forward_differences_full(values: Sequence[float]) -> List[np.ndarray]:
    """Return the triangular table of forward differences."""
    current = np.asarray(values, dtype=float)
    table = [current]
    while current.size > 1:
        current = np.diff(current)
        table.append(current)
    return table


def first_column_forward_diffs(values: Sequence[float]) -> np.ndarray:
    """Return the first column of the forward-difference table."""
    table = forward_differences_full(values)
    return np.array([row[0] for row in table], dtype=float)


def falling_factorial(t: float, k: int) -> float:
    """Compute the falling factorial ``t (t-1) ... (t-k+1)``."""
    result = 1.0
    for j in range(k):
        result *= (t - j)
    return result


def newton_forward_terms(
    x: float,
    x0: float,
    h: float,
    diffs0: Sequence[float],
) -> Tuple[float, List[float], np.ndarray]:
    """Return ``t`` as well as the individual and cumulative Newton terms."""
    t = (x - x0) / h
    terms: List[float] = []
    for k, delta in enumerate(diffs0):
        term = falling_factorial(t, k) / factorial(k) * delta
        terms.append(term)
    partial_sums = np.cumsum(terms)
    return t, terms, partial_sums


def newton_polynomial(
    xs: Sequence[float],
    diffs0: Sequence[float],
    step: float,
) -> np.poly1d:
    """Construct the Newton forward interpolation polynomial in power basis."""
    x0 = xs[0]
    poly = np.poly1d(0.0)
    basis = np.poly1d([1.0])
    for k, delta in enumerate(diffs0):
        if k == 0:
            term_poly = basis * delta
        else:
            basis *= np.poly1d([1.0, -(x0 + (k - 1) * step)])
            coefficient = delta / factorial(k) / (step ** k)
            term_poly = basis * coefficient
        poly += term_poly
    return poly


# ---------------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------------

def format_polynomial(poly: np.poly1d, variable: str = "x", precision: int = 6) -> str:
    """Return a readable textual representation of a polynomial."""
    coeffs = poly.c
    degree = len(coeffs) - 1
    pieces: List[str] = []

    for i, coef in enumerate(coeffs):
        power = degree - i
        if np.isclose(coef, 0.0, atol=1e-12):
            continue

        abs_coef = abs(coef)
        coef_str = f"{abs_coef:.{precision}f}".rstrip("0").rstrip(".")
        if coef_str == "":
            coef_str = "0"

        if power == 0:
            term = coef_str
        elif power == 1:
            if np.isclose(abs_coef, 1.0):
                term = variable
            else:
                term = f"{coef_str}{variable}"
        else:
            if np.isclose(abs_coef, 1.0):
                term = f"{variable}^{power}"
            else:
                term = f"{coef_str}{variable}^{power}"

        sign = "-" if coef < 0 else "+"
        pieces.append((sign, term))

    if not pieces:
        return "0"

    first_sign, first_term = pieces[0]
    result = ("-" if first_sign == "-" else "") + first_term
    for sign, term in pieces[1:]:
        result += f" {sign} {term}"
    return result


def print_lagrange_table(xs: np.ndarray, ys: np.ndarray) -> None:
    x_mid = (xs[:-1] + xs[1:]) / 2
    x_all = np.unique(np.concatenate([xs, x_mid]))

    lagrange_values = [lagrange_value(x, xs, ys) for x in x_all]
    function_values = [f(x) for x in x_all]

    print("x\tf(x)\t\tL(x)")
    print("-" * 35)
    for xi, fi, li in zip(x_all, function_values, lagrange_values):
        print(f"{xi:<.2f}\t{fi:<.6f}\t{li:<.6f}")


def print_forward_difference_table(table: List[np.ndarray]) -> None:
    print("=== Таблиця прямих різниць (вперед) ===")
    headers = ["\ty"] + [f"  Δ^{k} y\t" for k in range(1, len(table))]
    print("\t".join(headers))

    width = len(table[0])
    for i in range(width):
        row = []
        for column in table:
            row.append(f"{column[i]: .6f}" if i < len(column) else "")
        print("\t".join(row))
    print()


def print_newton_evaluation(
    xs: np.ndarray,
    ys: np.ndarray,
    diffs0: np.ndarray,
) -> None:
    x_mid = (xs[:-1] + xs[1:]) / 2
    x_all = np.sort(np.unique(np.concatenate([xs, x_mid])))

    columns = ["x", "f(x)", "t", "N0", "N1", "N2", "N3", "N4", "N(x)"]
    widths = [4, 12, 10, 12, 12, 12, 12, 14, 14]
    header = " ".join(name.ljust(w) for name, w in zip(columns, widths))
    print(header)
    print("-" * len(header))

    x0, step = xs[0], xs[1] - xs[0]
    for x in x_all:
        t, terms, partial = newton_forward_terms(x, x0, step, diffs0)
        terms = (terms + [0.0] * 5)[:5]
        polynomial_value = partial[-1]

        row = [
            _fmt(x, widths[0] - 1, 1),
            _fmt(f(x), widths[1] - 1, 6),
            _fmt(t, widths[2] - 1, 2),
            *[_fmt(value, width - 1, 6) for value, width in zip(terms, widths[3:8])],
            _fmt(polynomial_value, widths[8] - 1, 6),
        ]
        print(" ".join(row))


def _fmt(value: float, width: int, precision: int) -> str:
    return f"{value:{width}.{precision}f}"


def main() -> None:
    a, b = -1, 3
    n = 5
    xs = np.linspace(a, b, n)
    ys = f(xs)

    print_lagrange_table(xs, ys)

    differences = forward_differences_full(ys)
    print_forward_difference_table(differences)

    diffs0 = first_column_forward_diffs(ys)
    print_newton_evaluation(xs, ys, diffs0)

    lagrange_poly = lagrange_polynomial(xs, ys)
    newton_poly = newton_polynomial(xs, diffs0, xs[1] - xs[0])

    print("\nПоліном Лагранжа у степеневій формі:")
    print(f"L_n(x) = {format_polynomial(lagrange_poly)}")

    print("\nПоліном Ньютона у степеневій формі:")
    print(f"N_n(x) = {format_polynomial(newton_poly)}")


if __name__ == "__main__":
    main()
