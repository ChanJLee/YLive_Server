# coding=utf-8
import httplib
from operator import eq

from django.contrib.auth.models import User
from rest_framework import serializers

from AnchorModel.views import CATEGORY_MAP
from CategoryModel.models import CategoryModel
from RoomModel.models import RoomModel
from decor.decor import return_error, CODE_OK, return_message
from misc.base import JsonSerializer, create_response, DEFAULT_CHAR_LENGTH
from misc.xmpp import create_chat_room, query_chat_room
from ylive.settings import STATIC_FILE_SERVER_CONFIG


class Room:
    def __init__(self, id, title, snapshot, anchor, audience_count):
        self.id = id
        self.title = title
        self.snapshot = snapshot
        self.anchor = anchor
        self.audienceCount = audience_count
        pass


class RoomSerializer(serializers.Serializer):
    id = serializers.IntegerField(default=-1)
    title = serializers.CharField(max_length=DEFAULT_CHAR_LENGTH)
    snapshot = serializers.URLField()
    anchor = serializers.CharField(max_length=DEFAULT_CHAR_LENGTH)
    audienceCount = serializers.IntegerField(default=-1)


class RoomResponseSerializer(JsonSerializer):
    data = RoomSerializer(many=True)


'''
get
program/{id}/?page=1


{
    "code": 512,
    "message": "Ok",
    "data": [
        {
            "id": 4,
            "title": "开播啦",
            "snapshot": "http://192.168.1.102:8080/show/user12.jpg",
            "anchor": "",
            "audienceCount": 0
        }
    ]
}
'''


# 获取房间列表
def fetch_rooms(request, category):
    if not category or not CATEGORY_MAP[int(category)]:
        return return_error(u"类别有误")
    category = CategoryModel.objects.get(name=CATEGORY_MAP[int(category)])
    index = 0
    if 'page' in request.GET:
        index = int(request.GET['page'])
    rooms = RoomModel.objects.all()[index * 10: (index + 1) * 10]
    response = []
    for room in rooms:
        roomResponse = Room(room.id, room.title, room_snapshot(category.name, room.ownerId.user.username),
                            room.ownerId.user.last_name, room.count)
        response.append(RoomSerializer(roomResponse).data)
    return create_response(CODE_OK, u'Ok', response, RoomResponseSerializer)


def room_snapshot(category, username):
    if eq(category, u'音乐'):
        dir_name = 'music'
    elif eq(category, u'户外'):
        dir_name = 'sport'
    elif eq(category, u'星秀'):
        dir_name = 'show'
    elif eq(category, u'桌游'):
        dir_name = 'desktop_game'
    else:
        dir_name = 'pet'
    return "http://%s:%s/%s/%s.jpg" % (
        STATIC_FILE_SERVER_CONFIG['ip'], STATIC_FILE_SERVER_CONFIG['port'], dir_name, username)


'''
program/room/{room_id}/

put

{
    "code": 512,
    "message": "OK",
    "data": {
        "chat_room": "spark@reference.192.168.1.101",
        "title": "开播啦",
        "count": 14,
        "owner_name": "user12",
        "owner_id": 13
    }
}

delete
{
    "code": 512,
    "message": "退出房间成功",
    "data": null
}
'''


def watch_program(request, room_id, *args, **kwargs):
    try:
        if request.method == 'DELETE':
            return do_delete_watch_program(request, room_id, args, kwargs)
        elif request.method == 'PUT':
            return do_put_watch_program(request, room_id, args, kwargs)
        else:
            return return_error(u'仅支持delete和post')
    except Exception as e:
        return return_error(u'服务端异常')


def do_delete_watch_program(request, room_id, *args, **kwargs):
    id = int(room_id)
    room = RoomModel.objects.get(id=id)
    if room.count != 0:
        room.count -= 1
        room.save()
    return return_message(u'退出房间成功')


class Program:
    def __init__(self, chat_room, title, count, owner_name, owner_id):
        self.chat_room = chat_room
        self.title = title
        self.count = count
        self.owner_name = owner_name
        self.owner_id = owner_id


class ProgramSerializer(serializers.Serializer):
    chat_room = serializers.EmailField(required=True)
    title = serializers.CharField(max_length=DEFAULT_CHAR_LENGTH)
    count = serializers.IntegerField(default=0)
    owner_name = serializers.CharField(max_length=DEFAULT_CHAR_LENGTH)
    owner_id = serializers.IntegerField(default=-1)


class ProgramResponseSerializer(JsonSerializer):
    data = ProgramSerializer()


def do_put_watch_program(request, room_id, *args, **kwargs):
    id = int(room_id)
    room = RoomModel.objects.get(id=id)
    room.count += 1
    room.save()

    owner = room.ownerId.user
    try:
        jid = query_chat_room(owner)
        if not jid:
            return return_error(u"连接弹幕服务器失败")
        program = Program(chat_room=jid, title=room.title, count=room.count, owner_id=room.ownerId.id,
                          owner_name=room.ownerId.user.username)
        return create_response(CODE_OK, u"OK", ProgramSerializer(program).data, ProgramResponseSerializer)
    except Exception as e:
        print e.message
        return return_error(u"连接弹幕服务器失败")


def init_chat_room(request):
    for user in User.objects.all():
        try:
            create_chat_room(user)
        except Exception as e:
            print e.message
            return_error(u"failed")
    return return_message(u"ok")