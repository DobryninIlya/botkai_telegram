import json

map = []
for y in range(10):
    line = []
    for x in range(10):
        line.append(['⬜', json.dumps({'button': 'game_map', 'x': x, 'y': y})])
    map.append(line)