import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from covid import Covid
import geocoder
import ipinfo


### Geting Location ###
location = geocoder.ip("me")

access_token = '25e3046c673e12'
handler = ipinfo.getHandler(access_token)
ip_address = location.ip
details = handler.getDetails(str(ip_address))

# st.write(location.country)
county_name = details.country_name
# st.write(county_name)

# Creating Title
st.title(
    """
    Covid Tracker
    WorldWide
    """
)

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
        st.write(f"Location Detected {country['country'][i].upper()}")
        break
    else:
        i = 0
if i == 0:
    st.write("Location Detection Error! Please Select from Below.")

st.subheader("Select Country")
# st.write(country)
selected_country = st.selectbox("Country:", country, index=i)

st.write(f"You selected {selected_country.upper()}")

world_total_confirmed_cases = covid.get_total_confirmed_cases()

st.write(f"Total Cases Worldwide: {world_total_confirmed_cases}")

country_cases = covid.get_status_by_country_name(selected_country)
st.write(f"Total Cases in {selected_country.upper()}: {country_cases['confirmed']}")

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
				<h2>This is header</h2>
			</section>
			<section class="big-box box">
				<h2>Total Cases WorldWide</h2>
				<p>{world_total_confirmed_cases}</p>
			</section>
			<section class="big-box box">
				<h2>Total Cases in {selected_country.upper()}</h2>
				<p>{country_cases["confirmed"]}</p>
			</section>
			<section class="box">
				<h2>This is header</h2>
			</section>
		</div>
''', unsafe_allow_html=True)
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