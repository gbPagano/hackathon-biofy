from conftest import get_body_post_webhook


def test_generic_post_webhook(client):
    result = client.post("/webhook", json=get_body_post_webhook("test: hello world"))
    assert result.status_code == 200
