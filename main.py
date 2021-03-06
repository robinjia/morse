import flask
from flask import Flask
import yaml

DEFAULT_PORT = 9090
DEFAULT_VALUES = {'string': '', 'textarea': '', 'integer': 0, 'float': 0.0}
TYPE_FUNCTIONS = {'string': lambda x: x, 'textarea': lambda x: x, 'integer': int, 'float': float}
BOOTSTRAP_MAX_COLS = 12

class Morse(object):
  def __init__(self, query_func, config_filename):
    self.query_func = query_func
    self.config_filename = config_filename
    with open(config_filename) as f:
      self.config = yaml.load(f)
    self.app = Flask(__name__)
    self.app.debug = True
    self.app.env = 'development'

    @self.app.route('/')
    def index():
      inputs = self.prep_input_fields(False)
      return flask.render_template('index.html', title=self.config['title'],
                                   inputs=inputs)

    @self.app.route('/query', methods=['post'])
    def query():
      inputs = self.prep_input_fields(True)
      input_dict = self.prep_input_dict()
      output_values = self.query_func(**input_dict)
      return flask.render_template(
          'query.html', title=self.config['title'], inputs=inputs,
          output_config=self.config['outputs'], output_values=output_values)

    @self.app.route('/raw', methods=['post'])
    def query_raw():
      print(flask.request.data)
      input_dict = flask.request.get_json()
      output_values = self.query_func(**input_dict)
      return flask.jsonify(output_values)

  def prep_input_fields(self, use_request):
    cur_cols = 0
    inputs = []
    for x in self.config['inputs']:
      cur_cols += x['bootstrap-cols']
      if cur_cols > BOOTSTRAP_MAX_COLS:
        new_row = True
        cur_cols = x['bootstrap-cols']
      else:
        new_row = False
      if use_request:
        value = self.get_value(x)
      elif 'default' in x:
        value = x['default']
      else:
        value = DEFAULT_VALUES[x['type']]
      inputs.append((x, value, new_row))
    return inputs

  def prep_input_dict(self):
    return {x['name']: self.get_value(x)
            for x in self.config['inputs']}

  def get_value(self, x_config):
    return TYPE_FUNCTIONS[x_config['type']](
        flask.request.form[x_config['name']].strip())

  def serve(self, port=None, debug=False):
    if not port:
      port = DEFAULT_PORT
    self.app.run('0.0.0.0', port=port, debug=debug)
