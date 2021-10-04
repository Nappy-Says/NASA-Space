# import socketio
# from flask_socketio import SocketIO

# socket = SocketIO(app, cors_allowed_origins="*")
# socket = socketio.Server(cors_allowed_origins='*')
# app.wsgi_app = socketio.WSGIApp(socket, app.wsgi_app)



# @socket.event
# def connect():
#     print('CLIENT IS CONNECTED')


# @socket.on('location_handler_time_multiply_acceleration')
# def get(timeseconds):
#     print('Received data: ', timeseconds)

#     while True:
#         now = int(time.mktime(datetime.now().timetuple()))
#         allseconds = now+timeseconds
#         datestamp = datetime.fromtimestamp(allseconds)

#         day = datestamp.day
#         hour = datestamp.hour
#         year = datestamp.year
#         month = datestamp.month
#         minute = datestamp.minute
#         second = datestamp.second

#         socket.sleep(1)

#         dtobj = datetime(year, month, day, hour, minute, second)
#         dtobj2 = datetime(year, month, day, hour+5, minute, second)
#         dataa = get_more_data(dtobj)

#         print(get_more_data(dtobj2))

#         socket.emit('location', 'list(dataa)')


# @socket.on('location')
# def ll(s):
#     print(s)
