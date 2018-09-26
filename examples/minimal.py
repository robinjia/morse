"""Minimal morse example.""" 
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from morse import Morse

CONFIG_FILENAME = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               'minimal.yaml')

def main():
  port = int(sys.argv[1]) if len(sys.argv) > 1 else None
  def query_model(x):
    return {'y': x}
  app = Morse(query_model, CONFIG_FILENAME)
  app.serve(port=port)

if __name__ == '__main__':
  main()
