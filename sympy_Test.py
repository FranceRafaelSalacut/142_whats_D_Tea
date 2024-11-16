import sympy as sp

n = sp.symbols("n")
m = sp.symbols("m")

print(sp.simplify(4*(n-m+1) + 2))

form1 = sp.simplify((6*n)+4)

print(form1)

print(sp.expand((form1)*n))
