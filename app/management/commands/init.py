#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 下午4:38
# @Author  : tudoudou
# @File    : init.py
# @Software: PyCharm

import os
import subprocess
from app.models import Score,Status
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
['aaabbc','311F8A54SV9K6B5FF4EAB20535','311F8A54SV9K6B5FF4EAB20535']
            ]
            for i in user:
                Score(
                    player_num=i[0],
                    fraction=0,
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
