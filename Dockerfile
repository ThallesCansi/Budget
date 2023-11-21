# Usar uma imagem oficial do Python como imagem pai
FROM python:3.11.6
# Definir o diretório de trabalho no contêiner
WORKDIR /
# Copiar os arquivos de dependências e instalar as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
# Copiar o código fonte da aplicação para o contêiner
COPY . .
# Definir a porta em que a aplicação irá rodar
EXPOSE 8000
# Comando para executar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]