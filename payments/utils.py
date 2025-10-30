# payments/utils.py
import hmac, hashlib

def hmac_sha256_signature(secret: str, params: dict) -> str:
    """
    Signature générique: on trie les clés et on joint key=value avec &.
    Adapte le canonical string aux exigences de ton PSP (CMI, etc.).
    """
    items = [(k, str(v)) for k, v in params.items() if v is not None]
    items.sort(key=lambda x: x[0].lower())
    signable = "&".join(f"{k}={v}" for k, v in items)
    return hmac.new(secret.encode("utf-8"), signable.encode("utf-8"), hashlib.sha256).hexdigest()
