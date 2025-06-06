import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Fonction de simulation DCA avec GBM
def simulate_dca(capital_initial, investissement_mensuel, nb_annees, proba_defaut_epargne, nb_simulations, mu_annual, sigma_annual):
    nb_mois = nb_annees * 12
    drift = (mu_annual - 0.5 * sigma_annual ** 2) / 12
    diffusion = sigma_annual / np.sqrt(12)

    simulations = np.zeros((nb_simulations, nb_mois + 1))
    simulations[:, 0] = capital_initial

    for i in range(1, nb_mois + 1):
        rendements = np.exp(drift + diffusion * np.random.normal(size=nb_simulations)) - 1
        defauts = np.random.rand(nb_simulations) < proba_defaut_epargne
        apports = np.where(defauts, 0, investissement_mensuel)
        simulations[:, i] = (simulations[:, i - 1] + apports) * (1 + rendements)

    return simulations

# Interface Streamlit
st.title("📊 Simulation réaliste de DCA en ETF (modèle GBM)")

st.markdown("""
Bienvenue sur ce simulateur de DCA en ETF utilisant un modèle à volatilité réaliste (Geometric Brownian Motion).

👉 **À noter** :  
Entre **2008 et 2025**, le MSCI ACWI a eu :  
- 📈 un CAGR moyen d’environ **9.11%**
- 📉 une volatilité annualisée d’environ **17.09%**

Vous pouvez personnaliser ces paramètres ci-dessous.
""")

st.sidebar.header("Paramètres de la simulation")

capital_initial = st.sidebar.number_input("💰 Capital initial (€)", min_value=0, value=10000, step=500)
investissement_mensuel = st.sidebar.number_input("💸 Apport mensuel (€)", min_value=0, value=500, step=50)
nb_annees = st.sidebar.slider("⏳ Durée de l'investissement (années)", min_value=1, max_value=50, value=20)
proba_defaut_epargne = st.sidebar.slider("🎲 Taux de défaut d’épargne (%)", min_value=0.0, max_value=20.0, value=1.0) / 100
nb_simulations = st.sidebar.slider("🔁 Nombre de simulations", min_value=1, max_value=5000, value=10)

mu_annual = st.sidebar.slider("📈 CAGR estimé (%)", min_value=0.0, max_value=20.0, value=9.11) / 100
sigma_annual = st.sidebar.slider("📉 Volatilité annualisée (%)", min_value=5.0, max_value=40.0, value=17.09) / 100

if st.button("Lancer la simulation 🚀"):
    simulations = simulate_dca(capital_initial, investissement_mensuel, nb_annees, proba_defaut_epargne, nb_simulations, mu_annual, sigma_annual)

    nb_mois = nb_annees * 12
    x = np.arange(nb_mois + 1) / 12  # Convertit les mois en années

    percentile_5 = np.percentile(simulations, 5, axis=0)
    percentile_95 = np.percentile(simulations, 95, axis=0)
    percentile_50 = np.percentile(simulations, 50, axis=0)

    plt.figure(figsize=(12, 6))
    plt.plot(x, percentile_50, label="Médiane", color='blue')
    plt.fill_between(x, percentile_5, percentile_95, color='lightblue', alpha=0.4, label="5-95%")
    plt.title(f"Simulation DCA ({nb_simulations} runs) - Capital: {capital_initial}€, Apport: {investissement_mensuel}€, Défaut: {proba_defaut_epargne:.1%}, CAGR: {mu_annual:.2%}, Vol: {sigma_annual:.2%}")
    plt.xlabel("Années")
    plt.ylabel("Valeur du portefeuille (€)")
    plt.grid(True)
    plt.legend()
    st.pyplot(plt.gcf())

    st.success("Simulation terminée ✅")

else:
    st.info("Choisissez vos paramètres dans le menu à gauche et cliquez sur 'Lancer la simulation'.")

