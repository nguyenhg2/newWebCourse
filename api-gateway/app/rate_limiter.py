import time
import logging
from fastapi import Request, HTTPException
import redis.asyncio as redis # Sử dụng bản async để không làm nghẽn Gateway

class RateLimiter:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
        self.limit = 100 
        self.window = 60 

    async def check_rate_limit(self, request: Request):
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"

        try:
            async with self.redis.pipeline(transaction=True) as pipe:
                now = time.time()
                # Xóa các bản ghi cũ ngoài khoảng thời gian window
                await pipe.zremrangebyscore(key, 0, now - self.window)
                # Đếm số lượng request hiện tại của IP này
                await pipe.zcard(key)
                # Thêm request hiện tại vào (dùng timestamp làm score)
                await pipe.zadd(key, {str(now): now})
                # Thiết lập thời gian sống cho key để tránh rác dữ liệu
                await pipe.expire(key, self.window)
                
                # Thực thi các lệnh
                _, current_requests, _, _ = await pipe.execute()

            # Nếu vượt quá giới hạn, báo lỗi 429
            if current_requests > self.limit:
                logging.warning(f"Rate limit exceeded for IP: {client_ip}")
                raise HTTPException(
                    status_code=429, 
                    detail="Too many requests. Please try again later."
                )
                
        except redis.ConnectionError:
            # Nếu Redis sập, chúng ta cho phép request đi qua để tránh làm hỏng toàn bộ hệ thống
            logging.error("Could not connect to Redis for Rate Limiting")
            return

# Khởi tạo instance (Bạn nên truyền cấu hình từ file .env vào đây)
limiter = RateLimiter(host="localhost", port=6379)