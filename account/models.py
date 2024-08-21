import io

from django.core.files.base import ContentFile
from django.db import models
from django.conf import settings
from PIL import Image as PilImage



class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='media/photo/', blank=True)
    Description = models.TextField(default='Нет описания')

    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        if self.photo:  # Проверяем, загружено ли изображение
            # Открываем изображение
            img = PilImage.open(self.photo)

            # Изменяем размер до фиксированного разрешения (например, 300x300)
            img = img.resize((600, 600), PilImage.LANCZOS)

            # Конвертируем изображение в RGB, если оно в RGBA
            if img.mode == 'RGBA':
                img = img.convert('RGB')

            # Сохраняем изображение в буфер
            img_bytes = io.BytesIO()
            img.save(img_bytes, format='JPEG')  # Или 'PNG', в зависимости от типа изображения
            img_bytes.seek(0)

            # Создаем новое ContentFile
            self.photo.save(self.photo.name, ContentFile(img_bytes.read()), save=False)

        # Вызываем родительский метод save
        super(Profile, self).save(*args, **kwargs)
