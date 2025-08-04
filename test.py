import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('Hotelnew.csv')
df['arrival_date_month'] = df['arrival_date_month'].str.strip()

st.set_page_config(layout="wide")
st.title("\U0001F3E8 Hotel Booking Dashboard")
st.subheader("Key Performance Indicators & Trends")

# Sidebar
st.sidebar.header("Hotel Dashboard")
st.sidebar.image('download.jpg', width=150)
st.sidebar.write("Explore hotel booking trends and performance metrics.")

# Filters
hotel_filter = st.sidebar.multiselect("Select Hotel(s)", options=df['hotel'].unique(), default=df['hotel'].unique())
filtered_df = df[df['hotel'].isin(hotel_filter)]

if filtered_df.empty:
    st.warning("No data available with the current filters.")
    st.stop()

# KPIs
col1, col2, col3, col4 = st.columns(4)
col1.metric("\U0001F4E6 Total Bookings", f"{len(filtered_df):,}")
col2.metric("\u274C Cancellation Rate", f"{filtered_df['is_canceled'].mean() * 100:.1f}%")
col3.metric("\u23F3 Avg Lead Time", f"{filtered_df['lead_time'].mean():.1f} days")
col4.metric("\U0001F4B0 Avg Daily Rate", f"${filtered_df['adr'].mean():.2f}")

#  month order
month_order = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']
filtered_df['arrival_date_month'] = pd.Categorical(
    filtered_df['arrival_date_month'], categories=month_order, ordered=True)

# Tabs for insights
tab1, tab2, tab3 = st.tabs(["\U0001F4C5 Bookings", "\U0001F4B0 ADR", "\U0001F52C Cancellations"])

with tab1:
    st.markdown("### Monthly Booking Trends")
    monthly_bookings = filtered_df.groupby('arrival_date_month').size().reset_index(name='Bookings')
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=monthly_bookings['arrival_date_month'],
        y=monthly_bookings['Bookings'],
        mode='lines',
        line_shape='hv',
        fill='tozeroy',
        fillcolor='rgba(0, 123, 255, 0.3)',
        line=dict(color='blue'),
        name='Bookings'))
    fig.update_layout(title="\U0001F4C5 Monthly Booking Volume", xaxis_title="Month", yaxis_title="Bookings", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Bookings by Hotel Type")
    hotel_counts = filtered_df['hotel'].value_counts().reset_index()
    hotel_counts.columns = ['Hotel Type', 'Bookings']
    fig = px.pie(hotel_counts, values='Bookings', names='Hotel Type',
                 title="\U0001F3E8 Booking Distribution by Hotel Type",
                 hole=0.4, template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)


    st.markdown("### Top 10 Countries by Number of Bookings")
    country_counts = filtered_df['country'].value_counts().head(10).reset_index()
    country_counts.columns = ['Country', 'Bookings']
    fig = px.bar(country_counts, x='Country', y='Bookings',
                 color='Bookings', color_continuous_scale='blues',
                 title="\U0001F30F Top 10 Countries by Bookings",
                 template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)


with tab2:
    st.markdown("### ADR by Hotel Type")
    fig = px.box(filtered_df, x='hotel', y='adr', color='hotel',
                 title="\U0001F4B0 ADR Distribution by Hotel Type",
                 labels={'adr': 'Average Daily Rate', 'hotel': 'Hotel Type'},
                 template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### ADR by Room Type")
    adr_by_room = filtered_df.groupby('reserved_room_type')['adr'].mean().reset_index()
    adr_by_room = adr_by_room.sort_values('adr', ascending=False)
    fig = px.bar(adr_by_room, x='reserved_room_type', y='adr',
                 color='adr', labels={'reserved_room_type': 'Room Type', 'adr': 'Average Daily Rate'},
                 title='\U0001F4B0 ADR by Room Type', template='plotly_white',
                 color_continuous_scale='tealgrn')
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.markdown("### Monthly Cancellation Rate")
    cancel_month = filtered_df.groupby('arrival_date_month')['is_canceled'].mean().reset_index()
    cancel_month['is_canceled'] *= 100
    cancel_month.sort_values('arrival_date_month', inplace=True)
    fig = px.line(cancel_month, x='arrival_date_month', y='is_canceled',
                  labels={'arrival_date_month': 'Month', 'is_canceled': 'Cancellation Rate (%)'},
                  title="\U0001F4C9 Monthly Cancellation Rate", template="plotly_white")
    fig.update_traces(mode="lines+markers")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Cancellation Rate by Market Segment")
    cancel_seg = filtered_df.groupby('market_segment')['is_canceled'].mean().reset_index()
    cancel_seg['is_canceled'] *= 100
    fig = px.bar(cancel_seg, x='is_canceled', y='market_segment', orientation='h',
                 labels={'market_segment': 'Market Segment', 'is_canceled': 'Cancellation Rate (%)'},
                 title="\U0001F4CA Cancellation Rate by Market Segment", template="plotly_white",
                 color='is_canceled', color_continuous_scale='reds')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Heatmap of Correlations")
    numeric_cols = filtered_df.select_dtypes(include=np.number)
    corr = numeric_cols.corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, fmt=".1f", cmap="coolwarm", ax=ax)
    st.pyplot(fig)
