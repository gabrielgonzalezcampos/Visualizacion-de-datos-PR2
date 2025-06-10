# Pantalla dividida: Dos Visiones de la Misma Industria

## Cuando Críticos y Usuarios No Se Entienden en los Videojuegos

Este proyecto analiza las discrepancias entre las puntuaciones de críticos profesionales (Metacritic) y las valoraciones de usuarios para más de 5,800 videojuegos. La visualización interactiva permite explorar patrones en estas diferencias de opinión a través de diferentes géneros, años y desarrolladores.

Visualización disponible online en https://gabriel-gonzalez-visualizacion-de-datos-pr2.streamlit.app/

## Estructura del Proyecto

```
├── data/
│   ├── csv/                  # Datos originales
│   └── processed/            # Datos procesados para visualización
├── src/
│   ├── etl/                  # Notebooks de procesamiento de datos
│   └── visualization/        # Código de visualización Streamlit
├── .streamlit/               # Configuración de Streamlit
├── requirements.txt          # Dependencias del proyecto
└── README.md                 # Este archivo
```

### Archivos Clave

- `src/etl/consensus_etl.ipynb`: Notebook que procesa los datos originales y genera los datasets para visualización
- `src/visualization/consensus_visualization.py`: Aplicación Streamlit para visualización interactiva
- `data/processed/*.csv`: Datasets procesados con métricas de discrepancia

## Requisitos e Instalación

El proyecto requiere Python 3.8+ y las siguientes dependencias:

```
streamlit==1.45.1
plotly==6.1.1
pandas==2.2.3
numpy==1.26.4
```

Para instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Procesamiento de Datos

El proceso ETL (Extracción, Transformación y Carga) se realiza en el notebook `src/etl/consensus_etl.ipynb` y consiste en:

1. Carga de datos originales desde `data/csv/`
2. Limpieza y filtrado de juegos con puntuaciones tanto de Metacritic como de usuarios
3. Cálculo de métricas de discrepancia entre críticos y usuarios
4. Clasificación de juegos en categorías: consensus, polarizing, hidden_gem, overhyped
5. Generación de datasets agregados por género, desarrollador y año
6. Almacenamiento de resultados en `data/processed/`

### Datasets Generados

- `scatter_data.csv`: Dataset principal con todos los juegos y sus métricas
- `genre_discrepancies.csv`: Discrepancias agregadas por género
- `developer_discrepancies.csv`: Discrepancias agregadas por desarrollador
- `temporal_discrepancies.csv`: Evolución temporal de discrepancias por género
- `extreme_cases.csv`: Casos extremos de desacuerdo entre críticos y usuarios

## Ejecución de la Aplicación

Para ejecutar la aplicación de visualización:

```bash
streamlit run src/visualization/consensus_visualization.py
```

La aplicación estará disponible en `http://localhost:8501` por defecto.

## Características

La visualización incluye:

- **Dashboard interactivo** con métricas clave sobre discrepancias
- **Histograma y gráfico de pastel** mostrando la distribución de discrepancias
- **Gráfico de barras** con los géneros que presentan mayores discrepancias
- **Scatter plot interactivo** que permite explorar la relación entre puntuaciones de críticos y usuarios
- **Filtros dinámicos** por género, año y tipo de discrepancia
- **Heatmap temporal** que muestra la evolución de discrepancias a lo largo del tiempo
- **Tablas de casos extremos** con los juegos que presentan mayores desacuerdos
