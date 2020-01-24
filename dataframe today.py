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

def group_by_day(date,dateframe): 
    month=date.month
    year=date.year
    day=date.day
    
    groups = dataframe.groupby(['create_year','create_month', 'create_day'])
    return groups.get_group((str(year),str(month),str(day)))

def group_by_hour(hour,dateframe): 
    groups = dataframe.groupby(['create_year','create_month', 'create_day'])
    return groups.get_group((str(year),str(month),str(day)))

df_for_date=split_date(dataframe)
#hour_data_group = dataframe.groupby(dataframe['create_time'].dt.hour)

#st.dataframe(pd.DataFrame(df.groupby(df['username'])))

users = set(dataframe['username'])

dataframe_by_name = pd.DataFrame(dataframe.groupby(['username']).sum(), columns=['memory_percent', 'cpu_percent','num_threads','create_day','create_month','create_day'])
st.dataframe(dataframe_by_name)

ndf = pd.DataFrame(dataframe.groupby(dataframe['create_time'].dt.day).mean(),columns=['memory_percent', 'cpu_percent','num_threads','cmdline','create_day','create_month','create_day'])
st.line_chart(ndf)
    
info_mode = st.sidebar.radio('Ver info:',('General','Por Usuario'))


#day_data = day_data_group.get_group(date) 

if info_mode == 'General':
    
    # details_hour_mode = st.sidebar.checkbox('ver datos por hora',key='details')
    # if details_hour_mode:
    #     date_hour = st.sidebar.date_input("fecha",datetime.datetime.now(), key="hourdate")
    #     hora = st.sidebar.slider("hora", 0,23,12,key="hora")
    #     try:
    #         df = group_by_day(date_day,ndf)  
    #         df = pd.DataFrame(df.groupby('create_time').sum(),columns=['memory_percent','cpu_percent','num_threads','create_hour'])
            
    #         st.line_chart(df)
    #         if st.checkbox("mostrar dataframe"):
    #             #poner el dataframe completo
    #             df
        # except:
        #     st.text("No hay datos de la fecha selecionada")
            
    details_day_mode = st.sidebar.checkbox('ver datos de un día',key='details_day')
    if details_day_mode:
        date_day = st.sidebar.date_input("fecha",datetime.datetime.now(), key="daydate")
        st.text(str(date_day.day)+'-'+str(date_day.month)+'-'+str(date_day.year))
        try:            
            df = group_by_day(date_day,ndf)  
            df = pd.DataFrame(df.groupby('create_time').sum(),columns=['memory_percent','cpu_percent','num_threads'])
            st.line_chart(df)
            if st.checkbox("mostrar dataframe"):
                day_df = dataframe[dataframe['create_day'] == str(date_day.day)]     
                day_df = day_df[day_df['create_month'] == str(date_day.month)]
                day_df = day_df[day_df['create_year'] == str(date_day.year)]
                day_df = day_df.sort_values('create_time')
                day_df
        except:
           st.text("No hay datos de la fecha selecionada") 
           
# else:
#     selected = st.multiselect("Usuarios", [x for x in users])
#     st.text(x for x in selected)


summary = st.sidebar.checkbox("Mostrar total de recursos consumidos en un mes")
if summary: 
    date = st.sidebar.date_input("fecha",datetime.datetime.now(),key='summary_date')
    month=date.month
    year=date.year
    tupla=(str(year),str(month))
    new_df=df_for_date.groupby(['create_year' , 'create_month'])
    try:
        new_df=new_df.get_group(tupla)
        new_df=new_df.drop(new_df.columns[6:], axis=1)
        st.dataframe(new_df)
    except:
        st.text("No hay datos de la fecha selecionada")
        
# def hour_filter(dataframe,date,):
 
