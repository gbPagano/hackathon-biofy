import httpx

from src.config import settings


async def predict(img):
    url = "https://hackathon-biofy.fly.dev/predict"
    headers = {
        "accept": "application/json",
    }

    files = {
        "file": ("file.jpg", img, "image/jpeg"),
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, files=files)
        print(response.json())
        return response.json()

async def send_message(
    text, from_number_id=settings.PHONE_NUMBER_ID, from_number=settings.RECIPIENT_WAID
):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": from_number,
        "type": "text",
        "text": {"preview_url": False, "body": text},
    }
    async with httpx.AsyncClient() as client:
        url = f"https://graph.facebook.com/v18.0/{from_number_id}/messages"
        return await client.post(url, json=data, headers=headers)


async def get_image(img_id):
    headers = {
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
    }

    async with httpx.AsyncClient() as client:
        url = f"https://graph.facebook.com/{settings.VERSION}/{img_id}"
        res = await client.get(url, headers=headers)
        print(res.json())
        next_url = res.json()["url"]
        res = await client.get(next_url, headers=headers)
        img = res.content

        return img


async def backup_database():
    headers = {
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
    }

    file_path = "database/db.json"
    files = {
        "file": ("file.txt", open(file_path, "rb")),
        "type": (None, "text/plain"),
        "messaging_product": (None, "whatsapp"),
    }
    # getting file id
    async with httpx.AsyncClient() as client:
        url = f"https://graph.facebook.com/{settings.VERSION}/{settings.PHONE_NUMBER_ID}/media"
        response = await client.post(url, files=files, headers=headers)

        document_id = response.json()["id"]

    # sending file
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": settings.RECIPIENT_WAID,
        "type": "document",
        "document": {"id": document_id, "filename": "db.json"},
    }

    async with httpx.AsyncClient() as client:
        url = f"https://graph.facebook.com/{settings.VERSION}/{settings.PHONE_NUMBER_ID}/messages"
        return await client.post(url, json=data, headers=headers)


if __name__ == "__main__":
    import asyncio

    asyncio.run(send_message("ola"))
    asyncio.run(backup_database())
