def build_query(host: str, method: str, params: dict) -> str:
    url = host + method + "?"
    if "v" not in params:
        params["v"] = "5.131"
    url += "&".join([f"{k}={v}" for k, v in params.items()])
    return url
