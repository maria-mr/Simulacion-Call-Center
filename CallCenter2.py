import pandas as pd
import random

semilla =  19219106 # Utiliza tu matricula como semilla
random.seed(semilla)

num_clientes = 20

cliente=[]
num=1
for i in range(num_clientes):
    cliente.append(num)
    num = num+1

def getCumulative(probabilities):
    cumulative = []
    cumulative.append(probabilities[0])
    for i in range(1, len(probabilities)):
        cumulative.append(cumulative[i-1] + probabilities[i])
    return cumulative

times1 = [1, 2, 3, 4]
probabilities1 = [0.25,0.40 ,0.20 ,0.15]

cumulatives1 = getCumulative(probabilities1)

def getInterArrivalTimes(times1, cumulative1):
    assert len(times1) == len(cumulative1)
    r = random.random()
    for i in range(len(cumulative1)):
        if r < cumulative1[i]:
            return times1[i]

def generateInterArrivalTimes():
    InterArrival = [getInterArrivalTimes(times1, cumulatives1) for _ in range(num_clientes-1)]
    return InterArrival

InterArrival = generateInterArrivalTimes()


clock = 0

arrivalTimes = [clock]

for i in range(num_clientes-1):
    arrivalTimes.append(arrivalTimes[i] + InterArrival[i])

times2 = [3,4,5,6]
probabilities2 = [0.35,0.25,0.20,0.20]
        
cumulatives2 = getCumulative(probabilities2)
def getServiceTime(times2, cumulative2):
    assert len(times2) == len(cumulative2)
    r = random.random()
    for i in range(len(cumulative2)):
        if r < cumulative2[i]:
            return times2[i]

def generateServiceTimes():
    service_times = [getServiceTime(times2, cumulatives2) for _ in range(num_clientes)]
    return service_times

service_times = generateServiceTimes()
        
endService = []
service_begins=[]

for i in range(num_clientes):
        endService.append(arrivalTimes[i]+service_times[i])

InterArrival.insert(0, 0)
service_begins.insert(0,0)

for j in (j+1 for j in range(num_clientes-1)):
    if endService[j-1] >= arrivalTimes[j]:
        service_begins.append(endService[j-1])
        endService[j]=service_begins[j]+service_times[j] 
    else:
        service_begins.append(arrivalTimes[j])
        endService[j]=service_begins[j]+service_times[j]

waiting_time = []
for i in range(num_clientes):
    waiting_time.append(service_begins[i]-arrivalTimes[i])

time_system = []
for i in range(num_clientes):
    time_system.append(endService[i]-arrivalTimes[i])

idle_time = []
for i in range(num_clientes):
    if (arrivalTimes[i] == endService[i-1]):
        idle_time.append(0)
    elif (arrivalTimes[i] - endService[i-1] < 0):
        idle_time.append(0)
    else:
        idle_time.append(arrivalTimes[i]-endService[i-1])

df = pd.DataFrame({"Cliente": cliente,"Tiempo entre Llegada" : InterArrival,"Tiempo de Llegada" : arrivalTimes,"Tiempo de Servicio" : service_times,  "Inicio de Servicio" : service_begins,"Fin de Servicio" : endService,
"Tiempo de espera": waiting_time,"Tiempo del Cliente en el Sistema" : time_system, "Tiempo de inactividad":idle_time })
print(df)

#Tiempo promedio de espera = tiempo total de clientes en la fila / numero total de clientes
avgWaitingTime = sum(waiting_time)/num_clientes
print("Tiempo de espera promedio: ", avgWaitingTime)

#Tiempo promedio de servicio = tiempo total de servicio / numero total de clientes
x = num_clientes
avgServiceTime = endService[x-1]/num_clientes
print("Tiempo promedio de servicio: ", avgServiceTime)

#Tiempo promedio que pasa un cliente en el sistema = total de tiempo que los clientes pasan en el sistema / numero total de clientes
avgTimeSystem = sum(time_system) / num_clientes
print("Tiempo promedio que pasa un cliente en el sistema: ", avgTimeSystem)