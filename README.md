# Gebang Thunder Dashboard — *Ready to Take Off* 🚀

> **Tim:** Gebang Thunder · **Karya:** Ready to Take Off  
> **Kompetisi Data Analytics 2026**

---

## Deskripsi

Dashboard analitik data berbasis **Streamlit** untuk kompetisi, menampilkan:
- **Home** — Hero section & overview proyek
- **Executive Summary** — Insight utama & visualisasi data
- **GT Lab** — Projection & what-if analysis (Regression, Classification, Clustering)
- **Ask to Gemini** — Conversational AI grounded ke dataset

---

## Tech Stack

| Layer | Tools |
|---|---|
| Core | Python 3.11, Streamlit 1.37 |
| Data | Pandas 2.2, NumPy 1.26, Scikit-learn 1.5 |
| Visualisasi | Plotly 5.23 |
| UI Components | streamlit-shadcn-ui, streamlit-lottie |
| AI | Google Gemini API (gemini-flash) |
| Deployment | Streamlit Community Cloud |

---

## Instalasi & Setup

### 1. Clone repo

```bash
git clone https://github.com/<org>/gebang-thunder-dashboard.git
cd gebang-thunder-dashboard
```

### 2. Buat environment Conda

```bash
conda env create -f environment.yml
conda activate gt-dashboard-env
```

### 3. Setup secrets (Gemini API keys)

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# Edit secrets.toml, isi API key Gemini milik masing-masing anggota tim
```

### 4. Jalankan aplikasi

```bash
streamlit run app.py
```

Akses di: `http://localhost:8501`

---

## Struktur Repository

```
gebang-thunder-dashboard/
├── .streamlit/          # Streamlit config & secrets
├── app.py               # Entrypoint + query_params router
├── requirements.txt     # Untuk Streamlit Cloud deployment
├── environment.yml     # Conda environment (gt-dashboard-env)
├── assets/              # Icons (SVG), images, fonts, animations
├── config/              # Settings, constants, theme tokens
├── data/                # raw/, processed/, sample/
├── models/              # Model artifacts
├── pages/               # executive_summary/, gt_lab/, ask_gemini/
├── components/          # Reusable UI components
├── services/            # CSV, Gemini, ML, cache, export services
├── utils/               # Formatter, session, key_pool, logger, dll.
├── styles/              # Custom CSS files
└── tests/               # Unit tests
```

---

## Routing

Dashboard menggunakan **satu domain** dengan `st.query_params` untuk navigasi:

| URL | Halaman |
|---|---|
| `/?page=home` | Home |
| `/?page=executive_summary` | Executive Summary |
| `/?page=gt_lab` | GT Lab |
| `/?page=ask_gemini` | Ask to Gemini |

---

## Deployment ke Streamlit Cloud

1. Push repo ke GitHub
2. Buka [share.streamlit.io](https://share.streamlit.io), connect repo
3. Tambahkan secrets Gemini API key di **Settings → Secrets** (format sama dengan `secrets.toml.example`)
4. Deploy — akses via link yang diberikan Streamlit

---

## Lisensi

Proyek ini dibuat untuk keperluan kompetisi. Hak cipta © 2026 Tim Gebang Thunder.
