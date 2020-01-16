import json
import streamlit as st
import time
import datetime
import pandas as pd
from datetime import date
import matplotlib.pyplot as plt

#f = st.cache(open)('data.json')
f = open('data.json')
process = []
for i, line in enumerate(f):
    process.append(json.loads(line))

users = {}

for p in process:
    if not p['username'] in users:
        users[p['username']] = []
 
    users[p['username']].append([p["cmdline"],p['num_threads'],p['memory_percent'],p['cpu_percent'],p['create_time']])

selected = st.multiselect("Usuarios", [x for x in users])

for x in selected:
    st.header(x)
    st.sidebar.header(x)
    mem = []
    threads = []
    cpu = []
    lines = []
    times = []

    for y in users[x]:
        lines.append(y[0])
        threads.append(y[1])
        mem.append(y[2])
        cpu.append(y[3])
        times.append(datetime.datetime.strptime(time.ctime(y[4]), "%a %b %d %H:%M:%S %Y"))

    df = {"times":times,"memory_percent":mem,"number of threads":threads,"cpu_percent":cpu,"cmd_lines":lines}
    df = pd.DataFrame(df)
    
    if st.sidebar.checkbox("Show Dataframe",key=str(x)+"showdf"):
        st.dataframe(df)
    
    modo = st.sidebar.radio("Ver informacion por:", ("Dia", "Hora"),key=str(x)+"radio")
    if modo == 'Hora':
        dia = st.sidebar.date_input("dia",datetime.datetime.now(),key = str(x)+"date")
        hora = st.sidebar.slider("hora", 0,23,12,key=str(x)+"hora")
        new_df = pd.DataFrame(df.groupby(df['times'].dt.minute))
        new_df
    if modo == 'Dia':
        dia = st.sidebar.date_input("dia",datetime.datetime.now(),key = str(x)+"date")
    
    # if st.checkbox("Show All Data",key = x):
        
    #     for x in lines:
    #         st.code(x)

    #     #grafico de threads
    #     fig = plt.figure(u'Uso de Threads')
    #     ax = fig.add_subplot(111)
    #     xx = range(len(threads))
    #     ax.bar(xx,threads,align='center')
    #     plt.ylim(0)
        
    #     st.markdown('### Uso de Threads')
    #     st.pyplot(plt.show())
        
    #     #grafico de memoria
    #     fig = plt.figure(u'% de uso Memoria')
    #     ax = fig.add_subplot(111)
    #     xx = range(len(mem))
    #     ax.bar(xx,mem,align='center')
    #     plt.ylim(0)
        
    #     st.markdown('### Uso de Memoria')
    #     st.pyplot(plt.show()) 
        
    #     #grafico de CPU
    #     fig = plt.figure(u'Uso de CPU')
    #     ax = fig.add_subplot(111)
    #     xx = range(len(cpu))
    #     ax.bar(xx,cpu,align='center')
    #     plt.ylim(0)
        
    #     st.markdown('### Uso de CPU')
    #     st.pyplot(plt.show())
    
    # start_date = st.date_input("From",datetime.datetime.now(),key = str(x)+"date_start")
    # end_date = st.date_input("To",datetime.datetime.now(),key = str(x)+"date_end")
   
    # if start_date > end_date:
    #     st.error("Invalid Date interval")

    # for i in range(len(lines)):
    #     i_mem = []
    #     i_threads = []
    #     i_cpu = []
    #     i_times = []
    
    #     #if times[i].date <= end_date and date[i] >= start_date:
    #     if times[i].day <= end_date.day and times[i].day >= start_date.day and times[i].month <= end_date.month and times[i].month >= start_date.month and times[i].year <= end_date.year and times[i].year >= start_date.year:
    #         st.text(times[i])
    #         st.code(lines[i])
    #         i_threads.append(threads[i])
    #         i_mem.append(mem[i])
    #         i_cpu.append(cpu[i])
    #         i_times.append(times[i])


        

     