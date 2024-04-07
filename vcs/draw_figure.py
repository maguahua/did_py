import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

matplotlib.use('TkAgg')
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文显示字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号'-'显示为方块的问题


def draw_line_graph(filename, title, index_y, file_title, xlabel=None, ylabel=None):
    df = pd.read_csv(filename)
    plt.plot(df.index, df[index_y], color='#928395')  # 绘制线图，指定颜色为橙色

    plt.title(title)

    if xlabel:
        plt.xlabel(xlabel)  # 设置横坐标标签为传入的值
    else:
        plt.xlabel('Index')  # 默认为 'Index'（如果未指定）

    if ylabel:
        plt.ylabel(ylabel)  # 设置纵坐标标签为传入的值
    else:
        plt.ylabel(index_y)  # 默认为 index_y 的列名（如果未指定）

    # 将图像保存为SVG格式
    plt.savefig(file_title + '.svg')


# 中文标签
draw_line_graph('doc/VC validation time.csv', 'VC验证时间', 'elapse_time', 'VC验证时间', '次数', '时间')
# 英文标签
draw_line_graph('doc/VC validation time.csv', 'VC validation time', 'elapse_time', 'VC validation time', 'cnt', 'time')
