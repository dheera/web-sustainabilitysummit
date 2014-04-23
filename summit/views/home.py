from flask import Blueprint, render_template, abort, request
from jinja2 import TemplateNotFound
from pygeoip import GeoIP

import json

home = Blueprint('home', __name__,template_folder='../template')

@home.route('/')
def show():
  g = GeoIP('pygeoip/GeoIP.dat')
  user_country = g.country_code_by_addr(request.remote_addr);

  return render_template('home.html', user_country=user_country)
