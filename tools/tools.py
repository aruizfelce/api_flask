from datetime import datetime,timedelta,date

class Tools:
    @staticmethod
    def convertir_json_sql(query):
        obj={}
        for c in query.__table__.columns:
            data_conv= "" if getattr(query, c.name) is None else getattr(query, c.name)
            obj[c.name] =   str(data_conv) if isinstance(data_conv, datetime) or isinstance(data_conv, date) else data_conv

        return obj