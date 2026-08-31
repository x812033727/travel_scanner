import base64
import hashlib
import hmac

from app.line.client import verify_webhook_signature


def test_verify_webhook_signature_uses_exact_raw_body() -> None:
    secret = "channel-secret"
    body = b'{"events": []}\n'
    signature = base64.b64encode(
        hmac.new(secret.encode(), body, hashlib.sha256).digest()
    ).decode()
    assert verify_webhook_signature(body, signature, secret) is True
    assert verify_webhook_signature(body.rstrip(), signature, secret) is False
    assert verify_webhook_signature(body, "invalid", secret) is False
