from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from google_images_search import GoogleImagesSearch
from rest_framework import viewsets, permissions, generics

from django.conf import settings
from memes.models import Memes
from tags.models import Tags
from .indexer import query
from .indexer.simplifier import simplify_string
from .models import ImageDescriptions
from .models import Images
from .models import TextDescriptions
from .serializers import ImagesDescriptionsSerializer
from .serializers import ImagesSerializer
from .serializers import TextDescriptionsSerializer


def split_query(q):
    res = []
    for i in q.split(", "):
        for j in i.split(" "):
            res.append(j)
    return res


DEV_API_KEY = 'AIzaSyD1Na311j0BcW2_xw8IJwxic3GB1f-x_vo'
PROJECT_CX = '002908623333556470340:g0fw495dowk'


def google_search(query_text, num=5):
    gis = GoogleImagesSearch(DEV_API_KEY, PROJECT_CX)
    gis.search({'q': '{query} meme'.format(query=query_text), 'num': num})
    return [img._url for img in gis.results()]


def search(query_text, query_image):
    # разбиваем запросы на отдельные слова.
    if query_text is not None:
        text_words = simplify_string(query_text)
    else:
        text_words = ""
        query_text = ""
    if query_image is not None:
        image_words = simplify_string(query_image)
    else:
        image_words = ""
        query_image = ""

    # на данный момент достаем все внутри индексера
    # ищем все картинки в описании которых совпало хотя бы одно слово. получаем список объектов модели
    # queryset_text = TextDescriptions.objects.filter(Q(word__in=text_words))
    # queryset_image = ImageDescriptions.objects.filter(Q(word__in=image_words))

    # получаем список из URL
    # ([urls],"error")
    if query_text == query_image:  # не расширенный поиск, тогда объединяем
        res1 = query.make_query(text_phrase=query_text,
                                descr_words="")
        res2 = query.make_query(text_phrase="",
                                descr_words=query_text)
        result = [list(dict.fromkeys(list(res2[0] + res1[0]))), ""]  # delete duplicates
    else:
        result = query.make_query(text_phrase=query_text,
                                  descr_words=query_image)

    return result


class SearchAPI(generics.GenericAPIView):
    serializer_class = ImagesSerializer

    def get(self, request, *args, **kwargs):
        # приходит запрос в виде двух строк - слова через пробел, мб запятые, с ключевыми словами
        query_text = self.request.GET.get('qText')
        query_image = self.request.GET.get('qImage')

        # поиск и ранжировка всех мемов подходящих под запрос
        result = search(query_text, query_image)
        google_urls = []

        # фильтруем по тегам
        query_tags = self.request.GET.get('tags')
        res = result[0]
        if query_tags is not None and query_tags != '':
            tags = query_tags.split(',')
            for tag_id in tags:
                res = [meme.id for meme in Tags.objects.get(pk=tag_id).taggedMemes.filter(Q(id__in=res))]
        else:
            try:
                if len(result[0]) < 10 and not settings.DEBUG:
                    google_urls = list(google_search(query_text))
            except Exception as ex:
                print("GOOGLE SEARCH ERROR: " + str(ex))
                pass

        # записываем их в  response
        if result[1] == "":
            response = JsonResponse([{
                'id': i,
                'url': Memes.objects.get(pk=i).url  # _compressed
            } for i in res] + [{
                'url': url
            } for url in google_urls], safe=False)
        else:
            response = HttpResponse(result[1])
        return response


class TextDescriptionsViewSet(viewsets.ModelViewSet):
    queryset = TextDescriptions.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = TextDescriptionsSerializer


class ImageDescriptionsViewSet(viewsets.ModelViewSet):
    queryset = ImageDescriptions.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ImagesDescriptionsSerializer


class OwnMemesViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = ImagesSerializer

    def get_queryset(self):
        return self.request.user.ownImages.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MemesViewSet(viewsets.ModelViewSet):
    queryset = Images.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ImagesSerializer


class SearchOwnMemesAPI(generics.GenericAPIView):
    serializer_class = ImagesSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get(self, request, *args, **kwargs):
        # приходит запрос в виде двух строк - слова через пробел, мб запятые, с ключевыми словами
        query_text = self.request.GET.get('qText')
        query_image = self.request.GET.get('qImage')

        # поиск и ранжировка всех мемов подходящих под запрос
        result = search(query_text, query_image)

        # фильтруем по своим мемам
        queryset = request.user.ownImages.filter(Q(id__in=result[0]))

        # фильтруем по тегам
        query_tags = self.request.GET.get('tags')
        res = [i.id for i in queryset]
        if query_tags is not None and query_tags != '':
            tags = query_tags.split(',')
            for tag_id in tags:
                res = [meme.id for meme in Tags.objects.get(pk=tag_id).taggedMemes.filter(Q(id__in=res))]

        # записываем их в  response
        if result[1] == "":
            response = JsonResponse([{
                'id': i,
                'url': Memes.objects.get(pk=i).url  # _compressed
            } for i in res], safe=False)
        else:
            response = HttpResponse(result[1])

        return response
