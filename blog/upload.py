# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.conf import settings
import os
import uuid
import json


def upload_image(request, dir_name):
    result = {"error": 1, "message": "上传出错"}
    files = request.FILES.get("imgFile", None)   # 取得上传的图片数据
    if files:
        result = image_upload(files, dir_name)   # dir_name是保存图片的文件夹，即kindeditor
    return HttpResponse(json.dumps(result), content_type="application/json")


def image_upload(files, dir_name):
    allow_suffix = ['.jpg', '.png', '.jpeg', '.gif', '.bmp']
    file_suffix = os.path.splitext(files.name)[1]   # 图片扩展名
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    path = os.path.join(settings.MEDIA_ROOT, dir_name)
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = str(uuid.uuid1()) + file_suffix
    path_file = os.path.join(path, file_name).replace('\\', '/')  # 绝对路径
    file_url = settings.MEDIA_URL + dir_name + '/' + file_name    # 相对路径，两者指向的目的地一样，即都是自己创建的uploads/kindeditor中的图片名
    open(path_file, 'wb').write(files.file.read())   # 写入上传的图片数据
    return {"error": 0, "url": file_url}
