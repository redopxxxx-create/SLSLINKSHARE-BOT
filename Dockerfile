FROM python:3.8-slim-buster

# Setting Work Directory
WORKDIR /app

# Updating and installing basic tools
RUN apt-get update && apt-get upgrade -y

# Copying requirements first for better caching
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copying all files to the container
COPY . .

# Bot ko run karne ki command
CMD ["python3", "main.py"]

# +++ Modified By @itsryosudhish [SLS Bots] +++
# aNDI BANDI SANDI JISNE BHI CREDIT HATAYA USKI BANDI RAndi 
