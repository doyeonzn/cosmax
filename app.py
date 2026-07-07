import streamlit as st
import pandas as pd
from pathlib import Path

# ----------------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------------
st.set_page_config(
    page_title="COSMAX Package Hub",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "package_hub_sample_50.csv"
ASSETS_DIR = BASE_DIR / "assets"

RED = "#EA1D22"
RED_DARK = "#c91318"
RED_TINT = "rgba(234,29,34,0.08)"
BG = "#F5F5F7"
TEXT = "#1D1D1F"
TEXT_SECONDARY = "#6E6E73"
BORDER = "#E3E3E6"

# ----------------------------------------------------------------------------
# Static reference data (kept in Korean to match the vendor catalog)
# ----------------------------------------------------------------------------
CATEGORY_LABELS = {
    "자": "자 Jar",
    "병": "병 Bottle",
    "튜브": "튜브 Tube",
    "펌프": "펌프 Pump",
    "콤팩트": "콤팩트 Compact",
    "앰플": "앰플 Ampoule",
    "스틱": "스틱 Stick",
    "드롭퍼": "드롭퍼 Dropper",
    "견본용기": "견본용기 Sample",
}

CATEGORY_ICONS = {
    "자": "🫙", "병": "🍼", "튜브": "🧴", "펌프": "🧪",
    "콤팩트": "🎨", "앰플": "💧", "스틱": "🖊️", "드롭퍼": "🩸",
    "견본용기": "🧫",
}

CATEGORY_ORDER = ["자", "병", "튜브", "펌프", "콤팩트", "앰플", "스틱", "드롭퍼", "견본용기"]

# tone-on-tone brand red, darkest for categories further down the list
_RED_STEPS = ["#EA1D22", "#CC1B24", "#AD1820", "#8F141C", "#711018",
              "#5B0D12", "#4D0B10", "#420A0E", "#38080C"]
CATEGORY_COLORS = {cat: _RED_STEPS[i % len(_RED_STEPS)] for i, cat in enumerate(CATEGORY_ORDER)}

MATERIAL_INFO = {
    "PP": {"장점": "내약품성이 우수하고 유연해 다양한 캡·자 구조에 적용 가능",
           "단점": "투명도가 PET 대비 낮아 내용물 노출 디자인에는 한계",
           "유의점": "고온 충전 시 변형 가능성이 있어 충전 온도 스펙 확인 필요"},
    "PET": {"장점": "가볍고 투명도가 높아 내용물 시각적 어필에 유리, 단가 경쟁력이 좋음",
            "단점": "내열성이 낮아 고온 충전·살균 공정에 취약",
            "유의점": "고농도 오일·알코올 성분에서 크랙(변형) 발생 가능성 유의"},
    "PCTG": {"장점": "PETG와 비슷한 투명도에 내충격성이 더 우수해 파손 위험이 낮음",
             "단점": "PET·PP 대비 원재료 단가가 높은 편",
             "유의점": "재활용 등급이 별도로 분류되어 분리배출 표기 확인 필요"},
    "ABS": {"장점": "강도와 치수 안정성이 높아 캡·뚜껑·콤팩트 구조물에 적합",
            "단점": "내용물과 직접 접촉 시 화학적 반응 가능성 있어 이너캡이 필요할 수 있음",
            "유의점": "도금·메탈릭 마감 적용 시 도금층 박리 여부 사전 테스트 권장"},
    "Glass": {"장점": "고급스러운 질감과 내화학성이 뛰어나 프리미엄 라인에 적합",
              "단점": "무게가 무겁고 파손 위험이 있어 물류비·파손율 증가",
              "유의점": "낙하·충격에 약하므로 배송 및 진열 시 완충 포장 필수"},
    "Aluminum": {"장점": "차광성이 우수해 광분해에 취약한 성분 보호에 유리, 재활용 용이",
                 "단점": "내부 코팅 없이는 내용물과 반응 가능, 상대적으로 단가 높음",
                 "유의점": "산성·알칼리성 포뮬러는 내부 라이닝 코팅 사양 확인 필요"},
}

GRAM_CATEGORIES = {"콤팩트", "스틱"}


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["note"] = df["note"].fillna("")
    df["unit"] = df["category"].apply(lambda c: "g" if c in GRAM_CATEGORIES else "mL")
    return df


df = load_data()

ALL_CATEGORIES = [c for c in CATEGORY_ORDER if c in df["category"].unique()]
ALL_MATERIALS = sorted(df["material"].unique())
ALL_FINISHES = sorted(df["finish"].unique())
ALL_VENDORS = sorted(df["vendor"].unique())
PRICE_MIN = int(df["price_krw"].min())
PRICE_MAX = int(df["price_krw"].max())


def fmt_won(n) -> str:
    return f"{int(n):,}원"


def category_label(c: str) -> str:
    return CATEGORY_LABELS.get(c, c)


# ----------------------------------------------------------------------------
# Global CSS
# ----------------------------------------------------------------------------
st.markdown(f"""
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style>
  html, body, [class*="css"] {{
      font-family: "Noto Sans KR", -apple-system, "Malgun Gothic", sans-serif;
  }}
  .stApp {{ background: {BG}; }}

  /* ---------- Hero ---------- */
  .ph-hero {{
      background: #fff; border-radius: 24px; padding: 40px 40px 28px;
      margin-bottom: 22px; border: 1px solid {BORDER};
  }}
  .ph-eyebrow {{
      font-size: 12px; font-weight: 700; letter-spacing: .18em; text-transform: uppercase;
      color: {RED}; margin-bottom: 14px;
  }}
  .ph-title {{
      font-size: clamp(30px, 4.5vw, 48px); font-weight: 300; letter-spacing: -0.01em;
      line-height: 1.2; color: {TEXT}; margin: 0 0 14px;
  }}
  .ph-title b {{ color: {RED}; font-weight: 300; }}
  .ph-sub {{ font-size: 15px; color: {TEXT_SECONDARY}; line-height: 1.6; margin: 0; }}

  /* ---------- Product cards ---------- */
  .ph-card {{
      background: #fff; border: 1px solid {BORDER}; border-radius: 18px;
      padding: 16px 16px 14px; height: 100%; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  }}
  .ph-cat-icon {{
      display:inline-flex; align-items:center; justify-content:center;
      width:38px; height:38px; border-radius:11px; font-size:19px;
      margin-bottom:10px;
  }}
  .ph-card-name {{ font-size: 14.5px; font-weight: 700; color:{TEXT}; margin:0 0 4px; line-height:1.35; }}
  .ph-card-vendor {{ font-size: 12px; color:{TEXT_SECONDARY}; margin:0 0 10px; }}
  .ph-tag-row {{ display:flex; flex-wrap:wrap; gap:6px; margin-bottom:10px; }}
  .ph-tag {{
      font-size:11px; font-weight:600; color:{TEXT_SECONDARY}; background:{BG};
      border-radius:999px; padding:3px 9px; border:1px solid {BORDER};
  }}
  .ph-price {{ font-size: 17px; font-weight: 800; color:{TEXT}; margin: 4px 0 2px; }}
  .ph-meta {{ font-size: 11.5px; color:{TEXT_SECONDARY}; margin:0 0 2px; }}
  .ph-note {{ font-size: 11px; color:{TEXT_SECONDARY}; font-style: italic; margin-top:6px; }}

  /* ---------- Vendor cards ---------- */
  .ph-vendor-card {{
      background:#fff; border:1px solid {BORDER}; border-radius:18px; padding:18px;
      height:100%;
  }}
  .ph-vendor-name {{ font-size:15px; font-weight:700; margin:0 0 4px; color:{TEXT}; }}
  .ph-vendor-site {{ font-size:12px; color:{RED}; margin:0 0 10px; }}
  .ph-vendor-count {{ font-size:12px; color:{TEXT_SECONDARY}; margin-top:8px; }}

  /* ---------- Sidebar tweaks ---------- */
  section[data-testid="stSidebar"] {{ background:#fff; }}
  .ph-filter-title {{
      font-size:12px; font-weight:700; color:{TEXT_SECONDARY}; text-transform:uppercase;
      letter-spacing:.03em; margin-top:6px;
  }}

  .ph-results-count {{ font-size:13px; color:{TEXT_SECONDARY}; margin-bottom:10px; }}
</style>
""", unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Session state
# ----------------------------------------------------------------------------
if "compare_ids" not in st.session_state:
    st.session_state.compare_ids = set()


def toggle_compare(pid):
    key = f"cmp_{pid}"
    if st.session_state.get(key):
        st.session_state.compare_ids.add(pid)
    else:
        st.session_state.compare_ids.discard(pid)


def reset_filters():
    st.session_state.f_search = ""
    st.session_state.f_categories = []
    st.session_state.f_materials = []
    st.session_state.f_finishes = []
    st.session_state.f_vendors = []
    st.session_state.f_price = PRICE_MAX


# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
hero_col1, hero_col2 = st.columns([1.4, 1], gap="large")
with hero_col1:
    st.markdown(f"""
    <div class="ph-hero" style="height:100%;">
      <p class="ph-eyebrow">COSMAX Design R&amp;I</p>
      <p class="ph-title">코스맥스,<br><b>Package Hub</b></p>
      <p class="ph-sub">흩어진 벤더 카탈로그를 한 곳에 모아,<br>조건 검색부터 스펙 비교까지<br>몇 번의 클릭으로 끝내는 통합 검색.</p>
    </div>
    """, unsafe_allow_html=True)
with hero_col2:
    img_cols = st.columns(3)
    hero_imgs = [
        (ASSETS_DIR / "hero_tall.jpg", "스킨케어 제품을 피부에 적용하는 모습"),
        (ASSETS_DIR / "hero_small.jpg", "용기 부자재 커넥터 클로즈업"),
        (ASSETS_DIR / "hero_wide.jpg", "뷰티 모델 클로즈업"),
    ]
    for c, (path, alt) in zip(img_cols, hero_imgs):
        if path.exists():
            c.image(str(path), use_container_width=True, caption=None)

st.write("")

# ----------------------------------------------------------------------------
# Tabs: search hub / vendor directory
# ----------------------------------------------------------------------------
tab_search, tab_vendors = st.tabs(["🔎 Package Hub", "🏭 등록 벤더"])

# ============================================================================
# TAB 1 — search & filter hub
# ============================================================================
with tab_search:
    # ---------------- Sidebar filters ----------------
    with st.sidebar:
        st.markdown("## 필터")
        st.button("초기화", on_click=reset_filters, use_container_width=False)

        search = st.text_input(
            "검색", key="f_search", placeholder="제품명, 재질, 벤더로 검색",
            label_visibility="collapsed",
        )

        st.markdown('<p class="ph-filter-title">카테고리</p>', unsafe_allow_html=True)
        sel_categories = st.multiselect(
            "카테고리", options=ALL_CATEGORIES, format_func=category_label,
            key="f_categories", label_visibility="collapsed",
        )

        st.markdown('<p class="ph-filter-title">재질</p>', unsafe_allow_html=True)
        sel_materials = st.multiselect(
            "재질", options=ALL_MATERIALS, key="f_materials", label_visibility="collapsed",
        )
        with st.expander("재질 특성 보기 (장점·단점·유의점)"):
            for m in ALL_MATERIALS:
                info = MATERIAL_INFO.get(m)
                if info:
                    st.markdown(f"**{m}**")
                    st.caption(f"👍 {info['장점']}")
                    st.caption(f"⚠️ {info['단점']}")
                    st.caption(f"🔎 {info['유의점']}")

        st.markdown('<p class="ph-filter-title">마감</p>', unsafe_allow_html=True)
        sel_finishes = st.multiselect(
            "마감", options=ALL_FINISHES, key="f_finishes", label_visibility="collapsed",
        )

        st.markdown('<p class="ph-filter-title">벤더</p>', unsafe_allow_html=True)
        sel_vendors = st.multiselect(
            "벤더", options=ALL_VENDORS, key="f_vendors", label_visibility="collapsed",
        )

        st.markdown('<p class="ph-filter-title">최대 단가</p>', unsafe_allow_html=True)
        price_max = st.slider(
            "최대 단가", min_value=PRICE_MIN, max_value=PRICE_MAX, value=PRICE_MAX,
            step=10, key="f_price", format="%d원", label_visibility="collapsed",
        )

    # ---------------- Apply filters ----------------
    filtered = df.copy()
    if search:
        q = search.lower()
        hay = (
            filtered["name"].str.lower() + " " +
            filtered["material"].str.lower() + " " +
            filtered["vendor"].str.lower() + " " +
            filtered["category"].str.lower() + " " +
            filtered["finish"].str.lower()
        )
        filtered = filtered[hay.str.contains(q, na=False)]
    if sel_categories:
        filtered = filtered[filtered["category"].isin(sel_categories)]
    if sel_materials:
        filtered = filtered[filtered["material"].isin(sel_materials)]
    if sel_finishes:
        filtered = filtered[filtered["finish"].isin(sel_finishes)]
    if sel_vendors:
        filtered = filtered[filtered["vendor"].isin(sel_vendors)]
    filtered = filtered[filtered["price_krw"] <= price_max]

    st.markdown(
        f'<p class="ph-results-count">총 <b>{len(filtered)}</b>개 제품 '
        f'(전체 {len(df)}개 중)</p>',
        unsafe_allow_html=True,
    )

    # ---------------- Compare tray ----------------
    compare_ids = st.session_state.compare_ids
    if compare_ids:
        tray_l, tray_r = st.columns([4, 1])
        with tray_l:
            st.info(f"🧮 비교함: {len(compare_ids)}개 선택됨")
        with tray_r:
            if st.button("비우기", use_container_width=True):
                for pid in list(compare_ids):
                    st.session_state.pop(f"cmp_{pid}", None)
                st.session_state.compare_ids = set()
                st.rerun()

        with st.expander(f"📊 스펙 비교 ({len(compare_ids)}개)", expanded=True):
            cmp_df = df[df["id"].isin(compare_ids)].copy()
            cmp_df["단가"] = cmp_df["price_krw"].apply(fmt_won)
            cmp_df["규격"] = cmp_df.apply(lambda r: f"{r['capacity_ml']}{r['unit']}", axis=1)
            show_cols = {
                "name": "제품명", "category": "카테고리", "vendor": "벤더",
                "material": "재질", "규격": "규격", "finish": "마감",
                "단가": "단가", "moq": "MOQ", "lead_time_days": "리드타임(일)",
            }
            cmp_df["category"] = cmp_df["category"].apply(category_label)
            st.dataframe(
                cmp_df.rename(columns=show_cols)[list(show_cols.values())],
                hide_index=True, use_container_width=True,
            )

    st.divider()

    # ---------------- Product grid ----------------
    N_COLS = 4
    rows = [filtered.iloc[i:i + N_COLS] for i in range(0, len(filtered), N_COLS)]

    if len(filtered) == 0:
        st.warning("조건에 맞는 제품이 없습니다. 필터를 조정해보세요.")

    for chunk in rows:
        cols = st.columns(N_COLS)
        for col, (_, p) in zip(cols, chunk.iterrows()):
            with col:
                color = CATEGORY_COLORS.get(p["category"], RED)
                icon = CATEGORY_ICONS.get(p["category"], "📦")
                note_html = f'<p class="ph-note">💬 {p["note"]}</p>' if p["note"] else ""
                st.markdown(f"""
                <div class="ph-card">
                  <div class="ph-cat-icon" style="background:{color};color:#fff;">{icon}</div>
                  <p class="ph-card-name">{p['name']}</p>
                  <p class="ph-card-vendor">{p['vendor']} · {p['vendor_site']}</p>
                  <div class="ph-tag-row">
                    <span class="ph-tag">{category_label(p['category'])}</span>
                    <span class="ph-tag">{p['material']}</span>
                    <span class="ph-tag">{p['capacity_ml']}{p['unit']}</span>
                    <span class="ph-tag">{p['finish']}</span>
                  </div>
                  <p class="ph-price">{fmt_won(p['price_krw'])}</p>
                  <p class="ph-meta">MOQ {int(p['moq']):,}개 · 리드타임 {int(p['lead_time_days'])}일</p>
                  {note_html}
                </div>
                """, unsafe_allow_html=True)
                st.checkbox(
                    "비교함에 추가", key=f"cmp_{p['id']}",
                    value=p["id"] in compare_ids,
                    on_change=toggle_compare, args=(p["id"],),
                )
        st.write("")

# ============================================================================
# TAB 2 — vendor directory
# ============================================================================
with tab_vendors:
    st.markdown(f"### 등록 벤더 · Package Hub와 함께하는 **{len(ALL_VENDORS)}**개 협력 벤더")
    st.write("")

    v_cols_per_row = 3
    vendor_chunks = [ALL_VENDORS[i:i + v_cols_per_row] for i in range(0, len(ALL_VENDORS), v_cols_per_row)]
    for chunk in vendor_chunks:
        cols = st.columns(v_cols_per_row)
        for col, vendor in zip(cols, chunk):
            v_items = df[df["vendor"] == vendor]
            site = v_items["vendor_site"].iloc[0]
            cats = sorted({category_label(c) for c in v_items["category"].unique()})
            with col:
                st.markdown(f"""
                <div class="ph-vendor-card">
                  <p class="ph-vendor-name">{vendor}</p>
                  <p class="ph-vendor-site">🌐 {site}</p>
                  <div class="ph-tag-row">
                    {''.join(f'<span class="ph-tag">{c}</span>' for c in cats)}
                  </div>
                  <p class="ph-vendor-count">등록 제품 <b>{len(v_items)}</b>종</p>
                </div>
                """, unsafe_allow_html=True)
        st.write("")
