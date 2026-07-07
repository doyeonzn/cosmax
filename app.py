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
CATEGORY_ORDER = ["용기", "자", "펌프", "튜브", "캡", "스포이드", "콤팩트", "스틱", "견본용기"]

CATEGORY_LABELS = {
    "용기": "용기 Bottle",
    "자": "자 Jar",
    "펌프": "펌프 Pump",
    "튜브": "튜브 Tube",
    "캡": "캡 Cap",
    "스포이드": "스포이드 Dropper",
    "콤팩트": "콤팩트 Compact",
    "스틱": "스틱 Stick",
    "견본용기": "견본용기 Sample",
}

CATEGORY_ICONS = {
    "용기": "🍼", "자": "🫙", "펌프": "🧪", "튜브": "🧴", "캡": "🧢",
    "스포이드": "🩸", "콤팩트": "🎨", "스틱": "🖊️", "견본용기": "🧫",
}

# tone-on-tone from the COSMAX brand red, darkest for categories further down the list
CATEGORY_COLORS = {
    "용기": "#EA1D22",
    "자": "#CC1B24",
    "펌프": "#AD1820",
    "튜브": "#8F141C",
    "캡": "#711018",
    "스포이드": "#4D0B10",
    "콤팩트": "#B5474C",
    "스틱": "#8C5257",
    "견본용기": "#6B3A3D",
}

MATERIAL_INFO = {
    "PET": {"장점": "가볍고 투명도가 높아 내용물 시각적 어필에 유리, 단가 경쟁력이 좋음",
            "단점": "내열성이 낮아 고온 충전·살균 공정에 취약",
            "유의점": "고농도 오일·알코올 성분에서 크랙(변형) 발생 가능성 유의"},
    "PCR-PET": {"장점": "재생 원료 사용으로 ESG·친환경 어필에 강점",
                "단점": "원료 수급에 따라 색상 편차 발생 가능, 일반 PET보다 단가 높음",
                "유의점": "재생 원료 비율(%)에 따라 투명도·강도 차이가 있어 사전 확인 필요"},
    "유리": {"장점": "고급스러운 질감과 내화학성이 뛰어나 프리미엄 라인에 적합",
             "단점": "무게가 무겁고 파손 위험이 있어 물류비·파손율 증가",
             "유의점": "낙하·충격에 약하므로 배송 및 진열 시 완충 포장 필수"},
    "알루미늄": {"장점": "차광성이 우수해 광분해에 취약한 성분 보호에 유리, 재활용 용이",
               "단점": "내부 코팅 없이는 내용물과 반응 가능, 상대적으로 단가 높음",
               "유의점": "산성·알칼리성 포뮬러는 내부 라이닝 코팅 사양 확인 필요"},
    "PP": {"장점": "내약품성이 우수하고 유연해 다양한 캡·자 구조에 적용 가능",
           "단점": "투명도가 PET 대비 낮아 내용물 노출 디자인에는 한계",
           "유의점": "고온 충전 시 변형 가능성이 있어 충전 온도 스펙 확인 필요"},
    "PETG": {"장점": "PET보다 투명도와 광택이 우수해 고급스러운 룩 연출 가능",
             "단점": "PET 대비 단가가 높고 내열성은 유사하게 낮음",
             "유의점": "재활용 등급이 PET와 달라 분리배출 표기 확인 필요"},
    "AS": {"장점": "투명도와 광택이 뛰어나 펌프·캡 등 정밀 부품에 적합",
           "단점": "내충격성이 약해 반복 낙하 시 크랙 발생 가능",
           "유의점": "일부 향료·오일 성분과 접촉 시 백화(크레이징) 현상 유의"},
    "PE": {"장점": "유연성이 좋아 튜브형 용기에 적합, 내용물 짜내기 용이",
           "단점": "투명도가 낮고 인쇄 발색이 PET 대비 제한적",
           "유의점": "얇은 두께 설계 시 내용물 압력에 의한 변형 가능성 확인 필요"},
    "ABS": {"장점": "강도와 치수 안정성이 높아 캡·뚜껑 구조물에 적합",
            "단점": "내용물과 직접 접촉 시 화학적 반응 가능성 있어 이너캡이 필요할 수 있음",
            "유의점": "도금·메탈릭 마감 적용 시 도금층 박리 여부 사전 테스트 권장"},
    "PCTG": {"장점": "PETG와 비슷한 투명도에 내충격성이 더 우수해 파손 위험이 낮음",
             "단점": "PET·PP 대비 원재료 단가가 높은 편",
             "유의점": "재활용 등급이 별도로 분류되어 분리배출 표기 확인 필요"},
}

VENDOR_INFO = {
    "그린패키징": {"location": "경기 김포시", "specialty": "친환경 소재 전문, PCR·PETG 용기 특화"},
    "에코팩코리아": {"location": "인천 서구", "specialty": "재생 플라스틱 기반 용기 제조"},
    "코스텍글라스": {"location": "경기 파주시", "specialty": "유리 용기·스포이드 전문 생산"},
    "메탈크래프트": {"location": "경기 안산시", "specialty": "알루미늄·메탈릭 마감 부자재 전문"},
    "베스트팩": {"location": "경기 부천시", "specialty": "범용 자·병 OEM 다품종 소량생산"},
    "펌프텍": {"location": "경기 화성시", "specialty": "디스펜서 펌프 헤드 전문 제조"},
    "튜브월드": {"location": "충남 아산시", "specialty": "튜브 용기 전문, 다양한 노즐 옵션"},
    "코스맥스 프리몰드": {"location": "경기 오산시", "specialty": "자유 사용 금형 기반 범용 용기 (중국 생산)"},
    "코스맥스 익스클루시브": {"location": "경기 화성시", "specialty": "코스맥스 단독 개발·보유 전용 용기"},
    "연우": {"location": "인천 남동구", "specialty": "국내 최대급 화장품 용기 종합 벤더"},
    "삼화": {"location": "경기 시흥시", "specialty": "콤팩트·스틱 케이스 전문"},
    "펌텍코리아": {"location": "인천 서구", "specialty": "펌프·디스펜서 시스템 글로벌 공급"},
    "태성산업": {"location": "경기 안성시", "specialty": "범용 자·병 사출 성형 전문"},
    "코드": {"location": "경기 광주시", "specialty": "베이직 라인 용기 OEM"},
    "퍼펙트글라스": {"location": "충북 청주시", "specialty": "프리미엄 유리 용기 전문"},
    "성신패키지": {"location": "경기 평택시", "specialty": "유리 자·향수병 특화 생산"},
    "코스팜": {"location": "경기 화성시", "specialty": "펌프·디스펜서 보틀 종합 제조"},
    "코스PNC": {"location": "경기 김포시", "specialty": "메탈릭 마감 특화 용기·자"},
    "유미코스": {"location": "인천 남동구", "specialty": "범용 용기·튜브·스포이드 종합"},
}

# ----------------------------------------------------------------------------
# Product catalog (id, name, category, material, capacity, finish, vendor,
# price, lead_time; unit defaults to "ml" unless overridden, e.g. compact/
# stick items sold by gram weight)
# ----------------------------------------------------------------------------
PRODUCTS = [
    {"id": 1, "name": "라운드 PET 보틀 100", "category": "용기", "material": "PET", "capacity": 100, "finish": "유광", "vendor": "그린패키징", "price": 320, "lead_time": 14},
    {"id": 2, "name": "PCR 스퀘어 보틀 150", "category": "용기", "material": "PCR-PET", "capacity": 150, "finish": "무광", "vendor": "에코팩코리아", "price": 480, "lead_time": 21},
    {"id": 3, "name": "글라스 보틀 50 클리어", "category": "용기", "material": "유리", "capacity": 50, "finish": "투명", "vendor": "코스텍글라스", "price": 650, "lead_time": 30},
    {"id": 4, "name": "알루미늄 슬림 보틀 250", "category": "용기", "material": "알루미늄", "capacity": 250, "finish": "메탈릭", "vendor": "메탈크래프트", "price": 890, "lead_time": 35},
    {"id": 5, "name": "크림 자 30 무광화이트", "category": "자", "material": "PP", "capacity": 30, "finish": "무광", "vendor": "베스트팩", "price": 210, "lead_time": 10},
    {"id": 6, "name": "글라스 자 50 프로스티드", "category": "자", "material": "유리", "capacity": 50, "finish": "프로스티드", "vendor": "코스텍글라스", "price": 720, "lead_time": 28},
    {"id": 7, "name": "PETG 투명 자 100", "category": "자", "material": "PETG", "capacity": 100, "finish": "투명", "vendor": "그린패키징", "price": 380, "lead_time": 18},
    {"id": 8, "name": "에어리스 펌프 30", "category": "펌프", "material": "AS", "capacity": 30, "finish": "유광", "vendor": "펌프텍", "price": 560, "lead_time": 20},
    {"id": 9, "name": "로션 펌프 보틀 150", "category": "펌프", "material": "PP", "capacity": 150, "finish": "반광", "vendor": "펌프텍", "price": 430, "lead_time": 16},
    {"id": 10, "name": "포밍 펌프 보틀 200", "category": "펌프", "material": "PET", "capacity": 200, "finish": "무광", "vendor": "베스트팩", "price": 390, "lead_time": 15},
    {"id": 11, "name": "알루미늄 튜브 50", "category": "튜브", "material": "알루미늄", "capacity": 50, "finish": "메탈릭", "vendor": "메탈크래프트", "price": 340, "lead_time": 22},
    {"id": 12, "name": "라미튜브 100 무광", "category": "튜브", "material": "PE", "capacity": 100, "finish": "무광", "vendor": "튜브월드", "price": 260, "lead_time": 12},
    {"id": 13, "name": "클리어 튜브 30", "category": "튜브", "material": "PETG", "capacity": 30, "finish": "투명", "vendor": "튜브월드", "price": 190, "lead_time": 9},
    {"id": 14, "name": "스크류 캡 골드", "category": "캡", "material": "ABS", "capacity": 0, "finish": "메탈릭", "vendor": "메탈크래프트", "price": 95, "lead_time": 7},
    {"id": 15, "name": "디스크탑 캡 화이트", "category": "캡", "material": "PP", "capacity": 0, "finish": "유광", "vendor": "베스트팩", "price": 60, "lead_time": 6},
    {"id": 16, "name": "유리 스포이드 30", "category": "스포이드", "material": "유리", "capacity": 30, "finish": "투명", "vendor": "코스텍글라스", "price": 410, "lead_time": 19},
    {"id": 17, "name": "스퀘어 크림 자 50 무광블랙", "category": "자", "material": "PP", "capacity": 50, "finish": "무광", "vendor": "코스맥스 프리몰드", "price": 240, "lead_time": 12},
    {"id": 18, "name": "라운드 자 100 유광화이트", "category": "자", "material": "ABS", "capacity": 100, "finish": "유광", "vendor": "코스맥스 프리몰드", "price": 260, "lead_time": 11},
    {"id": 19, "name": "미니 보틀 30 투명", "category": "용기", "material": "PETG", "capacity": 30, "finish": "투명", "vendor": "코스맥스 프리몰드", "price": 150, "lead_time": 9},
    {"id": 20, "name": "스프레이 보틀 100 무광그레이", "category": "용기", "material": "PP", "capacity": 100, "finish": "무광", "vendor": "코스맥스 익스클루시브", "price": 410, "lead_time": 24},
    {"id": 21, "name": "디스펜서 보틀 200 반광", "category": "용기", "material": "PET", "capacity": 200, "finish": "반광", "vendor": "코스맥스 익스클루시브", "price": 470, "lead_time": 20},
    {"id": 22, "name": "코받침 로션펌프 30", "category": "펌프", "material": "PP", "capacity": 30, "finish": "무광", "vendor": "코스맥스 프리몰드", "price": 310, "lead_time": 14},
    {"id": 23, "name": "듀얼챔버 펌프 100", "category": "펌프", "material": "AS", "capacity": 100, "finish": "유광", "vendor": "코스맥스 익스클루시브", "price": 680, "lead_time": 26},
    {"id": 24, "name": "미니 펌프 50 화이트", "category": "펌프", "material": "PP", "capacity": 50, "finish": "무광", "vendor": "베스트팩", "price": 300, "lead_time": 13},
    {"id": 25, "name": "스퀴즈 튜브 150 유광", "category": "튜브", "material": "PE", "capacity": 150, "finish": "유광", "vendor": "튜브월드", "price": 300, "lead_time": 14},
    {"id": 26, "name": "알루미늄 튜브 30 메탈릭골드", "category": "튜브", "material": "알루미늄", "capacity": 30, "finish": "메탈릭", "vendor": "메탈크래프트", "price": 290, "lead_time": 20},
    {"id": 27, "name": "하이바디 튜브 200 무광", "category": "튜브", "material": "PE", "capacity": 200, "finish": "무광", "vendor": "코스맥스 프리몰드", "price": 330, "lead_time": 16},
    {"id": 28, "name": "원터치 캡 실버", "category": "캡", "material": "ABS", "capacity": 0, "finish": "메탈릭", "vendor": "메탈크래프트", "price": 110, "lead_time": 8},
    {"id": 29, "name": "플립탑 캡 클리어", "category": "캡", "material": "PP", "capacity": 0, "finish": "투명", "vendor": "코스맥스 프리몰드", "price": 70, "lead_time": 6},
    {"id": 30, "name": "스포이드 펜슬타입 50", "category": "스포이드", "material": "유리", "capacity": 50, "finish": "투명", "vendor": "코스텍글라스", "price": 460, "lead_time": 21},
    {"id": 31, "name": "라운드 PP 자 40", "category": "자", "material": "PP", "capacity": 40, "finish": "유광", "vendor": "연우", "price": 565, "lead_time": 12},
    {"id": 32, "name": "에어리스 PCTG 자 50", "category": "자", "material": "PCTG", "capacity": 50, "finish": "유광", "vendor": "연우", "price": 1350, "lead_time": 20},
    {"id": 33, "name": "라운드 PET 보틀 135", "category": "용기", "material": "PET", "capacity": 135, "finish": "투명", "vendor": "연우", "price": 375, "lead_time": 16},
    {"id": 34, "name": "스퀴즈 PP 튜브 75", "category": "튜브", "material": "PP", "capacity": 75, "finish": "유광", "vendor": "연우", "price": 265, "lead_time": 13},
    {"id": 35, "name": "트라이얼 견본용기 5", "category": "견본용기", "material": "PP", "capacity": 5, "finish": "투명", "vendor": "연우", "price": 120, "lead_time": 8},
    {"id": 36, "name": "로션 펌프 보틀 90", "category": "펌프", "material": "PP", "capacity": 90, "finish": "무광", "vendor": "연우", "price": 965, "lead_time": 15},
    {"id": 37, "name": "쿠션 콤팩트 13g", "category": "콤팩트", "material": "ABS", "capacity": 13, "unit": "g", "finish": "유광", "vendor": "삼화", "price": 1340, "lead_time": 24},
    {"id": 38, "name": "미니 PP 자 6", "category": "자", "material": "PP", "capacity": 6, "finish": "투명", "vendor": "삼화", "price": 345, "lead_time": 10},
    {"id": 39, "name": "메탈릭 스틱 3.5g", "category": "스틱", "material": "ABS", "capacity": 3.5, "unit": "g", "finish": "메탈릭", "vendor": "삼화", "price": 720, "lead_time": 14},
    {"id": 40, "name": "포밍 펌프 보틀 175", "category": "펌프", "material": "PP", "capacity": 175, "finish": "무광", "vendor": "펌텍코리아", "price": 755, "lead_time": 17},
    {"id": 41, "name": "슬림 PP 튜브 40", "category": "튜브", "material": "PP", "capacity": 40, "finish": "유광", "vendor": "펌텍코리아", "price": 285, "lead_time": 13},
    {"id": 42, "name": "투웨이 콤팩트 10g", "category": "콤팩트", "material": "PP", "capacity": 10, "unit": "g", "finish": "유광", "vendor": "펌텍코리아", "price": 890, "lead_time": 22},
    {"id": 43, "name": "글라스 스포이드 22", "category": "스포이드", "material": "유리", "capacity": 22, "finish": "투명", "vendor": "펌텍코리아", "price": 720, "lead_time": 26},
    {"id": 44, "name": "글로시 스틱 5g", "category": "스틱", "material": "PP", "capacity": 5, "unit": "g", "finish": "유광", "vendor": "펌텍코리아", "price": 560, "lead_time": 12},
    {"id": 45, "name": "스프레이 캔 보틀 100", "category": "용기", "material": "알루미늄", "capacity": 100, "finish": "메탈릭", "vendor": "펌텍코리아", "price": 980, "lead_time": 28},
    {"id": 46, "name": "라운드 PP 자 75", "category": "자", "material": "PP", "capacity": 75, "finish": "유광", "vendor": "태성산업", "price": 510, "lead_time": 13},
    {"id": 47, "name": "라운드 PET 보틀 125", "category": "용기", "material": "PET", "capacity": 125, "finish": "투명", "vendor": "태성산업", "price": 355, "lead_time": 15},
    {"id": 48, "name": "베이직 PP 자 40", "category": "자", "material": "PP", "capacity": 40, "finish": "유광", "vendor": "코드", "price": 415, "lead_time": 11},
    {"id": 49, "name": "베이직 PET 보틀 130", "category": "용기", "material": "PET", "capacity": 130, "finish": "투명", "vendor": "코드", "price": 370, "lead_time": 12},
    {"id": 50, "name": "글라스 보틀 65 클리어", "category": "용기", "material": "유리", "capacity": 65, "finish": "투명", "vendor": "퍼펙트글라스", "price": 970, "lead_time": 27},
    {"id": 51, "name": "크림 글라스 자 75g", "category": "자", "material": "유리", "capacity": 75, "unit": "g", "finish": "유광", "vendor": "성신패키지", "price": 1250, "lead_time": 29},
    {"id": 52, "name": "향수병 50 클리어", "category": "용기", "material": "유리", "capacity": 50, "finish": "투명", "vendor": "성신패키지", "price": 1240, "lead_time": 30},
    {"id": 53, "name": "로션 펌프 보틀 200", "category": "펌프", "material": "PP", "capacity": 200, "finish": "유광", "vendor": "코스팜", "price": 650, "lead_time": 18},
    {"id": 54, "name": "디스펜서 보틀 200", "category": "용기", "material": "PET", "capacity": 200, "finish": "투명", "vendor": "코스팜", "price": 420, "lead_time": 14},
    {"id": 55, "name": "메탈릭 PP 자 40", "category": "자", "material": "PP", "capacity": 40, "finish": "메탈릭", "vendor": "코스PNC", "price": 565, "lead_time": 19},
    {"id": 56, "name": "글라스 보틀 150 유광", "category": "용기", "material": "유리", "capacity": 150, "finish": "유광", "vendor": "코스PNC", "price": 1180, "lead_time": 25},
    {"id": 57, "name": "라운드 PP 보틀 100", "category": "용기", "material": "PP", "capacity": 100, "finish": "유광", "vendor": "유미코스", "price": 710, "lead_time": 16},
    {"id": 58, "name": "하이바디 PP 튜브 120", "category": "튜브", "material": "PP", "capacity": 120, "finish": "무광", "vendor": "유미코스", "price": 320, "lead_time": 14},
    {"id": 59, "name": "PCTG 스포이드 20", "category": "스포이드", "material": "PCTG", "capacity": 20, "finish": "무광", "vendor": "유미코스", "price": 610, "lead_time": 18},
]


# ----------------------------------------------------------------------------
# Data loading
# ----------------------------------------------------------------------------
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.DataFrame(PRODUCTS)
    df["unit"] = df["unit"].fillna("ml") if "unit" in df else "ml"
    return df


df = load_data()

ALL_CATEGORIES = [c for c in CATEGORY_ORDER if c in df["category"].unique()]
ALL_MATERIALS = sorted(df["material"].unique())
ALL_FINISHES = sorted(df["finish"].unique())
ALL_VENDORS = sorted(df["vendor"].unique())
PRICE_MIN = int(df["price"].min())
PRICE_MAX = int(df["price"].max())


def fmt_won(n) -> str:
    return f"{int(n):,}원"


def category_label(c: str) -> str:
    return CATEGORY_LABELS.get(c, c)


def capacity_text(row) -> str:
    if row["capacity"] <= 0:
        return "-"
    cap = row["capacity"]
    cap_str = f"{cap:g}"
    return f"{cap_str}{row['unit']}"


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

  /* ---------- Vendor cards ---------- */
  .ph-vendor-card {{
      background:#fff; border:1px solid {BORDER}; border-radius:18px; padding:18px;
      height:100%;
  }}
  .ph-vendor-name {{ font-size:15px; font-weight:700; margin:0 0 4px; color:{TEXT}; }}
  .ph-vendor-location {{ font-size:12px; color:{RED}; margin:0 0 8px; }}
  .ph-vendor-specialty {{ font-size:12.5px; color:{TEXT}; line-height:1.5; margin:0 0 10px; }}
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
    filtered = filtered[filtered["price"] <= price_max]

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
            cmp_df["단가"] = cmp_df["price"].apply(fmt_won)
            cmp_df["규격"] = cmp_df.apply(capacity_text, axis=1)
            show_cols = {
                "name": "제품명", "category": "카테고리", "vendor": "벤더",
                "material": "재질", "규격": "규격", "finish": "마감",
                "단가": "단가", "lead_time": "리드타임(일)",
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
                st.markdown(f"""
                <div class="ph-card">
                  <div class="ph-cat-icon" style="background:{color};color:#fff;">{icon}</div>
                  <p class="ph-card-name">{p['name']}</p>
                  <p class="ph-card-vendor">{p['vendor']}</p>
                  <div class="ph-tag-row">
                    <span class="ph-tag">{category_label(p['category'])}</span>
                    <span class="ph-tag">{p['material']}</span>
                    <span class="ph-tag">{capacity_text(p)}</span>
                    <span class="ph-tag">{p['finish']}</span>
                  </div>
                  <p class="ph-price">{fmt_won(p['price'])}</p>
                  <p class="ph-meta">리드타임 {int(p['lead_time'])}일</p>
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
            info = VENDOR_INFO.get(vendor, {"location": "-", "specialty": "등록된 소개 정보가 없습니다."})
            cats = sorted({category_label(c) for c in v_items["category"].unique()})
            with col:
                st.markdown(f"""
                <div class="ph-vendor-card">
                  <p class="ph-vendor-name">{vendor}</p>
                  <p class="ph-vendor-location">📍 {info['location']}</p>
                  <p class="ph-vendor-specialty">{info['specialty']}</p>
                  <div class="ph-tag-row">
                    {''.join(f'<span class="ph-tag">{c}</span>' for c in cats)}
                  </div>
                  <p class="ph-vendor-count">등록 제품 <b>{len(v_items)}</b>종</p>
                </div>
                """, unsafe_allow_html=True)
        st.write("")
