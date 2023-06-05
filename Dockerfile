FROM python:3.10

# Expose streamlit port
EXPOSE 8501

# Environment args
ARG OPENAI_API_KEY
ENV OPENAI_API_KEY=$OPENAI_API_KEY

ENV PYTHONPATH="${PYTHONPATH}:/app/src"

RUN mkdir -p /app
RUN mkdir -p /app/assets
RUN mkdir -p /app/src
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY assets /app/assets
COPY src/ /app/src

COPY config.yaml .

CMD ["streamlit", "run", "src/frontend/streamlit_application.py"]
