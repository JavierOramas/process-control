import pandas as pd
import json
import streamlit as st
import matplotlib.pyplot as plt
import datetime
import numpy as np
from matplotlib import colors as mcolors
import random


def remove_columns(dataframe, columns_needed):
    columns=list(dataframe)
    
    for x in columns_needed:
        columns.remove(x)

    dataframe=dataframe.drop(columns, axis=1)  
    return dataframe

dataframe = pd.read_json('log.json', lines=True, convert_dates=True)
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

def generate_random_colors(amount):
    colors=[]
    color= "#{:06x}".format(random.randint(0, 0xFFFFFF))

    for i in range(amount+1):
        color= "#{:06x}".format(random.randint(0, 0xFFFFFF))
        if not color in colors:
            colors.append(color)
        else:
            i-=1
    
    return colors

def group_by_day(date,dateframe): 
    month=date.month
    year=date.year
    day=date.day
    
    groups = dataframe.groupby(['create_year','create_month', 'create_day'])
    return groups.get_group((str(year),str(month),str(day)))

df_for_date=split_date(dataframe)
#hour_data_group = dataframe.groupby(dataframe['create_time'].dt.hour)

#st.dataframe(pd.DataFrame(df.groupby(df['username'])))

users = set(dataframe['username'])

dataframe_by_name = pd.DataFrame(dataframe.groupby(['username']).sum(), columns=['memory_percent', 'cpu_percent','num_threads'])
#st.dataframe(dataframe_by_name)

ndf = pd.DataFrame(dataframe.groupby(dataframe['create_time'].dt.day).mean(),columns=['memory_percent', 'cpu_percent','num_threads','cmdline'])
st.text("Consumo general")
st.line_chart(ndf)
    
info_mode = st.sidebar.radio('Ver info:',('General','Por Usuario'))


#day_data = day_data_group.get_group(date) 

if info_mode == 'General':
    #details_mode = st.sidebar.checkbox('ver datos por hora',key='details')
    
    details_day_mode = st.sidebar.checkbox('ver datos de un día',key='details_day')
    if details_day_mode:
        date_day = st.sidebar.date_input("fecha",datetime.datetime.now(), key="daydate")
        st.text("Consumo en el dia: "+str(date_day.day)+'-'+str(date_day.month)+'-'+str(date_day.year))
        try:            
            df = group_by_day(date_day,ndf)  
            df = pd.DataFrame(df.groupby('create_time').sum(),columns=['memory_percent','cpu_percent','num_threads'])
            st.line_chart(df)
            if st.checkbox("mostrar eventos"):
                day_df = dataframe[dataframe['create_day'] == str(date_day.day)]     
                day_df = day_df[day_df['create_month'] == str(date_day.month)]
                day_df = day_df[day_df['create_year'] == str(date_day.year)]
                day_df = day_df.sort_values('create_time')
                day_df
        except:
           st.text("No hay datos de la fecha selecionada") 
           
    #     day_data
    #     day_df_data = pd.DataFrame(day_data.groupby(day_data[DATE_COLUMN].dt.minute).median(),
    #                                 columns=['memory_percent', 'cpu_percent','num_threads','cmdline'])
    #     day_df_data
else:
    selected = st.multiselect("Usuarios", [x for x in users])

summary = st.sidebar.checkbox("Mostrar total de recursos consumidos en un mes")

if summary: 
    try:
        date = st.sidebar.date_input("fecha",datetime.datetime.now())
        month=date.month
        year=date.year
        tupla=(str(year),str(month))
        new_df=df_for_date.groupby(['create_year' , 'create_month'])
        new_df=new_df.get_group(tupla)
        new_df=new_df.drop(new_df.columns[6:], axis=1)
        st.dataframe(new_df)
        users_df = new_df

        usernames = new_df.groupby(['username'])
        new_df = pd.DataFrame(usernames.mean(), columns=['memory_percent', 'cpu_percent','num_threads'])
        st.dataframe(new_df)    

        plt.figure(figsize=(10,5))
        barWidth=0.25
        x_position=np.arange(3)
        x_position=[x-barWidth for x in x_position]
        count=0
        #new_df.iloc[:,0]
        #st.text(list(new_df.iloc[0]))
        usernames = usernames.groups.keys()
        colors=generate_random_colors(len(usernames))

        for names in usernames:  
            values=list(new_df.iloc[count])
            x_position=[x+barWidth for x in x_position]
            plt.bar(x_position, values, color=colors[count], width=barWidth, label=names)
            count+=1

        columns_names=list(new_df)
        plt.xticks([y + barWidth for y in range(3)], columns_names) 
        plt.ylabel('Total en el mes')
        plt.legend()
        st.pyplot(plt.show())
        
    except:
        st.text("No hay datos de la fecha selecionada")
        
    selected = st.multiselect("Usuarios", [x for x in users])
    for x in selected:
        st.markdown(x)
        df_filter = users_df['username'] == x
        user_df = users_df[df_filter]
        user_df
        plot_df = pd.DataFrame(user_df.groupby(dataframe['create_time'].dt.day).mean(),columns=['memory_percent', 'cpu_percent','num_threads'])
        st.line_chart(plot_df)