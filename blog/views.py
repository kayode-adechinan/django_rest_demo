from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from blog.models import Note
from blog.serializers import NoteSerializer


# Create your views here.


@csrf_exempt
def note_list(request):
    """
    List all code notes, or create a new note.
    """
    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = NoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            # return JsonResponse(serializer.data, status=201)
            # customise response
            return JsonResponse(serializer.data['title'], status=201, safe=False)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def note_detail(request, note_id):
    """
    Retrieve, update or delete a code note.
    """
    try:
        note = Note.objects.get(pk=note_id)
    except Note.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = NoteSerializer(note, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        note.delete()
        return HttpResponse(status=204)
