import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title="Performance Étudiants",
    layout="wide"
)

FICHIER = "donnees.csv"

def charger_donnees():
    if os.path.exists(FICHIER):
        return pd.read_csv(FICHIER)
    return pd.DataFrame()

def get_mention(moyenne):
    if moyenne >= 18: return "Excellent"
    elif moyenne >= 16: return "Très Bien"
    elif moyenne >= 14: return "Bien"
    elif moyenne >= 12: return "Assez Bien"
    elif moyenne >= 10: return "Passable"
    else: return "Insuffisant"

st.markdown("""
<style>
    .main { background-color: #f0f4f8; }
    .stButton>button {
        background-color: #2c3e50;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: bold;
        width: 100%;
    }
    .stButton>button:hover { background-color: #3498db; }
    h1, h2, h3 { color: #2c3e50; }
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    .sidebar .sidebar-content { background-color: #2c3e50; }
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Performance Étudiants")
page = st.sidebar.radio("Navigation", [
    "Collecte des données",
    "Tableau de bord",
    "Courbes"
])

FILIERES = [
    "Informatique", "Génie Logiciel", "Réseaux & Télécommunications",
    "Génie Civil", "Génie Électrique", "Génie Mécanique",
    "Génie Industriel", "Génie Biomédical", "Intelligence Artificielle",
    "Médecine", "Pharmacie", "Droit", "Économie",
    "Mathématiques", "Physique", "BTS Informatique",
    "BTS Comptabilité", "BTS Commerce", "BTS Électronique",
    "BTS Maintenance Industrielle", "Autre"
]

NIVEAUX = ["BTS 1", "BTS 2", "L1", "L2", "L3", "M1", "M2", "Doctorat"]

DISTRACTIONS = [
    "Réseaux sociaux (Facebook, Instagram...)",
    "YouTube / Netflix / Séries",
    "Jeux vidéo",
    "Sorties / Fêtes",
    "Discussions / Bavardages",
    "Téléphone (appels/SMS)",
    "Aucune distraction majeure"
]

# ══════════════════════════════════════
# PAGE 1 : COLLECTE
# ══════════════════════════════════════
if page == "Collecte des données":
    st.title("Collecte des données")
    st.caption("Remplis le formulaire pour enregistrer ton profil étudiant.")

    with st.form("formulaire"):
        st.subheader("Informations personnelles")
        col1, col2 = st.columns(2)
        with col1:
            nom = st.text_input("Nom complet")
            age = st.number_input("Âge", min_value=15, max_value=45, value=20)
            niveau = st.selectbox("Niveau d'études", NIVEAUX)
        with col2:
            sexe = st.selectbox("Sexe", ["Masculin", "Féminin"])
            filiere = st.selectbox("Filière", FILIERES)
            acces_internet = st.selectbox("Accès internet", ["Oui", "Non"])

        st.subheader("Habitudes de travail")
        col3, col4 = st.columns(2)
        with col3:
            heures_etude = st.slider("Heures d'étude / jour", 0, 12, 4)
            heures_sommeil = st.slider("Heures de sommeil / nuit", 3, 10, 7)
        with col4:
            revisions = st.slider("Révisions / semaine", 0, 7, 3)
            heures_tel = st.slider("Heures sur téléphone / jour", 0, 16, 3)

        st.subheader("Distraction & Résultats")
        col5, col6 = st.columns(2)
        with col5:
            # UNE SEULE distraction (selectbox au lieu de multiselect)
            distraction = st.selectbox("Principale distraction", DISTRACTIONS)
        with col6:
            moyenne = st.number_input(
                "Moyenne générale /20",
                min_value=0.0, max_value=20.0, value=10.0, step=0.25
            )
            # Mention automatique affichée en temps réel
            mention_auto = get_mention(moyenne)
            st.info(f"Mention automatique : **{mention_auto}**")

        soumettre = st.form_submit_button("Enregistrer mes données")

    if soumettre:
        if nom.strip() == "":
            st.error("Veuillez entrer un nom !")
        else:
            mention = get_mention(moyenne)
            nouvelle_ligne = {
                "Nom": nom, "Âge": age, "Sexe": sexe,
                "Niveau": niveau, "Filière": filiere,
                "Accès internet": acces_internet,
                "Heures étude/jour": heures_etude,
                "Heures sommeil/nuit": heures_sommeil,
                "Révisions/semaine": revisions,
                "Heures téléphone/jour": heures_tel,
                "Distraction principale": distraction,
                "Moyenne/20": moyenne,
                "Mention": mention
            }
            df = charger_donnees()
            df = pd.concat([df, pd.DataFrame([nouvelle_ligne])], ignore_index=True)
            df.to_csv(FICHIER, index=False)
            st.success(f"Données de **{nom}** enregistrées ! Mention : **{mention}**")
            st.balloons()

# ══════════════════════════════════════
# PAGE 2 : TABLEAU DE BORD
# ══════════════════════════════════════
elif page == "Tableau de bord":
    st.title("Tableau de bord")
    df = charger_donnees()

    if df.empty:
        st.warning("Aucune donnée disponible. Commence par remplir le formulaire !")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Étudiants enregistrés", len(df))
        col2.metric("Moyenne générale", f"{df['Moyenne/20'].mean():.2f}/20")
        col3.metric("Moy. heures étude", f"{df['Heures étude/jour'].mean():.1f}h/j")
        col4.metric("Moy. heures téléphone", f"{df['Heures téléphone/jour'].mean():.1f}h/j")

        st.divider()
        st.subheader("Données collectées")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Télécharger les données CSV",
            csv, "donnees_etudiants.csv", "text/csv"
        )

# ══════════════════════════════════════
# PAGE 3 : COURBES
# ══════════════════════════════════════
elif page == "Courbes":
    st.title("Visualisations & Courbes")
    df = charger_donnees()

    if df.empty:
        st.warning("Aucune donnée disponible.")
    else:
        st.markdown("### Vue d'ensemble des performances")

        col1, col2 = st.columns(2)

        with col1:
            fig1 = px.histogram(
                df, x="Moyenne/20", nbins=10,
                title="Distribution des moyennes",
                color_discrete_sequence=["#3498db"],
                template="plotly_white"
            )
            fig1.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(size=13),
                title_font_size=16
            )
            st.plotly_chart(fig1, use_container_width=True)

            fig3 = px.pie(
                df, names="Filière",
                title="Répartition par filière",
                hole=0.4,
                template="plotly_white",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig3.update_layout(title_font_size=16)
            st.plotly_chart(fig3, use_container_width=True)

            fig5 = px.bar(
                df["Distraction principale"].value_counts().reset_index(),
                x="Distraction principale", y="count",
                title="Principales distractions",
                color="count",
                color_continuous_scale="Reds",
                template="plotly_white"
            )
            fig5.update_layout(title_font_size=16)
            st.plotly_chart(fig5, use_container_width=True)

        with col2:
            fig2 = px.scatter(
                df, x="Heures étude/jour", y="Moyenne/20",
                color="Filière", size_max=15,
                title="Heures d'étude vs Moyenne",
                trendline="ols",
                template="plotly_white"
            )
            fig2.update_layout(title_font_size=16)
            st.plotly_chart(fig2, use_container_width=True)

            fig4 = px.scatter(
                df, x="Heures téléphone/jour", y="Moyenne/20",
                color="Sexe",
                title="Temps téléphone vs Moyenne",
                trendline="ols",
                template="plotly_white",
                color_discrete_sequence=["#e74c3c", "#3498db"]
            )
            fig4.update_layout(title_font_size=16)
            st.plotly_chart(fig4, use_container_width=True)

            if len(df["Niveau"].unique()) > 1:
                fig6 = px.bar(
                    df.groupby("Niveau")["Moyenne/20"].mean().reset_index(),
                    x="Niveau", y="Moyenne/20",
                    title="Moyenne par niveau d'études",
                    color="Moyenne/20",
                    color_continuous_scale="Blues",
                    template="plotly_white"
                )
                fig6.update_layout(title_font_size=16)
                st.plotly_chart(fig6, use_container_width=True)
            else:
                st.info("Ajoute des étudiants de niveaux différents pour voir ce graphique.")