import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np


class DiffTimingChart:
    # ヘッダー行（データ依存）
    HEADER_INDEX = 3
    # 起点ラベル（この信号に変化があった直前にオフセットを付ける）
    STARTING_LABEL = 'エラー１'

    def __init__(self):
        # CSVにあわせて設定 のちにYAMLにうつすか？
        # 「開く」で正解値パス、比較対象パスを選ばせるか？
        self.TRUE_CSV = glob.glob('TRUE*.csv')[0]
        self.INPUT_CSV = glob.glob('*.csv')[0]

    def get_offset(self, df_all_data, starting_label):
        '''
        Get the offset time when the value of the starting label changes from the previous value.
        '''
        df = df_all_data[starting_label]
        df_val = df.values

        prev_val = df_val[0]
        for i, d in enumerate(df_val):
            if d != prev_val:
                starting_idex = i
                break
            prev_val = d

        return df.index[starting_idex-1]

    def make_chart(self):
        # read csv file
        df = pd.read_csv(self.INPUT_CSV, index_col=0, header=self.HEADER_INDEX, encoding='utf-8')
        df_true = pd.read_csv(self.TRUE_CSV, index_col=0, header=self.HEADER_INDEX, encoding='utf-8')
        # 信号名ラベル
        label = df.columns.values
        label_true = df_true.columns.values
        # 相関係数計算
        self.calc_corrcoef(df, label, df_true, label_true)

        # 以降、描画系、まとめるなりもう少し何とかするか？
        # グラフ数（多い方にあわせる）
        graph_num = len(df.columns) if len(df.columns) > len(df_true.columns) else len(df_true.columns)

        # 始点オフセット
        x_starting = self.get_offset(df, self.STARTING_LABEL)
        x_starting_true = self.get_offset(df_true, self.STARTING_LABEL)
        ## X軸情報(X軸共通化のため別途定義)
        x = df.index.values
        x_true = df_true.index.values

        # 日本語用フォント設定
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

        plt.rcParams['xtick.direction'] = 'in' #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
        plt.rcParams['ytick.direction'] = 'in' #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
        # データプロットと表示レイアウト
        fig, axis = plt.subplots(graph_num, sharex=True)  # 複数グラフをx軸を共有して表示
        for i, d in enumerate(df.T.values):
            axis[i].plot(x, d, drawstyle='steps', label=label[i] + ' @' + self.INPUT_CSV)   # データをステップでプロット
            axis[i].spines['right'].set_visible(False)              # 右枠非表示
            axis[i].spines['top'].set_visible(False)                # 上枠非表示
            axis[i].legend(loc=2)                                   # 凡例表示
            axis[i].grid(linestyle='-')                             # グリッド線表示
            x_min, x_max = axis[i].get_xlim()
            axis[i].set_xlim(x_starting, x_max)                     # X軸を起点ラベルの変化タイミングにする
        
        for i, d in enumerate(df_true.T.values):
            axis[i].plot(x_true, d, drawstyle='steps', label=label_true[i] + ' @' + self.TRUE_CSV) # データをステップでプロット
            x_min, x_max = axis[i].get_xlim()
            axis[i].set_xlim(x_starting_true, x_max)                # X軸を起点ラベルの変化タイミングにする
            axis[i].legend(loc=2)                                   # 凡例表示

        # 縦方向に、間隔を密にグラフをレイアウト
        fig.subplots_adjust(hspace=0.1)
        # メモリの重なりをなくす
        plt.tight_layout()
        # グラフ表示
        plt.show()
    
    def calc_corrcoef(self, df_input, label_input, df_true, label_true):
        label_input_list = list(label_input)
        label_true_list = list(label_true)
        # 数が多い方をインデックスリストとする
        index_list = label_input_list if len(label_input_list) > len(label_true_list) else label_true_list
        # 共通ラベル
        common_labels = list(sorted(set(label_input_list) & set(label_true_list), key=index_list.index))
        for label in common_labels:
            print(np.corrcoef(df_input[label], df_true[label]))


if __name__ == "__main__":
    dtc = DiffTimingChart()
    dtc.make_chart()
    
