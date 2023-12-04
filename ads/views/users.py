import json

from django.core.paginator import Paginator
from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView

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
    fields = ["username", "first_name", "last_name", "role", "age", "location"]

    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        user = User.objects.create(
            username=user_data["username"],
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

        # user.locations.set(user_data["locations"])

        return JsonResponse({
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "role": user.role,
            "age": user.age,
            "location": list(map(str, user.locations.all())),
        }, safe=False, status=200, json_dumps_params={'ensure_ascii': False})


class UserUpdateView(UpdateView):
    pass



