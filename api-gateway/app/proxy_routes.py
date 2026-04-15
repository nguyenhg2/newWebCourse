from fastapi import APIRouter, Request, HTTPException, Response
import httpx
import logging

router = APIRouter()

SERVICES = {
    "core": "http://localhost:8001",
    "payment": "http://localhost:8002",
    "video": "http://localhost:8003",
    "blog": "http://localhost:8004",
}

client = httpx.AsyncClient(timeout=10.0)

async def proxy_request(service_name: str, path: str, request: Request):
    if service_name not in SERVICES:
        raise HTTPException(status_code=404, detail="Service không tồn tại")
    target_url = f"{SERVICES[service_name]}/{path}"
    
    method = request.method
    params = request.query_params
    headers = dict(request.headers)
    headers.pop("host", None)
    body = await request.body()

    try:
        response = await client.request(
            method=method,
            url=target_url,
            params=params,
            headers=headers,
            content=body
        )

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )
        
    except httpx.RequestError as exc:
        logging.error(f"Lỗi kết nối đến {service_name}: {exc}")
        raise HTTPException(status_code=503, detail=f"Dịch vụ {service_name} tạm thời không khả dụng")

@router.api_route("/core/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def core_proxy(path: str, request: Request):
    return await proxy_request("core", path, request)

@router.api_route("/payment/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def payment_proxy(path: str, request: Request):
    return await proxy_request("payment", path, request)

@router.api_route("/video/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def video_proxy(path: str, request: Request):
    return await proxy_request("video", path, request)

@router.api_route("/blog/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def blog_proxy(path: str, request: Request):
    return await proxy_request("blog", path, request)