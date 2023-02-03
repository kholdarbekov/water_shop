from uuid import uuid4

from django.http import JsonResponse
from django.views.generic import DetailView, TemplateView

from .models import Water


def tinymce_upload(request):
    file = request.FILES.get("file")
    filename = f"tinymce/{uuid4()}/{str(file)}"
    with open(filename, "wb") as f:
        f.write(file.read())

    return JsonResponse({"location": f"/media/{filename}"})


class HomePage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        warehouse = []
        for water in Water.objects.all()[:3]:
            warehouse.append({"water": water, "warehouse": water.warehouse})
        if warehouse:
            kwargs["best_water_warehouse"] = warehouse[0]
            kwargs["water_warehouses"] = warehouse[1:]
        return super().get_context_data(**kwargs)


class ProductDetailView(DetailView):
    model = Water
    template_name = "product/water.html"
