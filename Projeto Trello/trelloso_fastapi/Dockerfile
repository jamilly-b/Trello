FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /home/app

WORKDIR /home/app
COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

# A opção reload fará os conteiners reiniciarem a qualquer mudança nos arquivos do projeto, isso é interessante para ambiente de desenvolvimento
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
