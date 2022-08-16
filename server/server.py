import time

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def hello():
    return "Hello World!"