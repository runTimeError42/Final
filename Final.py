"""
Name: Jeremy
CS230: Section Glick
Data: Volcanoes
URL:
Description: This program is designed to use data frames to analysis data from a csv file
and then display it in an user friendly manner
To run: streamlit run C:/Python/Final.py [ARGUMENTS]
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import pprint as pp
import streamlit as st
from streamlit_folium import folium_static
import folium



volcano = pd.read_csv('FinalProject/volcanoes.csv', encoding='latin-1')
st.title("Welcome to my website!")
st.sidebar.header("Average Elevation Analysis")
countryOrRegion = st.sidebar.selectbox("Please select the topographical size:", ("Country", "Region"))
highestOrLowest = st.sidebar.selectbox("Please select the average elevation analysis:", ("Highest Average", "Lowest Average"))
def aveElevations(cOR, hOL):
    if cOR == "Country":
        cande = volcano.iloc[:, [2, 10]]
    else:
        cande = volcano.iloc[:, [6, 10]]
    candeAverage = cande.groupby(by = cOR).sum() / cande.groupby(by = cOR).count()
    if hOL == "Highest Average":
        candeAverage = candeAverage.sort_values(["Elevation (m)"], ascending=False)
    else:
        candeAverage = candeAverage.sort_values(["Elevation (m)"], ascending=True)
    region = []
    average = []
    candeAverage = candeAverage.reset_index()
    for i in range(len(candeAverage)):
        average.append(f"{candeAverage.iloc[i, 1]:.0f}")
        region.append(f"{candeAverage.iloc[i, 0]}")
    region = region[0:5]
    average = average[0:5]
    return region, average
def main():
    a, b = aveElevations(countryOrRegion, highestOrLowest)
    if highestOrLowest == "Highest Average":
        a.reverse()
        b.reverse()
    fig, ax = plt.subplots()
    st.header(f"Top 5 {highestOrLowest} Elevations by {countryOrRegion}")
    ax.bar(a, b, width=0.45)
    st.pyplot(fig)
main()
st.write(f"You chose to evaluate the top 5 {highestOrLowest} elevations by {countryOrRegion}")



st.header("Map of Volcanoes and Links to More Information")
volcano.head()
center = [0, 0]
volcanoMap = folium.Map(location=center, zoom_start=1)
for j, f in volcano.iterrows():
    location = [f["Latitude"], f["Longitude"]]
    folium.Marker(location, popup=f"Name: {f['Volcano Name']}\nCountry: {f['Country']}\nLink: {f['Link']}").add_to(volcanoMap)
folium_static(volcanoMap)


st.sidebar.header("Criteria for Region Pie Chart")
st.header("Percentage Break Down of Total Volcanoes By Region")
regionData = []
averageData = []
criteria = st.sidebar.multiselect("Please choose the criteria to filter by:", ["Elevation (m)", "Activity Evidence"])
if len(criteria) == 0:
    elevation = ""
    evidence = ""
    covbr = volcano.loc[:, ["Region", "Elevation (m)"]]
    covbr = covbr.groupby(by="Region").count()
    covbr = covbr.reset_index()
    for v in range(len(covbr)):
        averageData.append(f"{covbr.iloc[v, 1]:.0f}")
        regionData.append(f"{covbr.iloc[v, 0]}")
    fig, ax = plt.subplots()
    ax.pie(averageData, labels=regionData, autopct='%.1f%%')
    st.pyplot(fig)
elif len(criteria) == 1:
    if criteria[0] == "Elevation (m)":
        elevation = st.sidebar.slider("Pick the minimum elevation", -5000, 7000)
        evidence = ""
        covbr = volcano.loc[(volcano["Elevation (m)"] > elevation), ["Region", "Elevation (m)"]]
        covbr = covbr.groupby(by="Region").count()
        covbr = covbr.reset_index()
        for v in range(len(covbr)):
            averageData.append(f"{covbr.iloc[v, 1]:.0f}")
            regionData.append(f"{covbr.iloc[v, 0]}")
        fig, ax = plt.subplots()
        ax.pie(averageData, labels=regionData, autopct='%.1f%%')
        st.pyplot(fig)
    elif criteria[0] == "Activity Evidence":
        elevation = ""
        evidence = st.sidebar.radio("Please the type of evidence:", ("Evidence Uncertain/ Uncertain Evidence", "Evidence Credible", "Eruption Observed", "Unrest / Holocene", "Confirmed Eruption", "Eruption Dated"))
        covbr = volcano.loc[(volcano["Activity Evidence"] == evidence), ["Region", "Elevation (m)"]]
        covbr = covbr.groupby(by="Region").count()
        covbr = covbr.reset_index()
        for v in range(len(covbr)):
            averageData.append(f"{covbr.iloc[v, 1]:.0f}")
            regionData.append(f"{covbr.iloc[v, 0]}")
        fig, ax = plt.subplots()
        ax.pie(averageData, labels=regionData, autopct='%.1f%%')
        st.pyplot(fig)
elif len(criteria) == 2:
    if criteria[0] == "Elevation (m)" and criteria[1] == "Activity Evidence":
        elevation = st.sidebar.slider("Pick the minimum elevation", -5000, 7000)
        evidence = st.sidebar.radio("Please the type of evidence:", ("Evidence Uncertain/ Uncertain Evidence", "Evidence Credible", "Eruption Observed", "Unrest / Holocene", "Confirmed Eruption", "Eruption Dated"))
        covbr = volcano.loc[(volcano["Activity Evidence"] == evidence) & (volcano["Elevation (m)"] > elevation), ["Region", "Elevation (m)"]]
        covbr = covbr.groupby(by="Region").count()
        covbr = covbr.reset_index()
        for v in range(len(covbr)):
            averageData.append(f"{covbr.iloc[v, 1]:.0f}")
            regionData.append(f"{covbr.iloc[v, 0]}")
        fig, ax = plt.subplots()
        ax.pie(averageData, labels=regionData, autopct='%.1f%%')
        st.pyplot(fig)
    elif criteria[1] == "Elevation (m)" and criteria[0] == "Activity Evidence":
        elevation = st.sidebar.slider("Pick the minimum elevation", -5000, 7000)
        evidence = st.sidebar.radio("Please the type of evidence:", ("Evidence Uncertain/ Uncertain Evidence", "Evidence Credible", "Eruption Observed", "Unrest / Holocene", "Confirmed Eruption", "Eruption Dated"))
        covbr = volcano.loc[(volcano["Activity Evidence"] == evidence) & (volcano["Elevation (m)"] > elevation), ["Region", "Elevation (m)"]]
        covbr = covbr.groupby(by="Region").count()
        covbr = covbr.reset_index()
        for v in range(len(covbr)):
            averageData.append(f"{covbr.iloc[v, 1]:.0f}")
            regionData.append(f"{covbr.iloc[v, 0]}")
        fig, ax = plt.subplots()
        ax.pie(averageData, labels=regionData, autopct='%.1f%%')
        st.pyplot(fig)


st.header("The more you know!")
if st.button("Click to see what happens when you jump in a volcano"):
    st.image("myWish.jfif", width=400)
    st.balloons()



a, b = aveElevations(countryOrRegion, highestOrLowest)
if highestOrLowest == "Highest Average":
    a.reverse()
    b.reverse()
plt.bar(a, b, color="g")
plt.xlabel(countryOrRegion)
plt.ylabel("Average Elevation")
plt.title(f"Top 5 {highestOrLowest} Elevations by {countryOrRegion}")
plt.show()
