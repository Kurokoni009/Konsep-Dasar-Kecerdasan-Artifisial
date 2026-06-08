import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file = "RT_IOT2022.csv"
df = pd.read_csv(file)

SAMPLE_SIZE = 5000
if SAMPLE_SIZE is not None and SAMPLE_SIZE < len(df):
    df = df.sample(n=SAMPLE_SIZE, random_state=42).reset_index(drop=True)

fitur = [
    "flow_duration",
    "fwd_pkts_tot",
    "bwd_pkts_tot",
    "fwd_data_pkts_tot",
    "bwd_data_pkts_tot",
    "fwd_pkts_per_sec",
    "bwd_pkts_per_sec",
    "flow_pkts_per_sec",
    "down_up_ratio",
    "flow_SYN_flag_count",
    "flow_RST_flag_count",
    "flow_ACK_flag_count",
    "fwd_pkts_payload.tot",
    "bwd_pkts_payload.tot",
    "flow_pkts_payload.tot",
    "payload_bytes_per_second",
    "fwd_init_window_size",
    "bwd_init_window_size",
    "fwd_last_window_size"
]

label_asli = "Attack_type"
X_asli = df[fitur].replace([np.inf, -np.inf], np.nan).fillna(0).values.astype(float)

rata_rata = X_asli.mean(axis=0)
standar_deviasi = X_asli.std(axis=0)
standar_deviasi[standar_deviasi == 0] = 1
X = (X_asli - rata_rata) / standar_deviasi

def hitung_jarak(data, centroid, metode, p=3):
    if metode == "euclidean":
        return np.sqrt(np.sum((data - centroid) ** 2, axis=1))

    elif metode == "manhattan":
        return np.sum(np.abs(data - centroid), axis=1)

    elif metode == "minkowski":
        return np.sum(np.abs(data - centroid) ** p, axis=1) ** (1 / p)

    else:
        raise ValueError("Metode jarak tidak dikenali")

def kmeans_threshold(X, k, metode, threshold=0.001, max_iter=100):
    np.random.seed(42)

    indeks_awal = np.random.choice(len(X), k, replace=False)
    centroid = X[indeks_awal]

    for iterasi in range(1, max_iter + 1):
        semua_jarak = []

        for c in centroid:
            semua_jarak.append(hitung_jarak(X, c, metode))

        semua_jarak = np.array(semua_jarak).T
        label = np.argmin(semua_jarak, axis=1)

        centroid_baru = []
        for i in range(k):
            data_cluster = X[label == i]
            if len(data_cluster) > 0:
                centroid_baru.append(data_cluster.mean(axis=0))
            else:
                centroid_baru.append(centroid[i])

        centroid_baru = np.array(centroid_baru)

        delta = np.sqrt(np.sum((centroid_baru - centroid) ** 2))
        print(f"Iterasi {iterasi} | Delta = {delta:.6f}")

        if delta <= threshold:
            break

        centroid = centroid_baru

    return label, centroid, iterasi

def beri_nama_cluster(label):
    df_temp = df.copy()
    df_temp["Cluster"] = label

    kolom_skor = [
        "flow_pkts_per_sec",
        "payload_bytes_per_second",
        "flow_pkts_payload.tot",
        "flow_SYN_flag_count",
        "flow_RST_flag_count",
        "flow_ACK_flag_count"
    ]

    data_skor = df_temp[kolom_skor].replace([np.inf, -np.inf], np.nan).fillna(0).values.astype(float)
    std_skor = data_skor.std(axis=0)
    std_skor[std_skor == 0] = 1
    data_skor = (data_skor - data_skor.mean(axis=0)) / std_skor
    df_temp["Skor_Intensitas_Trafik"] = data_skor.mean(axis=1)

    rata_skor = df_temp.groupby("Cluster")["Skor_Intensitas_Trafik"].mean()
    urutan = rata_skor.sort_values(ascending=True).index.tolist()

    nama_cluster = {
        urutan[0]: "Trafik Intensitas Rendah",
        urutan[1]: "Trafik Intensitas Sedang",
        urutan[2]: "Trafik Intensitas Tinggi"
    }

    return nama_cluster

k = 3
threshold = 0.001
metode_jarak = ["euclidean", "manhattan", "minkowski"]

plt.figure(figsize=(15, 5))

for idx, metode in enumerate(metode_jarak, start=1):
    
    print("\n==============================")
    print("K-MEANS DENGAN THRESHOLD")
    print("Dataset      : RT-IoT2022 asli")
    print("Metode Jarak :", metode)
    print("Jumlah K     :", k)
    print("Threshold    :", threshold)
    print("Jumlah Data  :", len(df))

    label, centroid, iterasi = kmeans_threshold(X, k, metode, threshold)
    nama_cluster = beri_nama_cluster(label)

    print("\nHasil Akhir")
    print("Iterasi berhenti pada:", iterasi)

    for i in range(k):
        kategori = nama_cluster[i]
        jumlah_data = np.sum(label == i)

        print(f"\nCluster {i} - {kategori}")
        print("Jumlah data:", jumlah_data)

        if label_asli in df.columns:
            print("Komposisi Attack_type terbanyak:")
            print(df.loc[label == i, label_asli].value_counts().head(5).to_string())

    plt.subplot(1, 3, idx)
    plt.scatter(
        np.log1p(df["flow_duration"]),
        np.log1p(df["flow_pkts_per_sec"].replace([np.inf, -np.inf], 0)),
        c=label,
        s=10
    )

    plt.title(metode.capitalize())
    plt.xlabel("log(1 + flow_duration)")
    plt.ylabel("log(1 + flow_pkts_per_sec)")

plt.suptitle("K-Means dengan Threshold - Dataset RT-IoT2022 Asli")
plt.tight_layout()
plt.savefig("grafik_kmeans_threshold.png", dpi=200)
plt.show()
