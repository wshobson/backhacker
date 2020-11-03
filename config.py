import os

PRODUCTION = "production"
DEVELOPMENT = "development"

# COIN_TARGET = "BTC"
# COIN_REFER = "USDT"

#ENV = os.getenv("ENVIRONMENT", DEVELOPMENT)
ENV = os.getenv("ENVIRONMENT", PRODUCTION)

ALPACA = {
    "key": "PKNTMEMK1QCOE0JQIPRT",
    "secret": "98suhOSCNL4cagduVzLl7hk7JNCnmUGpf8LXv3ES"
}

ALPHAVANTAGE = {
    "key": "UISQPDG0DYI3R5YY"
}

# TELEGRAM = {
#     "channel": "<CHANEL ID>",
#     "bot": "<BOT KEY HERE>"
# }

print("ENV = ", ENV)
