import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from covid import Covid
import datetime
import plotly.express as px
from requests.exceptions import ConnectionError
import requests
import urllib.request
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

try:
    ext_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
    ### Geting Location ###
    ip = requests.get('https://api64.ipify.org').text
    ip_url = f"https://reallyfreegeoip.org/json/{ip}"
    r = requests.get(ip_url)
    ip_details = r.json()
    county_name = ip_details["country_name"]
    # st.write(county_name)

    ### Creating Title ###
    st.title(
        """
        Covid Tracker
        WorldWide
        """
    )

    dt = datetime.datetime.now()
    date = dt.date()
    time = dt.time()
    st.write(f"Date: {date.strftime('%d - %B - %Y')}, Time: {time.strftime('%I:%M %p')}")

    ### Getting worldometer data ###
    covid = Covid(source="worldometers")

    ### Taking Country Input ###

    # Processing Countries Start
    countries = covid.list_countries()
    country = pd.DataFrame(countries, columns=["country"])
    # country["index"] = country.index
    # columns_titles = ["index", "country"]
    # country = country.reindex(columns=columns_titles)
    # Processing Countries End

    # Dropping empty columns
    # nan_value = float("NaN")
    # c.replace("", nan_value, inplace=True)
    # c.dropna(subset = ["country"], inplace=True)

    for i in range(country["country"].count()):
        if country["country"][i] == county_name.lower():
            st.sidebar.write(f"Location Detected {country['country'][i].upper()}")
            break
        else:
            i = 0
    if i == 0:
        st.sidebar.write("Location Detection Error! Please Select from Below.")

    st.sidebar.subheader("Select Country")
    # st.write(country)
    selected_country = st.sidebar.selectbox("Country:", country, index=i)


    ### Getting Additional Covid Data For Visualization and Prediction ###
    ### Caching Data ###
    # @st.cache(suppress_st_warning=True)
    def extra_data():
        url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
        db = pd.read_csv(url)
        return db


    db = extra_data()
    world = db[db["location"] == "World"]
    country = db[db["location"] == selected_country.capitalize()]
    world_total = world[["location", "date", "total_cases", "total_deaths"]]
    country_total = country[["location", "date", "total_cases", "total_deaths"]]
    world_total = pd.DataFrame(world_total)
    world_total.insert(0, 'id', range(0, 0 + len(world_total)))
    country_total = pd.DataFrame(country_total)
    country_total.insert(0, 'id', range(0, 0 + len(country_total)))
    last_date = world_total.tail(1)
    last_cases = int(last_date["total_cases"])
    last_death = int(last_date["total_deaths"])

    st.write(f"You selected {selected_country.upper()}")

    ### Getting All Datas ###
    world_total_confirmed_cases = covid.get_total_confirmed_cases()
    world_total_confirmed_cases_new = world_total_confirmed_cases - last_cases
    world_total_death = covid.get_total_deaths()
    world_total_death_new = world_total_death - last_death
    world_total_recovered = covid.get_total_recovered()
    world_total_active = covid.get_total_active_cases()

    country_cases = covid.get_status_by_country_name(selected_country)
    country_total_cases = country_cases['confirmed']
    country_total_death = country_cases['deaths']
    country_total_recovered = country_cases['recovered']
    country_total_active = country_cases['active']
    country_cases_new = country_cases['new_cases']
    country_death_new = country_cases['new_deaths']


    # st.write(f"Total Cases Worldwide: {world_total_confirmed_cases}")

    # st.write(f"Total Cases in {selected_country.upper()}: {country_cases['confirmed']}")

    def output(location, total_recovered, total_case, new_case, total_death, new_death, total_active):
        st.write('''
                    <style>
            			.container{
            				width: 80%;
            				padding-top: 150px;
            				margin:auto;
            			}
            			.box{
            				float: left;
            				display: inline;
            				width: 19%;
            				text-align: center;
            				font-weight: 400;
            				font-family: "roboto", cursive;
            				height: 300px;
            				margin: .5%;
            				box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
            				padding: 5px
            			}
            			.big-box{
            				width: 28%;
            				height: 350px;
            				transform: translateY(-25px); 
            				padding: 5px
            			}
            		</style>
            ''', unsafe_allow_html=True)

        st.write(f'''
                <div class="container">
                    <section class="box">
                        <h3>Total Recovered {location}</h3>
                        <p>{total_recovered}</p>
                    </section>
                    <section class="big-box box">
                        <h3>Total Cases {location}</h3>
                        <p>{total_case}</p>
                        <p>New Cases: {new_case}</p>
                    </section>
                    <section class="big-box box">
                        <h3>Total Death {location}</h3>
                        <p>{total_death}</p>
                        <p>New Deaths: {new_death}</p>
                    </section>
                    <section class="box">
                        <h3>Total Active {location}</h3>
                        <p>{total_active}</p>
                    </section>
                </div>
        ''', unsafe_allow_html=True)


    ### Display World Data ###
    output("WorldWide", world_total_recovered, world_total_confirmed_cases, world_total_confirmed_cases_new,
           world_total_death, world_total_death_new, world_total_active)

    ### Display Figure ###
    world_country = [world_total, country_total]
    world_country = pd.concat(world_country)
    fig = px.line(world_country, x="date", y="total_cases", title='Total Cases World and Country', color='location')
    st.plotly_chart(fig, use_container_width=True)

    ### Display Country Data ###
    output(selected_country.upper(), country_total_recovered, country_total_cases, country_cases_new,
           country_total_death, country_death_new, country_total_active)

    st.markdown(
        f"""
    <style>
        .reportview-container .main .block-container{{
            max-width: 80%;
        }}
        .container {{
            width: 100%;
            padding-top: 150px;
            margin: auto;
        }}
    </style>
    """,
        unsafe_allow_html=True,
    )

except ConnectionError:
    st.error("Connection Error")
    st.warning("Check Your Internet Connection")