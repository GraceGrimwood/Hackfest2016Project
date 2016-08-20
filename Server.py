from bottle import route, run, static_file, get, post, request, redirect

@route('/')
def route_to_index():
	redirect('static/index.html')

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root = 'static\\')

	
run(host = 'localhost', port = 8080, debug = True)