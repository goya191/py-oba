from bottle import route, run

import json
import datetime
import main 
import formatters

# def route_info_to_html(route_info, title):
# 	ret_str = '''
# 	Routes in {title}\n
# 	{sep}\n
# 	'''.format(title=title, sep="*" * 80)
# 	for time in route_info:
# 		ret_str +=time.isoformat
# 	return ret_str


@route('/36')
def route_36():
	route_info = main.get_bus()
	res = formatters.fmt_py_dt_list(route_info, title="Route 36").replace('\n', '<br>')
	return res

@route('/link')
def link():
	route_info = main.get_link()
	res = formatters.fmt_py_dt_list(route_info, title="Link").replace('\n', '<br>')
	return res

@route('/')
def do_all():
	res = ''
	now = datetime.datetime.now()
	res += formatters.fmt_py_dt_list([now], "Current time").replace('\n', '<br>')

	bus_rounte_info = main.get_bus()
	res += formatters.fmt_py_dt_list(bus_rounte_info, title="Route 36").replace('\n', '<br>')
	link_route_info = main.get_link()
	res += formatters.fmt_py_dt_list(link_route_info, title="LINK light rail").replace('\n', '<br>')
	return res

run(host='localhost', port=8080, debug=True)