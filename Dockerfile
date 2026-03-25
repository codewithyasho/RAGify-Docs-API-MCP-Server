# base image
FROM python:3.11

# set working directory
WORKDIR /app

# install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . .

# expose port
EXPOSE 8888

# run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8888"]


