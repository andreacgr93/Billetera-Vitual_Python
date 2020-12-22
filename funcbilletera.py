# FUNCIONES
from datetime import datetime
dia=datetime.now()

# Reporte de recepción o transferencia de monto 
# rot: "recibir" o "transferir"
def reporte(moneda, monto, usd, rot):
    if rot=="recibir":
        print("La cantidad de %7.2f"%monto+" "+moneda+", fue recibida con éxito.")
        print("Se ingresan: %7.2f"%usd+" USD, según a la cotización actual de la moneda "+moneda)
    else:
        print("La cantidad de %7.2f"%monto+" "+moneda+", fue transferida con éxito.")
        print("Se tranfieren: %7.2f"%usd+" USD, según a la cotización actual de la moneda "+moneda)

def guardarexistente(dicc, moneda, nuevosaldo, archivo, monto, usd, rot):
    dicc[moneda]=nuevosaldo
    monedaslista=list(dicc.keys())
    saldoslista=list(dicc.values())
    arch=open(archivo,"w")
    for i in range(0,len(monedaslista)):
        arch.write(monedaslista[i]+":"+str(saldoslista[i])+"\n")
    arch.close()
    if rot=="recibir":
        print(reporte(moneda, float(monto), usd, "recibir"))
    else:
        print(reporte(moneda, float(monto), usd, "transferir"))

def guardaralfinal(archivo, moneda, monto, usd, rot):
    arch=open(archivo,"a")
    arch.write(moneda+":"+str(monto)+"\n")
    arch.close()
    if rot=="recibir":
        print(reporte(moneda, float(monto), usd, "recibir"))
    else:
        print(reporte(moneda, float(monto), usd, "transferir"))

def guardarhist(archivo, monto, moneda, usd, codigo, rot):
    arch=open(archivo,"a")
    if rot=="recibir":
        arch.write(dia.strftime("Fecha: %d/%m/%Y.")+" Moneda: "+moneda+". Monto (+): %9.2f"%monto+". Cantidad (USD): %9.2f"%usd+". Código: "+codigo+"\n")
    else:
        arch.write(dia.strftime("Fecha: %d/%m/%Y.")+" Moneda: "+moneda+". Monto (-): %9.2f"%monto+". Cantidad (USD): %9.2f"%usd+". Código: "+codigo+"\n")
    arch.close()