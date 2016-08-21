import json
import sys
from bottle import route, run, static_file, get, post, request, redirect, os

pos_inf = 999999999

class suburb(object):
	def _init_(self,name,price,region):
		self.name = name
		self.price = price
		self.region = region
		
class region(object):
	def _init_(self,name = 'region', suburbs = None):
		self.name = name
		self.suburbs = suburbs
		self.average = 0
		self.max_price = 0
		self.min_price = pos_inf


@route('/')
def route_to_index():
	redirect('static/index.html')

@route('/api/regions')
def api_regions():
	return list_all_regions()

@route('/api/region/<region>')
def api_region(region):
	return parse_region(region)
	
@route('/api/region/<region>/colourmap.json')
def api_colours(region):
	return region_to_colourmap(region)

"""""
@route('/api/region/<region>/population')   # Population of each region
def api_population_region(region):
	return parse_population_region(region)
"""
@route('/static/<filename:path>')
def server_static(filename):
    return static_file(filename, root = 'static\\')

def get_region_minmax(region_obj):
	assert region_obj.suburbs != None
	min_price = pos_inf
	max_price = 0
	for sub in region_obj.suburbs:
		if sub.price < min_price:
			min_price = sub.price
		elif sub.price > max_price:
			max_price = sub.price
	return [int(min_price), int(max_price)]

def get_region_avg(region_obj):
	assert region_obj.suburbs != None
	if len(region_obj.suburbs) == 0:
		return -1
	avg = pos_inf
	for i in range(len(region_obj.suburbs)):
		avg += region_obj.suburbs[i].price
	avg = avg/len(region_obj.suburbs)
	return int(avg)

def region_summary(region_name):
	suburb_json = json.loads(parse_region(region_name))
	region_obj = region()
	region_obj._init_(region_name, None)
	region_obj.suburbs = [len(suburb_json)]
	suburb_list = []
	name_indx = -1
	price_indx = -1
	for categ in suburb_json:
		suburb_obj = suburb()
		suburb_obj._init_(None, None, None)
		suburb_obj.name = categ.get("Suburb")
		suburb_obj.price = categ.get("Median_Sale_Price")
		suburb_obj.region = region_obj
		if suburb_obj.name != None and suburb_obj.price != None:
			suburb_obj.price = int(suburb_obj.price)
			suburb_list.append(suburb_obj)
	
	region_obj.suburbs = suburb_list
	region_obj.average = get_region_avg(region_obj)
	rminmax = get_region_minmax(region_obj)
	region_obj.min_price = rminmax[0]
	region_obj.max_price = rminmax[1]
	return region_obj
	
def get_sub_latlon(suburb_obj):
	latlon_json = open('Population/SuburbsLatlon.json')
	latlon_data = json.loads(latlon_json.read())
	latlon_json.close()
	suburb_latlon = None
	suburb_name = None
	for categ in latlon_data:
		suburb_name = categ.get('name')
		if suburb_obj.name == suburb_name:
			print(suburb_name + ", " + suburb_obj.name)
			suburb_latlon = categ.get('center')
			lat = suburb_latlon.get('lat')
			lon = suburb_latlon.get('lng')
			print(suburb_latlon)
	return suburb_latlon

def region_to_colourmap(region_name):
	region_obj = region_summary(region_name)
	region_map = []
	for sub in region_obj.suburbs:
		get_sub_latlon(sub)
		color = suburb_to_colour(sub)
		print(sub.name)
		center = get_sub_latlon(sub)
		print(center)
		suburb_map = {'Suburb': sub.name, 'center': center, 'Price': sub.price, 'Color': color, 'Region_min': region_obj.min_price, 'Region_max': region_obj.max_price, 'Region_avg': region_obj.average}
		region_map.append(suburb_map)
	return json.dumps(region_map)
	
def suburb_to_colour(suburb_obj):
	col_modifier = 255 * ((suburb_obj.price - suburb_obj.region.min_price) / (suburb_obj.region.max_price - suburb_obj.region.min_price))
	red = col_modifier
	blue_modifier = red / 100
	blue = abs(255 - col_modifier * blue_modifier)
	if blue > 255:
		blue -= 255
	if red < blue:
		green = blue - red
	else:
		green = blue
	return str(int(red)) + "," + str(int(green)) + "," + str(int(blue))


def list_all_regions():
    regions = os.listdir("PropertyCVSData")

    for i in range(len(regions)):
        regions[i] = regions[i][:-4]

    return json.dumps(regions)


def parse_region(region):
    region_file = open("PropertyCVSData/" + region + ".csv")
    suburb_list = []

    pop_file = open("DistrictPopulation/DistrictPop.csv")
    pop_list = []

    next(pop_file)

    for line in pop_file:
        keys = line.split('",')
        for k in range(len(keys)):
            keys[k] = keys[k].replace("\"", "")
            keys[k] = keys[k].replace(',', "")

        suburb_pop = {'Suburb': keys[0], 'Population': keys[4]}
        pop_list.append(suburb_pop)

    next(region_file)
    for line in region_file:
        keys = line.split('",')

        for k in range(len(keys)):
            keys[k] = keys[k].replace("\"", "")	# Remove unnecessary info
            keys[k] = keys[k].replace("\n", "")
            keys[k] = keys[k].replace("$", "")
            keys[k] = keys[k].replace(",", "")


        suburb_info = {'Suburb': keys[0], 'Number of Sales': keys[1],
        'Median Sale Price': keys[2], 'Difference Between Sales Price and CV': keys[3],
        'Capital Value Date': keys[4], 'Population': -1}
        suburb_list.append(suburb_info)

    for sub_dict in suburb_list:
        for pop_dict in pop_list:
            #if sub_dict['Population'].find()
             #if sub_dict['Suburb'] in pop_dict:
            #for pop_dict_key in pop_dict:
            if pop_dict['Suburb'] == sub_dict['Suburb']:

                #if pop_dict_key.find(sub_dict['Suburb']) != 1 or sub_dict['Suburb'].find(pop_dict_key) != 1:
                sub_dict['Population'] = pop_dict['Population']
                sub_dict['Population'] = sub_dict['Population'].replace("\n", "")

    region_file.close()
    return json.dumps(suburb_list)

run(host = 'localhost', port = 8080, debug = True)
