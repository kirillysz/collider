import math
import matplotlib.pyplot as plt

N_A = 6.02214076e23
BARN = 1e-24 # барн
CI = 3.7e10 # 1 кбри в беккерелях
DAY = 86400.0
HOUR = 3600.0
W = 0.34

AMOUNT_ITER_I_131 = 8
AMOUNT_ITER_TE_131 = 1500

T_I_131 = DAY * 8.02
T_TE_130 = DAY * 7.91 * 10**20
T_TE_131 = DAY * 25.01

T_I_131_1_DAY = T_I_131 / 8
T_TE_130_1_DAY = T_TE_130 / 8
T_TE_131_1_DAY = T_TE_131 / 8

LAMBDA_I_131 = math.log(2, math.e) / T_I_131
LAMBDA_TE_130 = math.log(2, math.e) / T_TE_130
LAMBDA_TE_131 = math.log(2, math.e) / T_TE_131

print(LAMBDA_TE_130)

M_I_131 = 130.91
M_TE_130 = 129.91
M_TE_131 = 130.9

SIGMA = 0.3 * float(10**-24)
F = 10**13

V_TE_130 = 1/(6.24 * 10**-3)


def find_amount_core(m, M):
    """N = m * N_a / M
    m - масса в-ва
    M - молярка
    """

    N = m * (N_A / M)
    return N

def find_amount_te_core(m):
    N = (m / M_TE_130) * N_A * W
    return N

def find_A(R, t):
    A = R * (1 - math.e**(-LAMBDA_TE_130 * t))
    return A

def find_R(N):
    R = SIGMA * F * N * V_TE_130
    return R

def find_rad_zahvata(F, N):
    """Rz = sigma * F * N
    
    Sigma - сечение захвата
    F - potok
    N - кол-во ядер
    """

    Rz = SIGMA * F * N
    return Rz


def raspad(N0, lambd, t):
    "R = N0 * e^(-lambda * t)"
    R = N0 * math.e**(-lambd * t)
    return R


def change_cores(N0, t, T):
    """N = N0 * 2^(-t/T)
    t - прошедшее время
    T - полураспад    
    """

    N = N0 * 2**(-t/T)
    return N


def dynamic(m, M, amount_iter, t, T):
    cores = find_amount_core(m, M)
    arr = []
    arr.append(cores)
    for i in range(amount_iter):
        cores = change_cores(cores, t, T)
        arr.append(cores)
    
    print(arr)


def find_A(R, t):
    A = R * (1 - 2.7**(-LAMBDA_I_131* t))
    return A
print(-LAMBDA_I_131)


N = find_amount_te_core(1)
R = find_R(N)
print(R)

x1 = [i for i in range(0, int(7*DAY), 1000)]
y1 = [find_A(R, i) for i in range(0, int(7*DAY), 1000)]

plt.plot(x1, y1, label="A(t)")
plt.xlabel("T (ч)")
plt.ylabel("A (Бк)")
plt.show()