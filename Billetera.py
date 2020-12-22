# Billetera de Escritorio realizado por: Ing. Andrea González

# SALUDO DE BIENVENIDA
print("\nHola, bienvenido(a) a tu billetera virtual de escritorio \n")

# ARCHIVOS
saldos="Saldos.txt"
cod="Codigo.txt"
hist="Historial.txt"

# CÓDIGO PROPIO
archivo1=open(cod,"r")
texto=archivo1.read()
archivo1.close()
if texto == "":
    print("\nNos complace tenerte por primera vez en tu nueva billera virtual \n")
    print("\nPor favor, cree el código propio de su cuenta. \nEl mismo debe tener al menos seis (6) carácteres. \nLos mismos deben ser carácteres alfabéticos y/o numéricos")
    codpropio=input("\nIngrese su código propio: ")
    codpropioset=set(codpropio)
    caractvalidos="abcedefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    caractvalidosset=set(caractvalidos)
    while not codpropioset<=caractvalidosset:
        print("Código inválido")
        codpropio=input("\nIngrese su código propio: ")
    else:
        while not len(codpropio)>6:
            print("Código inválido")
            codpropio=input("\nIngrese su código propio: ")
        else: 
            print("\nCódigo creado con éxito. Tu código es: "+codpropio)
            archivo1=open(cod,"a")
            archivo1.write(codpropio)
            archivo1.close()


# MENÚ DE OPCIONES
print("\nMENÚ DE OPCIONES")
menu=input("""
1. Recibir monto
2. Transferir monto
3. Mostrar balance parcial
4. Mostrar balance general
5. Mostrar historial de transacciones
6. Salir
\nIngresa el número correpondiente a la operación que desea realizar: """)
while not int(menu) in range(1,7):
    menu=input("\nOpción inválida, las opciones válidas son números del 1 al 6. \nIngrese el número correpondiente a la operación que desea realizar: ")

# Módulos y funciones
import requests
from funcbilletera import *

# Monedas válidas a ingresar, almacenadas en www.api.binance.com
monedas={}
moneda=requests.get("https://api.binance.com/api/v3/ticker/price").json()
for cripto in moneda:
    monedas[cripto["symbol"]]=cripto["price"]
    montupla=tuple(monedas.keys())

# Diccionario de monedas existentes en la billetera:
archivo2=open(saldos,"r")   
texto=archivo2.read()
archivo2.close()
if texto!="":
    lineas=texto.splitlines()
    monedasexist={}
    for linea in lineas:
        saldo=linea.split(":")
        monedasexist[saldo[0]]=saldo[1]
        monedasexisttupla=tuple(monedasexist.keys())
        monedasexistlista=list(monedasexist.keys())
else:
    monedasexist={}

# Opción 1: RECIBIR MONTO
if menu=="1":
    monedaing=input("Ingrese las siglas de la moneda que desea recibir: ")
    while (monedaing+"USDT") not in montupla:  
        print("Moneda inválida. Intente ingresando otra moneda")
        monedaing=input("Ingrese las siglas de la moneda que desea recibir: ")
    else:
        print("Moneda válida")
        montoing=input("Ingrese la cantidad de "+monedaing+" que desea recibir: ")
        while not montoing.replace(".","",1).isdigit():
            print("Cantidad inválida")
            montoing=input("Ingrese la cantidad de "+monedaing+" que desea recibir: ")
        else:
            print("Cantidad válida")
            archivo1=open(cod,"r")
            codigo=archivo1.read()
            archivo1.close()
            codigoing=input("Ingrese el código de la cantidad de "+montoing+" "+monedaing+" que desea recibir: ")
            while codigoing==codigo:
                print("Código inválido")
                codigoing=input("Ingrese el código de la cantidad de "+montoing+" "+monedaing+" que desea recibir: ") 
            else: 
                print("Código válido")
                usd=float(monedas.get((monedaing+"USDT")))*float(montoing)
                if monedasexist!={}: # Cuando existen monedas en el diccionario
                    if monedasexist.get(monedaing): # Cuando la moneda ingresada existe
                        nuevosaldo=float(monedasexist.get(monedaing))+float(montoing)
                        guardarexistente(monedasexist, monedaing, nuevosaldo, saldos, montoing, usd, "recibir")
                        usdtotal=float(monedas.get((monedaing+"USDT")))*nuevosaldo 
                        print("Su saldo actual es de %9.2f"%nuevosaldo+" "+monedaing+" siendo un total de: %9.2f"%usdtotal+" USD para el momento de la transacción")
                    else: # Cuando la moneda ingresasa no existe
                        monedasexist[monedaing]=montoing
                        guardaralfinal(saldos, monedaing, float(montoing), usd, "recibir")
                else: # Cuando el diccionario "monedasexist" (monedas existentes) está vacío
                    guardaralfinal(saldos, monedaing, float(montoing), usd, "recibir")
                guardarhist(hist, float(montoing), monedaing, usd, codigoing, "recibir")

# Opción 2: TRANSFERIR MONTO
elif menu=="2":
    if monedasexist!={}: # Cuando existen monedas a transferir
        monedaing=input("Ingrese las siglas de la moneda que desea transferir: ")
        while monedaing not in monedasexisttupla: # Cuando la moneda no está dentro de las monedas existentes
            print("Moneda no existente. Ingrese alguna de las monedas que posee para el momento:")
            i=0
            while i<(len(monedasexistlista)):
                print(monedasexistlista[i])
                i+=1
            monedaing=input("Ingrese las siglas de la moneda que desea transferir: ")
        else: # Cuando la moneda se encuentra en la billetera
            print("Moneda válida")
            print("Recuerde que el monto a transferir debe ser menor o igual a su saldo actual en "+monedaing)
            print("Usted dispone de un total de "+monedasexist.get(monedaing)+" "+monedaing+".")
            montoing=input("Ingrese la cantidad de "+monedaing+" que desea transferir: ")
            while not montoing.replace(".","",1).isdigit() or float(montoing)>float(monedasexist.get(monedaing)):
                if not montoing.replace(".","",1).isdigit():
                    print("Ingrese un monto con carácteres numéricos")
                    montoing=input("Ingrese la cantidad de "+monedaing+" que desea transferir: ")
                elif float(montoing)>float(monedasexist.get(monedaing)):
                    print("Saldo insuficiente")
                    montoing=input("Ingrese la cantidad de "+monedaing+" que desea transferir: ")
                elif not montoing.replace(".","",1).isdigit() and float(montoing)>float(monedasexist.get(monedaing)):
                    print("Cantidad inválida")
                    montoing=input("Ingrese la cantidad de "+monedaing+" que desea transferir: ")
            else:
                print("Cantidad válida")
                archivo1=open(cod,"r")
                codigo=archivo1.read()
                archivo1.close()
                codigoing=input("Ingrese el código destino para la transferencia de "+montoing+" "+monedaing+": ")
                while codigoing==codigo:
                    print("Código inválido")
                    codigoing=input("Ingrese el código destino para la transferencia de "+montoing+" "+monedaing+": ") 
                else: 
                    print("Código válido")
                    usd=float(monedas.get((monedaing+"USDT")))*float(montoing)
                    nuevosaldo=float(monedasexist.get(monedaing))-float(montoing)
                    guardarexistente(monedasexist, monedaing, nuevosaldo, saldos, montoing, usd, "transferir")
                    usdtotal=float(monedas.get((monedaing+"USDT")))*nuevosaldo 
                    print("Su saldo actual es de %7.2f"%nuevosaldo+" "+monedaing) 
                    print("Cantidad en dólares: %9.2f"%usdtotal+" USD para el momento de la transacción")
                    guardarhist(hist, float(montoing), monedaing, usd, codigoing, "transferir")
    else:
        print("Usted aún no posee monedas en su billetera para realizar esta transacción")

# Opción 3: MOSTRAR BALANCE PARCIAL
elif menu=="3": 
    if monedasexist!={}: # Cuando existen monedas que consultar:
        monedaing=input("Ingrese las siglas de la moneda que desea consultar: ")
        while not monedaing in monedasexisttupla:  # Cuando la moneda no está dentro de la billetera
            print("Moneda no existente. Intente ingresando alguna de las monedas que posee para el momento, mostradas a continuación: ")
            i=0
            while i<(len(monedasexisttupla)):
                print(monedasexistlista[i])
                i+=1
            monedaing=input("Ingrese las siglas de la moneda que desea consultar: ")
        else: # Cuando la moneda se encuentra en la billetera
            print("Moneda válida")
            usd=float(monedas.get((monedaing+"USDT")))*float(monedasexist.get(monedaing))
            print("Usted posee la cantidad de: "+monedasexist.get(monedaing)+" "+monedaing)
            print("Cantidad en USD: %7.2f"%usd+", de acuerdo a la cotización actual de la moneda "+monedaing)
    else:
        print("Usted aún no posee monedas a consultar")

# Opción 4: MOSTRAR BALANCE GENERAL
elif menu=="4":
    if monedasexist!={}: # Cuando existen monedas
        monedaslista=list(monedasexist.keys())
        saldoslista=list(monedasexist.values())
        print("\nBALANCE PARCIAL\n")
        i=0
        usd=0.0
        usdtotal=0.0
        while i<len(monedaslista):
            usd=float(monedas.get((monedaslista[i]+"USDT")))*float(saldoslista[i])
            print("Moneda: "+monedaslista[i]+". Cantidad: %7.2f"%float(saldoslista[i])+". Monto en USD: %7.2f"%usd)
            i+=1
            usdtotal+=usd
        print("\nUsted posee un total de USD %7.2f"%usdtotal)
    else:
        print("Usted aún no posee monedas a consultar")

# Opción 5: MOSTRAR HISTORIAL
elif menu=="5":
    archivo3=open(hist,"r")
    texto=archivo3.read()
    archivo3.close()
    vacio="HISTORIAL DE TRANSACCIONES\n\n"
    if texto==vacio:
        print("Usted aún no posee historial de movimientos a consultar")
    else:
        print("\n"+texto)

# Opción 6: SALIR
else:
    exit()