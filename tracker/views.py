from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone


@login_required
def homepage(request):
    clients = request.user.clients.all()
    return render(request, "tracker/homepage.html", {
        "clients": clients,
    })


@login_required
@require_GET
def check_timer(request):
    open_interval = request.user.intervals.filter(
        finished_at__isnull=True).first()
    if open_interval is None:
        return JsonResponse({"status": "ok", "data": None})
    else:
        return JsonResponse({
            "status": "ok",
            "data": {
                "pk": open_interval.pk,
                "client_name": open_interval.client.name,
                "started_at": open_interval.started_at
            },
        })


@login_required
@csrf_exempt
@require_POST
def start_timer(request):
    # decode the request body
    data = json.loads(request.body.decode("utf-8"))

    # make sure there's a client ID
    # if not, give the user a warning

    client_pk = data.get('clientId')
    note = data.get('note')

    if client_pk is None:
        return JsonResponse(
            {
                "status": "error",
                "message": "clientId is required"
            }, status=400)

    # find the client
    client = request.user.clients.filter(pk=client_pk).first()
    if client is None:
        return JsonResponse(
            {
                "status": "error",
                "message": f"client {client_pk} does not exist"
            },
            status=400)

    # first, check and make sure there's not an open work interval for this user
    open_interval = request.user.intervals.filter(
        finished_at__isnull=True).first()
    if open_interval is not None:
        return JsonResponse({
            "status": "error",
            "message": "user already has an open work interval"
        })

    # create a new WorkInterval for the current user and the client
    work_interval = request.user.intervals.create(client=client,
                                                  note=note,
                                                  started_at=timezone.now())

    return JsonResponse({
        "status": "ok",
        "data": {
            "pk": work_interval.pk,
            "client_name": work_interval.client.name,
            "note": work_interval.note,
            "started_at": work_interval.started_at
        },
    })


@login_required
@csrf_exempt
@require_POST
def stop_timer(request):
    open_interval = request.user.intervals.filter(
        finished_at__isnull=True).first()
    if open_interval is None:
        return JsonResponse({
            "status": "error",
            "message": "no open work interval"
        })

    open_interval.finished_at = timezone.now()
    open_interval.save()
    return JsonResponse({
        "status": "ok",
        "data": {
            "pk": open_interval.pk,
            "client_name": open_interval.client.name,
            "started_at": open_interval.started_at,
            "finished_at": open_interval.finished_at,
        }
    })
