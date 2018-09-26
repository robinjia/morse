import flask
from flask import Flask
import yaml

DEFAULT_PORT = 9090
DEFAULT_VALUES = {'string': '', 'integer': 0, 'float': 0.0}
TYPE_FUNCTIONS = {'string': str, 'integer': int, 'float': float}
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

    @self.app.route('/post_query', methods=['post'])
    def post_query():
      inputs = self.prep_input_fields(True)
      input_dict = self.prep_input_dict()
      output_values = self.query_func(**input_dict)
      print(output_values)
      outputs = [(y, output_values[y['name']]) for y in self.config['outputs']]
      return flask.render_template('query.html', title=self.config['title'],
                                   inputs=inputs, outputs=outputs)

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
        value = TYPE_FUNCTIONS[x['type']](flask.request.form[x['name']].strip())
      elif 'default' in x:
        value = x['default']
      else:
        value = DEFAULT_VALUES[x['type']]
      inputs.append((x, value, new_row))
    return inputs

  def prep_input_dict(self):
    return {x['name']: flask.request.form[x['name']]
            for x in self.config['inputs']}

  def serve(self, port=None):
    if not port:
      port = DEFAULT_PORT
    self.app.run(port=port, debug=True)
