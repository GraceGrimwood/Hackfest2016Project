import json
from bottle import route, run, static_file, get, post, request, redirect, os

@route('/')
def route_to_index():
	redirect('static/index.html')

@route('/api/regions')
def api_regions():
	return list_all_regions()

@route('/api/region/<region>')
def api_region(region):
	return parse_region(region)

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

def list_all_regions():
    regions = os.listdir("PropertyCVSData")

    for i in range(len(regions)):
        regions[i] = regions[i][:-4]

    return json.dumps(regions)

def parse_region(region):
    region_file = open("PropertyCVSData/" + region + ".csv")
    suburb_list = []

    next(region_file)   #Remove the first line
    for line in region_file:
        keys = line.split('",')

        print(keys)

        for k in range(len(keys)):
            keys[k] = keys[k].replace("\"", "")   #Remove quotes around string
            keys[k] = keys[k].replace("\n", "")

        print(keys)

        suburb_info = {'Suburb': keys[0], 'Number of Sales': keys[1],
        'Median Sale Price': keys[2], 'Difference Between Sales Price and CV': keys[3],
        'Capital Value Date': keys[4]}
        suburb_list.append(suburb_info)

    return json.dumps(suburb_list)


run(host = 'localhost', port = 8080, debug = True)
