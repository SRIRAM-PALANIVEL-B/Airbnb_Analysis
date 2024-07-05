
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

# Function to load data from uploaded file or default location
def load_data(file):
    if file is not None:
        df = pd.read_csv(file, encoding="ISO-8859-1")
    else:
        default_file_path = r"D:\\SRIRAM\\PROJECTS (CAPSTONE)\\PROJECTS\\MINI\\Capstone Project\\AIR BNB\\data\\sample_airbnb.listingsAndReviews.csv"
        df = pd.read_csv(default_file_path, encoding="ISO-8859-1")
    return df

# Function to create visualizations
def visualize_data(df):
    st.sidebar.header("Choose your filter:")

    # Filter by address.country (neighbourhood_group)
    country_options = df["address.country"].unique()
    neighbourhood_group = st.sidebar.multiselect("Pick your Country", country_options, country_options)

    if neighbourhood_group:
        df = df[df["address.country"].isin(neighbourhood_group)]

    # Filter by address.street (neighbourhood)
    street_options = df["address.street"].unique()
    neighbourhood = st.sidebar.multiselect("Pick the Street", street_options, street_options)

    if neighbourhood:
        df = df[df["address.street"].isin(neighbourhood)]

    # Visualizations
    st.subheader("Room Type View Data")
    room_type_df = df.groupby("room_type", as_index=False)["price"].sum()
    fig1 = px.bar(room_type_df, x="room_type", y="price", text=room_type_df["price"].apply(lambda x: f"${x:,.2f}"), template="seaborn")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Country View Data")
    fig2 = px.pie(df, values="price", names="address.country", hole=0.5)
    fig2.update_traces(textinfo="value+percent")
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Room Type vs Street Scatter Plot")
    fig3 = px.scatter(df, x="address.country", y="address.street", color="room_type")
    fig3.update_layout(title="Room Type in Country and Street", xaxis_title="Country", yaxis_title="Street")
    st.plotly_chart(fig3, use_container_width=True)

    with st.expander("Room Type wise Price"):
        st.write(room_type_df.style.background_gradient(cmap="Blues"))
        csv1 = room_type_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Room Type Data", data=csv1, file_name="room_type.csv", mime="text/csv")

    with st.expander("Country wise Price"):
        country_df = df.groupby("address.country", as_index=False)["price"].sum()
        st.write(country_df.style.background_gradient(cmap="Oranges"))
        csv2 = country_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Country Data", data=csv2, file_name="country.csv", mime="text/csv")

    with st.expander("Detailed Room Availability and Price View Data in the Street"):
        st.write(df.iloc[:500, 1:20:2].style.background_gradient(cmap="Oranges"))

    st.subheader("Summary Table")
    df_sample = df.sample(frac=0.5)[["address.country", "address.street", "reviews_per_month", "room_type", "price", "minimum_nights", "host.host_name"]]
    fig4 = ff.create_table(df_sample, colorscale="Cividis")
    st.plotly_chart(fig4, use_container_width=True)

# Streamlit layout and configuration
st.set_page_config(layout="wide", page_icon=":bar_chart:")
st.title(":bar_chart: Airbnb - Data Analysis")

select = st.radio("Navigate", ["Home", "Visual Exploration"])

if select == "Home":
    st.header('Airbnb Analysis')
    st.subheader('Airbnb, Inc. is an American company operating an online marketplace for short- and long-term homestays and experiences.')
    st.subheader('Travel Industry, Property Management & Tourism')

elif select == "Visual Exploration":
    st.header('Visual Exploration')
    f1 = st.file_uploader(":file_folder: Upload a file", type=["csv", "txt", "xlsx", "xls"])
    df = load_data(f1)

    visualize_data(df)
