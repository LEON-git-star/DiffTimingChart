import matplotlib.pyplot as plt
import pandas as pd
import glob
import numpy as np
import scipy.signal as sig
import yaml # pip install yaml
import os
import math

class DiffTimingChart:
    def __init__(self):
        # Setting from yaml config
        try:
            self.yd = yaml.safe_load(open('diff_timing_chart.yaml', encoding='utf-8'))
        except:
            print('ERR: Config YAML file not found.')
            exit(0)
        self.input_folder = self.yd['path']['input_folder']
        self.input_file = self.yd['path']['input_file']
        self.output_file = self.yd['path']['output']
        try:
            self.TRUE_CSV = glob.glob(os.path.join(self.input_folder['true_f'], self.input_file['true_f']))[0]
        except:
            print('ERR: Wrong TRUE file path.')
            exit(0)
        try:
            self.INPUT_CSV = glob.glob(os.path.join(self.input_folder['target_f'], self.input_file['target_f']))[0]
        except:
            print('ERR: Wrong target file path.')
            exit(0)
        # ヘッダー行（データ依存）
        self.HEADER_INDEX = self.yd['header_index']
        self.graph_settings()

    def graph_settings(self):
        # 日本語用フォント設定
        plt.rcParams['font.family'] = 'sans-serif'
        plt.rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']
        plt.rcParams['xtick.direction'] = 'in'
        plt.rcParams['ytick.direction'] = 'in'

    def make_chart(self):
        # read csv file
        df = pd.read_csv(self.INPUT_CSV, index_col=0, header=self.HEADER_INDEX, encoding='utf-8')
        df_true = pd.read_csv(self.TRUE_CSV, index_col=0, header=self.HEADER_INDEX, encoding='utf-8')
        # 信号名ラベル
        label = df.columns.values
        label_true = df_true.columns.values
        # 相関係数計算
        self.calc_corrcoef(df, label, df_true, label_true)
    
    def calc_corrcoef(self, df_input, label_input, df_true, label_true):
        label_input_list = list(label_input)
        label_true_list = list(label_true)
        # 数が多い方をインデックスリストとする
        index_list = label_input_list if len(label_input_list) > len(label_true_list) else label_true_list
        
        # 共通ラベル
        common_labels = list(sorted(set(label_input_list) & set(label_true_list), key=index_list.index))
        fig, axis = plt.subplots(len(common_labels), sharex=True)  # 複数グラフをx軸を共有して表示
        
        weak_corr = []
        for i, label in enumerate(common_labels):
            sig_true = df_true[label]
            sig_input = df_input[label]
            # 畳み込み積分
            corr = np.correlate(sig_true, sig_input, 'full')
            # ラグ
            estimated_delay = corr.argmax() - (len(sig_input) - 1)
            estimated_delay = -estimated_delay if estimated_delay >= 0 else estimated_delay
            # with lag
            sig_true_lag = sig_true[estimated_delay:] if estimated_delay >= 0 else sig_true[:estimated_delay]
            sig_input_lag = sig_input.shift(estimated_delay).dropna()
            # 畳み込み積分（ラグ考慮）
            #corr_lag = np.correlate(sig_true_lag, sig_input_lag, 'full')
            corr2 = np.corrcoef(sig_true_lag, sig_input_lag)[0,1]
            """
            print(label)
            print("correlation coefficient is " + "{:.1f}".format(corr2))
            print("estimated delay is " + str(estimated_delay))
            """
            if corr2 <= 0.5 or math.isnan(corr2):
                weak_corr.append(label)
                
            axis[i].plot(corr, label=label + ' @', color = 'gray') # データをステップでプロット
            #axis[i].plot(corr_lag, label=label + ' @' + 'ラグ考慮', color = 'orange', ls="-.") # データをステップでプロット
            axis[i].legend(loc=2) # 凡例表示
        
        print("|相関係数|＝0.2～0.4 弱い相関")
        with open(self.output_file, mode='w', encoding='utf-8') as f:
            f.write('\n'.join(weak_corr))
        plt.show()

if __name__ == "__main__":
    dtc = DiffTimingChart()
    dtc.make_chart()
    
