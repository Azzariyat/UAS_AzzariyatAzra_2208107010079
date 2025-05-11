import requests
import streamlit as st
from typing import List



st.set_page_config(page_title="Email Generator", page_icon="✉️")
st.title("📨 Email Generator Otomatis dengan Gemini")

st.markdown("Masukkan detail email yang ingin kamu buat:")

recipient = st.text_input("Nama Penerima")
subject_options = [
    "Permohonan Izin Tidak Hadir Kuliah",
    "Permintaan Surat Rekomendasi",
    "Pengajuan Tugas atau Proyek",
    "Permohonan Revisi Nilai",
    "Permintaan Jadwal Bimbingan",
    "Undangan Acara Kampus",
    "Permintaan Informasi Akademik",
    "Pengajuan Beasiswa",
    "Laporan Kegiatan Organisasi",
    "Pengajuan Magang atau Penelitian",
    "Lainnya"
]

selected_subject = st.selectbox("Subjek Email", subject_options)

if selected_subject == "Lainnya":
    custom_subject = st.text_input("Tulis Subjek Email Anda")
    subject = custom_subject
else:
    subject = selected_subject
category = st.selectbox("Kategori Email", [
    "Akademik",
    "Administrasi",
    "Organisasi Kemahasiswaan",
    "Keuangan / Beasiswa",
    "Magang & Penelitian",
    "Acara Kampus",
    "Layanan Umum / Fasilitas"
])
tone = st.selectbox("Status Email", ["Formal", "Santai", "Serius", "Friendly"])
language = st.selectbox("Bahasa", ["Indonesia", "English"])
urgency = st.radio("Tingkat Urgensi", ["Biasa", "Segera", "Sangat Mendesak"])

points = st.text_area("Isi Email").split("\n")
example_email = st.text_area("Contoh email sebelumnya (opsional)")

if st.button("Buat Email"):
    payload = {
        "category": category,
        "recipient": recipient,
        "subject": subject,
        "tone": tone,
        "language": language,
        "urgency_level": urgency,
        "points": [p.strip() for p in points if p.strip()],
        "example_email": example_email or None
    }

    with st.spinner("Membuat email..."):
        res = requests.post("http://localhost:8000/generate/", json=payload)
        if res.status_code == 200:
            st.success("Email berhasil dibuat:")
            st.write(res.json()["generated_email"])
        else:
            st.error(f"Gagal: {res.json()['detail']}")