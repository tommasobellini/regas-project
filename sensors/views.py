from django.shortcuts import render


def SensorView(request):
    return render(request, 'sensor_template.html', {})
