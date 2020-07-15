# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
plt.style.use('ggplot')

# パラメータ
rho = 8000.0  # ステンレス密度 [kg/m3]
k = 16.0  # ステンレス熱伝導率 [W/m/w]
c = 500.0  # ステンレス比熱容量 [J/kg/K]
alpha = k/rho/c  # 温度拡散率
radius = 0.015  # ステンレス棒の半径 [m]
calc_time = 50  # 計算時間 [s]

t0 = 50.0  # 初期温度 [℃]
t1 = 0.0  # 冷水温度 [℃]

num_r_section = 10  # 位置方向分割数 [-]
num_time_step = 500  # 時間方向分割数 [s]
dr = radius/num_r_section  # 位置方向刻み幅 [m]
dt = calc_time/num_time_step  # 時間刻み幅 [s]


# 差分式
def calc_tnext(t_now, i, dr, dt, alpha):
    """
    現在時刻の温度を引数とし、次の時刻の温度を返す
    (注意点)
    1. 差分式に現れる 1/r の r については現位置iと次の位置i+1の平均とした
    2. i=0の点を計算するときに i=-1 の項が現れるが、円柱の対称性からi=-1はi=1と同じとみなした
    """
    r = (dr*i + dr*(i+1))/2.0  # 現位置と次の位置の平均
    if i == 0:  # i=-1の温度は存在しないが円柱の対称性からi=-1はi=1と同じとみなす
        tnext = t_now[i] + dt*alpha * ((t_now[i+1] - 2.0*t_now[i] + t_now[i+1])/(dr**2)
                                       + 1.0/r * (t_now[i+1] - t_now[i])/dr)
    else:
        tnext = t_now[i] + dt*alpha * ((t_now[i+1] - 2.0*t_now[i] + t_now[i-1])/(dr**2)
                                       + 1.0/r * (t_now[i+1] - t_now[i])/dr)
    return tnext


# データ収容するリストの準備
data = []


# 初期条件をdataに追加 分割数+1が節点(node)数なので注意
data.append([t0]*(num_r_section+1))


# 計算
for j in range(1, num_time_step+1):
    tnext_list = []
    for i in range(0, num_r_section+1-1):
        tnext = calc_tnext(data[-1], i, dr, dt, alpha)
        tnext_list.append(tnext)
    tnext_list.append(t1)  # 境界条件 t=t1 at r=R を追加
    data.append(tnext_list)


# 結果表示
r = [dr*i for i in range(0, num_r_section+1)]
plt.plot(r, data[0], label="t=0")
plt.plot(r, data[int(num_time_step*0.1)], label="t= 5[s]")
plt.plot(r, data[int(num_time_step*0.2)], label="t=10[s]")
plt.plot(r, data[int(num_time_step*0.4)], label="t=20[s]")
plt.plot(r, data[int(num_time_step*0.8)], label="t=40[s]")
plt.xlabel("r [m]")
plt.ylabel("Temperature [℃]")
plt.legend()
plt.show()
