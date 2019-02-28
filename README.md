pygeneactiv
===========
[![Build Status](https://travis-ci.org/harvard-nrg/pygeneactiv.svg?branch=master)](https://travis-ci.org/harvard-nrg/pygeneactiv)

pygeneactiv is a python package for reading [GENEActiv](https://www.activinsights.com/products/geneactiv/) 
watch data. Here's a simple example

```python
import json
import pygeneactiv

# read a GENEActiv dataset
ds = pygeneactiv.read(filename)

# print file headers (using json.dumps only to nicely print a dict)
print(json.dumps(ds.headers, indent=2))

# process data in chunks
for chunk in ds.get_data(chunksize=1000):
  print(chunk.shape) # (1000, 7)
```

> Note that every row of the GENEActiv files contains a timestamp. You can 
> instruct `ds.get_data` to automatically parse these dates into `Timestamp` 
> objects by passing `parsedates=True`, but this will significantly slow down 
> reading. If you really don't need every date parsed, don't pass this.

At the moment, only the full CSV exported files are supported.

# Installation
Just use `pip`

```bash
pip install pygeneactiv 
```

