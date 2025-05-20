# Usa uma imagem base oficial do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de requisitos e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta 8080 (Cloud Run espera essa porta)
EXPOSE 8080

# Usa a porta 8080 fixamente
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
