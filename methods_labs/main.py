import math

from Newton_Method import newton_method
from Easy_Iter_Method import simple_iteration
from Method_Chord import chord_method
from bisection import bisection


def f(x):
    return math.sin(x) - 1/(2*x)
f_str = "sin(x) - 1/(2*x)"
def df(x):
    return math.cos(x) + 1/(2*x**2)

def phi(x):
    return x - 0.6*(math.sin(x) - 1/(2*x))
phi_str = "x - 0.6*(sin(x) - 1/(2*x))"

def method_output(root,iterations,history,name):
    for row in history:
        print(*[i if isinstance(i, bool) else round(i, 6) if isinstance(i, (int, float)) else i for i in row])
    print(f"Корінь ({name}):", round(root, 6))
    print("Ітерацій:", iterations)

# ------------------------------------------------------------
# Умови
alpha = 0.5
beta = 1
eps = 0.00001

print(f"f(x):{f_str}, a={alpha}, b={beta}, eps={eps}")
print("------------------------------------------------------------")
# Метод Ньютона
root1, iterations1, hist1 = newton_method(f,df, x0=0.5, eps=eps)
print(f"k | x | fx | dfx | x_new | diff < eps")
method_output(root1, iterations1, hist1,"Метод Ньютона")


print("------------------------------------------------------------")


# Метод простих ітерацій
root2, iterations2, hist2 = simple_iteration(phi, x0=1,  eps=eps)
print("Обрана φ(x):", phi_str)
print(f"k | x | x new | diff | diff < eps")
method_output(root2, iterations2, hist2,"Метод простих ітерацій")


print("------------------------------------------------------------")
# Метод ділення навпіл

print(f"k | a | b | abs(b - a) / 2 | abs(b - a) / 2 < eps")
root3, iterations3, hist3 = bisection(f, alpha, beta, eps)
method_output(root3, iterations3, hist3,"Метод ділення навпіл")

print("------------------------------------------------------------")
# Метод хорд
print(f"it| a | b | abs(x - x0) | < eps")
root4, iterations4, hist4 = chord_method(f, alpha, beta, eps)
method_output(root4, iterations4, hist4,"Метод хорд")


