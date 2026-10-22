import gradio as gr
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
# =====================================================================
# 1. BASES DE DATOS DEL ECOSISTEMA INTEGRADO
# =====================================================================
DATOS_CADENA = {
    "Insumos": {
        "Definición": "Conjunto de recursos financieros, humanos, tecnológicos y normativos que se movilizan para iniciar la cadena de intervención.",
        "Indicador": "Eficiencia y Gestión del Gasto (Relación Financiera/Insumo)",
        "Nodo Teórico": "Nodo D (Justicia Algorítmica y Tecnología) / Nodo E (Presupuesto Diferencial)",
        "Caso Tunja": "Recursos financieros asignados por el Fondo Local de Salud de Tunja y talento humano contratado para la atención de la vejez.",
        "Justificacion_Escenario": "Los insumos determinan el techo fiscal frente a crisis globales. Sin recursos iniciales, el índice de adaptabilidad cae críticamente.",
        "Metricas_Simuladas": [80, 20]
    },
    "Actividades": {
        "Definición": "Procesos y tareas de planificación, ejecución y gestión operativa que transforman los insumos en entregables.",
        "Indicador": "Gestión Operativa y Procesos (Eficiencia Técnica de Actividades)",
        "Nodo Teórico": "Nodo C (Gobernanza e Inclusión Transformativa)",
        "Caso Tunja": "Co-diseño y ejecución de talleres de estimulación cognitiva, salud física y adecuación de Centros Vida.",
        "Justificacion_Escenario": "Las actividades miden la capacidad de descentralizar la política frente a transformaciones digitales.",
        "Metricas_Simuladas": [70, 30]
    },
    "Productos": {
        "Definición": "Bienes y servicios cuantificables y tangibles entregados directamente a la población objetivo.",
        "Indicador": "Eficacia (Cumplimiento de Metas y Cobertura de Productos)",
        "Nodo Teórico": "Nodo E (Pertinencia territorial y enfoque diferencial)",
        "Caso Tunja": "500 Adultos mayores vulnerables atendidos con subsidios alimentarios y atención psicosocial.",
        "Justificacion_Escenario": "La entrega de productos amortigua el impacto inmediato de crisis macroeconómicas.",
        "Metricas_Simuladas": [90, 10]
    },
    "Resultados": {
        "Definición": "Cambios tangibles a corto y mediano plazo en las condiciones de vida atribuibles a los productos recibidos.",
        "Indicador": "Efectividad (Seguimiento al Desempeño y Efectos Intermedios)",
        "Nodo Teórico": "Nodo B (Causalidad Social e Incertidumbre)",
        "Caso Tunja": "Incremento medido del 35% en el índice de autonomía funcional y disminución del aislamiento social.",
        "Justificacion_Escenario": "Los resultados evalúan la resiliencia comunitaria ante desastres climáticos o sociales.",
        "Metricas_Simuladas": [65, 35]
    },
    "Impactos": {
        "Definición": "Transformaciones estructurales, sistémicas y de largo plazo en las condiciones de vida de la sociedad.",
        "Indicador": "Valor Público e Impacto Social (Evaluación de Impacto de Largo Plazo)",
        "Nodo Teórico": "Nodo A (Creación de Valor Público y Legitimidad)",
        "Caso Tunja": "Garantía constitucional y social de un envejecimiento digno, saludable y participativo.",
        "Justificacion_Escenario": "El impacto estructural es el fin último del desarrollo territorial sostenible.",
        "Metricas_Simuladas": [85, 15]
    }
}

ESCENARIOS_ADAPTABILIDAD = {
    "Transición Energética / Climática": {
        "Andina": {"Urbano": 85, "Rural": 55, "Crítico": 35},
        "Caribe": {"Urbano": 75, "Rural": 45, "Crítico": 25},
        "Pacífica": {"Urbano": 70, "Rural": 50, "Crítico": 30},
        "Orinoquía": {"Urbano": 65, "Rural": 40, "Crítico": 20},
        "Amazonía": {"Urbano": 60, "Rural": 35, "Crítico": 15}
    },
    "Transformación Digital de Servicios": {
        "Andina": {"Urbano": 90, "Rural": 40, "Crítico": 20},
        "Caribe": {"Urbano": 80, "Rural": 30, "Crítico": 15},
        "Pacífica": {"Urbano": 75, "Rural": 25, "Crítico": 10},
        "Orinoquía": {"Urbano": 70, "Rural": 20, "Crítico": 5},
        "Amazonía": {"Urbano": 65, "Rural": 15, "Crítico": 2}
    },
    "Crisis Económica e Inflación": {
        "Andina": {"Urbano": 60, "Rural": 50, "Crítico": 40},
        "Caribe": {"Urbano": 50, "Rural": 40, "Crítico": 30},
        "Pacífica": {"Urbano": 45, "Rural": 35, "Crítico": 25},
        "Orinoquía": {"Urbano": 55, "Rural": 45, "Crítico": 35},
        "Amazonía": {"Urbano": 40, "Rural": 30, "Crítico": 20}
    }
}

HISTORIAL_POLITICAS = {
    "CONPES 4010: Política Nacional de Salud Mental (2020-2023)": {
        "Año": 2020,
        "Entidad": "MinSalud / DNP",
        "Presupuesto": "$1.2 Billones COP",
        "Presupuesto_Billones": 1.2,
        "Impacto_Social": "Reducción esperada del 15% en tasas de depresión rural y fortalecimiento de telemedicina.",
        "Datos_Sinergia": "Avance físico reportado del 82.4% a diciembre de 2023, con brechas en zonas de conflicto armado."
    },
    "CONPES 3918: Implementación de la Agenda ODS en Colombia (2018-2030)": {
        "Año": 2018,
        "Entidad": "DNP",
        "Presupuesto": "$15.0 Billones COP",
        "Presupuesto_Billones": 15.0,
        "Impacto_Social": "Monitoreo de erradicación de pobreza extrema multidimensional en el Chocó y Amazonía.",
        "Datos_Sinergia": "Metas globales en agua limpia y saneamiento (ODS 6) registran un rezago regional de hasta el 40%."
    },
    "CONPES 4075: Política de Transición Energética (2022-2026)": {
        "Año": 2022,
        "Entidad": "MinMinas / DNP",
        "Presupuesto": "$23.5 Billones COP",
        "Presupuesto_Billones": 23.5,
        "Impacto_Social": "Inclusión de sistemas solares fotovoltaicos en comunidades de La Guajira y Orinoquía.",
        "Datos_Sinergia": "Avance del 62% con complejidades de licenciamiento ambiental en territorios étnicos."
    },
    "CONPES 3934: Política de Crecimiento Verde (2018-2030)": {
        "Año": 2018,
        "Entidad": "DNP / MinAmbiente",
        "Presupuesto": "$8.5 Billones COP",
        "Presupuesto_Billones": 8.5,
        "Impacto_Social": "Fomento de la bioeconomía, sustitución de plásticos de un solo uso y reducción de deforestación.",
        "Datos_Sinergia": "Control y vigilancia forestal en la Amazonía afectado por dinámicas de orden público local."
    }
}

# =====================================================================
# 2. FUNCIONES DE PROCESAMIENTO ESTADÍSTICO Y VISUALIZACIÓN
# =====================================================================
def generar_grafico_cadena(eslabon):
    info = DATOS_CADENA[eslabon]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    sizes = info["Metricas_Simuladas"]
    labels = ['Efectividad / Peso', 'Brecha / Pendiente']
    colors = ['#1f77b4', '#d62728']

    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors,
           wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1.5))
    ax.set_title(f"{info['Indicador']}", fontsize=10, fontweight='bold')
    fig.tight_layout()
    return fig

def analizar_simulacion_y_unir_datos(escenario, region, eslabon_seleccionado):
    datos_territorio = ESCENARIOS_ADAPTABILIDAD[escenario][region]
    territorios = list(datos_territorio.keys())
    valores = list(datos_territorio.values())

    media_adaptabilidad = np.mean(valores)
    eslabon_info = DATOS_CADENA[eslabon_seleccionado]
    efectividad_eslabon = eslabon_info["Metricas_Simuladas"][0]

    indice_sinergia = (media_adaptabilidad * 0.6) + (efectividad_eslabon * 0.4)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.8), constrained_layout=True)

    # Gráfico de barras territoriales
    bars = ax1.bar(territorios, valores, color=['#1f77b4', '#ff7f0e', '#d62728'], alpha=0.85, edgecolor='black', width=0.4)
    ax1.set_ylabel('Adaptabilidad (%)', fontsize=9, fontweight='bold')
    ax1.set_ylim(0, 100)
    ax1.set_title(f"Capacidad territorial ({region})\nEscenario: {escenario}", fontsize=10, fontweight="bold", pad=12)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height}%', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold')

    # Gráfico de pastel del eslabón
    ax2.pie(eslabon_info["Metricas_Simuladas"], labels=['Logrado', 'Pendiente'], autopct='%1.1f%%', startangle=90, colors=['#2ca02c', '#98df8a'],
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=1.5), textprops={'fontsize': 8})
    ax2.set_title(f"Efectividad del eslabón: {eslabon_seleccionado}", fontsize=10, fontweight="bold", pad=12)

    if indice_sinergia >= 75:
        diagnostico = f"Sinergia Sobresaliente ({indice_sinergia:.1f}%). Sólida alineación institucional territorial."
    elif indice_sinergia >= 50:
        diagnostico = f"Sinergia Moderada ({indice_sinergia:.1f}%). Brechas críticas identificadas en el sector rural y crítico."
    else:
        diagnostico = f"Alerta Crítica ({indice_sinergia:.1f}%). Fragilidad estructural severa ante choques externos."

    df_resumen = pd.DataFrame({
        "Dimensión de Control": ["Urbano", "Rural", "Institucionalidad Crítica", "Promedio Regional", f"Logro {eslabon_seleccionado}", "Índice Sinergia General"],
        "Valor Real (%)": [valores[0], valores[1], valores[2], round(media_adaptabilidad, 1), efectividad_eslabon, round(indice_sinergia, 1)]
    })

    return fig, df_resumen, diagnostico

def generar_serie_temporal(filtro="Todos los CONPES"):
    datos_temporales = []
    for k, v in HISTORIAL_POLITICAS.items():
        if filtro != "Todos los CONPES" and k != filtro:
            continue
        # Extraer porcentaje de avance desde el string de Datos_Sinergia
        avance = 60.0
        if "82.4%" in v["Datos_Sinergia"]:
            avance = 82.4
        elif "62%" in v["Datos_Sinergia"]:
            avance = 62.0
        elif "40%" in v["Datos_Sinergia"]:
            avance = 60.0 # ODS baseline
        elif "definitiva" in k or "Verde" in k:
            avance = 71.0

        datos_temporales.append({
            "Año": v["Año"],
            "CONPES": k.split(":")[0],
            "Avance": avance,
            "Presupuesto_Billones": v["Presupuesto_Billones"]
        })

    df_temporal = pd.DataFrame(datos_temporales).sort_values(by="Año")
    fig, ax1 = plt.subplots(figsize=(10, 5.2), constrained_layout=True)

    color_avance = '#008080'
    ax1.set_xlabel('Año de Formulación', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Avance Físico (%)', color=color_avance, fontsize=10, fontweight='bold')
    ax1.plot(df_temporal['Año'], df_temporal['Avance'], marker='o', markersize=8, linewidth=2.5, color=color_avance, zorder=3)
    ax1.tick_params(axis='y', labelcolor=color_avance)
    ax1.set_ylim(0, 100)
    ax1.grid(True, linestyle='--', alpha=0.5)

    ax2 = ax1.twinx()
    color_presupuesto = '#1f77b4'
    ax2.set_ylabel('Presupuesto (Billones COP)', color=color_presupuesto, fontsize=10, fontweight='bold')
    ax2.bar(df_temporal['Año'], df_temporal['Presupuesto_Billones'], alpha=0.25, color=color_presupuesto, width=0.3, zorder=1)
    ax2.tick_params(axis='y', labelcolor=color_presupuesto)

    for idx, row in df_temporal.iterrows():
        etiqueta = f"{row['CONPES']} ({row['Avance']}%)"
        ax1.annotate(
            etiqueta,
            xy=(row['Año'], row['Avance']),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            fontweight="bold",
            rotation=0
        )

    # Give a single-policy chart useful horizontal space instead of a cramped axis.
    if len(df_temporal) == 1:
        anio = float(df_temporal.iloc[0]["Año"])
        ax1.set_xlim(anio - 0.6, anio + 0.6)
        ax2.set_xlim(anio - 0.6, anio + 0.6)
    else:
        anios = df_temporal["Año"].astype(float).tolist()
        ax1.set_xlim(min(anios) - 0.35, max(anios) + 0.35)

    ax1.set_title(
        "Evolución histórica: avance y presupuesto CONPES",
        fontsize=11,
        fontweight="bold",
        pad=14
    )
    ax1.tick_params(axis="x", labelrotation=0)
    return fig

# =====================================================================
# 3. ESCENARIO TRIDIMENSIONAL ORIGINAL (PLOTLY DE ALTA FIDELIDAD)
# =====================================================================
ESCENARIOS_3D = {
    "Escenario Desarrollo Sostenible (Amazonía/Pacífico)": [
        {"name": "Gobernanza Territorial", "x": 1.5, "y": 3.2, "z": 4.1, "size": 22, "color": "#2ca02c", "desc": "Gobernanza regional comunitaria.", "metrica": "72%"},
        {"name": "Inversión Ambiental", "x": 3.0, "y": 5.5, "z": 2.0, "size": 28, "color": "#1f77b4", "desc": "Recursos dirigidos a mitigación climática.", "metrica": "85%"},
        {"name": "Resiliencia Social", "x": 4.5, "y": 2.1, "z": 5.0, "size": 25, "color": "#ff7f0e", "desc": "Capacidad de adaptación comunitaria.", "metrica": "68%"}
    ],
    "Escenario Crecimiento Económico e Infraestructura": [
        {"name": "Gobernanza Territorial", "x": 2.0, "y": 1.5, "z": 2.5, "size": 18, "color": "#9467bd", "desc": "Gobernanza corporativa centralizada.", "metrica": "55%"},
        {"name": "Inversión de Capital", "x": 5.2, "y": 4.1, "z": 6.0, "size": 32, "color": "#d62728", "desc": "Inversión en infraestructura vial.", "metrica": "90%"},
        {"name": "Resiliencia Social", "x": 3.1, "y": 3.0, "z": 3.2, "size": 20, "color": "#bcbd22", "desc": "Capacidad económica de absorción.", "metrica": "60%"}
    ]
}

def generar_grafico_3d_comparativo(escenario_3d="Ambos escenarios"):
    fig = go.Figure()
    esc1 = ESCENARIOS_3D["Escenario Desarrollo Sostenible (Amazonía/Pacífico)"]
    esc2 = ESCENARIOS_3D["Escenario Crecimiento Económico e Infraestructura"]
    if escenario_3d == "Desarrollo sostenible":
        esc2 = []
    elif escenario_3d == "Crecimiento económico":
        esc1 = []
    fig.add_trace(go.Scatter3d(
        x=[n["x"] for n in esc1], y=[n["y"] for n in esc1], z=[n["z"] for n in esc1],
        mode='markers',
        marker=dict(size=[n["size" ] for n in esc1], color=[n["color"] for n in esc1], opacity=0.85, line=dict(color='black', width=1.5)),
        text=[n["name"] for n in esc1], textposition="top center", name="Sostenible",
        hovertext=[n["name"] for n in esc1],
        hovertemplate="%{hovertext}<extra>Sostenible</extra>",
    ))
    if esc2:
        fig.add_trace(go.Scatter3d(
            x=[n["x"] for n in esc2], y=[n["y"] for n in esc2], z=[n["z"] for n in esc2],
            mode='markers',
            marker=dict(size=[n["size"] for n in esc2], color=[n["color"] for n in esc2], symbol='square', opacity=0.85, line=dict(color='white', width=1.5)),
            text=[n["name"] for n in esc2], textposition="bottom center", name="Crecimiento",
            hovertext=[n["name"] for n in esc2],
            hovertemplate="%{hovertext}<extra>Crecimiento</extra>",
        ))
    if esc1 and esc2:
        for i in range(min(len(esc1), len(esc2))):
            fig.add_trace(go.Scatter3d(
                x=[esc1[i]["x"], esc2[i]["x"]], y=[esc1[i]["y"], esc2[i]["y"]], z=[esc1[i]["z"], esc2[i]["z"]],
                mode='lines', line=dict(color='rgba(100, 100, 100, 0.6)', width=2.5, dash='dash'), showlegend=False
            ))
    fig.update_layout(
        title=dict(
            text="Comparación 3D: sostenibilidad y crecimiento",
            x=0.5,
            xanchor="center",
            y=0.99,
            font=dict(size=13)
        ),
        scene=dict(
            xaxis=dict(
                title="Gobernanza territorial (X)",
                title_font=dict(size=11),
                tickfont=dict(size=9)
            ),
            yaxis=dict(
                title="Inversión financiera (Y)",
                title_font=dict(size=11),
                tickfont=dict(size=9)
            ),
            zaxis=dict(
                title="Resiliencia social (Z)",
                title_font=dict(size=11),
                tickfont=dict(size=9)
            ),
            camera=dict(eye=dict(x=1.6, y=1.6, z=1.25)),
            aspectmode="cube"
        ),
        height=560,
        autosize=True,
        margin=dict(l=10, r=10, b=10, t=60),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.08,
            xanchor="center",
            x=0.5,
            font=dict(size=10)
        )
    )
    return fig

def cargar_datos_conpes(nombre_conpes):
    p = HISTORIAL_POLITICAS[nombre_conpes]
    return p["Año"], p["Entidad"], p["Presupuesto"], p["Impacto_Social"], p["Datos_Sinergia"]

def consultar_eslabon_completo(eslabon):
    info = DATOS_CADENA[eslabon]
    fig_eslabon = generar_grafico_cadena(eslabon)
    return info["Definición"], info["Indicador"], info["Nodo Teórico"], info["Caso Tunja"], info["Justificacion_Escenario"], fig_eslabon

def simular_matriz_relacion(conpes_sel, eslabon_sel, region_sel):
    conpes_raw = HISTORIAL_POLITICAS[conpes_sel]
    eslabon_raw = DATOS_CADENA[eslabon_sel]
    region_raw = ESCENARIOS_ADAPTABILIDAD["Transición Energética / Climática"][region_sel]
    res_df = pd.DataFrame({
        "Variable / Dimensión": ["Políticas Públicas - CONPES", "Cadena de Valor de Impacto", "Ecosistema Territorial"],
        "Métrica / Indicador Asociado": [conpes_raw["Presupuesto"], eslabon_raw["Indicador"], f"Urbano: {region_raw['Urbano']}% | Rural: {region_raw['Rural']}%"],
        "Enfoque y Datos de Desempeño": [conpes_raw["Datos_Sinergia"], eslabon_raw["Caso Tunja"], f"Brecha Crítica Regional de {region_raw['Urbano'] - region_raw['Crítico']}%"]
    })
    explicacion_detallada = (
        f"📊 EXPLICACIÓN INTEGRADA DE VARIABLES:\n\n"
        f"• Políticas Públicas ({conpes_sel}): Coordinado por {conpes_raw['Entidad']}. Impacto Social: {conpes_raw['Impacto_Social']}\n\n"
        f"• Cadena de Valor ({eslabon_sel}): Enfoque Teórico basado en {eslabon_raw['Nodo Teórico']}. Definido técnicamente como {eslabon_raw['Definición']}\n\n"
        f"• Ecosistema Regional ({region_sel}): Presenta niveles de resistencia asimétricos frente a crisis globales. "
        f"Justificación en el escenario de desarrollo: {eslabon_raw['Justificacion_Escenario']}"
    )
    return res_df, explicacion_detallada

# =====================================================================
# 5. DISEÑO DE LA INTERFAZ INTEGRADA (GRADIO)
# =====================================================================
with gr.Blocks(title="Ecosistema de Redes e Indicadores") as demo_3d:
    gr.Markdown("# 🏛️ Ecosistema Integrado de Políticas Públicas, Datos Abiertos y DNP")
    gr.Markdown("> **Nota metodológica:** esta versión usa valores de simulación y datos de referencia escritos en el código. No representa una conexión en tiempo real con fuentes oficiales.")

    with gr.Tab("🗺️ Simulador Integrado y Análisis de Datos"):
        with gr.Row():
            select_escenario = gr.Dropdown(choices=list(ESCENARIOS_ADAPTABILIDAD.keys()), label="Escenario Macroeconómico / Social:", value="Transición Energética / Climática")
            select_region = gr.Dropdown(choices=list(ESCENARIOS_ADAPTABILIDAD["Transición Energética / Climática"].keys()), label="Región Geográfica:", value="Andina")
            select_eslabon_sim = gr.Dropdown(choices=list(DATOS_CADENA.keys()), label="Cruzar con Eslabón de la Cadena:", value="Resultados")
        with gr.Row():
            with gr.Column(scale=3):
                plot_multisimulacion = gr.Plot(label="Visualizaciones del Modelo Estadístico Cruce Integrado")
            with gr.Column(scale=2):
                table_resumen_estadistico = gr.DataFrame(label="Análisis de Datos y Estadísticas del Modelo")
                txt_diagnostico_avanzado = gr.Textbox(label="Diagnóstico Sinergético & Recomendación de Política Pública", interactive=False, lines=5)
        inputs_sim = [select_escenario, select_region, select_eslabon_sim]
        outputs_sim = [plot_multisimulacion, table_resumen_estadistico, txt_diagnostico_avanzado]
        select_escenario.change(fn=analizar_simulacion_y_unir_datos, inputs=inputs_sim, outputs=outputs_sim)
        select_region.change(fn=analizar_simulacion_y_unir_datos, inputs=inputs_sim, outputs=outputs_sim)
        select_eslabon_sim.change(fn=analizar_simulacion_y_unir_datos, inputs=inputs_sim, outputs=outputs_sim)

    with gr.Tab("📊 Visualizador Comparativo 3D Original"):
        select_escenario_3d = gr.Dropdown(choices=["Ambos escenarios", "Desarrollo sostenible", "Crecimiento económico"], value="Ambos escenarios", label="Escenario que deseas visualizar")
        with gr.Row():
            with gr.Column(scale=2):
                plot_3d = gr.Plot(show_label=False)
            with gr.Column(scale=1):
                gr.Markdown("### 📝 Análisis Comparativo de Escenarios")
                gr.Markdown("**Esferas**: Modelo Sostenible. **Cubos**: Modelo de Crecimiento e Infraestructura. Al elegir un escenario, puedes mostrar uno o comparar ambos.")
        select_escenario_3d.change(fn=generar_grafico_3d_comparativo, inputs=select_escenario_3d, outputs=plot_3d)

    with gr.Tab("📈 Serie Temporal CONPES"):
        gr.Markdown("### 📊 Evolución del Desempeño y Asignación de Recursos")
        filtro_serie_conpes = gr.Dropdown(choices=["Todos los CONPES"] + list(HISTORIAL_POLITICAS.keys()), value="Todos los CONPES", label="Filtrar serie por política")
        plot_tiempo = gr.Plot(label="Línea de Tiempo de Avance y Presupuestos CONPES")
        filtro_serie_conpes.change(fn=generar_serie_temporal, inputs=filtro_serie_conpes, outputs=plot_tiempo)

    with gr.Tab("📚 Historial de Políticas CONPES"):
        conpes_select = gr.Dropdown(choices=list(HISTORIAL_POLITICAS.keys()), value=list(HISTORIAL_POLITICAS.keys())[0], label="Selecciona el Documento CONPES de Referencia")
        with gr.Row():
            txt_ano = gr.Textbox(label="Año de Publicación", interactive=False)
            txt_entidad = gr.Textbox(label="Entidad Coordinadora / Líder", interactive=False)
            txt_presupuesto = gr.Textbox(label="Presupuesto Estimado / Asignado", interactive=False)
        txt_impacto = gr.Textbox(label="Impacto Social Proyectado", interactive=False)
        txt_sinergia = gr.Textbox(label="Avance Físico / Desempeño Reportado (Sinergia)", interactive=False)
        conpes_select.change(fn=cargar_datos_conpes, inputs=conpes_select, outputs=[txt_ano, txt_entidad, txt_presupuesto, txt_impacto, txt_sinergia])

    with gr.Tab("🔄 Matriz de Triple Relación"):
        gr.Markdown("### 🎛️ Panel de Despliegue de Coherencia e Indicadores")
        with gr.Row():
            in_conpes = gr.Dropdown(choices=list(HISTORIAL_POLITICAS.keys()), value=list(HISTORIAL_POLITICAS.keys())[0], label="Seleccione la Política Pública:")
            in_eslabon = gr.Dropdown(choices=list(DATOS_CADENA.keys()), value="Resultados", label="Seleccione el Eslabón de la Cadena de Valor:")
            in_region = gr.Dropdown(choices=list(ESCENARIOS_ADAPTABILIDAD["Transición Energética / Climática"].keys()), value="Andina", label="Seleccione la Región Geográfica:")
        with gr.Row():
            with gr.Column(scale=3):
                matriz_df = gr.DataFrame(label="Matriz Comparativa de Variables Independientes del Modelo")
            with gr.Column(scale=2):
                explicacion_txt = gr.Textbox(label="Explicación Detallada y Sinergia de Variables", interactive=False, lines=10)
        inputs_matriz = [in_conpes, in_eslabon, in_region]
        outputs_matriz = [matriz_df, explicacion_txt]
        in_conpes.change(fn=simular_matriz_relacion, inputs=inputs_matriz, outputs=outputs_matriz)
        in_eslabon.change(fn=simular_matriz_relacion, inputs=inputs_matriz, outputs=outputs_matriz)
        in_region.change(fn=simular_matriz_relacion, inputs=inputs_matriz, outputs=outputs_matriz)

    # Inicializadores
    demo_3d.load(fn=analizar_simulacion_y_unir_datos, inputs=inputs_sim, outputs=outputs_sim)
    demo_3d.load(fn=generar_grafico_3d_comparativo, inputs=select_escenario_3d, outputs=plot_3d)
    demo_3d.load(fn=generar_serie_temporal, inputs=filtro_serie_conpes, outputs=plot_tiempo)
    demo_3d.load(fn=cargar_datos_conpes, inputs=conpes_select, outputs=[txt_ano, txt_entidad, txt_presupuesto, txt_impacto, txt_sinergia])
    demo_3d.load(fn=simular_matriz_relacion, inputs=inputs_matriz, outputs=outputs_matriz)

demo_3d.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 7860)),
    share=False,
    theme=gr.themes.Soft(primary_hue="teal", secondary_hue="blue")
)
