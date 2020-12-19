import matplotlib.pyplot as plt
import pandas as pd
# CSVにあわせて設定 のちにYAMLにうつすか
HEADER_INDEX = 3

# read csv file
df = pd.read_csv('sample.csv', index_col=0, header=HEADER_INDEX, encoding='shift_jis')

# グラフ情報
GRAPHNUM = len(df.columns)  # 数
LABEL = df.columns.values   # 種類

## X軸情報(X軸共通化のため別途定義)
x = df.index.values

plt.rcParams['xtick.direction'] = 'in' #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
plt.rcParams['ytick.direction'] = 'in' #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
# データプロットと表示レイアウト
fig, axis = plt.subplots(GRAPHNUM, sharex=True)  # 複数グラフをx軸を共有して表示
for i, d in enumerate(df.T.values):
    axis[i].plot(x, d, drawstyle='steps', label=LABEL[i])   # データをステップでプロット
    axis[i].spines['right'].set_visible(False)              # 右枠非表示
    axis[i].spines['top'].set_visible(False)                # 上枠非表示
    axis[i].legend(loc=2)                                   # 凡例表示
    axis[i].grid(linestyle='-')                             # グリッド線表示
    x_min, x_max = axis[i].get_xlim()
    axis[i].set_xlim(0, x_max)                              # X軸を0起点にする
# 縦方向に、間隔を密にグラフをレイアウト
fig.subplots_adjust(hspace=0.1)
# メモリの重なりをなくす
plt.tight_layout()

# グラフ表示
plt.show()