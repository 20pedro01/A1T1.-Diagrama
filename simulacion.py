import matplotlib.pyplot as plt
import random
import pandas as pd

# ----- Función de simulación -----
def generar_simulacion(tiempo_total=10*60):
    tiempos_llegada = []
    acumulado = 0

    while acumulado < tiempo_total:
        llegada = round(random.uniform(5, 60), 2)
        acumulado += llegada
        if acumulado > tiempo_total:
            break
        tiempos_llegada.append(acumulado)

    tiempos_entrega = []
    estado_entrega = []

    for llegada in tiempos_llegada:
        entrega = round(random.uniform(120, 180), 2)  # 2 a 3 minutos
        if llegada + entrega <= tiempo_total:
            tiempos_entrega.append(entrega)
            estado_entrega.append(True)
        else:
            tiempos_entrega.append(None)
            estado_entrega.append(False)

    df = pd.DataFrame({
        "Cliente": range(1, len(tiempos_llegada)+1),
        "Tiempo_llegada_seg": tiempos_llegada,
        "Tiempo_entrega_seg": tiempos_entrega,
        "Pedido_entregado": estado_entrega
    })
    return df

# ----- Estudio de campo (datos fijos) -----
estudio_campo = [
    (1, 6.62, 129.69, True), 
    (2, 15.04, 174.61, True),
    (3, 24.33, 165.76, True),
    (4, 47.36, 146.45, True),
    (5, 61.62, 172.87, True),
    (6, 85.32, 154.98, True),
    (7, 99.87, 159.30, True),
    (8, 142.00, 123.72, True),
    (9, 174.56, 150.92, True),
    (10, 218.73, 149.11, True),
    (11, 255.74, 122.85, True),
    (12, 293.02, 147.39, True),
    (13, 311.63, 147.20, True),
    (14, 336.25, 124.51, True),
    (15, 367.79, 130.37, True),
    (16, 403.71, 154.31, True),
    (17, 439.82, 175.24, False),
    (18, 445.82, 127.79, True),
    (19, 463.77, 172.40, False),
    (20, 477.24, 177.93, False),
    (21, 507.46, 134.05, False),
    (22, 534.89, 126.43, False),
    (23, 555.48, 162.41, False),
    (24, 592.84, 125.69, False)
]
df_campo = pd.DataFrame(estudio_campo, columns=["Cliente", "Tiempo_llegada_seg", "Tiempo_entrega_seg", "Pedido_entregado"])

# ----- Generar simulación -----
df_simulado = generar_simulacion()

print("=== Estudio de campo ===")
print(df_campo.to_string(index=False))

print("\n=== Simulación ===")
print(df_simulado.to_string(index=False))

# ----- Gráfica 1: Pedidos entregados vs no entregados -----
entregados_campo = df_campo["Pedido_entregado"].value_counts()
entregados_sim = df_simulado["Pedido_entregado"].value_counts()

labels = ["Entregado", "No entregado"]
campo_counts = [entregados_campo.get(True, 0), entregados_campo.get(False, 0)]
sim_counts = [entregados_sim.get(True, 0), entregados_sim.get(False, 0)]

x = range(len(labels))
width = 0.35

plt.figure(figsize=(8,5))
plt.bar([i - width/2 for i in x], campo_counts, width, label="Estudio de campo", color="skyblue")
plt.bar([i + width/2 for i in x], sim_counts, width, label="Simulación", color="salmon")
plt.xticks(x, labels)
plt.ylabel("Número de pedidos")
plt.title("Pedidos entregados vs no entregados")
plt.legend()
plt.show()

# ----- Gráfica 2: Tiempos de llegada acumulados -----
plt.figure(figsize=(10,5))
plt.plot(df_campo["Cliente"], df_campo["Tiempo_llegada_seg"], marker='o', label="Campo")
plt.plot(df_simulado["Cliente"], df_simulado["Tiempo_llegada_seg"], marker='s', label="Simulación")
plt.xlabel("Cliente")
plt.ylabel("Tiempo de llegada (segundos)")
plt.title("Comparación de tiempos de llegada")
plt.legend()
plt.grid(True)
plt.show()

# ----- Gráfica 3: Tiempos de entrega de pedidos completados -----
campo_entregados = df_campo[df_campo["Pedido_entregado"] == True]
sim_entregados = df_simulado[df_simulado["Pedido_entregado"] == True]

plt.figure(figsize=(10,5))
plt.plot(campo_entregados["Cliente"], campo_entregados["Tiempo_entrega_seg"], marker='o', label="Campo")
plt.plot(sim_entregados["Cliente"], sim_entregados["Tiempo_entrega_seg"], marker='s', label="Simulación")
plt.xlabel("Cliente")
plt.ylabel("Tiempo de entrega (segundos)")
plt.title("Tiempos de entrega de pedidos completados")
plt.legend()
plt.grid(True)
plt.show()

# ----- Gráfica 4: Distribución de tiempos de entrega -----
plt.figure(figsize=(8,5))
plt.hist(campo_entregados["Tiempo_entrega_seg"], bins=8, alpha=0.6, label="Campo")
plt.hist(sim_entregados["Tiempo_entrega_seg"], bins=8, alpha=0.6, label="Simulación")
plt.xlabel("Tiempo de entrega (segundos)")
plt.ylabel("Cantidad de pedidos")
plt.title("Distribución de tiempos de entrega")
plt.legend()
plt.show()