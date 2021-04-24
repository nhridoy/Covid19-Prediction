import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
from covid import Covid
import geocoder
import ipinfo
import datetime
import plotly.express as px
from requests.exceptions import ConnectionError
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

try:
    ### Geting Location ###
    location = geocoder.ip("me")

    access_token = '25e3046c673e12'
    handler = ipinfo.getHandler(access_token)
    ip_address = location.ip
    details = handler.getDetails(str(ip_address))

    # st.write(location.country)
    county_name = details.country_name
    st.write(county_name)


except ConnectionError:
    st.error("Connection Error")
    st.warning("Check Your Internet Connection")