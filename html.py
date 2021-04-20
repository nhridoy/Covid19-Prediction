import streamlit as st
import covid19

cases = covid19.world_total_confirmed_cases
country_cases = covid19.country_cases["confirmed"]
country = covid19.selected_country

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
				<p>{cases}</p>
			</section>
			<section class="big-box box">
				<h2>Total Cases in {country}</h2>
				<p>{country_cases}</p>
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