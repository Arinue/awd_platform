#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 下午4:38
# @Author  : tudoudou
# @File    : init.py
# @Software: PyCharm

import os
import subprocess
from app.models import Score,Status,Flags
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def add_arguments(self, parser):

        parser.add_argument(
            '-n',
            '--name',
            action='store',
            dest='name',
            default='ddd',
            help='name of author.',
        )

    def handle(self, *args, **options):
        try:
            os.system('python3 manage.py makemigrations')
            os.system('python3 manage.py migrate')
            user=[
                ['123456','FF9C92C7SDFABB71566F73422C','FF9C92C7SDFABB71566F73422C'],
                ['aaabbb','311F8A54SV9K6B5FF4EAB20536','311F8A54SV9K6B5FF4EAB20536'],
['cccccc','311F8A54SV9K6B5FF4EAB20537','311F8A54SV9K6B5FF4EAB20537'],
['法福建阿阿飞','福建拉福建拉','1111111111111111111111'],
['的身份离开','福建拉福建拉1','1111111111111111111111'],
['咸蛋超人','福建拉福建拉2','1111111111111111111111'],
['撒打发a撒打发是否','福建拉a福建拉3','1111111111111111111111'],
['撒打发f撒打发是否','福建拉f福建拉3','1111111111111111111111'],
['撒打发g撒打发是否','福建拉福s建拉3','1111111111111111111111'],
['撒打发h撒打发是否','福建as拉福建拉3','1111111111111111111111'],
['撒打发j撒打发是否','福建拉福a建拉3','1111111111111111111111'],
['撒打发k撒打发是否','福建拉s福f建拉3','1111111111111111111111'],
['撒打发n撒打发是否','福建a拉福a建拉3','1111111111111111111111'],
['撒打发b撒打发是否','福建拉福fa建拉3','1111111111111111111111'],
['撒打发 v撒打发是否','福建拉福a建拉3','1111111111111111111111'],
['撒打发 b撒打发是否','福建拉f福f建拉3','1111111111111111111111'],
['撒打发撒c打发是否','福建拉s福建拉3','1111111111111111111111'],
['撒打发撒x打发是否','福建拉a福f建拉3','1111111111111111111111'],
['撒打发xa撒打发是否','福建拉a福a建拉3','1111111111111111111111'],
['撒打发a撒打发是否','福建拉f福建拉3','1111111111111111111111'],
['aaabbc','311F8A54SV9K6B5FF4EAB20535','311F8A54SV9K6B5FF4EAB20535']
            ]
            for i in user:
                Score(
                    player_num=i[0],
                    fraction=1000,
                    flag_num=i[1]
                ).save()
                Status(
                    target_num=i[2],
                    player_num=i[0],
                    run=1
                ).save()
            self.stdout.write(self.style.SUCCESS('初始化成功，请尽情使用吧 (～o￣▽￣)～o ~。。。'))
        except Exception:
            self.stdout.write(self.style.ERROR('命令执行出错'))
