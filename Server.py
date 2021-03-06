import json
import sys
from bottle import route, run, static_file, get, post, request, redirect, os

pos_inf = 999999999

class suburb(object):
	def _init_(self,name,price,region,pop):
		self.name = name
		self.price = price
		self.region = region
		self.pop = pop
		
class region(object):
	def _init_(self,name = 'region', suburbs = None, nation = None):
		self.name = name
		self.suburbs = suburbs
		self.average = 0
		self.max_price = 0
		self.min_price = pos_inf
		self.nation = nation

class nation(object):
	def _init_(self, name = 'nation', regions = None, avg = -1):
		self.name = name
		self.regions = regions
		self.avg = avg
		self.min_price = pos_inf
		self.max_price = 0

@route('/')
def route_to_index():
	redirect('static/index.html')

@route('/api/regions')
def api_regions():
	return list_all_regions()

@route('/api/region/<region>')
def api_region(region):
	return parse_region(region)

@route('/api/regions/colourmap.json')
def api_nat_colours():
	return create_national_colourmap()

@route('/api/region/<region>/colourmap.json')
def api_colours(region):
	return json_region_colourmap(region)

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

def region_summary(region_name, nat):
	suburb_json = json.loads(parse_region(region_name))
	region_obj = region()
	region_obj._init_(region_name, None, nat)
	nat.regions.append(region_obj)
	region_obj.suburbs = [len(suburb_json)]
	suburb_list = []
	name_indx = -1
	price_indx = -1
	for categ in suburb_json:
		suburb_obj = suburb()
		suburb_obj._init_(None, None, None, None)
		suburb_obj.name = categ.get("Suburb")
		suburb_obj.price = categ.get("Median_Sale_Price")
		suburb_obj.region = region_obj
		suburb_obj.pop = categ.get("Population")
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
			suburb_latlon = categ.get('center')
			lat = suburb_latlon.get('lat')
			lon = suburb_latlon.get('lng')
	return suburb_latlon

def create_national_colourmap():
	nation_obj = nation()
	nation_obj._init_('New Zealand', [], -1)
	regions = json.loads(list_all_regions())
	regionmap = []
	avg = 0
	for reg in regions:
		regionmap.append(region_to_colourmap(reg,nation_obj))
	for reg in nation_obj.regions:
		avg += reg.average
		if nation_obj.min_price > reg.min_price:
			nation_obj.min_price = reg.min_price
		if nation_obj.max_price < reg.max_price:
			nation_obj.max_price = reg.max_price
	avg = avg/len(nation_obj.regions)
	for reg in range(len(nation_obj.regions)):
		for sub in range(len(nation_obj.regions[reg].suburbs)):
			regionmap[reg][sub]['Color'] = suburb_to_relative_colour(nation_obj.regions[reg].suburbs[sub])
	return json.dumps(regionmap)

def region_to_colourmap(region_name, nat):
	region_obj = region_summary(region_name, nat)
	region_map = []
	for sub in region_obj.suburbs:
		get_sub_latlon(sub)
		color = suburb_to_colour(sub)
		center = get_sub_latlon(sub)
		suburb_map = {'Suburb': sub.name, 'center': center, 'Price': sub.price, 'Color': color, 'Region_min': region_obj.min_price, 'Region_max': region_obj.max_price, 'Region_avg': region_obj.average, 'Population': sub.pop}
		region_map.append(suburb_map)
	return region_map
	
def json_region_colourmap(region_name):
	return json.dumps(region_to_colourmap(region_name))

def suburb_to_relative_colour(suburb_obj):
	col_modifier = 255 * ((suburb_obj.price - suburb_obj.region.nation.min_price) / (suburb_obj.region.max_price - suburb_obj.region.min_price))
	red = col_modifier
	while red > 255 or red < 0:
		if red > 255:
			red -= 255
		elif red < 0:
			red += 255
	blue_modifier = red / 100
	blue = abs(255 - col_modifier * blue_modifier)
	while blue > 255 or blue < 0:
		if blue > 255:
			blue -= 255
		elif blue < 0:
			blue += 255
	if red < blue:
		green = blue - red
	else:
		green = blue
	
	rgb = (int(red), int(green), int(blue))
	return '#%02x%02x%02x' % rgb;

def suburb_to_colour(suburb_obj):
	col_modifier = 255 * ((suburb_obj.price - suburb_obj.region.min_price) / (suburb_obj.region.max_price - suburb_obj.region.min_price))
	red = col_modifier
	while red > 255 or red < 0:
		if red > 255:
			red -= 255
		elif red < 0:
			red += 255
	blue_modifier = red / 100
	blue = abs(255 - col_modifier * blue_modifier)
	while blue > 255 or blue < 0:
		if blue > 255:
			blue -= 255
		elif blue < 0:
			blue += 255
	if red < blue:
		green = blue - red
	else:
		green = blue
	
	rgb = (int(red), int(green), int(blue))
	return '#%02x%02x%02x' % rgb


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

		suburb_info = {'Suburb': keys[0], 'Number_of_Sales': keys[1],
		'Median_Sale_Price': keys[2], 'Difference_Between_Sales_Price_and_CV': keys[3],
		'Capital_Value_Date': keys[4], 'Population': -1}
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
	pop_file.close()
	return json.dumps(suburb_list)

run(host = 'localhost', port = 8080, debug = True)
