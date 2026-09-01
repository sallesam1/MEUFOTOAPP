import os
from supabase import create_client
from supabase_config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET

_cliente = None

def get_client():
    global _cliente
    if _cliente is None:
        _cliente = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _cliente

def upload_bytes(data, filename, content_type="image/jpeg"):
    cliente = get_client()
    cliente.storage.from_(SUPABASE_BUCKET).upload(
        filename, data, {"content-type": content_type}
    )
    return filename

def download_bytes(filename):
    cliente = get_client()
    return cliente.storage.from_(SUPABASE_BUCKET).download(filename)

def get_public_url(filename):
    return f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{filename}"

def delete_file(filename):
    try:
        cliente = get_client()
        cliente.storage.from_(SUPABASE_BUCKET).remove([filename])
    except Exception:
        pass
