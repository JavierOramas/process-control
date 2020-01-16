import json
import streamlit as st
import matplotlib.pyplot as plt

f = open('data.json')

process = []
for i, line in enumerate(f):
    #print(i)
    process.append(json.loads(line))

#print([p['cmdline'] for p in process]
#print("start \n")

users = {}
usuarios = []
for p in process:
    users[p['username']] = []
    

for p in process:
    users[p['username']].append([p["cmdline"],p['num_threads'],p['memory_percent'],p['cpu_percent']])

usuarios = [x for x in users]


selected = st.multiselect("Usuarios", usuarios)
for x in selected:
    st.header(x)
    mem = []
    threads = []
    cpu = []
    for y in users[x]:
        st.text(y[0])
        threads.append(y[1])
        mem.append(y[2])
        cpu.append(y[3])
    
    #grafico de threads
    fig = plt.figure(u'Uso de Threads')
    ax = fig.add_subplot(111)
    xx = range(len(threads))
    ax.bar(xx,threads,align='center')
    plt.ylim(0)
    
    st.markdown('### Uso de Threads')
    st.pyplot(plt.show())
    
    #grafico de memoria
    fig = plt.figure(u'% de uso Memoria')
    ax = fig.add_subplot(111)
    xx = range(len(mem))
    ax.bar(xx,mem,align='center')
    plt.ylim(0)
    
    st.markdown('### Uso de Memoria')
    st.pyplot(plt.show()) 
    
    #grafico de CPU
    fig = plt.figure(u'Uso de CPU')
    ax = fig.add_subplot(111)
    xx = range(len(cpu))
    ax.bar(xx,cpu,align='center')
    plt.ylim(0)
    
    st.markdown('### Uso de CPU')
    st.pyplot(plt.show())
        
        

     