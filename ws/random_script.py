from sensors.models import Sensor


async def send(data):
    from channels.layers import get_channel_layer
    channel_layer = get_channel_layer()

    await channel_layer.group_send(
        'core',
        {
            'type': 'receive',
            'data': data
        }
    )


from datetime import datetime
import serial

ser = serial.Serial('/dev/tty.usbmodem14101', 9600)
xs = []
ys = []
while True:
    arduino_data = ser.readline().decode("utf-8").strip().split('|')
    temp_data = arduino_data[0]
    humidity_data = arduino_data[1]

    # import datetime as dt
    # import matplotlib.pyplot as plt
    #
    # # Create figure for plotting
    # fig = plt.figure()
    # ax = fig.add_subplot(1, 1, 1)
    #
    #
    # # This function is called periodically from FuncAnimation
    #
    # # Add x and y to lists
    # xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
    # ys.append(temp_data)
    #
    # # Limit x and y lists to 20 items
    # xs = xs[-20:]
    # ys = ys[-20:]
    #
    # # Draw x and y lists
    # ax.plot(xs, ys)
    #
    # # Format plot
    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    # plt.title('TMP102 Temperature over Time')
    # plt.ylabel('Temperature (deg C)')
    #
    # # Set up plot to call animate() function periodically
    #
    # my_stringIObytes = BytesIO()
    # plt.savefig(my_stringIObytes, format='jpg')
    # plt.style.use(['dark_background'])
    # my_stringIObytes.seek(0)
    # img = base64.b64encode(my_stringIObytes.read())

    sensor_obj = Sensor.objects.all()[0]
    sensor_lines = sensor_obj.sensorline_set.filter(datetime__minute__in=[5, 10, 15, 20, 25, 30],
                                                    datetime__second__lt=30, datetime__second__gt=10)

    data = {
        'name': 'DHT22 Sensor',
        'location': "Via Dell'Innominato 11",
        'humidity': humidity_data + "%",
        'temperature': temp_data + "°C",
        'datetime': str(datetime.today().strftime("%Y-%m-%d %H:%M:%S")),
        # 'temp_graph': img.decode('utf8')
    }
    import asyncio

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(send(data))
    loop.close()
