# coding=utf-8
from django.http import JsonResponse
from rest_framework import serializers


class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day


# 验证器
def month_validator(month):
    if month < 0:
        raise serializers.ValidationError('month must be lager than 0')


class DateSerializers(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField(validators=[month_validator])
    day = serializers.IntegerField(required=False)

    def create(self, validated_data):
        return Date(**validated_data)

    # 为了局部更新
    def update(self, instance, validated_data):
        instance.year = validated_data.get('year', instance.year)
        instance.month = validated_data.get('month', instance.month)
        instance.day = validated_data.get('day', instance.day)
        return instance

    # 域级别验证
    def validate_year(self, year):
        if year < 1970:
            raise serializers.ValidationError('year must be after 1970')
        return year

    # 对象级别验证
    def validate(self, thiz):
        if thiz['day'] <= 0:
            raise serializers.ValidationError('day must be lager than 0')
        return thiz


class Comment:
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data


class CommentSerializers(serializers.Serializer):
    data = DateSerializers(required=False)
    code = serializers.IntegerField()
    message = serializers.CharField(max_length=20)


class Record:
    def __init__(self, comments):
        self.comments = comments


class RecordSerializers(serializers.Serializer):
    comments = CommentSerializers(many=True)


class Message:
    def __init__(self, src):
        self.src = src


class MessageSerializer(serializers.Serializer):
    src = serializers.URLField()


class Base:
    def __init__(self, code, message, data):
        self.code = code
        self.message = message
        self.data = data


class BaseSerializer(serializers.Serializer):
    code = serializers.IntegerField()
    message = serializers.CharField(max_length=20)


class MessageResponseSerializer(BaseSerializer):
    data = MessageSerializer(required=False)


def json_func(request):
    return test_base()


def test_base():
    msg = Message("http://localhost:8080")
    serializer = MessageSerializer(msg)
    base = Base(10, 'ok', serializer.data)
    return JsonResponse(data=MessageResponseSerializer(base).data, safe=False)


def test_response():
    msg = Message("http://localhost:8080")
    serializer = MessageSerializer(msg)
    response = Base(200, u'ok', serializer.data)
    return JsonResponse(data=BaseSerializer(response).data, safe=False)


def test_link():
    msg = Message("http://localhost:8080")
    serializer = MessageSerializer(msg)
    return JsonResponse(data=serializer.data, safe=False)


def nest_object():
    date = Date(year=1970, month=1, day=1)
    daySerializers = DateSerializers(date)
    comment = Comment(200, u'Ok', daySerializers.data)
    commentSerializers = CommentSerializers(comment)
    list = [commentSerializers.data]
    record = Record(list)
    recordSerializers = RecordSerializers(record)
    return JsonResponse(data=recordSerializers.data, safe=False)


def deserializers():
    # {"comments": [{"data": {"year": 1970, "month": 1, "day": 1}, "code": 200, "message": "Ok"}]}
    date = Date(year=1970, month=1, day=1)
    daySerializers = DateSerializers(date)
    comment = Comment(200, u'Ok', daySerializers.data)
    commentSerializers = CommentSerializers(comment)
    list = [commentSerializers.data]
    record = Record(list)
    recordSerializers = RecordSerializers(record)
    temp = RecordSerializers(data=recordSerializers.data)
    temp.is_valid()
    print temp.data['comments'][0]['data']['year']


def normal():
    day = Date(year=1970, month=1, day=1)
    serializer = DateSerializers(day)
    return JsonResponse(data=serializer.data, safe=False)


# 检查合法性
def check_valid():
    serializer = DateSerializers(data={"year": 1970, "month": 1, "day": 1})
    serializer.is_valid()
    print serializer.errors


# 局部更新
def partial_update():
    day = Date(year=1970, month=12, day=1)
    # 我并不能更新
    serializer = DateSerializers(day, data={"day": 10}, partial=True)
    serializer.is_valid()
    serializer.update(day, {"day": 10})
    print serializer.errors
    return JsonResponse(data=serializer.data, safe=False)
