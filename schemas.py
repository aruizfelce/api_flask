from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, fields
from marshmallow import fields, ValidationError,validate
from models import StoreModel, ItemModel


class mensajeError:
     def handle_error(self, error, data, **kwargs):
        #recorro los errores y reemplazo el mensaje "Unknown field." por "Campo desconocido"
        for key, value in error.messages.items():
            if value[0] == "Unknown field.":
                error.messages[key][0] = "Campo desconocido"
        raise ValidationError(error.messages)
     
class ItemSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ItemModel


class StoreSchema(SQLAlchemyAutoSchema):
    #name = fields.String(required=True, error_messages={"required": "El nombre es requerido"})
    name = fields.String(required=True, error_messages={"required": "El nombre es requerido"},
                validate=[
                    validate.Length(
                        5, 15, error="El nombre debe tener entre 5 y 15 caracteres"
                    ),
                    validate.has_digit(error="El nombre debe contener un número"),
                ],
            )
    class Meta:
        model = StoreModel
    
    items = fields.Nested(ItemSchema, many=True)

    def handle_error(self, error, data, **kwargs):
        for key, value in error.messages.items():
            if value[0] == "Unknown field.":
                error.messages[key][0] = "Campo desconocido"
        raise ValidationError(error.messages)
    


class Store2Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = StoreModel
        exclude = ("id",)


