import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Pantalla dividida: Dos Visiones de la Misma Industria",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    color: #1f77b4;
    text-align: center;
    margin-bottom: 2rem;
}
.section-header {
    font-size: 2rem;
    color: #ff7f0e;
    margin-top: 3rem;
    margin-bottom: 1rem;
}
.metric-big {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
}
.insight-box {
    background-color: #222429;
    color: #fafafa;
    border-left: 5px solid #1f77b4;
    padding: 1rem;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Función para cargar datos
@st.cache_data
def load_data():
    """Carga todos los CSV necesarios"""
    BASE_PATH = './data/processed/'
    try:
        genre_data = pd.read_csv(BASE_PATH+'genre_discrepancies.csv')
        developer_data = pd.read_csv(BASE_PATH+'developer_discrepancies.csv')
        temporal_data = pd.read_csv(BASE_PATH+'temporal_discrepancies.csv')
        extreme_cases = pd.read_csv(BASE_PATH+'extreme_cases.csv')
        scatter_data = pd.read_csv(BASE_PATH+'scatter_data.csv')
        
        return genre_data, developer_data, temporal_data, extreme_cases, scatter_data
    except FileNotFoundError as e:
        st.error(f"Error cargando archivos: {e}")
        st.info("Asegúrate de que todos los CSV estén en el directorio correcto")
        return None, None, None, None, None

# Cargar datos
genre_data, developer_data, temporal_data, extreme_cases, scatter_data = load_data()

if scatter_data is not None:
    
    # HEADER PRINCIPAL
    st.markdown('<h1 class="main-header">🎮 Pantalla dividida: Dos Visiones de la Misma Industria</h1>', unsafe_allow_html=True)
    st.markdown('<h3 style="text-align: center; color: #666;">Cuando Críticos y Usuarios No Se Entienden en los Videojuegos</h3>', unsafe_allow_html=True)
    
    # MÉTRICAS PRINCIPALES
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_games = len(scatter_data)
        st.metric("Total de Juegos", f"{total_games:,}")
    
    with col2:
        avg_discrepancy = scatter_data['discrepancy_score'].mean()
        st.metric("Discrepancia Promedio", f"{avg_discrepancy:.2f}")
    
    with col3:
        extreme_count = len(scatter_data[scatter_data['is_extreme'] == True])
        extreme_pct = (extreme_count / total_games) * 100
        st.metric("Casos Extremos", f"{extreme_pct:.1f}%")
    
    with col4:
        genres_count = scatter_data['genre_name'].nunique()
        st.metric("Géneros Analizados", genres_count)
    
    # INTRODUCCIÓN
    st.markdown("""
    <div style="color: #fafafa;" class="insight-box">
    <h4>⚔️ El Problema</h4>
    En el mundo de los videojuegos, encontrar consenso entre críticos y jugadores puede ser tan desafiante 
    como encender una hoguera en territorio hostil. Con cada nuevo título se hace presente una brecha entre 
    lo que piensan los críticos profesionales y lo que experimentan los jugadores reales. Esta visualización 
    explora esa desconexión usando datos de más de 7,000 videojuegos, preparándote para morir... de curiosidad 
    por los patrones revelados.
    </div>
    """, unsafe_allow_html=True)
    
    # SECCIÓN 1: DISTRIBUCIÓN GENERAL
    st.markdown('<h2 class="section-header">La Distribución del Desacuerdo</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Histograma de discrepancias
        fig_hist = px.histogram(
            scatter_data, 
            x='discrepancy_score',
            color='discrepancy_type',
            title="Distribución de Discrepancias entre Críticos y Usuarios",
            labels={
                'discrepancy_score': 'Puntuación de Discrepancia',
                'count': 'Número de Juegos'
            },
            color_discrete_map={
                'overhyped': '#0057ab', 
                'polarizing': '#85c3db',
                'consensus': '#fcfdc9',
                'hidden_gem': '#6d001e'
            }
        )
        fig_hist.add_vline(x=0, line_dash="dash", line_color="black", 
                          annotation_text="Equilibrio Perfecto")
        fig_hist.update_layout(height=500,
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font_color='#fafafa',
            title_font_color='#fafafa',
            legend=dict(
                font=dict(color='#fafafa')
            ))
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        # Gráfico de pastel de tipos
        type_counts = scatter_data['discrepancy_type'].value_counts()
        
        pie_data = pd.DataFrame({
            'discrepancy_type': type_counts.index,
            'count': type_counts.values
        })
        fig_pie = px.pie(
            pie_data,
            values='count',
            names='discrepancy_type',
            title="Distribución por Tipo de Discrepancia",
            color='discrepancy_type',
            color_discrete_map={
                'overhyped': '#0057ab',
                'polarizing': '#85c3db', 
                'consensus': '#fcfdc9',
                'hidden_gem': '#6d001e'
            }
        )
        fig_pie.update_layout(height=500,
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font_color='#fafafa',
            title_font_color='#fafafa',
            legend=dict(
                font=dict(color='#fafafa')
            ))
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # SECCIÓN 2: ANÁLISIS POR GÉNEROS
    st.markdown('<h2 class="section-header">¿En Qué Géneros Discrepan Más?</h2>', unsafe_allow_html=True)
    
    if genre_data is not None:
        genre_sorted = genre_data.sort_values('discrepancy_score', ascending=False).head(15)
        
        # Gráfico de barras por género
        fig_genre = px.bar(
            genre_sorted,
            x='discrepancy_score',
            y='genre_name',
            color='discrepancy_score',
            title="Top 15 Géneros por Discrepancia (Críticos vs Usuarios)",
            labels={
                'discrepancy_score': 'Puntuación de Discrepancia',
                'genre_name': 'Género'
            },
            color_continuous_scale='RdBu_r',
            orientation='h'
        )
        
        # Línea vertical en x=0 desde la izquierda
        fig_genre.add_vline(x=0, line_dash="dash", line_color="black", line_width=2)
        
        # Configurar layout con orden descendente (mayor discrepancia arriba)
        fig_genre.update_layout(
            height=600, 
            yaxis={'categoryorder':'array', 'categoryarray': genre_sorted['genre_name'].tolist()},
            xaxis={'zeroline': True, 'zerolinecolor': 'black', 'zerolinewidth': 2},
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font_color='#fafafa',
            title_font_color='#fafafa',
            legend=dict(
                font=dict(color='#fafafa')
            )
        )
        
        # Personalizar hover
        fig_genre.update_traces(
            hovertemplate='<b>%{y}</b><br>Discrepancia: %{x:.2f}<br>Juegos: %{customdata[0]}<extra></extra>',
            customdata=genre_sorted[['game_count']].values
        )
        
        st.plotly_chart(fig_genre, use_container_width=True)
        
        # Insights de géneros mejorados
        best_genre = genre_sorted.iloc[0]  # Primer elemento tras ordenar descendente
        worst_genre = genre_sorted.iloc[-1]  # Último elemento tras ordenar descendente
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="insight-box">
            <h4>🥇 Género Más Valorado por Usuarios</h4>
            <b>Puzzle</b><br>
            Discrepancia: -0.09<br>
            Juegos analizados: 14<br>
            <small>La menor diferencia de opinión entre críticos y jugadores</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="insight-box">
            <h4>📉 Género Más Sobrevalorado</h4>
            <b>{worst_genre['genre_name']}</b><br>
            Discrepancia: {worst_genre['discrepancy_score']:.2f}<br>
            Juegos analizados: {worst_genre['game_count']}<br>
            <small>Los críticos valoran este género {abs(worst_genre['discrepancy_score']):.1f} puntos más que los usuarios</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            consensus_genres = genre_data[abs(genre_data['discrepancy_score']) <= 0.5]
            if len(consensus_genres) > 0:
                consensus_count = len(consensus_genres)
                st.markdown(f"""
                <div class="insight-box">
                <h4>🤝 Géneros en Consenso</h4>
                <b>{consensus_count} géneros</b><br>
                Discrepancia: ±0.5<br>
                <small>Géneros donde críticos y usuarios están de acuerdo</small>
                </div>
                """, unsafe_allow_html=True)
    
    # SECCIÓN 3: SCATTER PLOT PRINCIPAL
    st.markdown('<h2 class="section-header">Exploración Interactiva: Cada Juego Cuenta Su Historia</h2>', unsafe_allow_html=True)
    
    # Filtros interactivos
    st.markdown("### Filtros de Exploración")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        selected_genres = st.multiselect(
            "Selecciona Géneros",
            options=sorted(scatter_data['genre_name'].unique()),
            default=sorted(scatter_data['genre_name'].unique())
        )
    
    with col2:
        year_range = st.slider(
            "Rango de Años",
            min_value=int(scatter_data['year'].min()),
            max_value=int(scatter_data['year'].max()),
            value=(int(scatter_data['year'].min()), int(scatter_data['year'].max()))
        )
    
    with col3:
        selected_types = st.multiselect(
            "Tipos de Discrepancia",
            options=scatter_data['discrepancy_type'].unique(),
            default=scatter_data['discrepancy_type'].unique()
        )
    
    # Filtrar datos
    filtered_data = scatter_data[
        (scatter_data['genre_name'].isin(selected_genres)) &
        (scatter_data['year'] >= year_range[0]) &
        (scatter_data['year'] <= year_range[1]) &
        (scatter_data['discrepancy_type'].isin(selected_types))
    ]
    
    # Scatter plot principal
    fig_scatter = px.scatter(
        filtered_data,
        x='metacritic',
        y='rating',
        color='discrepancy_type',
        size='added',
        hover_data=['name', 'genre_name', 'developer_name', 'year', 'metacritic', 'rating', 'added', 'discrepancy_type'],
        title=f"Metacritic vs Rating de Usuarios ({len(filtered_data):,} juegos)",
        labels={
            'name': 'Nombre del Juego',
            'genre_name': 'Género',
            'developer_name': 'Desarrollador',
            'year': 'Año de Lanzamiento',
            'metacritic': 'Puntuación Metacritic (Críticos)',
            'rating': 'Rating Usuarios (1-5)',
            'added': 'Popularidad',
            'discrepancy_type': 'Tipo de Discrepancia'
        },
        color_discrete_map={
                'overhyped': '#0057ab',
                'polarizing': '#85c3db', 
                'consensus': '#fcfdc9',
                'hidden_gem': '#6d001e'
            }
    )
    
    # Añadir línea de equilibrio
    fig_scatter.add_shape(
        type="line",
        x0=0, y0=1, x1=100, y1=5,
        line=dict(color="white", width=2, dash="dash"),
        name="Equilibrio Perfecto"
    )
    
    fig_scatter.update_layout(height=600,
            plot_bgcolor='#0e1117',
            paper_bgcolor='#0e1117',
            font_color='#fafafa',
            title_font_color='#fafafa',
            legend=dict(
                font=dict(color='#fafafa')
            )
        )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # SECCIÓN 4: CASOS EXTREMOS
    if extreme_cases is not None:
        st.markdown('<h2 class="section-header">Los Casos Más Extremos</h2>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs([ "🟡 Sobrevalorados", "🟣 Joyas Ocultas"])
        
        with tab1:
            overhyped = extreme_cases[extreme_cases['type'] == 'overhyped'].head(10)
            if len(overhyped) > 0:
                st.dataframe(
                    overhyped[['game_name', 'genre_name', 'year', 'metacritic', 'rating', 'discrepancy_score']],
                    use_container_width=True
                )
        
        with tab2:
            hidden_gems = extreme_cases[extreme_cases['type'] == 'hidden_gem'].head(10)
            if len(hidden_gems) > 0:
                st.dataframe(
                    hidden_gems[['game_name', 'genre_name', 'year', 'metacritic', 'rating', 'discrepancy_score']],
                    use_container_width=True
                )
    
    # SECCIÓN 5: EVOLUCIÓN TEMPORAL
    if temporal_data is not None:
        st.markdown('<h2 class="section-header">¿Ha Empeorado el Desacuerdo con el Tiempo?</h2>', unsafe_allow_html=True)
        
        # Filtros para el heatmap temporal
        st.markdown("### Configuración del Heatmap Temporal")
        col1, col2 = st.columns(2)
        
        with col1:
            # Filtro de géneros para el heatmap
            available_genres = sorted(temporal_data['genre_name'].unique())
            selected_genres_heatmap = st.multiselect(
                "Selecciona Géneros para el Heatmap",
                options=available_genres,
                default=available_genres,
                key="heatmap_genres"
            )
        
        with col2:
            # Filtro de rango de años
            min_year = int(temporal_data['year'].min())
            max_year = int(temporal_data['year'].max())
            year_range_heatmap = st.slider(
                "Rango de Años para Heatmap",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year),
                key="heatmap_years"
            )
        
        # Filtrar datos temporales
        filtered_temporal = temporal_data[
            (temporal_data['genre_name'].isin(selected_genres_heatmap)) &
            (temporal_data['year'] >= year_range_heatmap[0]) &
            (temporal_data['year'] <= year_range_heatmap[1])
        ]
        
        if len(filtered_temporal) > 0:
            # Crear pivot table con datos filtrados
            temporal_pivot = filtered_temporal.pivot_table(
                index='year', 
                columns='genre_name', 
                values='discrepancy_score',
                fill_value=np.nan  # Usar NaN en lugar de 0 para mejor visualización
            )
            
            # Heatmap temporal filtrado
            fig_heatmap = px.imshow(
                temporal_pivot.T,
                title="Evolución de Discrepancias por Año y Género",
                labels=dict(x="Año", y="Género", color="Discrepancia"),
                color_continuous_scale="RdYlBu_r"
            )
            fig_heatmap.update_layout(height=600,
                plot_bgcolor='#0e1117',
                paper_bgcolor='#0e1117',
                font_color='#fafafa',
                title_font_color='#fafafa',
                legend=dict(
                    font=dict(color='#fafafa')
                )
            )
            st.plotly_chart(fig_heatmap, use_container_width=True)
            
            # Información adicional sobre la selección
            st.info(f"Mostrando {len(filtered_temporal)} combinaciones año-género de un total de {len(temporal_data)}")
            
        else:
            st.warning("No hay datos para la selección actual. Ajusta los filtros.")
            
    # CONCLUSIONES
    st.markdown('<h2 class="section-header">Conclusiones</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="insight-box">
    <h4>🔍 Hallazgos Principales</h4>
    <ul>
    <li><b>Tendencia General:</b> Los críticos tienden a ser más generosos que los usuarios (discrepancia promedio negativa)</li>
    <li><b>Géneros Problemáticos:</b> Algunos géneros muestran desacuerdos consistentes entre críticos y audiencia</li>
    <li><b>Casos Extremos:</b> Existen juegos con discrepancias superiores a 7 puntos, revelando problemas en la evaluación de los críticos</li>
    <li><b>Diversidad de Opiniones:</b> La industria del videojuego muestra una gran diversidad de perspectivas críticas</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

else:
    st.error("No se pudieron cargar los datos. Verifica que los archivos CSV estén disponibles.")
    st.info("Archivos necesarios: genre_discrepancies.csv, developer_discrepancies.csv, temporal_discrepancies.csv, extreme_cases.csv, scatter_data.csv")