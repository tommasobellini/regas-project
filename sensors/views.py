from django.shortcuts import render

from sensors.models import Sensor


def SensorView(request, pk=None):
    sensors = Sensor.objects.all()

    sensor = sensors.filter(pk=pk)
    if not sensor:
        return render(request, 'page_404.html', {})

    return render(request, 'sensor_template.html', {'sensors': sensors, 'sensor':sensor[0]})
