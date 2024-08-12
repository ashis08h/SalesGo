FROM python:3.6

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project code
COPY . .

# Run collectstatic to collect static files
RUN python manage.py collectstatic --noinput

# Start the Django development server

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "SalesGo.wsgi:application"]
