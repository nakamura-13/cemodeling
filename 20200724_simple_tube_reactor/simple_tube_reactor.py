# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# パラメータ
tube_length = 1.0  # 反応管長さ [m]
u = 0.1  # 空塔速度 [m/s]
k = 0.4  # 反応速度定数 [1/s]
c0 = 1.0  # 反応ガス入口濃度 [mol/m3]

num_z_section = 50  # 位置方向分割数 [-]
dz = tube_length/num_z_section  # 位置方向刻み幅 [m]
calc_time = 10  # 計算時間
num_t_section = 100  # 時間方向分割数 [-]
dt = calc_time/num_t_section  # 時間方向刻み幅 [s]


# 差分式
def calc_cnext(c_now, i, dz, dt, u, k):
    """
    現在時刻の濃度を引数とし、次の時刻の温度を返す
    """
    c = (c_now[i] + c_now[i-1])/2.0  # 現位置と1つ前の位置の濃度の平均
    c_next = c_now[i] - u*dt/dz*(c_now[i] - c_now[i-1]) - k*dt*c
    return c_next


# データ収容するリストの準備
data = []


# 初期条件をdataに追加 分割数+1が節点(node)数なので注意
data.append([0.0]*(num_z_section+1))


# 計算
for j in range(1, num_t_section+1):  # t=0の次から最後の時刻まで
    cnext_list = []  # 次の時刻の濃度分布を収容するリスト
    cnext_list.append(c0)  # 境界条件 c=c0 at z=0 を追加
    for i in range(1, num_z_section+1):  # z=0の次から出口まで
        cnext = calc_cnext(data[-1], i, dz, dt, u, k)
        cnext_list.append(cnext)
    data.append(cnext_list)


# 結果表示
## 数値解
z = [dz*i for i in range(0, num_z_section+1)]
plt.scatter(z, data[int(num_t_section*0.05)], label="t= 0.5[s]")
plt.scatter(z, data[int(num_t_section*0.2)], label="t= 2[s]")
plt.scatter(z, data[int(num_t_section*0.4)], label="t= 4[s]")
plt.scatter(z, data[int(num_t_section*1)], label="t=10[s]")
plt.xlabel("z [m]")
plt.ylabel("Concentration [mol/m3]")

## 解析解
z = np.linspace(0, tube_length, 40)
c = c0 * np.exp(-k*z/u)
plt.plot(z, c, label="t=∞ analytical")

plt.legend()
plt.show()
