import pandas as pd
from typing import Tuple
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


# ===============================
# 1️⃣ Load & Clean Data
# ===============================

def load_and_prepare_data(file_path: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(file_path, encoding="ISO-8859-1")

    df = df.drop_duplicates()
    df = df.dropna()

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    return df


# ===============================
# 2️⃣ KPI Calculation
# ===============================

def calculate_kpis(df: pd.DataFrame) -> Tuple[float, float, int]:
    total_revenue: float = df["TotalPrice"].sum()
    average_sale: float = df["TotalPrice"].mean()
    total_orders: int = df["InvoiceNo"].nunique()

    return total_revenue, average_sale, total_orders


# ===============================
# 3️⃣ Create Dash App
# ===============================

def create_dashboard(df: pd.DataFrame) -> None:
    app = dash.Dash(__name__)

    months = sorted(df["Month"].unique())

    app.layout = html.Div(
        style={
            "backgroundColor": "#111111",
            "color": "#EAEAEA",
            "padding": "30px",
            "fontFamily": "Arial"
        },
        children=[

            html.H1(
                "Starter Package - Sales Dashboard",
                style={
                    "textAlign": "center",
                    "marginBottom": "40px"
                }
            ),

            # Dropdown Filter
            html.Div([
                html.Label("Select Month:"),
                dcc.Dropdown(
                    id="month_filter",
                    options=[{"label": m, "value": m} for m in months],
                    value=months,
                    multi=True,
                    style={"color": "#000000"}
                )
            ], style={"marginBottom": "40px"}),

            # KPI Section
            html.Div(id="kpi_section", style={
                "display": "flex",
                "justifyContent": "space-between",
                "marginBottom": "50px"
            }),

            # Charts
            html.Div([
                dcc.Graph(id="bar_chart"),
                dcc.Graph(id="line_chart")
            ])
        ]
    )

    # ===============================
    # Callbacks
    # ===============================

    @app.callback(
        [
            Output("kpi_section", "children"),
            Output("bar_chart", "figure"),
            Output("line_chart", "figure")
        ],
        [Input("month_filter", "value")]
    )
    def update_dashboard(selected_months):

        filtered_df = df[df["Month"].isin(selected_months)]

        total_revenue, average_sale, total_orders = calculate_kpis(filtered_df)

        # KPI Cards
        kpis = [
            create_kpi_card("Total Revenue", f"${total_revenue:,.2f}"),
            create_kpi_card("Average Sale", f"${average_sale:,.2f}"),
            create_kpi_card("Total Orders", f"{total_orders}")
        ]

        # Bar Chart
        top_products = (
            filtered_df["Description"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        top_products.columns = ["Product", "Orders"]

        bar_fig = px.bar(
            top_products,
            x="Product",
            y="Orders",
            title="Top 10 Products by Orders",
            template="plotly_dark",
            color_discrete_sequence=["#00B5E2"]
        )

        bar_fig.update_layout(
            xaxis_tickangle=-45,
            plot_bgcolor="#111111",
            paper_bgcolor="#111111"
        )

        # Line Chart
        monthly_sales = (
            filtered_df
            .groupby("Month")["TotalPrice"]
            .sum()
            .reset_index()
        )

        line_fig = px.line(
            monthly_sales,
            x="Month",
            y="TotalPrice",
            title="Monthly Sales Trend",
            template="plotly_dark",
            markers=True,
            color_discrete_sequence=["#7FDBFF"]
        )

        line_fig.update_layout(
            plot_bgcolor="#111111",
            paper_bgcolor="#111111"
        )

        return kpis, bar_fig, line_fig

    app.run(debug=True)


# ===============================
# KPI Card Component
# ===============================

def create_kpi_card(title: str, value: str) -> html.Div:
    return html.Div(
        style={
            "backgroundColor": "#1E1E1E",
            "padding": "20px",
            "borderRadius": "10px",
            "width": "30%",
            "textAlign": "center",
            "boxShadow": "0px 0px 10px rgba(0,0,0,0.5)"
        },
        children=[
            html.H3(title, style={"color": "#AAAAAA"}),
            html.H2(value, style={"color": "#00B5E2"})
        ]
    )


# ===============================
# Main
# ===============================

def main() -> None:
    file_path: str = "data.csv"
    df: pd.DataFrame = load_and_prepare_data(file_path)
    create_dashboard(df)


if __name__ == "__main__":
    main()