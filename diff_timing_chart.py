import matplotlib.pyplot as plt
import pandas as pd
import glob

class DIFF_TIMING_CHART:
    # CSVにあわせて設定 のちにYAMLにうつすか
    TRUE_CSV = glob.glob('TRUE*.csv')[0]
    INPUT_CSV = glob.glob('*.csv')[0]
    HEADER_INDEX = 3
    STARTING_LABEL = ' hoge1'

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

        return df.index[starting_idex]

    def make_chart(self):
        # read csv file
        df = pd.read_csv(self.INPUT_CSV, index_col=0, header=self.HEADER_INDEX, encoding='shift_jis')
        x_starting = self.get_offset(df, self.STARTING_LABEL)

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
            axis[i].set_xlim(x_starting, x_max)                     # X軸を起点ラベルの変化タイミングにする
        # 縦方向に、間隔を密にグラフをレイアウト
        fig.subplots_adjust(hspace=0.1)
        # メモリの重なりをなくす
        plt.tight_layout()

        # グラフ表示
        plt.show()



if __name__ == "__main__":
    dtc = DIFF_TIMING_CHART()
    dtc.make_chart()
