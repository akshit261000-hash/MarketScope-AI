# ============================================================
# MARKETSCOPE AI
# Australian Suburb Intelligence & Business Expansion Platform
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="MarketScope AI",
    page_icon="🏙️",
    layout="wide"
)


# ============================================================
# 2. LOAD DATA
# ============================================================

# Using Path makes the file path more reliable when the app
# is run locally or later deployed online.

BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR /  "market_scope_industry1.xlsx"


@st.cache_data
def load_data():
    return pd.read_excel(DATA_PATH)


df = load_data()


# ============================================================
# 3. SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🏙️ MarketScope AI")

    st.write(
        "A data-driven location intelligence platform designed "
        "to support business expansion decisions across Australian suburbs."
    )

    st.divider()

    st.subheader("Industry")

    industry = st.selectbox(
        "Select an industry",
        [
            "Retail",
            "Health Insurance",
            "Telecommunications"
        ]
    )

    st.divider()

    st.markdown(
        """
        **Decision factors**

        • Market opportunity  
        • Business risk  
        • Population characteristics  
        • Income profile  
        • Population growth  
        • Accessibility  
        • Competition  
        • Industry suitability
        """
    )

    st.divider()

    st.caption(
        "Portfolio Proof of Concept"
    )


# ============================================================
# 4. INDUSTRY LOGIC
# ============================================================

industry_config = {

    "Retail": {
        "score": "retail_score",
        "label": "Retail Suitability Score"
    },

    "Health Insurance": {
        "score": "health_score",
        "label": "Health Insurance Suitability Score"
    },

    "Telecommunications": {
        "score": "telecom_score",
        "label": "Telecommunications Suitability Score"
    }
}


score_column = industry_config[industry]["score"]

score_label = industry_config[industry]["label"]


# ============================================================
# 5. HEADER
# ============================================================

st.title("🏙️ MarketScope AI")

st.subheader(
    "Australian Suburb Intelligence for Smarter Business Expansion"
)

st.write(
    "Explore suburb-level market opportunities, compare locations "
    "and identify high-potential expansion areas using opportunity, "
    "risk and industry-specific scoring."
)

st.divider()


# ============================================================
# 6. KEY METRICS
# ============================================================

top_suburb_row = df.loc[df[score_column].idxmax()]

high_priority_count = (
    df["recommendation"]
    .astype(str)
    .str.strip()
    .eq("High Priority")
    .sum()
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Suburbs Analysed",
        f"{len(df):,}"
    )


with col2:

    st.metric(
        "Average Opportunity",
        f"{df['opportunity_score'].mean():.1f}"
    )


with col3:

    st.metric(
        "High Priority Locations",
        int(high_priority_count)
    )


with col4:

    st.metric(
        f"Top {industry} Location",
        top_suburb_row["suburb"]
    )


st.divider()


# ============================================================
# 7. TOP 5 INDUSTRY RECOMMENDATIONS
# ============================================================

st.header(f" Top 5 {industry} Expansion Opportunities")


top5 = (
    df.sort_values(
        by=score_column,
        ascending=False
    )
    .head(5)
    .copy()
)


top5["Industry Score"] = (
    top5[score_column]
    .round(1)
)


display_top5 = top5[
    [
        "suburb",
        "Industry Score",
        "recommendation",
        "key_strengths"
    ]
].copy()


display_top5.columns = [
    "Suburb",
    score_label,
    "Priority",
    "Key Strengths"
]


st.dataframe(
    display_top5,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# 8. INDUSTRY RANKING CHART
# ============================================================

st.subheader(f" {industry} Suitability Ranking")


chart_data = top5.sort_values(
    by=score_column,
    ascending=True
)


ranking_fig = px.bar(

    chart_data,

    x=score_column,

    y="suburb",

    orientation="h",

    text=score_column,

    hover_data={
        "opportunity_score": ":.1f",
        "risk_score": ":.1f",
        "population": ":,.0f",
        score_column: ":.1f"
    },

    labels={
        score_column: score_label,
        "suburb": "Suburb"
    }
)


ranking_fig.update_traces(

    texttemplate="%{text:.1f}",

    textposition="outside"
)


ranking_fig.update_xaxes(

    range=[0, 100],

    title=score_label
)


ranking_fig.update_yaxes(

    title=""
)


ranking_fig.update_layout(

    height=430,

    margin=dict(
        l=20,
        r=30,
        t=20,
        b=20
    )
)


st.plotly_chart(

    ranking_fig,

    use_container_width=True
)


st.divider()


# ============================================================
# 9. OPPORTUNITY VS RISK ANALYSIS
# ============================================================

st.header(" Opportunity vs Risk Analysis")


st.write(
    "This view helps identify suburbs that combine stronger market "
    "opportunity with manageable business risk."
)


risk_fig = px.scatter(

    df,

    x="risk_score",

    y="opportunity_score",

    size="population",

    hover_name="suburb",

    color="recommendation",

    hover_data={

        "population": ":,.0f",

        "median_income": ":,.0f",

        "population_growth": ":.1f",

        score_column: ":.1f"
    },

    labels={

        "risk_score":
        "Risk Score",

        "opportunity_score":
        "Opportunity Score",

        "recommendation":
        "Priority"
    }
)


risk_fig.update_layout(

    height=560,

    legend_title_text="Recommendation"
)


st.plotly_chart(

    risk_fig,

    use_container_width=True
)


st.info(
    "A stronger expansion candidate generally combines a higher "
    "opportunity score with a lower or manageable risk score."
)


st.divider()


# ============================================================
# 10. SUBURB EXPLORER
# ============================================================

st.header(" Suburb Explorer")


selected_suburb = st.selectbox(

    "Select a suburb",

    sorted(
        df["suburb"]
        .dropna()
        .unique()
    )
)


suburb = (

    df[
        df["suburb"]
        == selected_suburb
    ]

    .iloc[0]
)


st.subheader(
    f"{selected_suburb} Market Profile"
)


m1, m2, m3, m4 = st.columns(4)


with m1:

    st.metric(

        "Population",

        f"{suburb['population']:,.0f}"
    )


with m2:

    st.metric(

        "Median Income",

        f"${suburb['median_income']:,.0f}"
    )


with m3:

    st.metric(

        "Population Growth",

        f"{suburb['population_growth']:.1f}%"
    )


with m4:

    st.metric(

        "Age 20–39",

        f"{suburb['age_20_39_percentage']:.1f}%"
    )


m5, m6, m7, m8 = st.columns(4)


with m5:

    st.metric(

        "Opportunity Score",

        f"{suburb['opportunity_score']:.1f}"
    )


with m6:

    st.metric(

        "Risk Score",

        f"{suburb['risk_score']:.1f}"
    )


with m7:

    st.metric(

        score_label,

        f"{suburb[score_column]:.1f}"
    )


with m8:

    st.metric(

        "Competitors",

        f"{suburb['competitor_count']:,.0f}"
    )


st.write(
    f"**Recommendation:** "
    f"{suburb['recommendation']}"
)


st.write(
    f"**Key strengths:** "
    f"{suburb['key_strengths']}"
)


st.write(
    f"**Train accessibility score:** "
    f"{suburb['train_station_score']:.1f}"
)


st.divider()


# ============================================================
# 11. COMPARE SUBURBS
# ============================================================

st.header("⚖️ Compare Suburbs")


st.write(
    "Compare up to three suburbs to evaluate their market "
    "characteristics and industry suitability."
)


selected_suburbs = st.multiselect(

    "Choose up to three suburbs",

    options=sorted(
        df["suburb"]
        .dropna()
        .unique()
    ),

    max_selections=3
)


if selected_suburbs:

    comparison_df = (

        df[
            df["suburb"]
            .isin(selected_suburbs)
        ]

        .copy()
    )


    comparison_df["Industry Score"] = (

        comparison_df[
            score_column
        ]

        .round(1)
    )


    comparison_display = (

        comparison_df[
            [
                "suburb",
                "population",
                "median_income",
                "population_growth",
                "age_20_39_percentage",
                "train_station_score",
                "competitor_count",
                "opportunity_score",
                "risk_score",
                "Industry Score",
                "recommendation"
            ]
        ]

        .copy()
    )


    comparison_display.columns = [

        "Suburb",

        "Population",

        "Median Income",

        "Population Growth (%)",

        "Age 20–39 (%)",

        "Accessibility",

        "Competitors",

        "Opportunity",

        "Risk",

        score_label,

        "Priority"
    ]


    st.dataframe(

        comparison_display,

        use_container_width=True,

        hide_index=True
    )


    # --------------------------------------------------------
    # Comparison chart
    # --------------------------------------------------------

    comparison_long = (

        comparison_df[
            [
                "suburb",
                "opportunity_score",
                score_column
            ]
        ]

        .rename(
            columns={

                "opportunity_score":
                "Opportunity Score",

                score_column:
                score_label
            }
        )

        .melt(

            id_vars="suburb",

            var_name="Metric",

            value_name="Score"
        )
    )


    comparison_fig = px.bar(

        comparison_long,

        x="suburb",

        y="Score",

        color="Metric",

        barmode="group",

        labels={
            "suburb": "Suburb"
        }
    )


    comparison_fig.update_layout(

        height=450
    )


    st.plotly_chart(

        comparison_fig,

        use_container_width=True
    )


    # --------------------------------------------------------
    # Best suburb from selected comparison
    # --------------------------------------------------------

    best_comparison = (

        comparison_df

        .sort_values(
            by=score_column,
            ascending=False
        )

        .iloc[0]
    )


    st.success(

        f"🏆 Best option among the selected suburbs for "
        f"{industry}: "
        f"{best_comparison['suburb']} "
        f"with a suitability score of "
        f"{best_comparison[score_column]:.1f}."
    )


    st.write(

        f"**Key strengths:** "
        f"{best_comparison['key_strengths']}"
    )


else:

    st.info(
        "Select two or three suburbs to begin the comparison."
    )


st.divider()


# ============================================================
# 12. EXECUTIVE RECOMMENDATION
# ============================================================

st.header(" Executive Recommendation")


best_suburb = top5.iloc[0]


st.success(

    f"""
### Recommended location for {industry}: {best_suburb['suburb']}

**{score_label}:** {best_suburb[score_column]:.1f}

**Opportunity Score:** {best_suburb['opportunity_score']:.1f}

**Risk Score:** {best_suburb['risk_score']:.1f}

**Priority:** {best_suburb['recommendation']}

**Key Strengths:** {best_suburb['key_strengths']}
"""
)


st.write(

    f"Based on the current scoring model, "
    f"**{best_suburb['suburb']}** ranks highest for "
    f"**{industry}** among the suburbs analysed. "
    f"The recommendation combines market opportunity, "
    f"risk indicators and industry-specific suitability factors."
)


st.divider()


# ============================================================
# 13. COMPLETE DATASET
# ============================================================

with st.expander(
    " View Complete Dataset"
):

    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True
    )


# ============================================================
# 14. DOWNLOAD RESULTS
# ============================================================

st.subheader("⬇ Export Analysis")


export_columns = [

    "suburb",

    "population",

    "median_income",

    "population_growth",

    "opportunity_score",

    "risk_score",

    "recommendation",

    score_column,

    "key_strengths"
]


export_df = (

    df[export_columns]

    .sort_values(
        by=score_column,
        ascending=False
    )
)


csv = export_df.to_csv(
    index=False
)


st.download_button(

    label=f"Download {industry} Analysis",

    data=csv,

    file_name=(
        f"marketscope_"
        f"{industry.lower().replace(' ', '_')}"
        f"_analysis.csv"
    ),

    mime="text/csv"
)


# ============================================================
# 15. METHODOLOGY / TRANSPARENCY
# ============================================================

with st.expander(
    " How MarketScope AI Works"
):

    st.markdown(
        """
MarketScope AI is a proof-of-concept decision-support platform.

The platform evaluates suburbs using demographic, economic,
accessibility, growth and competition indicators.

### Core analytical components

**Opportunity Score**  
Measures the overall attractiveness of a suburb using selected
market indicators.

**Risk Score**  
Represents factors that may increase expansion risk, including
competition and weaker market conditions.

**Industry Suitability Scores**  
Different industries use different factor weightings because
business requirements vary by sector.

The current proof of concept supports:

- Retail
- Health Insurance
- Telecommunications

The recommendations are intended to support business analysis
and should be combined with additional commercial due diligence
before making real investment decisions.
"""
    )


# ============================================================
# 16. FOOTER
# ============================================================

st.divider()


st.caption(
    "MarketScope AI | Australian Suburb Intelligence "
    "| Data Analytics & Business Decision-Support POC"
)
