import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

st.set_page_config(
    page_title="GreenAssо — Gestion de l'association",
    page_icon="🌿",
    layout="wide"
)


# ── Données simulées ─────────────────────────────────────────
@st.cache_data
def generate_data():
    random.seed(42)

    benevoles = [
        {"nom": "Sophie Martin", "role": "Coordinatrice", "email": "sophie@asso.fr"},
        {"nom": "Jean Dupont", "role": "Terrain", "email": "jean@asso.fr"},
        {"nom": "Marie Leroy", "role": "Communication", "email": "marie@asso.fr"},
        {"nom": "Karim Benali", "role": "Terrain", "email": "karim@asso.fr"},
        {"nom": "Claire Petit", "role": "Logistique", "email": "claire@asso.fr"},
        {"nom": "Thomas Bernard", "role": "Terrain", "email": "thomas@asso.fr"},
        {"nom": "Lucie Moreau", "role": "Communication", "email": "lucie@asso.fr"},
        {"nom": "Ahmed Sidi", "role": "Terrain", "email": "ahmed@asso.fr"},
    ]

    projets = [
        {"nom": "Nettoyage Forêt de Sénart", "statut": "En cours", "avancement": 65, "responsable": "Sophie Martin",
         "debut": "2026-01-15", "fin": "2026-06-30"},
        {"nom": "Plantation Haies Bocagères", "statut": "En cours", "avancement": 40, "responsable": "Jean Dupont",
         "debut": "2026-02-01", "fin": "2026-07-31"},
        {"nom": "Sensibilisation Écoles", "statut": "Terminé", "avancement": 100, "responsable": "Marie Leroy",
         "debut": "2025-09-01", "fin": "2026-01-31"},
        {"nom": "Inventaire Biodiversité", "statut": "Planifié", "avancement": 0, "responsable": "Karim Benali",
         "debut": "2026-04-01", "fin": "2026-09-30"},
        {"nom": "Compostage Collectif", "statut": "En cours", "avancement": 80, "responsable": "Claire Petit",
         "debut": "2025-11-01", "fin": "2026-04-30"},
        {"nom": "Atelier Zéro Déchet", "statut": "Terminé", "avancement": 100, "responsable": "Lucie Moreau",
         "debut": "2025-10-01", "fin": "2025-12-31"},
    ]

    competences_list = ["Gestion de projet", "Communication", "Animation", "Terrain",
                        "Data", "Rédaction", "Logistique", "Réseaux sociaux", "Botanique"]

    benevoles_df = pd.DataFrame(benevoles)
    benevoles_df["competences_acquises"] = [
        random.sample(competences_list, random.randint(2, 5)) for _ in range(len(benevoles))
    ]
    benevoles_df["competences_en_cours"] = [
        random.sample(competences_list, random.randint(1, 3)) for _ in range(len(benevoles))
    ]
    benevoles_df["total_heures"] = [random.randint(20, 150) for _ in range(len(benevoles))]

    # Suivi des heures
    heures_data = []
    for _ in range(200):
        benevole = random.choice(benevoles)
        projet = random.choice(projets)
        date = datetime(2026, 1, 1) + timedelta(days=random.randint(0, 80))
        heures_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "benevole": benevole["nom"],
            "projet": projet["nom"],
            "heures": round(random.uniform(1, 8), 1),
            "tache": random.choice(["Terrain", "Réunion", "Communication", "Logistique", "Formation"]),
        })

    return pd.DataFrame(benevoles_df), pd.DataFrame(projets), pd.DataFrame(heures_data)


benevoles_df, projets_df, heures_df = generate_data()

# ── Style ────────────────────────────────────────────────────
st.markdown("""
<style>
    [data-testid="metric-container"] {
        background-color: #f0fff4;
        border: 1px solid #9ae6b4;
        border-radius: 12px;
        padding: 16px;
    }
    [data-testid="stMetricValue"] { color: #276749; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("# 🌿 GreenAssо — Tableau de bord")
st.markdown("**Gestion de projet & équipe · Association Environnement**")
st.markdown("---")

# ── Tabs ─────────────────────────────────────────────────────
tabs = st.tabs(["🏠 Vue globale", "📋 Projets", "⏱️ Heures", "👥 Bénévoles", "📊 Rapports"])

# ══ TAB 1 — VUE GLOBALE ══════════════════════════════════════
with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Bénévoles actifs", len(benevoles_df))
    col2.metric("Projets en cours", len(projets_df[projets_df["statut"] == "En cours"]))
    col3.metric("Heures totales 2026", f"{heures_df['heures'].sum():.0f}h")
    col4.metric("Projets terminés", len(projets_df[projets_df["statut"] == "Terminé"]))

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Statut des projets**")
        statut_counts = projets_df["statut"].value_counts().reset_index()
        fig = px.pie(statut_counts, values="count", names="statut",
                     hole=0.45, template="plotly_white",
                     color_discrete_map={"En cours": "#48BB78", "Terminé": "#2C5F2D", "Planifié": "#BEE3F8"})
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Avancement des projets**")
        fig = px.bar(projets_df.sort_values("avancement"),
                     x="avancement", y="nom", orientation="h",
                     template="plotly_white", color="avancement",
                     color_continuous_scale="Greens")
        fig.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

# ══ TAB 2 — PROJETS ══════════════════════════════════════════
with tabs[1]:
    st.markdown("**📋 Kanban des projets**")

    col1, col2, col3 = st.columns(3)
    statuts = {"Planifié": col1, "En cours": col2, "Terminé": col3}
    colors = {"Planifié": "#BEE3F8", "En cours": "#C6F6D5", "Terminé": "#C3DAFE"}

    for statut, col in statuts.items():
        with col:
            st.markdown(f"**{statut}** ({len(projets_df[projets_df['statut'] == statut])})")
            for _, p in projets_df[projets_df["statut"] == statut].iterrows():
                st.markdown(f"""
                <div style='background:{colors[statut]};padding:10px;border-radius:8px;margin:5px 0'>
                    <b>{p['nom']}</b><br>
                    👤 {p['responsable']}<br>
                    📅 {p['debut']} → {p['fin']}<br>
                    ⏩ {p['avancement']}%
                </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Détail des projets**")
    st.dataframe(projets_df, use_container_width=True)

# ══ TAB 3 — HEURES ═══════════════════════════════════════════
with tabs[2]:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Filtre bénévole**")
        benevole_sel = st.selectbox("Bénévole", ["Tous"] + list(benevoles_df["nom"]))
    with col2:
        st.markdown("**Filtre projet**")
        projet_sel = st.selectbox("Projet", ["Tous"] + list(projets_df["nom"]))

    heures_filtered = heures_df.copy()
    if benevole_sel != "Tous":
        heures_filtered = heures_filtered[heures_filtered["benevole"] == benevole_sel]
    if projet_sel != "Tous":
        heures_filtered = heures_filtered[heures_filtered["projet"] == projet_sel]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Heures par bénévole**")
        h_benv = heures_filtered.groupby("benevole")["heures"].sum().reset_index().sort_values("heures")
        fig = px.bar(h_benv, x="heures", y="benevole", orientation="h",
                     template="plotly_white", color="heures",
                     color_continuous_scale="Greens")
        fig.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Heures par projet**")
        h_proj = heures_filtered.groupby("projet")["heures"].sum().reset_index().sort_values("heures")
        fig = px.bar(h_proj, x="heures", y="projet", orientation="h",
                     template="plotly_white", color="heures",
                     color_continuous_scale="Greens")
        fig.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Évolution mensuelle des heures**")
    heures_filtered["mois"] = pd.to_datetime(heures_filtered["date"]).dt.strftime("%Y-%m")
    h_mois = heures_filtered.groupby("mois")["heures"].sum().reset_index()
    fig = px.line(h_mois, x="mois", y="heures", markers=True,
                  template="plotly_white", color_discrete_sequence=["#2C5F2D"])
    fig.update_layout(height=280)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Journal des heures**")
    st.dataframe(heures_filtered.sort_values("date", ascending=False), use_container_width=True)

# ══ TAB 4 — BÉNÉVOLES ════════════════════════════════════════
with tabs[3]:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Heures par bénévole**")
        fig = px.bar(benevoles_df.sort_values("total_heures"),
                     x="total_heures", y="nom", orientation="h",
                     template="plotly_white", color="total_heures",
                     color_continuous_scale="Greens")
        fig.update_layout(height=320, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("**Répartition par rôle**")
        role_counts = benevoles_df["role"].value_counts().reset_index()
        fig = px.pie(role_counts, values="count", names="role",
                     hole=0.45, template="plotly_white",
                     color_discrete_sequence=px.colors.sequential.Greens[::-1])
        fig.update_layout(height=320)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("**Fiches bénévoles**")
    for _, b in benevoles_df.iterrows():
        with st.expander(f"👤 {b['nom']} — {b['role']} — {b['total_heures']}h"):
            c1, c2, c3 = st.columns(3)
            c1.metric("Heures 2026", f"{b['total_heures']}h")
            c2.write(f"**Compétences acquises :**\n{', '.join(b['competences_acquises'])}")
            c3.write(f"**En cours d'apprentissage :**\n{', '.join(b['competences_en_cours'])}")

# ══ TAB 5 — RAPPORTS ═════════════════════════════════════════
with tabs[4]:
    st.markdown("**📊 Rapport mensuel automatique**")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total heures ce mois", f"{heures_df['heures'].sum():.0f}h")
    col2.metric("Bénévole le plus actif", heures_df.groupby("benevole")["heures"].sum().idxmax())
    col3.metric("Projet le plus chargé", heures_df.groupby("projet")["heures"].sum().idxmax())

    st.markdown("---")
    st.markdown("**Synthèse par projet**")
    synthese = heures_df.groupby("projet").agg(
        heures_totales=("heures", "sum"),
        nb_benevoles=("benevole", "nunique"),
        nb_sessions=("heures", "count")
    ).reset_index().sort_values("heures_totales", ascending=False)
    synthese["heures_totales"] = synthese["heures_totales"].round(1)
    st.dataframe(synthese, use_container_width=True)

    st.markdown("**Compétences les plus développées**")
    all_comp = []
    for comps in benevoles_df["competences_acquises"]:
        all_comp.extend(comps)
    comp_df = pd.Series(all_comp).value_counts().reset_index()
    comp_df.columns = ["competence", "nb_benevoles"]
    fig = px.bar(comp_df, x="competence", y="nb_benevoles",
                 template="plotly_white", color="nb_benevoles",
                 color_continuous_scale="Greens")
    fig.update_layout(height=300, showlegend=False, xaxis_tickangle=-20)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("*🌿 GreenAssо · Gestion de projet & équipe · Rafika Cervera*")