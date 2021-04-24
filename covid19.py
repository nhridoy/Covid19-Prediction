import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from covid import Covid
import geocoder
import datetime
import plotly.express as px
from requests.exceptions import ConnectionError
import requests
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

try:
    ### Geting Location ###
    location = geocoder.ip("me")
    ip_address = location.ip
    ip_url = f"https://reallyfreegeoip.org/json/{ip_address}"
    r = requests.get(ip_url)
    ip_details = r.json()
    county_name = ip_details["country_name"]
    st.write(county_name)

except ConnectionError:
    st.error("Connection Error")
    st.warning("Check Your Internet Connection")