from __future__ import annotations

import math

import streamlit as st

from science import PLANETS, QUIZ, calculate_formula, free_fall_distance, pendulum_period, quiz_score


st.set_page_config(
    page_title="SainsLab — Belajar sains dengan mencoba",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded",
)

BG = "#090d1a"
PANEL = "#11182a"
MUTED = "#9aa8c7"
CYAN = "#61e7dd"
PURPLE = "#a78bfa"

st.markdown(
    f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
      .stApp {{ background: radial-gradient(ellipse at 75% -10%, #202552 0%, {BG} 52%); color: #f4f6ff; }}
      html, body, [class*="css"] {{ font-family: 'Manrope', sans-serif; }}
      [data-testid="stSidebar"] {{ background: #0c1120; border-right: 1px solid #202944; }}
      [data-testid="stHeader"] {{ background: transparent; }}
      [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{ color: {MUTED}; }}
      .hero {{ padding: 2.2rem 2.2rem 1.8rem; border: 1px solid #293454; border-radius: 24px;
        background: linear-gradient(125deg, rgba(29,39,75,.94), rgba(15,23,42,.75) 55%, rgba(36,24,71,.75)); }}
      .eyebrow {{ color: {CYAN}; font: 500 .78rem 'DM Mono', monospace; letter-spacing: .16em; text-transform: uppercase; }}
      .hero h1 {{ font-size: clamp(2.3rem, 5vw, 4rem); line-height: 1.04; margin: .5rem 0 .8rem; letter-spacing: -.055em; }}
      .hero p {{ max-width: 700px; color: #bdc8e3; font-size: 1.05rem; }}
      .panel {{ background: {PANEL}; border: 1px solid #222d48; border-radius: 18px; padding: 1.15rem 1.3rem; height: 100%; }}
      .panel-label {{ color: {MUTED}; font: .75rem 'DM Mono', monospace; text-transform: uppercase; letter-spacing: .08em; }}
      .panel-value {{ font-size: 1.7rem; font-weight: 800; margin: .45rem 0 .15rem; }}
      .panel-copy {{ color: {MUTED}; font-size: .88rem; }}
      .tag {{ color: {CYAN}; font: .72rem 'DM Mono', monospace; background: #102c36; padding: .32rem .6rem; border-radius: 20px; }}
      .callout {{ border-left: 3px solid {CYAN}; background: #111d2c; padding: .9rem 1rem; border-radius: 0 12px 12px 0; color: #c7d2e8; }}
      .stButton > button {{ border-radius: 12px; font-weight: 700; }}
      .stTabs [data-baseweb="tab-list"] {{ gap: .5rem; }}
      .stTabs [data-baseweb="tab"] {{ background: #11182a; border-radius: 10px; padding: .65rem 1rem; }}
      div[data-testid="stMetric"] {{ background: #11182a; border: 1px solid #222d48; padding: .8rem 1rem; border-radius: 14px; }}
      code, pre {{ font-family: 'DM Mono', monospace !important; }}
      h1, h2, h3 {{ letter-spacing: -.035em; }}
      hr {{ border-color: #24304b; }}
    </style>
    """,
    unsafe_allow_html=True,
)


def section_heading(kicker: str, title: str, description: str) -> None:
    st.markdown(f'<div class="eyebrow">{kicker}</div>', unsafe_allow_html=True)
    st.title(title)
    st.markdown(f"<p style='color:{MUTED};margin-top:-.6rem'>{description}</p>", unsafe_allow_html=True)


def card(label: str, value: str, copy: str) -> None:
    st.markdown(
        f'<div class="panel"><div class="panel-label">{label}</div>'
        f'<div class="panel-value">{value}</div><div class="panel-copy">{copy}</div></div>',
        unsafe_allow_html=True,
    )


def render_line_chart(
    x_values: list[float],
    y_values: list[float],
    x_label: str,
    y_label: str,
    title: str,
    color: str = CYAN,
    marker: tuple[float, float] | None = None,
) -> None:
    width, height = 800, 380
    left, right, top, bottom = 76, 24, 52, 58
    plot_width, plot_height = width - left - right, height - top - bottom
    x_min, x_max = min(x_values), max(x_values)
    y_min, y_max = min(y_values), max(y_values)
    y_span = y_max - y_min or 1
    y_min -= y_span * .08
    y_max += y_span * .08

    def point(x: float, y: float) -> tuple[float, float]:
        px = left + (x - x_min) / (x_max - x_min or 1) * plot_width
        py = top + (y_max - y) / (y_max - y_min) * plot_height
        return px, py

    path = " ".join(
        ("M" if index == 0 else "L") + f" {point(x, y)[0]:.1f} {point(x, y)[1]:.1f}"
        for index, (x, y) in enumerate(zip(x_values, y_values))
    )
    grid = []
    for index in range(5):
        y = top + plot_height * index / 4
        label = y_max - (y_max - y_min) * index / 4
        grid.append(
            f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#34405a"/>'
            f'<text x="{left-12}" y="{y+4:.1f}" fill="#9aa8c7" text-anchor="end" font-size="12">{label:.2g}</text>'
        )
        x = left + plot_width * index / 4
        x_value = x_min + (x_max - x_min) * index / 4
        grid.append(
            f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{height-bottom}" stroke="#27334c" stroke-dasharray="3 5"/>'
            f'<text x="{x:.1f}" y="{height-bottom+22}" fill="#9aa8c7" text-anchor="middle" font-size="12">{x_value:.2g}</text>'
        )
    dot = ""
    if marker is not None:
        px, py = point(*marker)
        dot = f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="{CYAN}" stroke="white" stroke-width="2"/>'
    svg = (
        f'<svg viewBox="0 0 {width} {height}" role="img" aria-label="{title}" '
        f'style="width:100%;height:auto;background:{PANEL};border:1px solid #222d48;border-radius:16px">'
        f'<text x="{left}" y="29" fill="#f4f6ff" font-size="16" font-weight="700">{title}</text>'
        f'{"".join(grid)}<path d="{path}" fill="none" stroke="{color}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>'
        f'{dot}<text x="{width/2}" y="{height-8}" fill="#9aa8c7" text-anchor="middle" font-size="12">{x_label}</text>'
        f'<text transform="translate(19 {height/2}) rotate(-90)" fill="#9aa8c7" text-anchor="middle" font-size="12">{y_label}</text>'
        "</svg>"
    )
    st.markdown(svg, unsafe_allow_html=True)


def render_home() -> None:
    st.markdown(
        """
        <div class="hero">
          <div class="eyebrow">LABORATORIUM SAINS INTERAKTIF · EDISI 01</div>
          <h1>Rasa ingin tahu,<br>jadi <span style="color:#61e7dd">pengetahuan.</span></h1>
          <p>Jangan hanya menghafal rumus. Ubah variabel, amati pola, lalu gunakan matematika dan kode Python untuk menjelaskan alam semesta.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    columns = st.columns(4)
    cards = [
        ("01 / FISIKA", "Gerak & gaya", "Uji gravitasi dan hukum Newton."),
        ("02 / ANTARIKSA", "Tata surya", "Jelajahi orbit delapan planet."),
        ("03 / MATEMATIKA", "Kalkulator", "Gunakan rumus, lihat satuannya."),
        ("04 / EKSPERIMEN", "Ayunan", "Cari tahu variabel yang berpengaruh."),
    ]
    for column, (label, value, copy) in zip(columns, cards):
        with column:
            card(label, value, copy)

    st.write("")
    left, right = st.columns([1.2, 1])
    with left:
        st.subheader("Sains bekerja seperti program")
        st.markdown(
            f"""
            <div class="panel">
            <p><span class="tag">INPUT</span> Besaran yang bisa kita ukur</p>
            <p><span class="tag">MODEL</span> Hubungan matematika antarbesaran</p>
            <p><span class="tag">OUTPUT</span> Prediksi yang dapat diuji</p>
            <p style="color:{MUTED};margin-bottom:0">Di SainsLab, slider adalah input, rumus adalah model, dan grafik adalah output. Ubah inputnya—apakah prediksi berubah seperti yang kamu harapkan?</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with right:
        st.subheader("Mulai eksplorasi")
        st.markdown(
            f'<div class="callout">Pilih modul dari menu di sebelah kiri. Setiap simulasi menampilkan variabel, persamaan, visualisasi, dan potongan kode Python yang menghasilkan prediksi.</div>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.caption("Semua nilai simulasi bersifat edukatif. Model fisika menggunakan asumsi ideal yang dijelaskan pada tiap modul.")


def render_physics() -> None:
    section_heading("01 / MEKANIKA", "Jatuh bebas", "Amati hubungan waktu, gravitasi, dan jarak jatuh dengan model gerak lurus berubah beraturan.")
    col_input, col_chart = st.columns([0.78, 1.55], gap="large")
    with col_input:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        height = st.slider("Ketinggian awal (m)", 5, 200, 80, 5)
        gravity = st.slider("Gravitasi (m/s²)", 1.0, 20.0, 9.8, 0.1)
        st.markdown("</div>", unsafe_allow_html=True)

    time_to_ground = math.sqrt(2 * height / gravity)
    impact_speed = gravity * time_to_ground
    sample_times = [time_to_ground * index / 99 for index in range(100)]
    distances = [min(free_fall_distance(t, gravity), height) for t in sample_times]
    with col_chart:
        render_line_chart(sample_times, distances, "Waktu (s)", "Jarak jatuh (m)", "Jarak jatuh terhadap waktu", marker=(time_to_ground, height))

    metrics = st.columns(3)
    with metrics[0]:
        st.metric("Waktu hingga tanah", f"{time_to_ground:.2f} s")
    with metrics[1]:
        st.metric("Kecepatan saat tumbukan", f"{impact_speed:.2f} m/s")
    with metrics[2]:
        st.metric("Model", "Tanpa hambatan udara")
    st.latex(r"s = \frac{1}{2}gt^2 \qquad v = gt")
    with st.expander("Lihat hubungan sains, matematika, dan Python"):
        st.markdown("**Fisika:** percepatan dianggap konstan dan kecepatan awal nol. **Matematika:** jarak tumbuh sebanding dengan kuadrat waktu. **Pemrograman:** slider mengubah input; fungsi di bawah menghitung output setiap kali tampilan diperbarui.")
        st.code("jarak = 0.5 * gravitasi * waktu**2\nkecepatan = gravitasi * waktu", language="python")


def render_solar_system() -> None:
    section_heading("02 / ASTRONOMI", "Tata surya", "Gerakkan waktu simulasi untuk melihat planet berpindah di orbitnya. Posisi bersifat model edukatif, bukan efemeris presisi.")
    days = st.slider("Hari sejak awal simulasi", 0, 3650, 0, 10)
    selected = st.selectbox("Pilih planet untuk dipelajari", [planet["name"] for planet in PLANETS], index=2)
    svg_parts = [
        '<svg viewBox="0 0 900 650" role="img" aria-label="Visualisasi interaktif orbit delapan planet" '
        'style="width:100%;height:auto;background:#080d1a;border:1px solid #222d48;border-radius:16px">',
        '<text x="35" y="35" fill="#c5cee4" font-size="12" letter-spacing="2">ORBITAL VIEW / SKALA VISUAL LOGARITMIK</text>',
        '<circle cx="450" cy="330" r="16" fill="#ffd166" stroke="#fff1a8" stroke-width="2"/>',
    ]
    center_x, center_y = 450, 330
    for planet in PLANETS:
        orbit_radius = math.log1p(planet["distance_au"]) * 77
        angle = planet["distance_au"] * .71 + 2 * math.pi * days / planet["period_days"]
        px = center_x + orbit_radius * math.cos(angle)
        py = center_y + orbit_radius * math.sin(angle)
        is_selected = planet["name"] == selected
        size = 9 if is_selected else 6
        label_x = center_x + (orbit_radius + 15) * math.cos(angle)
        label_y = center_y + (orbit_radius + 15) * math.sin(angle)
        svg_parts.extend(
            [
                f'<circle cx="{center_x}" cy="{center_y}" r="{orbit_radius:.1f}" fill="none" stroke="#45516e" stroke-width="1" opacity=".65"/>',
                f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{size}" fill="{planet["color"]}" stroke="{"white" if is_selected else "#080d1a"}" stroke-width="2"/>',
                f'<text x="{label_x:.1f}" y="{label_y:.1f}" fill="#e9edfa" text-anchor="middle" dominant-baseline="middle" font-size="11">{planet["name"]}</text>',
            ]
        )
    svg_parts.append("</svg>")
    st.markdown("".join(svg_parts), unsafe_allow_html=True)

    planet = next(item for item in PLANETS if item["name"] == selected)
    detail, model = st.columns([1, 1], gap="large")
    with detail:
        st.markdown(f'<div class="panel"><div class="panel-label">DATA PLANET · {planet["name"].upper()}</div><div class="panel-value">{planet["distance_au"]:.2f} AU</div><div class="panel-copy">Jarak rata-rata dari Matahari</div><hr><p>{planet["fact"]}</p><p style="color:{MUTED}">Periode orbit: {planet["period_days"]:,} hari · Diameter: {planet["diameter_km"]:,} km</p></div>', unsafe_allow_html=True)
    with model:
        st.markdown('<div class="panel"><div class="panel-label">CATATAN MODEL</div><p>Jarak orbit pada gambar dipadatkan dengan transformasi logaritmik agar planet bagian dalam tetap terlihat. Ukuran planet juga tidak dibuat sesuai skala.</p><p style="color:#61e7dd">Sudut orbit = 2π × hari simulasi ÷ periode orbit</p><p class="panel-copy">AU adalah satuan astronomi, kira-kira jarak rata-rata Bumi ke Matahari.</p></div>', unsafe_allow_html=True)
    st.code("sudut = 2 * pi * hari_simulasi / periode_orbit_hari\nx = radius_orbit * cos(sudut)\ny = radius_orbit * sin(sudut)", language="python")


FORMULAS = {
    "Gaya (F = m × a)": ("Massa", "kg", "Percepatan", "m/s²", "Gaya", "N"),
    "Energi kinetik (Ek = ½ × m × v²)": ("Massa", "kg", "Kecepatan", "m/s", "Energi kinetik", "J"),
    "Kecepatan (v = s ÷ t)": ("Jarak", "m", "Waktu", "s", "Kecepatan", "m/s"),
    "Berat (w = m × g)": ("Massa", "kg", "Gravitasi", "m/s²", "Berat", "N"),
    "Hukum Ohm (V = I × R)": ("Arus", "A", "Hambatan", "Ω", "Tegangan", "V"),
    "Massa jenis (ρ = m ÷ V)": ("Massa", "kg", "Volume", "m³", "Massa jenis", "kg/m³"),
}

FORMULA_CODE = {
    "Gaya (F = m × a)": "gaya_n = massa_kg * percepatan_m_s2",
    "Energi kinetik (Ek = ½ × m × v²)": "energi_j = 0.5 * massa_kg * kecepatan_m_s**2",
    "Kecepatan (v = s ÷ t)": "kecepatan_m_s = jarak_m / waktu_s",
    "Berat (w = m × g)": "berat_n = massa_kg * gravitasi_m_s2",
    "Hukum Ohm (V = I × R)": "tegangan_v = arus_a * hambatan_ohm",
    "Massa jenis (ρ = m ÷ V)": "massa_jenis_kg_m3 = massa_kg / volume_m3",
}


def render_calculator() -> None:
    section_heading("03 / ALAT MATEMATIKA", "Kalkulator rumus", "Pilih model, masukkan nilai besaran, lalu periksa hasil dan satuan.")
    formula = st.selectbox("Pilih rumus", list(FORMULAS))
    first_name, first_unit, second_name, second_unit, result_name, result_unit = FORMULAS[formula]
    left, right = st.columns(2, gap="large")
    with left:
        first = st.number_input(f"{first_name} ({first_unit})", min_value=0.0, value=2.0, step=0.5)
    with right:
        second = st.number_input(f"{second_name} ({second_unit})", min_value=0.0, value=3.0, step=0.5)
    try:
        result = calculate_formula(formula, first, second)
        st.markdown(f'<div class="panel"><div class="panel-label">HASIL PERHITUNGAN</div><div class="panel-value">{result_name}: {result:,.4g} {result_unit}</div><div class="panel-copy">{formula}</div></div>', unsafe_allow_html=True)
    except ValueError as error:
        st.error(str(error))
    st.write("")
    st.markdown('<div class="callout">Pemrograman mengubah rumus menjadi fungsi yang dapat digunakan ulang. Satuan masukan menentukan satuan hasil—pastikan semuanya konsisten.</div>', unsafe_allow_html=True)
    st.code(FORMULA_CODE[formula], language="python")


def render_experiment() -> None:
    section_heading("04 / EKSPERIMEN VIRTUAL", "Laboratorium ayunan", "Ubah panjang tali, gravitasi, dan massa beban. Buat prediksi sebelum melihat hasilnya.")
    inputs, chart = st.columns([.8, 1.5], gap="large")
    with inputs:
        length = st.slider("Panjang tali (m)", .2, 3.0, 1.0, .1)
        gravity = st.slider("Gravitasi (m/s²)", 1.0, 20.0, 9.8, .1)
        mass = st.slider("Massa beban (kg)", .1, 5.0, 1.0, .1)
    period = pendulum_period(length, gravity)
    lengths = [.2 + 2.8 * index / 119 for index in range(120)]
    periods = [pendulum_period(item, gravity) for item in lengths]
    with chart:
        render_line_chart(lengths, periods, "Panjang tali (m)", "Periode (s)", "Periode ayunan menurut panjang tali", color=PURPLE, marker=(length, period))
    a, b, c = st.columns(3)
    with a:
        st.metric("Periode", f"{period:.3f} s")
    with b:
        st.metric("Ayunan per menit", f"{60 / period:.1f}")
    with c:
        st.metric("Massa beban", f"{mass:.1f} kg")
    st.latex(r"T = 2\pi\sqrt{\frac{L}{g}}")
    st.info("Ubah massa beban: periode model tetap sama. Ubah panjang tali atau gravitasi: periode berubah. Ini adalah prediksi model ayunan sederhana untuk simpangan kecil; efek gesekan diabaikan.")
    st.code("periode = 2 * pi * sqrt(panjang_tali / gravitasi)\n# massa tidak muncul dalam persamaan periode", language="python")


def render_quiz() -> None:
    section_heading("05 / CEK PEMAHAMAN", "Kuis sains", "Lima pertanyaan singkat tentang fisika, matematika, dan tata surya.")
    with st.form("science_quiz"):
        answers: list[int] = []
        for index, item in enumerate(QUIZ):
            st.markdown(f"**{index + 1:02d} / {item['question']}**")
            answer = st.radio("Pilih jawaban", item["options"], index=None, key=f"quiz_{index}", label_visibility="collapsed")
            answers.append(item["options"].index(answer) if answer is not None else -1)
            st.divider()
        submitted = st.form_submit_button("Periksa jawaban", type="primary", use_container_width=True)
    if submitted:
        score = quiz_score(answers)
        st.session_state["last_quiz_score"] = score
        st.session_state["last_quiz_answers"] = answers
    if "last_quiz_score" in st.session_state:
        score = st.session_state["last_quiz_score"]
        st.success(f"Skor kamu: {score} dari {len(QUIZ)} — {'Hebat! Terus eksplorasi.' if score >= 4 else 'Bagus, cek pembahasan dan coba lagi!'}")
        with st.expander("Buka pembahasan"):
            for index, item in enumerate(QUIZ):
                answer = st.session_state["last_quiz_answers"][index]
                is_correct = answer == item["answer"]
                st.markdown(f"**{index + 1}. {'Benar' if is_correct else 'Jawaban benar: ' + item['options'][item['answer']]}**  \n{item['explanation']}")


PAGES = {
    "Beranda": ("⌂", render_home),
    "Simulasi fisika": ("◉", render_physics),
    "Tata surya": ("✳", render_solar_system),
    "Kalkulator rumus": ("∑", render_calculator),
    "Eksperimen virtual": ("⌁", render_experiment),
    "Kuis sains": ("✓", render_quiz),
}

with st.sidebar:
    st.markdown(f"<div style='font-size:1.55rem;font-weight:800;letter-spacing:-.05em'>Sains<span style='color:{CYAN}'>Lab</span> <span style='font-size:.8rem;color:{MUTED}'>/ PY</span></div>", unsafe_allow_html=True)
    st.caption("BELAJAR · MENGUJI · MEMAHAMI")
    st.divider()
    page_name = st.radio("JELAJAHI LAB", list(PAGES), format_func=lambda name: f"{PAGES[name][0]}   {name}", label_visibility="visible")
    st.divider()
    st.markdown(f"<div class='panel-label'>METODE ILMIAH</div><p style='font-size:.86rem'>Amati → buat prediksi → ubah satu variabel → bandingkan hasil.</p>", unsafe_allow_html=True)
    st.caption("SainsLab · Aplikasi belajar sains interaktif")

PAGES[page_name][1]()
