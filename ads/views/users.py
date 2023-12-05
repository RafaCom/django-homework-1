import json

from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from ads.models import User, Location
from homework_1 import settings


class UserListView(ListView):
    model = User
    queryset = User.objects.all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.filter(ad__is_published=True).annotate(total_ads=Count('ad'))

        paginator = Paginator(self.object_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page', 0)
        page_obj = paginator.get_page(page_number)

        users = []
        for user in page_obj:
            users.append({
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "age": user.age,
                "location": list(map(str, user.locations.all())),
                "total_ads": user.total_ads
            })

        response = {
            "items": users,
            "num_pages": paginator.num_pages,
            "total": paginator.count
        }

        return JsonResponse(response, status=200, json_dumps_params={'ensure_ascii': False})


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return JsonResponse({"error": "Not found"}, status=404)

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "location": list(map(str, user.locations.all())),
        }, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age", "location"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data["username"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            role=user_data["role"],
            age=user_data["age"],
        )

        for location in user_data["locations"]:
            location_obj, created = Location.objects.get_or_create(
                name=location,
                defaults={"lat": 0, "lng": 0}
            )
            user.locations.add(location_obj)
        user.save()

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "location": list(map(str, user.locations.all())),
        }, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ["username", "password", "first_name", "last_name", "role", "age", "locations"]

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_data = json.loads(request.body)
        self.object.username = user_data["username"]
        self.object.password = user_data["password"]
        self.object.first_name = user_data["first_name"]
        self.object.last_name = user_data["last_name"]
        self.object.role = user_data["role"]
        self.object.age = user_data["age"]

        for location in user_data["locations"]:
            location_obj, created = Location.objects.get_or_create(
                name=location,
                defaults={"lat": 0, "lng": 0}
            )
            self.object.locations.add(location_obj)

        try:
            self.object.full_clean()
        except ValidationError as e:
            return JsonResponse(e.message_dict, status=422)

        self.object.save()

        return JsonResponse({
            "id": self.object.id,
            "username": self.object.username,
            "first_name": self.object.first_name,
            "last_name": self.object.last_name,
            "role": self.object.role,
            "age": self.object.age,
            "locations": list(map(str, self.object.locations.all())),
        }, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


@method_decorator(csrf_exempt, name="dispatch")
class UserDeleteView(DeleteView):
    model = User
    success_url = "/"

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)

        return JsonResponse({"status": "ok"}, status=200)



