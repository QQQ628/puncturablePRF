import numpy as np
from matplotlib.pyplot import MultipleLocator
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Arial']  # 如果要显示中文字体,则在此处设为：SimHei
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

x = np.array([0,200,400,600,800,1000,1200,1400,1600,1800])
#Traditional= np.array([0,0.007,0.034,0.0563, 0.0769, 0.0817])
ourscheme = np.array([0.0015,0.0019,0.002,0.00206,0.002,0.0021,0.00219,0.0022,0.0025,0.0024])
#ourNetwork = np.array([2.0205495, 2.6509762, 3.1876223, 4.380781, 6.004548, 9.9298])

    # label在图示(legend)中显示。若为数学公式,则最好在字符串前后添加"$"符号
    # color：b:blue、g:green、r:red、c:cyan、m:magenta、y:yellow、k:black、w:white、、、
    # 线型：-  --   -.  :    ,
    # marker：.  ,   o   v    <    *    +    1
plt.figure(figsize=(10, 5))
plt.grid(linestyle="--")  # 设置背景网格线为虚线
ax = plt.gca()
ax.spines['top'].set_visible(False)  # 去掉上边框
ax.spines['right'].set_visible(False)  # 去掉右边框


#plt.plot(x, Traditional, marker='*', color="blue", label="Search Time of Traditional Scheme ", linewidth=1.5)
plt.plot(x, ourscheme, marker='o', color="red", label="Search Time of Our Scheme ", linewidth=1.5)
#plt.plot(x, ourNetwork, marker='o', color="red", label="ShuffleNet-style Network", linewidth=1.5)

group_labels = ['1000','2000','3000','4000','5000','6000','7000','8000','9000','10000']  # x轴刻度的标识
plt.xticks(x, group_labels, fontsize=12, fontweight='bold')  # 默认字体大小为10
plt.yticks(fontsize=12, fontweight='bold')
    # plt.title("example", fontsize=12, fontweight='bold')  # 默认字体大小为12
plt.xlabel("Amount of Record", fontsize=13, fontweight='bold')
plt.ylabel("Search Time (ms)", fontsize=13, fontweight='bold')


y_major_locator=MultipleLocator(0.0003)
    
ax.yaxis.set_major_locator(y_major_locator)#设置刻度
x_major_locator=MultipleLocator(200)
ax.xaxis.set_major_locator(x_major_locator)
plt.xlim(0, 1850)  # 设置x轴的范围
plt.ylim(0,0.0026)

    # plt.legend()          #显示各曲线的图例
plt.legend(loc=0, numpoints=1)
leg = plt.gca().get_legend()
ltext = leg.get_texts()
plt.setp(ltext, fontsize=12, fontweight='bold')  # 设置图例字体的大小和粗细

plt.savefig('./searchT.jpg', format='jpg')  # 建议保存为svg格式,再用inkscape转为矢量图emf后插入word中
#plt.show()
