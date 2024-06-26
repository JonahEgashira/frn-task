import mne
import numpy as np
import matplotlib.pyplot as plt
import os


def load_and_preprocess_data(filename):
    # データのロード
    epochs = mne.read_epochs(filename, preload=True)
    epochs.filter(l_freq=None, h_freq=30)
    return epochs


def calculate_frn(epochs, ch_list):
    # 正解と誤答のEpochsを分ける
    epochs_resp_cor = epochs["Correct"]
    epochs_resp_wro = epochs["Incorrect"]

    # チャンネル名を指定
    epochs_resp_cor.pick(ch_list)
    epochs_resp_wro.pick(ch_list)

    # 平均を取得
    evoked_resp_cor = epochs_resp_cor.average()
    evoked_resp_wro = epochs_resp_wro.average()

    print(f"Evoke Correct Response: {evoked_resp_cor.data}")
    print(f"Evoke Incorrect Response: {evoked_resp_wro.data}")

    print(f"Correct Response: {evoked_resp_cor}")
    print(f"Incorrect Response: {evoked_resp_wro}")

    return evoked_resp_cor, evoked_resp_wro


def plot_frn(evoked_resp_cor, evoked_resp_wro, ch_name, large_scale=False):
    # チャンネルを選択
    print(f"Channel Name: {evoked_resp_wro.ch_names}")

    ch_index = evoked_resp_wro.ch_names.index(ch_name)
    time_ms = evoked_resp_wro.times * 1000

    print(f"time_ms: {time_ms}")

    # ERNをプロット
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(
        time_ms, evoked_resp_cor.data[ch_index], label="Correct Response", color="blue"
    )
    ax.plot(
        time_ms, evoked_resp_wro.data[ch_index], label="Incorrect Response", color="red"
    )

    # プロットの設定
    ax.set_title(f"FRN at {ch_name}")
    ax.set_xlabel("Time (ms)")

    ax.set_ylabel("Amplitude (μV)")
    ax.legend()
    ax.grid(True)

    # 0秒の位置に縦線を追加
    ax.axvline(x=0, color="black", linestyle="--", linewidth=1)

    # 横軸のScaleを設定
    tmin = -300
    tmax = 801
    t_step = 100

    if large_scale:
        tmin = -2000
        tmax = 4001
        t_step = 500
    else:
        tmin = -300
        tmax = 801
        t_step = 100

    # 縦軸の範囲を設定
    ax.set_ylim(-10, 10)

    # 横軸の範囲を設定
    ax.set_xlim(tmin, tmax)

    # 横軸の目盛の間隔を設定
    ax.set_xticks(np.arange(tmin, tmax, t_step))

    plt.show()


# メイン関数
if __name__ == "__main__":
    data_dir = "./epoch"
    folders = [os.path.join(data_dir, folder) for folder in os.listdir(data_dir)]
    folders = [folder for folder in folders if os.path.isdir(folder)]
    latest_folder = max(folders, key=os.path.getmtime)
    
    print(f"Latest folder: {latest_folder}")
    file_path = os.path.join(latest_folder, "epoch.fif")

    epochs = load_and_preprocess_data(file_path)

    print("Epochs Info:", epochs.info)

    ch_list = ["Cz"]

    evoked_resp_cor, evoked_resp_wro = calculate_frn(epochs, ch_list)
    plot_frn(evoked_resp_cor, evoked_resp_wro, "Cz", large_scale=False)
