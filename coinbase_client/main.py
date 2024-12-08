from coinbase_client.client import CoinbaseClient
from datetime import datetime, timedelta

def main():
    try:
        # Initialize client
        client = CoinbaseClient(
            api_key="api-key",
            api_secret="api-secret",
            api_passphrase="api-passphrase"
        )

        # Get all products
        products = client.get_products()
        print(f"Successfully retrieved {len(products)} products")

        # Get all accounts
        accounts = client.get_accounts()
        print(f"Successfully retrieved {len(accounts)} accounts")

    except Exception as e:
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":
    main()