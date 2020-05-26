import os

PRODUCTION = "production"
DEVELOPMENT = "development"

# COIN_TARGET = "BTC"
# COIN_REFER = "USDT"

ENV = os.getenv("ENVIRONMENT", DEVELOPMENT)

ALPACA = {
    "key": "PKO2LOVJQ40HTVUVWTQY",
    "secret": "a20LbMWJqwLi44FsH1XU2fPzmMVAxLGLS43NcHbg"
}

ALPHAVANTAGE = {
    "key": "UISQPDG0DYI3R5YY"
}

# TELEGRAM = {
#     "channel": "<CHANEL ID>",
#     "bot": "<BOT KEY HERE>"
# }

print("ENV = ", ENV)
