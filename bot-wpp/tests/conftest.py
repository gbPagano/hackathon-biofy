from fastapi.testclient import TestClient
from pytest import fixture

from src.config import settings
from src.main import app


@fixture(scope="session")
def client():
    return TestClient(app)


def get_body_post_webhook(message):
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "1111111111111111",
                "changes": [
                    {
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {
                                "display_phone_number": "1111111111",
                                "phone_number_id": settings.PHONE_NUMBER_ID,
                            },
                            "contacts": [
                                {
                                    "profile": {"name": "User Name"},
                                    "wa_id": settings.RECIPIENT_WAID,
                                }
                            ],
                            "messages": [
                                {
                                    "from": settings.RECIPIENT_WAID,
                                    "id": "aaaaaaaaaaaaaaaaaaa",
                                    "timestamp": "1704551583",
                                    "text": {"body": message},
                                    "type": "text",
                                }
                            ],
                        },
                        "field": "messages",
                    }
                ],
            }
        ],
    }
