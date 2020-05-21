# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

# Copy local code to the container image.
WORKDIR /app
COPY . .

# Install production dependencies.
RUN pip install -r requirements.txt

ENV APCA_KEY_ID PKO2LOVJQ40HTVUVWTQY
ENV APCA_SECRET_KEY a20LbMWJqwLi44FsH1XU2fPzmMVAxLGLS43NcHbg

CMD exec python main.py --symbol1=SPY --strategy=connors_rsi --key-id=$APCA_KEY_ID --secret-key=$APCA_SECRET_KEY
