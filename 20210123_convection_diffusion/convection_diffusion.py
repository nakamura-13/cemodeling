# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
plt.style.use('ggplot')

L = 0.1  # 管長さ [m]
D = 1.0e-7  # 拡散係数 [m2/s]
U = 4.0e-5  # 空塔速度 [m/s]

X_SECTIONS = 100  # 位置方向分割数
DX = L/X_SECTIONS  # 位置方向ステップ幅 [m]
DT = 1  # 時間ステップ幅 [s]

# 初期条件
INIT = [1 if 0.02 <= k*DX <= 0.025 else 0 for k in range(X_SECTIONS)]

# 境界条件
BOUND_L = 0  # at x = 0 m
BOUND_R = 0  # at x = 0.1 m


# 差分式
def get_c_next(c):
    """
    Parameters
    ------
    c: list of float
        0:c_i-1,j  1:c_i,j  2:c_i+1,j の3つを収容したリスト
    Returns
    -----
    float
        c_i,j+1
    """
    convection = - DT/DX * U * (c[2] - c[1])
    diffusion = DT/DX/DX * D * (c[2] - 2*c[1] + c[0])
    return c[1] + convection + diffusion


# 時間j+1の濃度分布計算
def get_cp_next(cp):
    """
    Parameters
    ------
    cp: list of float
        時間jの濃度分布
    Returns
    -----
    list of float
        時間j+1の濃度分布
    """
    l = [BOUND_L]
    m = [get_c_next([cp[i-1], cp[i], cp[i+1]]) for i in range(1, X_SECTIONS-1)]
    r = [BOUND_R]
    return l + m + r


# 濃度分布の時間変化計算
def get_cp_series(init_cond, time_steps):
    """
    Parameters
    ------
    init_cond: list of float
        時間0の濃度分布
    time_steps:
        時間ステップ数
    Returns
    -----
    list of [float]
        時系列濃度分布のリスト
    """
    cp_series = [init_cond]
    for j in range(1, time_steps):
        cp_now = cp_series[-1]
        cp_next = get_cp_next(cp_now)
        cp_series.append(cp_next)
    return cp_series


series = get_cp_series(INIT, 1000)

x = [k*DX for k in range(X_SECTIONS)]
plt.plot(x, series[0], label="t = 0")
plt.plot(x, series[50], label="t = 50")
plt.plot(x, series[300], label="t = 300")
plt.plot(x, series[-1], label="t = 1000")
plt.xlabel("x [m]")
plt.ylabel("c [mol/m3]")
plt.legend()
plt.show()
