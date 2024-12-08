import time
import base64
import hmac
import hashlib
import requests
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class CoinbaseClient:
    api_key: str
    api_secret: str
    api_passphrase: str
    def __post_init__(self):
        self.base_url = "https://api-public.sandbox.exchange.coinbase.com"

    def _generate_signature(self, timestamp: str, method: str, request_path: str, body: str = "") -> str:
        """Generate the signature for request authentication"""
        message = timestamp + method + request_path + body
        signature = hmac.new(
            base64.b64decode(self.api_secret),
            message.encode('utf-8'),
            hashlib.sha256
        )
        return base64.b64encode(signature.digest()).decode('utf-8')

    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, data: Optional[Dict] = None) -> Any:
        """Make authenticated request to API"""
        url = f"{self.base_url}{endpoint}"
        timestamp = str(int(time.time()))
        
        # Convert data to string if present
        body = ""
        if data:
            import json
            body = json.dumps(data)

        # Generate signature
        signature = self._generate_signature(timestamp, method, endpoint, body)

        # Prepare headers
        headers = {
            'X-CB-ACCESS-KEY': self.api_key,
            'X-CB-ACCESS-SIGN': signature,
            'X-CB-ACCESS-TIMESTAMP': timestamp,
            'X-CB-ACCESS-PASSPHRASE': self.api_passphrase,
            'Content-Type': 'application/json'
        }

        # Make request
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            params=params,
            json=data
        )

        # Check for errors
        response.raise_for_status()

        return response.json()

    # Public Methods
    def get_products(self) -> Dict:
        """Get all products"""
        return self._request("GET", "/products")

    def get_product(self, product_id: str) -> Dict:
        """Get single product"""
        return self._request("GET", f"/products/{product_id}")
    
    def get_accounts(self) -> Dict:
        """Get all accounts"""
        return self._request("GET", "/accounts")

    def get_candles(self, product_id: str, start: str, end: str, granularity: str) -> Dict:
        """Get product candles"""
        params = {
            'start': start,
            'end': end,
            'granularity': granularity
        }
        return self._request("GET", f"/products/{product_id}/candles", params=params)

    def get_market_trades(self, product_id: str, limit: int = 100) -> Dict:
        """Get market trades"""
        params = {'limit': limit}
        return self._request("GET", f"/products/{product_id}/trades", params=params)

    def create_order(self, product_id: str, side: str, order_configuration: Dict) -> Dict:
        """Create order"""
        data = {
            'product_id': product_id,
            'side': side,
            'order_configuration': order_configuration
        }
        return self._request("POST", "/orders", data=data)

    def cancel_order(self, order_id: str) -> Dict:
        """Cancel order"""
        return self._request("DELETE", f"/orders/{order_id}")

    def list_orders(self, status: Optional[str] = None, product_id: Optional[str] = None, limit: int = 100) -> Dict:
        """List orders"""
        params = {
            'status': status,
            'product_id': product_id,
            'limit': limit
        }
        # Remove None values
        params = {k: v for k, v in params.items() if v is not None}
        return self._request("GET", "/orders", params=params)