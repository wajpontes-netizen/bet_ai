import pandas as pd
import streamlit as st
import os

DATASET_PATH = "data/dataset.csv"

st.set_page_config(page_title="Bet AI Dashboard", layout="wide")

st.title("📊 Dashboard de Performance - Bet AI")

if not os.path.exists(DATASET_PATH):
    st.warning("Nenhum dado disponível ainda.")
    st.stop()

try:
    df = pd.read_csv(DATASET_PATH)
except:
    st.error("Erro ao carregar dataset")
    st.stop()

if df.empty:
    st.warning("Dataset vazio")
    st.stop()

# -----------------------------
# PREPARAÇÃO
# -----------------------------

df["result"] = df["result"].astype(int)

df["win"] = df["result"]

df["loss"] = 1 - df["result"]

# ROI simples

def calc_profit(row):
    if row["result"] == 1:
        return row["odd"] - 1
    else:
        return -1


df["profit"] = df.apply(calc_profit, axis=1)

# -----------------------------
# KPIs
# -----------------------------

total_bets = len(df)
wins = df["win"].sum()
losses = df["loss"].sum()
winrate = wins / total_bets if total_bets > 0 else 0
roi = df["profit"].sum() / total_bets if total_bets > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Apostas", total_bets)
col2.metric("Winrate", f"{winrate:.2%}")
col3.metric("ROI", f"{roi:.2%}")
col4.metric("Lucro Total", round(df["profit"].sum(), 2))

# -----------------------------
# GRÁFICO DE EVOLUÇÃO
# -----------------------------

st.subheader("📈 Evolução do Lucro")

df["cumulative_profit"] = df["profit"].cumsum()

st.line_chart(df["cumulative_profit"])

# -----------------------------
# POR LIGA
# -----------------------------

st.subheader("🏆 Performance por Liga")

league_stats = df.groupby("league")["profit"].agg(["count", "sum"])
league_stats.columns = ["Apostas", "Lucro"]

st.dataframe(league_stats.sort_values(by="Lucro", ascending=False))

# -----------------------------
# MELHORES APOSTAS
# -----------------------------

st.subheader("🔥 Top Apostas")

st.dataframe(df.sort_values(by="profit", ascending=False).head(10))

# -----------------------------
# PIORES APOSTAS
# -----------------------------

st.subheader("⚠️ Piores Apostas")

st.dataframe(df.sort_values(by="profit", ascending=True).head(10))
