# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# 条件
ca0 = 1  # 初期濃度 [mol/m3]
k = 0.01  # 反応速度定数 [1/s]
t_range = 600  # 計算する時間範囲 [s]

# 解析解
t_an = np.linspace(0, t_range, 100)
ca_an = ca0 * np.exp(-k*t_an)

# 数値解
dt = 30  # 微小時間 [s]
n = int(t_range/dt)
t_nu = [0]  # 各計算ステップの時刻を保持するリスト
ca_nu = [ca0]  # 各計算ステップの濃度を保持するリスト
for n in range(n):
    t_next = t_nu[-1] + dt  # 次の時刻を算出
    ca_next = ca_nu[-1] - k*ca_nu[-1]*dt  # 次の時刻の濃度を算出
    t_nu.append(t_next)
    ca_nu.append(ca_next)

plt.plot(t_an, ca_an, label="analytical")
plt.plot(t_nu, ca_nu, label="numerical dt = 30")
plt.xlabel("Time [s]")
plt.ylabel("Concentration of A [mol/m3]")
plt.legend()
plt.show()
