# PRD — Gebang Thunder Dashboard "Ready to Take Off"

> **Tim:** Gebang Thunder · **Karya:** Ready to Take Off · **Tujuan:** Data Analytics Dashboard untuk Kompetisi

---

## 1. Role & Objective
Kamu bertindak sebagai **Professional UI/UX Developer** yang expert membangun **Data Analytics Dashboard**. Build dashboard berbasis single CSV fixed (sudah tersedia di repo, **bukan upload runtime**) yang **accessible**, **fully responsive** (Laptop/Tablet/Mobile), dan punya **strong differentiation** dari kompetitor — fokus pada visual impact & UX flow yang tidak generic.

**Design reference:** ui.shadcn.com, apple.com, notion.com — karakter minimalist, clean, futuristic.

**Bahasa aplikasi:** UI, pesan sistem, dan respons Gemini — Bahasa Indonesia (detail Section 3).

**Batasan peran AI Agent (penting):** AI Agent **tidak** melakukan data analysis, EDA, atau insight generation. Data table hasil analisis + brief chart/styling disiapkan manual oleh product owner (Giri). Tugas AI Agent terbatas pada **implementasi chart (Plotly), styling/theming, optimasi komponen, dan refactoring code** berdasarkan brief yang diberikan — bukan menentukan insight atau interpretasi data.

---

## 2. Scope & Out-of-Scope

**In-scope**
- Single fixed CSV, di-commit ke repo (`data/raw/` / `data/processed/`) — **tidak ada fitur upload CSV di UI**. Ukuran maksimum: belum ditentukan (TBD, tergantung ukuran dataset asli dari panitia).
- Dashboard read-only/presentational — tidak ada user-generated data yang perlu disimpan permanen.
- 4 page (Home, Executive Summary, GT Lab, Ask to Gemini) + navbar, dalam **1 aplikasi, 1 link/domain** (lihat Section 5).
- Ask to Gemini: conversational Q&A grounded ke dataset fixed (lihat Section 7).

**Out-of-scope**
- **Authentication/login** — dashboard publicly viewable buat juri/reviewer, tidak ada data privasi per-user yang perlu di-gate.
- **Persistent database** — tidak ada data yang berubah-ubah/disimpan permanen dari interaksi user. Cukup baca CSV sekali pas app start, tidak perlu PostgreSQL/MySQL/dst.
- **Multi-file CSV / data join** — single file CSV, tidak perlu logic merge/join antar tabel.
- **Upload CSV di UI** — data source fixed dari repo, bukan dari widget upload user.

---

## 3. Bahasa Aplikasi (UI & Content Language)

**Prinsip:** Seluruh **konten user-facing** di dashboard (bukan dokumen PRD ini) pakai **Bahasa Indonesia** sebagai bahasa utama — target audience utama panitia/juri kompetisi Indonesia.

**Cakupan:**
- **UI copy** — label navbar, heading, button, tooltip, empty state, placeholder text: Bahasa Indonesia. Istilah teknis umum yang sudah lazim dipakai di UI Indonesia (dashboard, filter, export, chart) boleh tetap as-is; kalimat/instruksi/pesan penuh tetap Bahasa Indonesia.
- **Error & exception handling** (Section 11) — pesan ke user Bahasa Indonesia, nada jelas & tidak teknis. Contoh: bukan `"Error: 429 Too Many Requests"`, tapi *"Maaf, sistem AI sedang sibuk. Coba beberapa saat lagi ya."*
- **Ask to Gemini** (Section 7.2) — system prompt mewajibkan Gemini merespons dalam Bahasa Indonesia secara default, kecuali user eksplisit menulis dalam Bahasa Inggris.
- **Format angka & tanggal** — konvensi Indonesia: titik (`.`) untuk ribuan, koma (`,`) untuk desimal, format tanggal `DD/MM/YYYY`. Implementasi di `utils/formatter.py`.
- **Kode & dokumentasi teknis** — nama variabel/fungsi/file, komentar code, commit message tetap Bahasa Inggris (standar praktik development). Aturan Bahasa Indonesia ini khusus konten yang dilihat end-user, bukan internal codebase.

---

## 4. Tech Stack
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

## 5. Information Architecture

**App Architecture & Routing**
Dashboard tetap **1 aplikasi, 1 link/domain dasar** (misal `https://gebang-thunder.streamlit.app`) — **bukan 4 link/deployment terpisah**. Navbar custom "dynamic island" (bukan sidebar bawaan Streamlit), jadi switching antar 4 page dilakukan lewat **`st.query_params`**: state halaman aktif ditambahkan sebagai parameter di belakang link yang sama (`?page=executive_summary`), `app.py` baca query param itu dan render module page yang sesuai.
- Kenapa `query_params` (bukan `st.session_state` doang): link dasar tetap satu, tapi kalau perlu, page tertentu bisa di-share via link yang sama + parameter (misal `.../?page=gt_lab`) — dan state page tetap kebaca walau browser di-refresh (`session_state` reset kalau refresh, `query_params` tidak).
- `st.session_state` tetap dipakai untuk state lain yang memang per-session (filter aktif, chat history Ask to Gemini, theme) — lihat Section 8.

**Navbar** (dynamic island style, fixed)
- Kiri: logo + nomor tim
- Tengah: 4 menu utama — Home, Executive Summary, GT Lab, Ask to Gemini
- Kanan: toggle light/dark mode

**Home** — Hero section: judul karya, deskripsi singkat, tanggal pembuatan. Visual: subtle gradient + thin glassmorphism.

**Executive Summary** — Ringkasan insight utama dari data CSV. **Data table & insight disiapkan manual oleh product owner** — AI Agent hanya implementasi chart & styling-nya (lihat Section 1).
- Layout bento-grid: card mixed-size (long & short)
- Area chart lebih luas untuk main insight
- Insight highlight via teks variatif (bukan plain caption)
- Sertakan filter component & hover interaction per card

**GT Lab** (Gebang Thunder Lab) — Modul projection & what-if analysis.
- Chart exploration interaktif
- Model selection: Regression, Classification, Clustering (sesuai struktur folder `gt_lab/`)
- Shell UI (layout, chart-selector, form what-if) bisa dibangun sekarang pakai dummy data; kolom/fitur final menyusul setelah dataset ada (lihat Section 9).

**Ask to Gemini** — Conversational AI assistant (Gemini API) grounded ke dataset fixed, untuk fast insight retrieval & analysis. **Key differentiator** vs kompetitor. Detail arsitektur → **Section 7**.

---

## 6. Design System

**Typography:** Font Inter, maksimal 3 level header.
**Spacing:** 8-point grid system, hindari layout padat/dense.

**Icon Implementation (Lucide SVG)**
- Approach: **bundle static SVG lokal** — bukan fetch runtime dari CDN, hindari network dependency saat demo kompetisi + lebih cepat.
- Ambil icon yang dipakai aja (bukan seluruh package) dari lucide.dev, simpan sebagai file individual di `assets/icons/*.svg`.
- Icon Lucide default pakai `stroke="currentColor"` → warna otomatis ngikut CSS `color` parent-nya, jadi **1 file SVG reusable** untuk light & dark mode tanpa duplikasi file.
- Helper `render_icon(name, size=20, color=None)` di `components/icon.py`: baca file SVG dari `assets/icons/`, inject atribut `width`/`height`/`color` via string replace, render lewat `st.markdown(html, unsafe_allow_html=True)`.
- Cache hasil baca file pakai `@st.cache_data` — hindari re-read disk tiap rerun Streamlit.

**Color Palette**
| Token | Light | Dark |
|---|---|---|
| Background | `#FFFFFF` | `#09090B` |
| Secondary Background | `#FAFAFA` | `#131316` |
| Card | `#FFFFFF` | `#18181B` |
| Border | `#E5E7EB` | `#27272A` |
| Primary | `#2563EB` | `#3B82F6` |
| Hover | `#EFF6FF` | `rgba(59,130,246,.12)` |
| Text Primary | `#111827` | `#FAFAFA` |
| Text Secondary | `#6B7280` | `#A1A1AA` |

> _Rationale nilai yang di-fill (Dark — Secondary Background & Hover):_ `Secondary Background` diinterpolasi antara `Background` & `Card` (±zinc-925) supaya layer section/bento-grid kelihatan subtle tanpa nabrak `Card`. `Hover` pakai alpha dari `Primary` (bukan flat hex) biar konsisten kelihatan di atas surface manapun; kalau butuh flat hex fallback: `#1C2535`.

**Component Style:** Konsisten di seluruh dashboard — button, card, border-radius, gradient, (glass)morphism, shadow.

**Responsive:** Grid row/column, adaptif Laptop/Tablet/Mobile (mobile-first breakpoint disarankan).

**Loading States** (scope saat ini)
- Skeleton loading saat page/layer dibuka pertama kali (transisi antar Home/Executive Summary/GT Lab/Ask to Gemini).
- Loading indicator saat menunggu response dari Ask to Gemini.
- Cakupan lain (misal loading saat training model GT Lab) menyusul kalau dibutuhkan — belum in-scope sekarang.

---

## 7. Ask to Gemini — API Architecture

### 7.1 Multi-Key Pooling
**Goal:** Pool beberapa Google AI (Gemini) API key — punya kamu + rekan tim, **masing-masing dari akun Google berbeda** — untuk extend total quota. Requirement: tambah/ganti key gampang (cukup edit array string, zero code change), dan aman dari exposure/privasi.

> ⚠️ **Cara kerja quota (dikonfirmasi dari dokumentasi resmi Google, per Jun 2026):** Rate limit Gemini API di-enforce **per Google Cloud Project**, bukan per API key — bikin banyak key dari 1 akun yang sama **tidak** menambah quota (semua key di project itu berbagi 1 pool yang sama). Strategi pooling ini efektif **hanya kalau tiap key berasal dari akun Google yang benar-benar berbeda** (1 key kamu dari akun kamu, 1 key tiap rekan dari akun masing-masing). Angka indikatif per project di 2026 untuk model Flash/Flash-Lite: ±10–15 RPM & ±1.500 RPD (model **Gemini Pro sudah tidak tersedia di free tier** sejak April 2026 — arahkan default model ke `gemini-flash` / `flash-lite`). Catatan tambahan: beberapa sumber community menyebut praktik multi-akun pooling sebagai gray area terhadap ToS Google kalau dipakai untuk traffic production jangka panjang — untuk kebutuhan demo kompetisi (short-term, low-traffic) risikonya relatif kecil, tapi worth dicek ulang ke ToS resmi Google AI Studio kalau project ini lanjut dipakai setelah kompetisi.

**Storage**
- Key disimpan di `.streamlit/secrets.toml` (local dev) / Streamlit Cloud → **Settings → Secrets** (production, format sama).
```toml
[gemini]
api_keys = [
  "key-1",  # akun kamu
  "key-2",  # akun rekan 1 — WAJIB dari Google account terpisah
  "key-3"   # akun rekan 2 — WAJIB dari Google account terpisah
]
```
- Tambah/ganti/hapus key = edit array ini aja — **tidak perlu ubah code**.
- Commit `.streamlit/secrets.toml.example` (isi placeholder) ke repo sebagai template; file `secrets.toml` asli **wajib** masuk `.gitignore` — cross-check sebelum push (repo kompetisi sering bersifat public).

**Key Pool Logic** (`utils/key_pool.py`)
- Class `KeyPool`: load `st.secrets["gemini"]["api_keys"]` sekali saat startup, cache via `st.cache_resource`.
- Method: `get_key()` (round-robin / least-used), `mark_failed(key)` (skip key yang lagi kena limit/error).
- Auto-rotate on error: HTTP 429 → cek jenis limit dari error body. Kalau RPM/TPM (rolling window) → retry key yang sama dengan exponential backoff singkat (~10–60 detik). Kalau RPD (daily cap, reset tengah malam Pacific Time) → key itu di-`mark_failed()` untuk sisa hari ini, langsung rotate ke key berikutnya (retry max = jumlah key tersedia) → kalau semua key exhausted, graceful fallback message dalam Bahasa Indonesia (lihat Section 11, bukan crash).

**Consumption** (`services/gemini_service.py`)
- Import `key_pool`, tiap call Gemini API ambil key via `get_key()`.
- Wrap tiap call dengan try-except spesifik per error type (quota, invalid key, timeout, network).

**Security & Privasi**
- Key **tidak pernah** di-hardcode, di-print full ke console/log, atau ditampilkan di UI. Kalau perlu debug, mask: `sk-...` + 4 karakter terakhir saja.
- Jangan expose "key ini milik siapa" ke user-facing UI — logging internal pakai alias generik (`key_1`, `key_2`), bukan nama rekan tim.
- Optional token-saving: cache response per query (hash dari prompt + context) pakai `@st.cache_data(ttl=...)` — query identik tidak re-consume quota.

### 7.2 Data Grounding (Fixed Dataset)
**Konsep grounding:** supaya Gemini bisa jawab pertanyaan spesifik soal dataset kamu (bukan cuma general knowledge), dia perlu "dikasih tau" dulu struktur & isi data lewat prompt/context.

Karena dataset **fixed** (tidak ada upload runtime, isinya sudah pasti), grounding disiapkan **sekali** pas dataset final ada, bukan generate ulang tiap request:
- **Data profile generation** (one-time, pas dataset final): rangkum schema (nama kolom + tipe data), statistik ringkas (`describe()`), beberapa sample rows, dan definisi istilah domain-specific kalau ada — simpan sebagai `data/processed/data_profile.md` atau constant string.
- **System prompt injection**: tiap sesi chat baru di Ask to Gemini, `data_profile` ini otomatis disisipin sebagai system prompt/context awal sebelum pertanyaan user — Gemini "paham" struktur data dari awal chat tanpa perlu kirim ulang raw CSV tiap request (lebih token-efficient, dan aman untuk precompute karena data tidak berubah).
- **Scope & bahasa jawaban**: instruksikan Gemini di system prompt untuk jawab **grounded ke data yang ada aja** (kalau di luar cakupan data, jawab jujur "tidak tersedia di dataset", bukan mengarang), dan **selalu merespons dalam Bahasa Indonesia** (lihat Section 3) kecuali user eksplisit menulis dalam Bahasa Inggris.
- Model default: `gemini-flash` / `flash-lite` (lihat 7.1), temperature rendah-medium (±0.3–0.5) untuk jawaban yang lebih factual/konsisten.

---

## 8. Repository Structure
```
gebang-thunder-dashboard/
│
├── .streamlit/
│   ├── config.toml            # theme & app config
│   └── secrets.toml.example   # template, secrets.toml asli di-gitignore
│
├── app.py                      # entrypoint + query_params router
├── requirements.txt
├── environment.yml
├── README.md
├── .gitignore
│
├── assets/
│   ├── icons/                 # SVG lucide, hanya yang dipakai (lihat Section 6)
│   ├── images/
│   ├── fonts/
│   └── animations/
│
├── config/
│   ├── settings.py
│   ├── constants.py
│   └── theme.py                # single source of truth token warna
│
├── data/
│   ├── raw/                   # CSV asli dari panitia, apa adanya
│   ├── processed/             # CSV/tabel hasil olahan manual + data_profile.md (Section 7.2)
│   └── sample/                # dummy CSV untuk dev/demo sebelum dataset final
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
│   ├── icon.py                 # render_icon() helper (lihat Section 6)
│   └── tables.py
│
├── services/
│   ├── csv_service.py          # load & validasi CSV fixed dari data/
│   ├── gemini_service.py       # consumer dari utils/key_pool.py
│   ├── ml_service.py
│   ├── cache_service.py
│   └── export_service.py
│
├── utils/
│   ├── formatter.py             # format angka/tanggal konvensi Indonesia (Section 3)
│   ├── validator.py
│   ├── logger.py
│   ├── session.py               # session_state: filter, chat history, theme
│   ├── key_pool.py             # multi-key rotation (lihat Section 7.1)
│   └── helper.py
│
├── styles/
│   ├── main.css
│   ├── cards.css
│   ├── sidebar.css
│   └── typography.css
│
└── tests/
    ├── test_key_pool.py
    └── test_csv_service.py
```

**Catatan Implementasi Tambahan**
- `config/theme.py` jadi single source of truth token warna (Section 6) — dipakai untuk inject custom CSS maupun logic Python (misal warna chart Plotly ngikut tema aktif).
- Caching: `@st.cache_data` untuk CSV load (`csv_service.py`) & icon file read (`components/icon.py`); `@st.cache_resource` untuk `KeyPool` & model objects (`ml_service.py`).
- Session state (`utils/session.py`) handle: filter aktif Executive Summary, chat history Ask to Gemini, dan theme (light/dark) — page routing sendiri pakai `query_params` (Section 5), bukan session_state.
- `tests/` minimal cover key rotation logic & CSV validation.

---

## 9. Execution Roadmap — Prioritas Task

**Bisa dikerjakan sekarang (tidak bergantung dataset final):**
- Setup repo, `.streamlit/` (config + secrets template), `.gitignore`
- Design system: `config/theme.py`, color tokens, typography, spacing, icon set (`render_icon()`)
- Navbar + routing (`query_params`) + light/dark toggle
- Home page (konten sudah fix, bisa langsung final)
- Component library dasar: cards, buttons, modal, metric, tables — pakai dummy data dari `data/sample/`
- Executive Summary & GT Lab: **shell UI aja** (layout bento-grid, chart placeholder, filter component, form what-if) — dummy data, chart final menyusul
- Ask to Gemini: infrastruktur penuh (`key_pool.py`, `gemini_service.py`, chat UI, session history) — bisa ditest pakai dummy grounding context
- Deployment pipeline ke Streamlit Cloud (test end-to-end pakai dummy data)

**Baru bisa dikerjakan setelah dataset & analisis final:**
- Executive Summary: chart & insight final — dari table + brief chart/styling yang disiapkan product owner (Section 1)
- GT Lab: model regression/classification/clustering final pakai kolom asli
- `data_profile.md` final untuk Gemini grounding (Section 7.2)
- Section 10 (Data & Analysis) di PRD ini — isi TBD

---

## 10. Data & Analysis *(Placeholder — isi setelah dataset rilis)*
> Dataset belum dirilis oleh panitia kompetisi. Section ini sengaja dikosongkan — update poin di bawah setelah data & EDA tersedia.

- **Dataset Overview:** _(TBD)_
- **Key Variables / Schema:** _(TBD)_
- **EDA Findings:** _(TBD)_
- **Feature Engineering:** _(TBD)_
- **Model Selection (GT Lab):** _(TBD)_
- **Key Insights (Executive Summary):** _(TBD)_

---

## 11. Non-Functional Requirements
- **Final Output:** Project siap deploy ke Streamlit Community Cloud, fully functional, zero error.
- **Error Handling:** Exception handling & default/fallback state detail per komponen — termasuk CSV source corrupt/kolom hilang (dataset fixed tapi tetap perlu validasi), dan **semua Gemini API key exhausted** (lihat Section 7.1). Semua pesan ke user Bahasa Indonesia, ramah, tidak menampilkan raw error teknis (lihat Section 3) — UX tetap graceful, tidak crash.
- **Security:** Seluruh API key/credential wajib di `.streamlit/secrets.toml` (gitignored) — no hardcoded secret, no full key ter-print ke log/UI (detail lihat Section 7.1).
- **Code Quality:** Full audit — pastikan tidak ada bug yang menyebabkan crash di production.
