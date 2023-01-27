from uuid import uuid4

from django.http import JsonResponse
from django.views.generic import TemplateView


def tinymce_upload(request):
    file = request.FILES.get("file")
    filename = f"tinymce/{uuid4()}/{str(file)}"
    with open(filename, "wb") as f:
        f.write(file.read())

    return JsonResponse({"location": f"/media/{filename}"})


class HomePage(TemplateView):
    template_name = "index.html"
