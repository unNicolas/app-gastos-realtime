# Usa la imagen base de Python 3.12
FROM python:3.12-slim

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Expone el puerto 8501 (puerto predeterminado de Streamlit)
EXPOSE 8501

# Comando para ejecutar la aplicación cuando el contenedor se inicia
CMD ["streamlit", "run", "main.py"]



