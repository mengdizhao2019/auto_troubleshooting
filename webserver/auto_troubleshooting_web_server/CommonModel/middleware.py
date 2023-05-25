import time
from . import models



class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 记录请求开始时间
        start_time = time.time()

        response = self.get_response(request)

        # 计算请求耗时
        duration = time.time() - start_time

        # 打印耗时信息
        print(f"Request to {request.path} took {duration} seconds")

        return response
    
class IPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 获取访问者的IP地址
        ip_address = request.META.get('REMOTE_ADDR')
        print('===>ip_address', ip_address)

        if ip_address == '127.0.0.1' or ip_address == '10.99.98.22':
            pass
        else:
            models.AccessLog.objects.create(url=request.path, ip_address=request.META['REMOTE_ADDR'])

        # 将IP地址添加到请求对象中，以便后续视图函数或其他中间件使用
        request.ip_address = ip_address

        response = self.get_response(request)
        return response

       
