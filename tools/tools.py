from datetime import datetime,date
#from flask import abort
from flask_restful import abort
class Tools:
    @staticmethod
    def convertir_json_sql(query):
        obj={}
        for c in query.__table__.columns:
            data_conv= "" if getattr(query, c.name) is None else getattr(query, c.name)
            obj[c.name] =   str(data_conv) if isinstance(data_conv, datetime) or isinstance(data_conv, date) else data_conv

        return obj
    
    @staticmethod
    def convertir_json_sql_list(query):
        obj=[]
        for item in query:
            obj.append(Tools.convertir_json_sql(item))
        return obj
    
    @staticmethod
    def abort_if_doesnt_exist(model,item_id, json=True):
        item = model.query.get(item_id)
        if item is None:
            #abort(400, "El id {} no existe".format(item_id))
            abort(400, status="error", mensaje="El id {} no existe".format(item_id), data=None)
        if json:
            return Tools.convertir_json_sql(item)
        return item