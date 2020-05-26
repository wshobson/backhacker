FROM python:3.7-slim

# Copy local code to the container image.
WORKDIR /app
COPY . .

# Install production dependencies.
RUN pip install -r requirements.txt

CMD python main.py --symbol1=SPY --strategy=connors_rsi
