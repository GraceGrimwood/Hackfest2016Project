import json
from bottle import route, run, static_file, get, post, request, redirect, os

@route('/')
def route_to_index():
	redirect('static/index.html')

@route('/api/suburbs')
def api_suburbs():
	return list_all_suburbs()

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root = 'static\\')

'''
def prices_to_colours(District):

    var max_price
    var min_price

    var suburb_price

    var col_modifier = 255 * (suburb_price - min_price) / (max_price - min_price)

    var red = 0 + col_modifier
    var blue_modifier = red / 100
    var blue = abs(255 - col_modifier * blue_modifier)
    var green = red < blue ? blue - red : blue

    return red + "," + green + "," + blue
'''

def list_all_suburbs():
    suburbs = os.listdir("PropertyCVSData")

    for i in range(len(suburbs)):
        suburbs[i] = suburbs[i][:-4]

    return json.dumps(suburbs)
#def search_district():



run(host = 'localhost', port = 8080, debug = True)
