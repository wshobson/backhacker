# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
WORKDIR /app
COPY . .

# Install production dependencies.
RUN pip install -r requirements.txt

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD ["python", "./main.py", "--symbol1=SPY", "--symbol2=QQQ", "--strategy=multiple_sma_cross", "--key-id=PKO2LOVJQ40HTVUVWTQY", "--secret-key=a20LbMWJqwLi44FsH1XU2fPzmMVAxLGLS43NcHbg"]
