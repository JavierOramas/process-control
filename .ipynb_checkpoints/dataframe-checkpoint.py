import pandas
import streamlit as st
import matplotlib.pyplot as plt

df = pandas.read_json("superdata.json")

print(df)