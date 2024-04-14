FROM python:3

WORKDIR /code

COPY requirements.txt ./
COPY .env ./

RUN pip install --no-cache-dir --upgrade pip \
    pip install --no-cache-dir -r requirements.txt
# Install dependencies

EXPOSE 8000

# Copy python files over
COPY . .

CMD [ "python", "manage.py" , "runserver", "0.0.0.0:8000"]