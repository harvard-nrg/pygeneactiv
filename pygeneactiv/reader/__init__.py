import pandas

class Reader(object):
    def __init__(self, f):
        self.f = f
        self.headers = dict()
        self.num_header_rows = 0
        self.sensor_type_str = 'Sensor type'
        self.num_sensor_rows = 4
        self.columns = ('datetime', 'x', 'y', 'z', 'lux', 'button', 'thermistor')
        self.get_header()

    def get_header(self):
        ''' read header blob '''
        # I defined a custom 'sep' argument here because I have encountered 
        # GENEActiv files where commas exist within the value field. Normally, 
        # this is not a problem, but in this case the files appear to enclose 
        # the value in parentheses. Because of this, there are two quote 
        # characters; the opening and closing parens. Unfortunately, the 
        # pandas.read_csv 'quotechar' argument only accepts a single quote 
        # character such as a single- or double-quote.
        reader = pandas.read_csv(self.f,
                                 chunksize=1,
                                 skip_blank_lines=False,
                                 sep=',+(?![^\(]*\))',
                                 engine='python',
                                 header=None)
        try:
            for i,row in enumerate(reader):
                self.num_header_rows += 1
                key,value = row.values[0]
                # skip blank rows
                if pandas.isnull(key) and pandas.isnull(value):
                    continue
                # special case if we encountered the start of a sensor
                if key == self.sensor_type_str:
                    if 'sensors' not in self.headers:
                        self.headers['sensors'] = list()
                    sensor,num_rows = self.__read_sensor(reader, value)
                    self.num_header_rows += num_rows
                    self.headers['sensors'].append(sensor)
                else:
                    self.headers[key] = value
        except ValueError: 
            # This exception is thrown by pandas when you hit a row that 
            # contains a different number of rows than the preceding rows. 
            # I'm using this as a signal that we have hit the end of the 
            # header. It's not a very robust assumption. I'm sure with a 
            # little more thought, there is a better way. This exception 
            # seems far too generic to be used for this purpose.
            return

    def __read_sensor(self, reader, sensor_type):
        ''' read sensor data rows '''
        sensor = {
            self.sensor_type_str: sensor_type
        }
        for i,row in enumerate(reader):
            key,value = row.values[0]
            sensor[key] = value
            if i == self.num_sensor_rows - 1:
                return sensor,self.num_sensor_rows - 1

    def get_data(self, chunksize=100, parsedates=False):
        ''' iterate over data in user-defined chunks i'''
        parser = None
        if parsedates:
            parser = lambda x: pandas.to_datetime(x, format='%Y-%m-%d %H:%M:%S:%f')
        df = pandas.read_csv(self.f, 
                             skiprows=self.num_header_rows,
                             parse_dates=['datetime'],
                             date_parser=parser,
                             chunksize=chunksize,
                             header=None,
                             names=self.columns)
        for chunk in df:
            yield chunk
