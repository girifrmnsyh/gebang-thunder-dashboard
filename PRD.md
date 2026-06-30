# PRD — Gebang Thunder Dashboard "Ready to Take Off"

> **Tim:** Gebang Thunder · **Karya:** Ready to Take Off · **Tujuan:** Data Analytics Dashboard untuk Kompetisi

---

## 1. Role & Objective
Kamu bertindak sebagai **Professional UI/UX Developer** yang expert membangun **Data Analytics Dashboard**. Build dashboard berbasis CSV input yang **accessible**, **fully responsive** (Laptop/Tablet/Mobile), dan punya **strong differentiation** dari kompetitor — fokus pada visual impact & UX flow yang tidak generic.

**Design reference:** ui.shadcn.com, apple.com, notion.com — karakter minimalist, clean, futuristic.

---

## 2. Tech Stack
| Layer | Tools |
|---|---|
| Core | Python, Streamlit |
| EDA & Modelling | Pandas, NumPy, Scikit-learn |
| UI Components | streamlit-shadcn-ui |
| Visualisasi | Plotly Express |
| Animasi | streamlit-lottie |
| Styling | Custom CSS + HTML (SaaS-modern style, maksimalkan custom styling di luar default Streamlit) |
| Deployment | Streamlit Community Cloud |

---

## 3. Information Architecture

**Navbar** (dynamic island style, fixed)
- Kiri: logo + nomor tim
- Tengah: 4 menu utama — Home, Executive Summary, GT Lab, Ask to Gemini
- Kanan: toggle light/dark mode

**Home** — Hero section: judul karya, deskripsi singkat, tanggal pembuatan. Visual: subtle gradient + thin glassmorphism.

**Executive Summary** — Ringkasan insight utama dari data CSV.
- Layout bento-grid: card mixed-size (long & short)
- Area chart lebih luas untuk main insight
- Insight highlight via teks variatif (bukan plain caption)
- Sertakan filter component & hover interaction per card

**GT Lab** (Gebang Thunder Lab) — Modul projection & what-if analysis.
- Chart exploration interaktif
- Model selection: Regression, Classification, Clustering (sesuai struktur folder `gt_lab/`)

**Ask to Gemini** — Conversational AI assistant (Gemini API) untuk fast insight retrieval & analysis langsung dari data. **Key differentiator** vs kompetitor.

---

## 4. Design System

**Typography:** Font Inter, maksimal 3 level header.
**Spacing:** 8-point grid system, hindari layout padat/dense.
**Icon:** lucide.dev (SVG-based).

**Color Palette**
| Token | Light | Dark |
|---|---|---|
| Background | `#FFFFFF` | `#09090B` |
| Secondary Background | `#FAFAFA` | — |
| Card | `#FFFFFF` | `#18181B` |
| Border | `#E5E7EB` | `#27272A` |
| Primary | `#2563EB` | `#3B82F6` |
| Hover | `#EFF6FF` | — |
| Text Primary | `#111827` | `#FAFAFA` |
| Text Secondary | `#6B7280` | `#A1A1AA` |

**Component Style:** Konsisten di seluruh dashboard — button, card, border-radius, gradient, (glass)morphism, shadow.

**Responsive:** Grid row/column, adaptif Laptop/Tablet/Mobile (mobile-first breakpoint disarankan).

---

## 5. Repository Structure
```
gebang-thunder-dashboard/
│
├── app.py
├── requirements.txt
├── environment.yml
├── README.md
├── .gitignore
│
├── assets/
│   ├── icons/
│   ├── images/
│   ├── fonts/
│   └── animations/
│
├── config/
│   ├── settings.py
│   ├── constants.py
│   └── theme.py
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── sample/
│
├── models/
│   ├── saved/
│   └── metadata/
│
├── pages/
│   ├── executive_summary/
│   │   ├── page.py
│   │   ├── charts.py
│   │   ├── insights.py
│   │   └── filters.py
│   │
│   ├── gt_lab/
│   │   ├── page.py
│   │   ├── regression.py
│   │   ├── classification.py
│   │   ├── clustering.py
│   │   └── preprocessing.py
│   │
│   └── ask_gemini/
│       ├── page.py
│       ├── chat.py
│       ├── prompts.py
│       └── history.py
│
├── components/
│   ├── cards.py
│   ├── navbar.py
│   ├── sidebar.py
│   ├── metric.py
│   ├── modal.py
│   ├── buttons.py
│   ├── uploader.py
│   └── tables.py
│
├── services/
│   ├── csv_service.py
│   ├── gemini_service.py
│   ├── ml_service.py
│   ├── cache_service.py
│   └── export_service.py
│
├── utils/
│   ├── formatter.py
│   ├── validator.py
│   ├── logger.py
│   ├── session.py
│   └── helper.py
│
├── styles/
│   ├── main.css
│   ├── cards.css
│   ├── sidebar.css
│   └── typography.css
│
└── tests/
```

---

## 6. Data & Analysis *(Placeholder — isi setelah dataset rilis)*
> Dataset belum dirilis oleh panitia kompetisi. Section ini sengaja dikosongkan — update poin di bawah setelah data & EDA tersedia.

- **Dataset Overview:** _(TBD)_
- **Key Variables / Schema:** _(TBD)_
- **EDA Findings:** _(TBD)_
- **Feature Engineering:** _(TBD)_
- **Model Selection (GT Lab):** _(TBD)_
- **Key Insights (Executive Summary):** _(TBD)_

---

## 7. Non-Functional Requirements
- **Final Output:** Project siap deploy ke Streamlit Community Cloud, fully functional, zero error.
- **Error Handling:** Exception handling & default/fallback state detail per komponen (contoh: CSV upload invalid, kolom hilang, Gemini API timeout/rate-limit) — UX tetap graceful, tidak crash.
- **Security:** API keys/credentials (Gemini API, dll) wajib di-hide via `st.secrets` / environment variables — no hardcoded secret di source code.
- **Code Quality:** Full audit — pastikan tidak ada bug yang menyebabkan crash di production.
