# Usa una imagen base de Python
FROM python:3.11.2

# Establecer el directorio de trabajo
WORKDIR /usr/src

# Instalar dependencias del sistema necesarias
RUN apt-get update && apt-get install -y git

# Configurar las credenciales para GitLab usando ARG
ARG GITLAB_TOKEN

# Clonar la librería nucleidechartlib

RUN git clone https://alfonsojph786:${GITLAB_TOKEN}/alfonsojph786/nucleidechartlib.git

# Instalar la librería nucleidechartlib
RUN pip install ./nucleidechartlib

# Clonar el repositorio nucleidechartAPI
RUN git clone https://git.granasat.space/alfonsojph786/nucleidechartAPI.git

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r ./nucleidechartAPI/requirements.txt

# Exponer el puerto en el que la API se ejecutará
EXPOSE 5000

# Comando para iniciar la API de Python
CMD ["python", "./nucleidechartAPI/run.py"]
