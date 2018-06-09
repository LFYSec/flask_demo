# -*- coding:utf-8 -*- 

from flask import Flask
import os,sys
import views
import config

app = Flask(__name__)
app.config.from_object(config)

