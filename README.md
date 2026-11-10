# Analizador de Opiniones sobre Universidades Peruanas

**PC3 - Procesamiento de Lenguaje Natural**

## Problemática
Los estudiantes peruanos que quieren elegir una universidad suelen guiarse por opiniones sueltas de Google Maps y redes sociales. Leer cientos de comentarios toma mucho tiempo y es difícil saber qué dice la mayoría. Esta aplicación analiza automáticamente los comentarios para mostrar qué opinan los demás de cada universidad.

## Aplicación
🔗 **Link de la app:** https://opiniones-universidades-lima.streamlit.app/

## Datos
- 198 comentarios sobre 8 universidades peruanas.
- Fuente: reseñas de Google Maps, recolectadas manualmente.
- Columnas: `id`, `universidad`, `comentario`, `estrellas`, `fuente`.

## Técnicas de PLN utilizadas
1. **Preprocesamiento:** limpieza con expresiones regulares, tokenización, stopwords, lematización, stemming y normalización.
2. **Análisis de sentimiento** (pysentimiento): clasifica cada comentario en positivo, negativo o neutro.
3. **TF-IDF:** encuentra las palabras que caracterizan a cada universidad.
4. **Modelado de temas (NMF):** agrupa los comentarios en temas de conversación.

## Resultados principales
- 71.2% de comentarios positivos, 14.6% neutros y 14.1% negativos.
- Los comentarios positivos tuvieron en promedio 4.67 estrellas y los negativos 2.92, lo que respalda el modelo de sentimiento.
- Se encontraron 4 temas: infraestructura y áreas verdes, ambiente y seguridad del campus, prestigio y nivel académico, y docentes y servicio educativo.

## Contenido del repositorio
| Archivo | Descripción |
|---|---|
| `app.py` | Aplicación en Streamlit |
| `requirements.txt` | Librerías necesarias |
| `resultados_analisis.csv` | Resultados del análisis |
| Notebook `.ipynb` | Análisis completo paso a paso |
| Excel | Comentarios recolectados |

## Cómo ejecutar la app en tu computadora
pip install -r requirements.txt
streamlit run app.py

## Limitaciones
- Muestra pequeña, recolectada a mano.
- En Google Maps opinan más las personas muy contentas o muy molestas.
- El modelo de sentimiento puede fallar con sarcasmo o jerga peruana.

## Integrantes
- Rodrigo Mendoza
- Gianela Huazo
- Juliana Quispe
