import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.
    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    color = "#E3256B"

    return start_response(color)

@bottle.post('/move')
def move():
    direction = ['up', 'down', 'left', 'right']
    data = bottle.request.json

    head = data['you']['body'][0]

    # ################## BODY CHECK ###################
    n = 0
    while(n <= len(data['you']['body'])-1):
        body = data['you']['body'][n]
        if body['y'] == head['y']:
            if body['x']-head['x'] == 1:
                direction.pop(direction.index('right'))
            elif body['x']-head['x'] == -1:
                direction.pop(direction.index('left'))
        elif body['x'] == head['x']:
            if body['y']-head['y'] == -1:
                direction.pop(direction.index('up'))
            elif body['y']-head['y'] == 1:
                direction.pop(direction.index('down'))
        n = n+1

    # ################## WALL CHECK ###################
    # If head is at top_wall don't go up
    if head['y'] == 0 and 'up' in direction:
        direction.pop(0)
    # If head is at bottom_wall don't go down
    if head['y'] == data['board']['width']-1 and 'down' in direction:
        direction.pop(direction.index('down'))
    # If head is at left_wall don't go left
    if head['x'] == 0 and 'left' in direction:
        direction.pop(direction.index('left'))
    # If head is at right_wall don't go right
    if head['x'] == data['board']['width']-1 and 'right' in direction:
        direction.pop(direction.index('right'))

    directions = random.choice(direction)
    return move_response(directions)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
