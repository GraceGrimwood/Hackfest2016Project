from bottle import route, run, static_file, get, post, request

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root = 'static\\')
	
run(host = 'localhost', port = 8080, debug = True)