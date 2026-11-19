import math
import matplotlib.pyplot as plt

N_A = 6.02214076e23
BARN = 1e-24 # барн
CI = 3.7e10 # 1 Ки в беккерелях
DAY = 86400.0
HOUR = 3600.0
W = 0.34 # массовая доля теллура-130

T_I_131 = DAY * 8.02 # период полураспада йода-131
LAMBDA_I_131 = math.log(2, math.e) / T_I_131

M_TE_130 = 129.91 # молярка теллура-130

SIGMA = 0.3 * float(10**-24) # сечение захвата
F = 10**13 # поток нейтронов

DOZA = 3.7 * 10**9 # доза на 1 пациента, Бк
CENTERS = 80
PATIENTS = 100


def find_amount_te_core(m):
    """N = (m * W / M) * N_a
    m - масса природного теллура
    """
    N = (m * W / M_TE_130) * N_A
    return N


def find_rad_zahvata(F, N):
    """Rz = sigma * F * N
    Sigma - сечение захвата
    F - potok
    N - кол-во ядер
    """
    Rz = SIGMA * F * N
    return Rz


def find_A(R, t):
    "A = R * (1 - e^(-lambda * t))"
    A = R * (1 - math.e**(-LAMBDA_I_131 * t))
    return A


def raspad(A0, t):
    "A = A0 * e^(-lambda * t)"
    A = A0 * math.e**(-LAMBDA_I_131 * t)
    return A


def perevod_v_ki(A):
    "перевод Бк -> Ки"
    return A / CI


def find_dostavka(A, poteri):
    """активность после 48ч выделения и дороги
    poteri - доля потерь в пути (0.2 = 20%)
    """
    A = raspad(A, 48 * HOUR)
    A = A * (1 - poteri) # минус потери в пути
    return A


def find_patients(A):
    "сколько пациентов покроет активность A"
    return A / DOZA


def find_emkost():
    "сколько всего нужно на 80 центров по 100 пациентов"
    return CENTERS * PATIENTS * DOZA


if __name__ == "__main__":
    N = find_amount_te_core(1)
    R = find_rad_zahvata(F, N)

    t = 7 * DAY
    A = find_A(R, t)

    print("ядра N =", N)
    print("скорость захвата R =", R, "Бк (насыщение)")
    print("активность за 7 сут A =", A, "Бк =", A / 10**9, "ГБк")
    print("в Ки:", perevod_v_ki(A), "Ки")

    A_dost = find_dostavka(A, 0.2)
    print("после доставки A =", A_dost, "Бк =", A_dost / 10**9, "ГБк")
    print("пациентов с 1 г:", find_patients(A_dost))
    print("нужно на 80 центров:", find_emkost(), "Бк =", find_emkost() / 10**12, "ТБк")

    x1 = [i / DAY for i in range(0, int(14*DAY), 3600)]
    y1 = [find_A(R, i) / 10**9 for i in range(0, int(14*DAY), 3600)]

    plt.plot(x1, y1, label="A(t)")
    plt.axhline(R / 10**9, ls="--", color="gray", label="насыщение")
    plt.xlabel("T (сут)")
    plt.ylabel("A (ГБк)")
    plt.legend()
    plt.show()
