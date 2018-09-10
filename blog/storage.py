import uuid
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os


# ImageField图片上传（修改保存的图片名）
class ImageStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(ImageStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        ext = os.path.splitext(name)[1]
        dir_name = os.path.dirname(name)
        name = os.path.join(dir_name, str(uuid.uuid1()) + ext)
        return super(ImageStorage, self)._save(name, content)
