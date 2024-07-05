import json
from pydantic import AnyUrl, BaseModel
import aiohttp


class CreateInvoiceError(Exception):
    pass


class CreateInvoiceData(BaseModel):
    """Data for creating an invoice in NowPayments API"""

    """The amount that users have to pay for the order stated in fiat currency.
    In case you do not indicate the price in crypto, 
    our system will automatically convert this fiat amount into its crypto equivalent."""
    price_amount: float
    """The fiat currency in which the price_amount is specified (usd, eur, etc);"""
    price_currency: str
    """The specified crypto currency (btc, eth, etc), 
    or one of available fiat currencies if it's enabled for your account (USD, EUR, ILS, GBP, AUD, RON);
    If not specified, can be chosen on the invoice_url"""
    pay_currency: str | None = None
    """Url to receive callbacks, should contain "http" or "https", eg. "https://nowpayments.io";"""
    ipn_callback_url: AnyUrl | None = None
    """Internal store order ID, e.g. "RGDBP-21314"""
    order_id: str | None = None
    """Internal store order description, e.g. "Apple Macbook Pro 2019 x 1"""
    order_description: str | None = None
    """Url where the customer will be redirected after successful payment;"""
    success_url: AnyUrl | None = None
    """Url where the customer will be redirected after failed payment"""
    cancel_url: AnyUrl | None = None


class CreatedInvoiceResult(BaseModel):
    id: str
    order_id: str
    order_description: str | None
    price_amount: str
    price_currency: str
    pay_currency: str | None
    ipn_callback_url: AnyUrl | None
    invoice_url: AnyUrl
    success_url: AnyUrl | None
    cancel_url: AnyUrl | None
    created_at: str
    updated_at: str


class NowPayments:
    def __init__(self, api_key: str, ipn_key: str):
        self.api_key = api_key
        self.ipn_key = ipn_key
        self.headers = {
            "x-api-key": str(self.api_key),
            "Content-Type": "application/json",
        }

    async def make_request(
        self,
        url: str,
        request_type: str,
        data=None,
        json: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ):
        if headers:
            self.headers = headers

        if request_type == "GET":
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=url, headers=self.headers, data=data, json=json, params=params
                ) as response:
                    return await response.json()

        elif request_type == "POST":
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url=url, headers=self.headers, data=data, json=json, params=params
                ) as response:
                    if response.status != 200:
                        raise CreateInvoiceError(
                            f"Ошибка создания счета: {response.status} - {await response.text()}"
                        )
                    return await response.json()
        else:
            raise ValueError("request_type must be GET or POST")

    async def parse_created_invoice(self, response: dict):
        return CreatedInvoiceResult(**response)

    async def create_invoice(
        self, invoice_data: CreateInvoiceData
    ) -> CreatedInvoiceResult:
        data = invoice_data.model_dump_json()
        url = "https://api.nowpayments.io/v1/invoice"
        # url = 'https://api-sandbox.nowpayments.io/v1/invoice'
        response = await self.make_request(url=url, request_type="POST", data=data)
        return await self.parse_created_invoice(response)
