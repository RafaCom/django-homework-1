import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Category, Ad


class IndexView(View):

    def get(self, request):
        return JsonResponse({
            "status": "ok"
        }, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class CategoryView(View):

    def get(self, request):
        categories = Category.objects.all()
        res = []
        for cat in categories:
            res.append({
                "id": cat.id,
                "name": cat.name
            })

        return JsonResponse(res, safe=False, status=200, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        category_data = json.loads(request.body)

        category = Category()
        category.name = category_data["name"]

        category.save()

        return JsonResponse({
            "id": category.pk,
            "name": category.name
        })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            cat = self.get_object()
        except Category.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": cat.id,
            "name": cat.name
        }, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class AdsView(View):

    def get(self, request):
        ads = Ad.objects.all()
        res = []
        for ad in ads:
            res.append({
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published
            })

        return JsonResponse(res, safe=False, status=200, json_dumps_params={'ensure_ascii': False})

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ad()
        ad.name = ad_data["name"]
        ad.author = ad_data["author"]
        ad.price = ad_data["price"]
        ad.description = ad_data["description"]
        ad.address = ad_data["address"]
        ad.is_published = ad_data["is_published"]

        ad.save()

        return JsonResponse({
            "id": ad.pk,
            "name": ad.name,
            "author": ad.author,
            "price": ad.price,
            "description": ad.description,
            "address": ad.address,
            "is_published": ad.is_published
        })


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
                "id": ad.pk,
                "name": ad.name,
                "author": ad.author,
                "price": ad.price,
                "description": ad.description,
                "address": ad.address,
                "is_published": ad.is_published
            }, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


