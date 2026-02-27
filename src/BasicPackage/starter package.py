import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os


# ===============================
#  Load Data
# ===============================

def load_data(file_path: str) -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(file_path, encoding="ISO-8859-1")
    return df


# ===============================
#  Basic Cleaning
# ===============================

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    print(f"Original shape: {df.shape}")

    df = df.drop_duplicates()

    df = df.dropna()

    print(f"After cleaning shape: {df.shape}")

    return df


# ===============================
#  Feature Engineering (Basic)
# ===============================

def prepare_features(df: pd.DataFrame) -> pd.DataFrame:
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    df["Month"] = df["InvoiceDate"].dt.to_period("M")

    return df


# ===============================
#  Descriptive Statistics
# ===============================

def descriptive_analysis(df: pd.DataFrame) -> Tuple[float, pd.Series, float]:
    average_sales: float = df["TotalPrice"].mean()
    orders_per_category: pd.Series = df["Description"].value_counts().head(10)
    total_quantity: float = df["Quantity"].sum()

    print(f"Average Sale Value: {average_sales:.2f}")
    print(f"Total Quantity Sold: {total_quantity}")

    return average_sales, orders_per_category, total_quantity


# ===============================
#  Visualizations
# ===============================

def create_bar_chart(orders_per_category: pd.Series) -> str:
    plt.figure()
    orders_per_category.plot(kind="bar")
    plt.title("Top 10 Products by Number of Orders")
    plt.xlabel("Product")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=45)
    plt.tight_layout()

    file_name: str = "bar_chart.png"
    plt.savefig(file_name)
    plt.close()

    return file_name


def create_line_chart(df: pd.DataFrame) -> str:
    monthly_sales = df.groupby("Month")["TotalPrice"].sum()
    monthly_sales.index = monthly_sales.index.astype(str)

    plt.figure()
    monthly_sales.plot(kind="line")
    plt.title("Monthly Sales Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Sales")
    plt.xticks(rotation=45)
    plt.tight_layout()

    file_name: str = "line_chart.png"
    plt.savefig(file_name)
    plt.close()

    return file_name


# ===============================
#  Generate PDF Report
# ===============================

def generate_pdf_report(
    average_sales: float,
    total_quantity: float,
    bar_chart_path: str,
    line_chart_path: str
) -> None:

    doc = SimpleDocTemplate("Starter_Package_Report.pdf", pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    normal_style = styles["Normal"]

    elements.append(Paragraph("Starter Package - Basic Data Analysis Report", title_style))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph(f"Average Sale Value: {average_sales:.2f}", normal_style))
    elements.append(Paragraph(f"Total Quantity Sold: {total_quantity}", normal_style))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph("Top Products by Orders:", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Image(bar_chart_path, width=5 * inch, height=3 * inch))
    elements.append(Spacer(1, 0.5 * inch))

    elements.append(Paragraph("Monthly Sales Trend:", styles["Heading2"]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(Image(line_chart_path, width=5 * inch, height=3 * inch))

    doc.build(elements)

    print("PDF report generated successfully!")


# ===============================
# 7️⃣ Main Execution
# ===============================

def main() -> None:
    file_path: str = "data.csv"

    df: pd.DataFrame = load_data(file_path)

    df = clean_data(df)

    df = prepare_features(df)

    average_sales, orders_per_category, total_quantity = descriptive_analysis(df)

    bar_chart_path: str = create_bar_chart(orders_per_category)

    line_chart_path: str = create_line_chart(df)

    generate_pdf_report(
        average_sales,
        total_quantity,
        bar_chart_path,
        line_chart_path
    )


if __name__ == "__main__":
    main()