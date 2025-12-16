#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.size": 12
})

save_figs = {1,2}
show_figs = {}

redis_baseline=1143118.38
# Could make a latency graph for redis

# Runtime, seconds.
# 1 core, 2 cores, ...
gapbs_baseline = np.array([2.62143, 1.85464, 1.72839, 1.76645])
# Fio 8MB seq Read  (1 core, 2 cores) IOPS
fio_baseline_readseq = np.array([111.41, 111.40])
# Fio 8MB random read and write, MB/s
fio_baseline_randread = 916
fio_baseline_randwrite = 894
# MB/s
stream_baseline_read = np.array([14065.046151, 13514.224174, 12922.793596])
stream_baseline_write = np.array([9634.421614, 10012.542420, 9851.005046])

# 2 cores of fio
redis_vs_fio2_readseq = 1137061.38
# 1 core of fio
# gapbs: 1 core, 2 cores, 3 cores.
gapbs_vs_fio1_readseq = np.array([2.81547, 2.00798, 1.95977])

stream_read_vs_fio1_read = np.array([13726.920156, 12584.818467, 11663.958699])
stream_read_vs_fio1_write = np.array([13927.724184, 13047.475195, 12227.381106])
stream_write_vs_fio1_read = np.array([8941.091816, 9407.626524, 9290.608707])
stream_write_vs_fio1_write = np.array([8838.485374, 9199.449559, 9106.378186])

fio1_read_vs_stream_read = np.array([907, 870, 851])
fio1_write_vs_stream_read = np.array([886, 853, 842])
fio1_read_vs_stream_write = np.array([905, 891, 870])
fio1_write_vs_stream_write = np.array([887, 879, 866])

degr_redis_fio2_readseq = redis_vs_fio2_readseq / redis_baseline
degr_gapbs_fio1_readseq = gapbs_vs_fio1_readseq / gapbs_baseline[:3]
#degr_gapbs_fio1_readseq = gapbs_baseline[:3] / gapbs_vs_fio1_readseq

# [stream, fio]
degr_stream_read_fio_read = [stream_baseline_read / stream_read_vs_fio1_read, fio_baseline_randread / fio1_read_vs_stream_read]
degr_stream_read_fio_write = [stream_baseline_read / stream_read_vs_fio1_write, fio_baseline_randwrite / fio1_write_vs_stream_read]
degr_stream_write_fio_read = [stream_baseline_write / stream_write_vs_fio1_read, fio_baseline_randread / fio1_read_vs_stream_write]
degr_stream_write_fio_write = [stream_baseline_write / stream_write_vs_fio1_write, fio_baseline_randwrite / fio1_write_vs_stream_write]


def save_show(n):
    if n in save_figs:
        plt.savefig(f'figures/fig{n}.pgf')
        plt.savefig(f'figures/fig{n}.png', dpi=600)
    if n in show_figs:
        plt.show(block=max(show_figs)==n)

if 1 in save_figs or 1 in show_figs:
    plt.figure()
    plt.plot(range(1, 4), degr_gapbs_fio1_readseq, marker='o', label='Colocated with fio (P2M-Read, 1 core)')
    plt.axhline(1, label='Isolated', linestyle='--', color='k')
    plt.ylim([0,1.2])
    plt.ylabel('GAPBS (C2M-Read) Degradation\n(colocated runtime / isolated runtime)')
    plt.xlabel('GAPBS Cores')
    plt.xticks([1,2,3])
#    plt.xticks(np.linspace(1, 3, 11), minor=True)
#    plt.grid(which='major', alpha=0.8)
#    plt.grid(which='minor', alpha=0.3)
    plt.tight_layout()
    plt.grid()
    plt.legend()
    save_show(1)

if 2 in save_figs or 2 in show_figs:
    fig2_data = np.array([[degr_stream_read_fio_write, degr_stream_read_fio_read], [degr_stream_write_fio_write, degr_stream_write_fio_read]])
#   plt.figure()
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    for i in range(2):
        for j in range(2):
            ax = axs[i][j]
            data = fig2_data[i,j]
            ax.plot(range(1,4), data[0], label='C2M Traffic', marker='o')
            ax.plot(range(1,4), data[1], label='P2M Traffic', marker='s')
            ax.set_ylabel("Degradation\n(isolated / colocated)")
            ax.set_xlabel("No. of C2M Cores")
            ax.grid()
            ax.set_xticks(range(1,4))
            ax.set_ylim([1,1.2])
        c2m_dir = ['Read', 'ReadWrite'][i]
        p2m_dir = ['Write', 'Read'][i]
        ax = axs[i][0]
        ax.annotate(f"C2M-{c2m_dir}", xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - 5, 0),
        xycoords=ax.yaxis.label, textcoords='offset points',
        size='large', ha='right', va='center', rotation=90)
        ax = axs[0][i]
        ax.annotate(f"P2M-{p2m_dir}", xy=(0.5, 1), xytext=(0, 5),
                xycoords='axes fraction', textcoords='offset points',
                size='large', ha='center', va='baseline')
    fig.legend(*plt.gca().get_legend_handles_labels(), loc = 'upper center', ncol = 2)
    fig.tight_layout()
    fig.subplots_adjust(top=0.85)
    save_show(2)
