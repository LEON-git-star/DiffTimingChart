import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np

class DIFF_TIMING_CHART:
    # CSVにあわせて設定 のちにYAMLにうつすか？
    # 「開く」で正解値パス、比較対象パスを選ばせるか？
    TRUE_CSV = glob.glob('TRUE*.csv')[0]
    INPUT_CSV = glob.glob('*.csv')[0]
    HEADER_INDEX = 3
    STARTING_LABEL = 'hoge1'

    def get_offset(self, df_all_data, starting_label):
        '''
        Get the offset time when the value of the starting label changes from the previous value.
        '''
        df = df_all_data[starting_label]
        df_val = df.values
        #starting_idex = [i for i, d in enumerate(df_val) if d > 0][0]
        prev_val = df_val[0]
        for i, d in enumerate(df_val):
            if d != prev_val:
                starting_idex = i
                break
            prev_val = d

        return df.index[starting_idex-1]

    def make_chart(self):
        # read csv file
        df = pd.read_csv(self.INPUT_CSV, index_col=0, header=self.HEADER_INDEX, encoding='shift_jis')
        df_true = pd.read_csv(self.TRUE_CSV, index_col=0, header=self.HEADER_INDEX, encoding='shift_jis')
        # 信号名ラベル
        LABEL = df.columns.values   # 種類
        LABEL_TRUE = df_true.columns.values   # 種類
        # 相関係数計算
        self.calc_corrcoef(df, LABEL, df_true, LABEL_TRUE)

        # 以降、描画系、まとめるなりもう少し何とかするか？
        # グラフ情報
        GRAPHNUM = len(df.columns)  # 数

        # 始点オフセット
        x_starting = self.get_offset(df, self.STARTING_LABEL)
        x_starting_true = self.get_offset(df_true, self.STARTING_LABEL)
        ## X軸情報(X軸共通化のため別途定義)
        x = df.index.values
        x_true = df_true.index.values

        plt.rcParams['xtick.direction'] = 'in' #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
        plt.rcParams['ytick.direction'] = 'in' #x軸の目盛線が内向き('in')か外向き('out')か双方向か('inout')
        # データプロットと表示レイアウト
        fig, axis = plt.subplots(GRAPHNUM, sharex=True)  # 複数グラフをx軸を共有して表示
        for i, d in enumerate(df.T.values):
            axis[i].plot(x, d, drawstyle='steps', label=LABEL[i] + ' @' + self.INPUT_CSV)   # データをステップでプロット
            axis[i].spines['right'].set_visible(False)              # 右枠非表示
            axis[i].spines['top'].set_visible(False)                # 上枠非表示
            axis[i].legend(loc=2)                                   # 凡例表示
            axis[i].grid(linestyle='-')                             # グリッド線表示
            x_min, x_max = axis[i].get_xlim()
            axis[i].set_xlim(x_starting, x_max)                     # X軸を起点ラベルの変化タイミングにする
        
        for i, d in enumerate(df_true.T.values):
            axis[i].plot(x_true, d, drawstyle='steps', label=LABEL_TRUE[i] + ' @' + self.TRUE_CSV) # データをステップでプロット
            x_min, x_max = axis[i].get_xlim()
            axis[i].set_xlim(x_starting_true, x_max)                     # X軸を起点ラベルの変化タイミングにする
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
            #corrcoef = [np.corrcoef(i, t) for (i, t) in zip(df_input[label], df_true[label])]
            print(np.corrcoef(df_input[label], df_true[label]))


if __name__ == "__main__":
    dtc = DIFF_TIMING_CHART()
    dtc.make_chart()
    
