import pandas as pd
import json
import streamlit as st
import matplotlib.pyplot as plt
import datetime

def remove_columns(dataframe, columns_needed):
    columns=list(dataframe)
    
    for x in columns_needed:
        columns.remove(x)

    dataframe=dataframe.drop(columns, axis=1)  
    return dataframe

dataframe = pd.read_json('data.json', lines=True, convert_dates=True)
columns_needed=['username','create_time', 'memory_percent', 'num_threads', 'cpu_percent','cmdline']

dataframe=remove_columns(dataframe, columns_needed)
st.dataframe(dataframe)

def split_date(dataframe):
    df=dataframe
    df.create_time = df.create_time.apply(pd.to_datetime)
    df['create_date'] = [str(d.date()) for d in df['create_time']]
    df['create_year'],df['create_month'],df['create_day'] = df['create_date'].str.split('-',2).str
    df['create_hour'] = [d.time() for d in df['create_time']]  
    return df

df_for_date=split_date(dataframe)
#hour_data_group = dataframe.groupby(dataframe['create_time'].dt.hour)

#st.dataframe(pd.DataFrame(df.groupby(df['username'])))

users = set(dataframe['username'])

dataframe_by_name = pd.DataFrame(dataframe.groupby(['username']).sum(), columns=['memory_percent', 'cpu_percent','num_threads'])
st.dataframe(dataframe_by_name)

ndf = pd.DataFrame(dataframe.groupby(dataframe['create_time'].dt.day).mean(),columns=['memory_percent', 'cpu_percent','num_threads','cmdline'])
st.line_chart(ndf)
    
info_mode = st.sidebar.radio('Ver info:',('General','Por Usuario'))


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
    selected = st.multiselect("Usuarios", [x for x in users])

summary = st.sidebar.checkbox("Mostrar total de recursos consumidos en un mes")

if summary: 
    date = st.sidebar.date_input("fecha",datetime.datetime.now())
    month=date.month
    year=date.year
    st.text(year)
    tupla=(str(year),str(month))
    new_df=df_for_date.groupby(['create_year' , 'create_month'])
    new_df=new_df.get_group(tupla)
    new_df=new_df.drop(new_df.columns[6:], axis=1)
    st.dataframe(new_df)