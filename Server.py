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
	
@route('/api/region/<region>/colourmap')
def api_colours(region):
	return region_to_colourmap(region)

@route('/api/region/<region>/population')   # Population of each region
def api_population_region(population):
	return parse_population_region(population)

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

def region_to_colourmap(region_name):
	region_obj = region_summary(region_name)
	region_map = []
	for sub in region_obj.suburbs:
		color = suburb_to_colour(sub)
		suburb_map = [{'Suburb': sub.name}, {'Price': sub.price}, {'Color': color}, {'Region_min': region_obj.min_price}, {'Region_max': region_obj.max_price}, {'Region_avg': region_obj.average}]
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
	next(region_file)	#Remove the first line
	for line in region_file:
		keys = line.split('",')

		print(keys)


		for k in range(len(keys)):
			keys[k] = keys[k].replace("\"", "")	#Remove quotes around string
			keys[k] = keys[k].replace("\n", "")
			keys[k] = keys[k].replace("$", "")
			keys[k] = keys[k].replace(",", "")

		print(keys)

		suburb_info = {'Suburb': keys[0], 'Number_of_Sales': keys[1],
        'Median_Sale_Price': keys[2], 'Difference_Between_Sales_Price_and_CV': keys[3],
        'Capital_Value_Date': keys[4]}
		suburb_list.append(suburb_info)
	region_file.close()
	return json.dumps(suburb_list)

def parse_population_region(population):
    pop_file = open(population)
    pop_list = []

    next(pop_file)  #Remove the first line

    for line in pop_file:
        keys = line.split('",')

        print (keys)

        district_info = {'District': keys[0], 'Population': keys[4]}

        pop_list.append(district_info)

    return json.dumps(pop_list)

run(host = 'localhost', port = 8080, debug = True)
