import json

from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView

from ads.models import Category, Ad


class IndexView(View):

    def get(self, request):
        return JsonResponse({
            "status": "ok"
        }, status=200)


class CategoryListView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        categories = self.object_list
        res = []
        for cat in categories:
            res.append({
                "id": cat.id,
                "name": cat.name
            })

        return JsonResponse(res, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


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
class CategoryCreateView(CreateView):
    model = Category
    fields = ["name"]

    def post(self, request, *args, **kwargs):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data["name"]
        )

        return JsonResponse({
            "id": category.id,
            "name": category.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ["name"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        category_data = json.loads(request.body)

        self.object.name = category_data["name"]

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name
        })


@method_decorator(csrf_exempt, name="dispatch")
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)


class AdsListView(ListView):
    model = Ad

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        self.object_list = self.object_list.select_related('author')

        res = []
        for ad in self.object_list:
            res.append({
                "id": ad.pk,
                "name": ad.name,
                "author": str(ad.author),
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published
            })

        return JsonResponse(res, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


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
                "author": str(ad.author),
                "price": ad.price,
                "description": ad.description,
                "is_published": ad.is_published
            }, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


# @method_decorator(csrf_exempt, name="dispatch")
# class AdCreateView(CreateView):
#     model = Ad
#     fields = ["name", "author", "price", "description", "address", "is_published"]
#
#     def post(self, request, *args, **kwargs):
#         ad_data = json.loads(request.body)
#
#         ad = Ad.objects.create(
#             name=ad_data["name"],
#             author=ad_data["author"],
#             price=ad_data["price"],
#             description=ad_data["description"],
#             is_published=ad_data["is_published"]
#         )
#
#         return JsonResponse({
#             "id": ad.pk,
#             "name": ad.name,
#             "author": ad.author,
#             "price": ad.price,
#             "description": ad.description,
#             "address": ad.address,
#             "is_published": ad.is_published
#         })


@method_decorator(csrf_exempt, name="dispatch")
class AdUpdateView(UpdateView):
    model = Ad
    fields = ["name", "author", "price", "description", "is_published"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        ad_data = json.loads(request.body)
        self.object.name = ad_data["name"]
        self.object.price = ad_data["price"]
        self.object.description = ad_data.get("description")
        self.object.is_published = ad_data.get("is_published")

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "name": self.object.name,
            "author": str(self.object.author),
            "price": self.object.price,
            "description": self.object.description,
            "is_published": self.object.is_published
        })


@method_decorator(csrf_exempt, name="dispatch")
class AdDeleteView(DeleteView):
    model = Ad
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)



