#!/usr/bin/env python

import requests
import turtle
import time

__author__ = 'ericmhanson'

indy_coord = {'lat': 39.7684, 'lon': -86.1581}


def get_astronauts():
    response = requests.get('http://api.open-notify.org/astros.json')
    response.raise_for_status()
    astro_dict = {}
    astronauts = response.json()['people']
    for name_obj in astronauts:
        astro_dict[name_obj['name']] = name_obj['craft']
    return astro_dict


def get_iss_location():
    response = requests.get('http://api.open-notify.org/iss-now.json')
    response.raise_for_status()
    location = response.json()['iss_position']
    longitude = float(location['longitude'])
    latitude = float(location['latitude'])
    timestamp = int(response.json()['timestamp'])
    return latitude, longitude, timestamp


def setup_turtle(lat, lon, pass_time):
    screen = turtle.Screen()
    screen.register_shape('iss.gif')
    screen.setup(width=720, height=360)
    screen.bgpic('map.gif')
    screen.setworldcoordinates(-180, -90, 180, 90)
    iss = turtle.Turtle()
    iss.shape('iss.gif')
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)
    indy_dot = turtle.Turtle()
    indy_dot.penup()
    indy_dot.color('yellow')
    indy_dot.goto(indy_coord['lon'], indy_coord['lat'])
    indy_dot.dot(10)
    next_time = turtle.Turtle()
    next_time.penup()
    next_time.goto(indy_coord['lon'], indy_coord['lat'])
    next_time.color('red')
    next_time.write(pass_time, align='left', font=('Arial', 15, 'normal'))
    screen.exitonclick()


def pass_indy():
    '''returns the next time that the ISS passes over Indianapolis'''
    url = 'http://api.open-notify.org/iss-pass.json'
    response = requests.get(url, params=indy_coord)
    response.raise_for_status()
    next_pass = response.json()['response']
    return time.ctime(next_pass[0]['risetime'])


def main():
    astro_dict = get_astronauts()
    print(f'There are currently {len(astro_dict)} astronauts in space!')
    for name in astro_dict:
        print(f'    {name} is on the {astro_dict[name]}')

    latitude, longitude, timestamp = get_iss_location()
    print(f'''Current ISS location is:
    Latitude = {latitude:.2f}, Longitude = {longitude:.2f}
    Timestamp = {timestamp}''')

    next_indy_pass = pass_indy()
    setup_turtle(latitude, longitude, next_indy_pass)


if __name__ == '__main__':
    main()
