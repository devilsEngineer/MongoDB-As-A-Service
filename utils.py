import logging

def form_selection_fields(fields):
    selection_fields={}
    for key in fields:
        selection_fields[key]=1
    return selection_fields

def unique_list(source_list):
  return list(dict.fromkeys(source_list))

def convert2bool(value):
    if type(value)==str:
        value=value.lower()
        return True if value =="true" else False
    return value

def response_data(data,status):
    if status <=300:
        return {"data":data,
                "status":status}
    else:
        return {"error":data,
                "status":status}
def logger():
    LOGGER = logging.getLogger("mongodb")  
    # set log level
    LOGGER.setLevel(logging.INFO)
    # define file handler and set formatter
    file_handler = logging.FileHandler('./log/mongodb.log')
    formatter    = logging.Formatter('DateTime= %(asctime)s  LEVEL= %(levelname)s  Module= %(name)s  %(message)s')
    file_handler.setFormatter(formatter)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    # add file handler to logger
    LOGGER.addHandler(file_handler)
    # add console handler to logger
    LOGGER.addHandler(ch)
    return LOGGER