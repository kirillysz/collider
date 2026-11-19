import math

N_A = 6.02214076e23
BARN = 1e-24 # барн
CI = 3.7e10 # 1 кбри в беккерелях
DAY = 86400.0
HOUR = 3600.0

AMOUNT_ITER_I_131 = 8
AMOUNT_ITER_TE_131 = 0.017361

T_I_131 = DAY * 8.02
T_TE_130 = DAY * 2.89 * 10**23

T_I_131_1_DAY = T_I_131 / 8
T_TE_130_1_DAY = T_TE_130 / 8

LAMBDA_I_131 = math.log(2, math.e) / T_I_131
LAMBDA_TE_130 = math.log(2, math.e) / T_TE_130

M_I_131 = 130.91
M_TE_130 = 129.91

SIGMA = 0.3 * float(10**24)
F = 10**13


def find_amount_core(m, M):
    """N = m * N_a / M
    m - масса в-ва
    M - молярка
    """

    N = m * N_A / M
    return N


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
    
    print(cores)
    print(arr)
    
dynamic(10, M_I_131, AMOUNT_ITER_I_131, DAY, T_I_131)
