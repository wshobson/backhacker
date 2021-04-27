import os

PRODUCTION = "production"
DEVELOPMENT = "development"

# COIN_TARGET = "BTC"
# COIN_REFER = "USDT"

#ENV = os.getenv("ENVIRONMENT", DEVELOPMENT)
ENV = os.getenv("ENVIRONMENT", PRODUCTION)

ALPACA = {
    "key": os.environ["ALPACA_KEY"],
    "secret": os.environ["ALPACA_SECRET"]
}

ALPHAVANTAGE = {
    "key": os.environ["ALPHAVANTAGE_KEY"]
}

# TELEGRAM = {
#     "channel": "<CHANEL ID>",
#     "bot": "<BOT KEY HERE>"
# }

print("ENV = ", ENV)
