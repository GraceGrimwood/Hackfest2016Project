import json
from bottle import route, run, static_file, get, post, request, redirect, os

class suburb(object):
	def _init_(self,name,price,region):
		self.name = name
		self.price = price
		self.region = region
		
class region(object):
	def _init_(self,name,suburbs):
		self.name = name
		self.suburbs = suburbs
		self.minprice = int(float('inf'))
		self.maxprice = 0

@route('/')
def route_to_index():
	redirect('static/index.html')

@route('/api/regions')
def api_regions():
	return list_all_regions()

@route('/api/region/<region>')
def api_region(region):
	return parse_region(region)

@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root = 'static\\')

#def region_to_colourmap(region):
	
	
def suburb_to_colour(suburb):
    col_modifier = 255 * (suburb.price - min_price) / (max_price - min_price)
    red = 0 + col_modifier
    blue_modifier = red / 100
    blue = abs(255 - col_modifier * blue_modifier)
    green = red < blue ? blue - red : blue
    return red + "," + green + "," + blue


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
