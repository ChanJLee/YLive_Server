# coding=utf-8
import httplib


def cal_room_name(user):
    return "room_%d" % user.id


def create_chat_room(user):
    uri = ("/chat_room/?room_name=%s&room_title=%s" % (cal_room_name(user), user.username))
    connection = httplib.HTTPConnection("localhost", 8080)
    connection.request("POST", uri, None)
    response = connection.getresponse()
    return response.read()


def query_chat_room(user):
    uri = ("/chat_room/?room_name=%s" % cal_room_name(user))
    connection = httplib.HTTPConnection("localhost", 8080)
    connection.request("GET", uri, None)
    response = connection.getresponse()
    return response.read()
