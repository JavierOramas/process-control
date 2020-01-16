import pandas as pd
import json
import streamlit as st
import matplotlib.pyplot as plt
import datetime

df = pd.read_json('data.json', lines=True,convert_dates=True)
df.create_time = df.create_time.apply(pd.to_datetime)
df['create_date'] = [d.date() for d in df['create_time']]
df['create_hour'] = [d.time() for d in df['create_time']]
df
#st.dataframe(pd.DataFrame(df.groupby(df['username'])))

users = set(df['username'])

ndf = pd.DataFrame(df.groupby(df['create_time'].dt.hour).mean(),columns=['memory_percent', 'cpu_percent','num_threads','cmdline'])
st.line_chart(ndf)
    
info_mode = st.sidebar.radio('Ver info:',('General','Por Usuario'))

date = st.sidebar.date_input("fecha",datetime.datetime.now())
#day_data = day_data_group.get_group(date) 

if info_mode == 'General':
    details_mode = st.sidebar.checkbox('ver datos por hora',key='details')
    
    if details_mode:
        hora = st.sidebar.slider("hora", 0,23,12,key="hora")
        if hora in [x[0] for x in hour_data_group]:
            hour_data = hour_data_group.get_group(hora)
            hour_data
            hour_df_data = pd.DataFrame(hour_data.groupby(hour_data['create_time'].dt.minute).sum(),columns=['memory_percent','cpu_percent','num_threads'])
            hour_df_data
            st.line_chart(hour_df_data)
    # else:
    #     day_data
    #     day_df_data = pd.DataFrame(day_data.groupby(day_data[DATE_COLUMN].dt.minute).median(),
    #                                 columns=['memory_percent', 'cpu_percent','num_threads','cmdline'])
    #     day_df_data
else:
    selected = st.sidebar.multiselect("Usuarios", [x for x in users])

    