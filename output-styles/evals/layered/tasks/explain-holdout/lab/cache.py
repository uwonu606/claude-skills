def make_key(product_id, request):
    lang = request.headers.get("Accept-Language", "ko")
    ts = request.query_params.get("ts", "")
    return f"product:{product_id}:{lang}:{ts}"
