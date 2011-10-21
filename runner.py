import time

def generator():
    for value in xrange(1, 1000):
        time.sleep(1)
        parameters = (randint(0,4), randint(0,100),
            random()*100, random()*100, random()*100)
        reading = '{"player":%d, "hits":%d, "temperature":%f, "humidity":%f, "acceleration":%f}' % parameters
        yield reading

def app(environ, start_response):
    data = 'something'
    status = '200 OK'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Transfer-Encoding', 'chunked')
    ]
    start_response(status, response_headers)
    return generator()
