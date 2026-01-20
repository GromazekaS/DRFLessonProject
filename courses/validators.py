from rest_framework.serializers import ValidationError


class LinkValidator():


    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        print(value)
        temp = value['video_link'].split('/')
        print(temp)
        if temp[2] != 'www.youtube.com':
            raise ValidationError(f'Ссылка на сторонний ресурс {temp[2]}')