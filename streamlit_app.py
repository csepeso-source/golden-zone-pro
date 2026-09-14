"""
═══════════════════════════════════════════════════════
GOLDEN ZONE PRO - Streamlit Edition
Corner Prediction System
═══════════════════════════════════════════════════════
"""

import streamlit as st
import pandas as pd
import numpy as np

# ═══════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════
st.set_page_config(
    page_title="Golden Zone Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════
# HEADER
# ═══════════════════════════════════════
st.title("🎯 Golden Zone Pro")
st.markdown("### Corner Prediction System")
st.markdown("---")

# ═══════════════════════════════════════
# SIDEBAR - INPUT
# ═══════════════════════════════════════
with st.sidebar:
    st.header("📋 Meccs Adatok")
    
    # Liga választás
    liga_dict = {
        "Brazil Serie A": {"avg": 10.21, "flag": "🇧🇷"},
        "Olasz Serie A": {"avg": 9.25, "flag": "🇮🇹"},
        "Francia Ligue 1": {"avg": 9.48, "flag": "🇫🇷"},
        "Holland Eredivisie": {"avg": 10.31, "flag": "🇳🇱"}
    }
    
    liga = st.selectbox(
        "Liga",
        list(liga_dict.keys()),
        format_func=lambda x: f"{liga_dict[x]['flag']} {x}"
    )
    
    st.markdown("---")
    
    # Csapatok
    st.subheader("Csapatok")
    home_team = st.text_input("Hazai csapat", placeholder="pl. Flamengo")
    away_team = st.text_input("Vendég csapat", placeholder="pl. Palmeiras")
    
    st.markdown("---")
    
    # Forma (egyszerűsített)
    st.subheader("⚙️ Forma")
    st.caption("(Liga átlag ha nem tudod)")
    
    liga_avg = liga_dict[liga]["avg"]
    
    hazai_forma = st.number_input(
        "Hazai szöglet átlag",
        min_value=0.0,
        max_value=20.0,
        value=liga_avg,
        step=0.5
    )
    
    vendeg_forma = st.number_input(
        "Vendég szöglet átlag",
        min_value=0.0,
        max_value=20.0,
        value=liga_avg,
        step=0.5
    )
    
    st.markdown("---")
    
    # Odds
    st.subheader("💰 Odds")
    
    pinnacle_line = st.number_input(
        "Pinnacle vonal",
        min_value=5.5,
        max_value=20.5,
        value=11.5,
        step=0.5
    )
    
    col1, col2 = st.columns(2)
    with col1:
        over_odds = st.number_input("Over", min_value=1.01, value=1.90, step=0.01)
    with col2:
        under_odds = st.number_input("Under", min_value=1.01, value=1.90, step=0.01)
    
    st.markdown("---")
    
    # SUBMIT BUTTON
    predict_btn = st.button("🔮 Előrejelzés", type="primary", use_container_width=True)

# ═══════════════════════════════════════
# MAIN AREA - RESULTS
# ═══════════════════════════════════════

if predict_btn:
    if not home_team or not away_team:
        st.error("❌ Add meg mindkét csapatot!")
    else:
        # EGYSZERŰ MODELL (sigmoid alapú becslés)
        # Később: betöltjük a valódi RandomForest-et
        
        # Feature számítás
        expected_corners = (hazai_forma + vendeg_forma) / 2 + np.random.uniform(-0.5, 0.5)
        
        # Sigmoid valószínűség
        def sigmoid_prob(pred, line, direction='over'):
            if direction == 'over':
                diff = pred - line - 0.5
            else:
                diff = line + 0.5 - pred
            return 1 / (1 + np.exp(-diff * 1.5))
        
        prob_over = sigmoid_prob(expected_corners, pinnacle_line, 'over')
        prob_under = sigmoid_prob(expected_corners, pinnacle_line, 'under')
        
        # ═══════════════════════════════════════
        # EREDMÉNY MEGJELENÍTÉS
        # ═══════════════════════════════════════
        
        st.success("✅ Előrejelzés kész!")
        
        # Metric cards
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "📊 Modell előrejelzés",
                f"{expected_corners:.2f}",
                delta=f"{expected_corners - pinnacle_line:+.2f} vs vonal"
            )
        
        with col2:
            st.metric(
                "📈 OVER valószínűség",
                f"{prob_over*100:.1f}%",
                delta=f"{over_odds:.2f} odds"
            )
        
        with col3:
            st.metric(
                "📉 UNDER valószínűség",
                f"{prob_under*100:.1f}%",
                delta=f"{under_odds:.2f} odds"
            )
        
        st.markdown("---")
        
        # Részletes elemzés
        st.subheader("📋 Részletes Elemzés")
        
        # Táblázat
        analysis_df = pd.DataFrame({
            'Típus': ['OVER', 'UNDER'],
            'Vonal': [f'{pinnacle_line}', f'{pinnacle_line}'],
            'Modell %': [f'{prob_over*100:.1f}%', f'{prob_under*100:.1f}%'],
            'Piac Odds': [over_odds, under_odds],
            'Piac %': [f'{(1/over_odds)*100:.1f}%', f'{(1/under_odds)*100:.1f}%'],
        })
        
        st.dataframe(analysis_df, use_container_width=True, hide_index=True)
        
        # Ajánlás
        st.markdown("---")
        st.subheader("💡 Ajánlás")
        
        if prob_over > prob_under:
            tip = "OVER"
            tip_prob = prob_over * 100
            tip_odds = over_odds
        else:
            tip = "UNDER"
            tip_prob = prob_under * 100
            tip_odds = under_odds
        
        # Value számítás
        fair_odds = 1 / (tip_prob / 100)
        value = ((tip_odds - 1) / (fair_odds - 1) - 1) * 100
        
        if value > 5:
            st.success(f"✅ **{tip} {pinnacle_line}** @ {tip_odds} ({tip_prob:.1f}% | Value: +{value:.1f}%)")
        elif value > 0:
            st.info(f"⚠️ **{tip} {pinnacle_line}** @ {tip_odds} ({tip_prob:.1f}% | Kicsi value: +{value:.1f}%)")
        else:
            st.warning(f"❌ **{tip} {pinnacle_line}** @ {tip_odds} ({tip_prob:.1f}% | Negatív value: {value:.1f}%)")
        
        # Golden Zone check (egyszerűsített)
        st.markdown("---")
        st.subheader("🏆 Golden Zone")
        
        if 80 <= tip_prob < 85:
            st.success("🔥 GOLDEN ZONE TALÁLAT! (80-85%)")
            st.caption("Backtest: Brazil 11.5 UNDER → 49 tipp, 83.7% találat")
        elif tip_prob >= 75:
            st.info("✅ Jó zóna (75%+)")
        else:
            st.warning("⚠️ Nincs golden zone találat")

else:
    # Alapértelmezett üzenet
    st.info("👈 Töltsd ki a bal oldali menüt és nyomd meg az 'Előrejelzés' gombot!")
    
    # Golden Zone lista
    st.markdown("---")
    st.subheader("🏆 Top Golden Zone-ok")
    
    golden_zones = pd.DataFrame({
        'Liga': ['🇧🇷 Brazil', '🇧🇷 Brazil', '🇮🇹 Olasz', '🇮🇹 Olasz', '🇳🇱 Holland'],
        'Vonal': ['11.5', '10.5', '11.5', '12.5', '12.5'],
        'Típus': ['UNDER', 'UNDER', 'UNDER', 'UNDER', 'UNDER'],
        'Zóna': ['80-85%', '80-85%', '85-90%', '90-95%', '90-95%'],
        'Találat': ['83.7%', '100%', '83.0%', '100%', '75.6%'],
        'Tippek': [49, 6, 47, 7, 45]
    })
    
    st.dataframe(golden_zones, use_container_width=True, hide_index=True)

# Footer
st.markdown("---")
st.caption("Golden Zone Pro v1.0 | Corner Prediction System")
