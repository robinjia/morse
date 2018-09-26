# Morse
A webapp for inspecting model predictions.

## Usage
First, write a YAML configuration file that may contain the following fields:

```
title: My Morse App
inputs:
  - name: x1
    display: First input
    type: string
    bootstrap-cols: 9
  - name: x2
    display: Second input
    type: integer
    bootstrap-cols: 3
    default: 1
    min: 1
    max: 100
outputs:
  - name: y1
    display: First output
    type: string
    bootstrap-cols: 12
  - name: y2
    display: Second output
    type: float
    bootstrap-cols: 12
```

Now write some code to get predictions out of your model and start the server: 

```python
from morse import Morse

def query_model(x1, x2):
  # Some code here to generate model predictions
  # Return a dict containing all predictions
  y1, y2 = my_model.predict(x1, x2) 
  return {'y1': y1, 'y2': y2}

app = morse.Morse(query_model, 'path/to/config.yaml')
app.serve()
```

See the `examples` directory for more information.
