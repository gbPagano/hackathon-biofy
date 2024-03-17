from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse

from src.config import settings
from src.utils import send_message, get_image, predict

wb_app = APIRouter(prefix="/webhook")



@wb_app.get("")
def get_webhook(request: Request):
    """We need this URL to setup webhook initially.

    Args:
        request (Request): https://developers.facebook.com/docs/graph-api/webhooks/getting-started#verification-requests
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == settings.VERIFY_TOKEN:
            return JSONResponse(content=int(challenge.strip()), status_code=200)

        return HTTPException(
            status_code=403, detail="Authentication failed. Invalid Token"
        )


@wb_app.post("")
async def post_webhook(request: Request):
    """We need this URL to process user messages.

    Args:
        request (Request): https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/payload-examples#text-messages
    """
    body = await request.json()
    # validating the payload of a message
    if not (
        body.get("entry", [{}])[0]
        .get("changes", [{}])[0]
        .get("value", {})
        .get("messages", [{}])[0]
    ):
        raise HTTPException(status_code=404)  # it is not a new message webhook

    try:
        print(body)

        body_value = body["entry"][0]["changes"][0]["value"]

        from_num_id = body_value["metadata"]["phone_number_id"]
        from_num = body_value["messages"][0]["from"]
        image_id = body_value["messages"][0]["image"]["id"]
        print("image id:", image_id)
        image = await get_image(image_id)

        try:
            response = await predict(image)
            result = response["result"]
        except Exception as e:
            print("ERRO ::", str(e))
            result = "Erro"

        await send_message(result, from_num_id, from_num)

        return JSONResponse(content={"success": True}, status_code=200)
    except Exception as e:
        print("ERRO ::", str(e))
        await send_message("Comando Inválido", from_num_id, from_num)
