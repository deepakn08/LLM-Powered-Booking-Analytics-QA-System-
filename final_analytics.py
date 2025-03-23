# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fastapi import FastAPI, HTTPException
import uvicorn
import nest_asyncio
from fastapi.responses import StreamingResponse
import io
from enum import Enum

# %%
data = pd.read_csv(r"C:\Users\nailw\OneDrive\Desktop\Intern_Assignement\hotel_bookings.csv")

# %%
## Dropping the booking that have not any country assigned.
data = data.dropna(subset=["country"])

# %%
def convert_datetime(data):
    data['arrival_date'] = data[["arrival_date_year", "arrival_date_month", "arrival_date_day_of_month"]].astype(str).agg("-".join, axis=1)
    data.drop(columns=['arrival_date_year','arrival_date_month','arrival_date_day_of_month'],inplace=True)
    data['arrival_date'] = pd.to_datetime(data['arrival_date'], format="%Y-%B-%d")
    data["arrival_date"] = data["arrival_date"].dt.strftime("%d-%m-%y")
    data['arrival_date']=pd.to_datetime(data["arrival_date"], dayfirst=True)
    data['checkout_date']=pd.to_datetime(data["reservation_status_date"], dayfirst=True)
    data.drop(columns = ['reservation_status_date'],inplace=True)
    
    return data

# %%
data_processed = convert_datetime(data)

# %%
def calc_revenue(data_processed):
    data_processed['night_stay'] = (data_processed['checkout_date']-data_processed['arrival_date']).dt.days
    data_processed['Total_revenue'] = data_processed['adr']*data_processed['night_stay']
    return data_processed

# %%
data_processed = calc_revenue(data_processed)

# %%
data_processed

# %% [markdown]
# ## Cancellation Rate % of total booking

# %%
def canc_rate(processed_data):
    return (processed_data['is_canceled'].sum()/len(data))*100

# %%
def plot_is_cancelled(processed_data):
    return sns.countplot(x=processed_data['is_canceled'])

# %%
def cancel_chann_distribution(processed_data):
    sizes = processed_data.loc[processed_data['is_canceled'] == 1]['distribution_channel'].value_counts()
    labels = processed_data.loc[processed_data['is_canceled'] == 1]['distribution_channel'].unique()
    colors = sns.color_palette('Set2', len(labels))
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90,labeldistance=1.1,textprops={'rotation': 40, 'fontsize': 8})
    plt.title("Booking Cancellation Distribution")
    return plt

# %% [markdown]
# Majority of the cancellationa re from TA/TO distribution channel. Which contribute total 90.8% of total cancellations.

# %% [markdown]
# From total booking 37.04 % of the booking got cancelled. It contains non of the missing values.

# %% [markdown]
# ## Revenue trends over time

# %%
def revenue_trend(data):
    df = data.loc[data['is_canceled']==0]
    daily_revenue_trend = df.groupby("checkout_date")["Total_revenue"].sum()
    plt.figure(figsize=(12, 6))
    plt.plot(daily_revenue_trend.index, daily_revenue_trend.values, label="Total Revenue", color="b")
    plt.xlabel("Date")
    plt.ylabel("Total Revenue")
    plt.title("Revenue Trends Over Time")
    plt.legend()
    plt.grid(True)

    return plt

# %% [markdown]
# ## Geographical Distribution of the people doing booking.

# %%
def geo_distribution(data):
    data['country'].isna().sum()
    df = data['country'].value_counts()
    mask = df > 100

    # Create subplots
    fig, axes = plt.subplots(2, 1, figsize=(15, 6))  

    # Plot for countries with >100 bookings
    axes[0].bar(df.loc[mask].index, (df.loc[mask].values / len(data)) * 100, color="skyblue")
    axes[0].set_xlabel("Country")
    axes[0].set_ylabel("Bookings percentage (%)")
    axes[0].set_title("Bookings per Country (>100 Bookings)")
    axes[0].tick_params(axis='x', rotation=45)
    axes[0].grid(axis="y", linestyle="--", alpha=0.7)

    # Plot for countries with <100 bookings
    axes[1].bar(df.loc[~mask].index, (df.loc[~mask].values / len(data)) * 100, color="skyblue")
    axes[1].set_xlabel("Country")
    axes[1].set_ylabel("Bookings percentage (%)")
    axes[1].set_title("Bookings per Country (<100 Bookings)")
    axes[1].tick_params(axis='x', rotation=90, labelsize=5)
    axes[1].grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()
    return fig 

# %% [markdown]
# ## Observing Lead Time Distribution

# %%
def lead_distribution(data):
    df = data['lead_time'].value_counts()
    mask = df>500
    values = np.array([((df.loc[df.index < 100]).sum())/len(data),((df.loc[(df.index >= 100) & (df.index < 180)]).sum())/len(data),((df.loc[(df.index >= 180) & (df.index < 365)]).sum())/len(data),((df.loc[(df.index >= 180) & (df.index < 365)]).sum())/len(data)])
    labels = ['Fewer than 100 days','100+ days but under 6 months','6+ months but under 1 year','Before 1 year']
    plt.figure(figsize=(15, 6))
    plt.bar(labels, (values)*100, color="skyblue")
    plt.xlabel("Timeline")
    plt.ylabel("Bookings percentage (%)")
    plt.title("Time Lead Distribution")
    plt.xticks(rotation=45,fontsize=10)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    return plt

# %% [markdown]
# Most of the booking have lead time of less than 100 days among them majority of the booking have lead time of 0 days.

# %% [markdown]
# ## Building Fast API

# %%
nest_asyncio.apply()

# %%
app = FastAPI()

class PlotType(str, Enum):
    Revenue = "Revenue Trends"
    Cancellation_Rate = "Cancellation rate as percentage of total bookings"
    Cancellation_Distribution = "Cancellation Distribution"
    Channel_Distri_Cancel = "Channel Distribution of Cancellation"
    Geographical_Distribution = "Geographical distribution of users doing the bookings"
    LeadTime_Distribution="Booking Lead time distribution"

def save_plot_as_pdf(plot):
    pdf_io = io.BytesIO()
    plot.savefig(pdf_io, format="pdf", bbox_inches="tight")
    plt.close()  # Free memory
    pdf_io.seek(0)
    return pdf_io

@app.get("/plot")
async def get_plot(plot: PlotType):
    if plot == PlotType.Revenue:
        fig = revenue_trend(data_processed)
        pdf_io = save_plot_as_pdf(fig)
        return StreamingResponse(pdf_io, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=revenue.pdf"})

    elif plot == PlotType.Cancellation_Rate:
        value = canc_rate(data_processed)
        return {"cancellation_rate": f"{value:.2f}%"}  # Return JSON instead of a file

    elif plot == PlotType.Geographical_Distribution:
        fig = geo_distribution(data_processed)
        pdf_io = save_plot_as_pdf(fig)
        return StreamingResponse(pdf_io, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=geo_distribution.pdf"})

    elif plot == PlotType.LeadTime_Distribution:
        fig = lead_distribution(data_processed)
        pdf_io = save_plot_as_pdf(fig)
        return StreamingResponse(pdf_io, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=leadtime_distribution.pdf"})

    elif plot == PlotType.Cancellation_Distribution:
        fig = plot_is_cancelled(data_processed)
        pdf_io = save_plot_as_pdf(fig)
        return StreamingResponse(pdf_io, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=cancellation_distribution.pdf"})

    elif plot == PlotType.Channel_Distri_Cancel:
        fig = cancel_chann_distribution(data_processed)
        pdf_io = save_plot_as_pdf(fig)
        return StreamingResponse(pdf_io, media_type="application/pdf", headers={"Content-Disposition": "attachment; filename=channel_distri_cancel.pdf"})

    return {"error": "Invalid plot type"}


# %%
uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")

# %%
canc_rate(data_processed)

# %%



