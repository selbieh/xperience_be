from django.conf import settings
from .handle_request import handle_request


class PayTabsGateway:

    def __init__(self) -> None:
        self.config = {
            "base_url": settings.PAYTABS.get("PAYTABS_BASEURL"),
            "profile_id": settings.PAYTABS.get("PAYTABS_PROFILE"),
            "auth_header_key": settings.PAYTABS.get("PAYTABS_AUTH"),
        }

    def process_payment(self, user, price, cart_id):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": self.config.get("auth_header_key"),
        }
        payload = {
            "profile_id": self.config["profile_id"],
            "tran_type": "sale",
            "tran_class": "ecom",
            "cart_id": str(cart_id),
            "cart_description": "payment for Event",
            "cart_currency": "EGP",
            "cart_amount": price,
            "callback": "https://wee-dev-api.shelter-technology.com/api/v1/payment/call-back/",
            # "return": "https://wee-dashboard.shelter-technology.com/home",
            "hide_shipping": True,
            "framed": True,
            "customer_details": {"name": user.name, "email": user.email, "phone": str(user.mobile_number)},
        }
        url = f'{self.config.get("base_url")}/payment/request'
        status, response = handle_request(method="POST", url=url, payload=payload, headers=headers)
        return status, response

    def payment_inquiry(self, tran_ref):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "authorization": self.config["auth_header_key"],
        }

        payload = {"profile_id": self.config.get("profile_id"), "tran_ref": tran_ref}
        url = f'{self.config.get("base_url")}/payment/query'
        status, response = handle_request(url=url, payload=payload, headers=headers)
        return status, response

    def refund(self, tran_ref, tran_id, amount):
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "authorization": self.config["auth_header_key"],
        }
        payload = {
            "profile_id": self.config.get("profile_id"),
            "tran_type": "refund",
            "tran_class": "ecom",
            "cart_id": str(tran_id),
            "cart_currency": "EGP",
            "cart_amount": amount,
            "cart_description": "Refund reason",
            "tran_ref": tran_ref,
        }
        url = f'{self.config.get("base_url")}/payment/request'
        status, response = handle_request(method="POST", url=url, payload=payload, headers=headers)
        return status, response
