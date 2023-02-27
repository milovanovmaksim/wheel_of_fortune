from marshmallow import Schema, fields

from app.web.schemes import OkResponseSchema


class AdminLoginRequestSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True, load_only=True)

    class Meta:
        ordered = True


class AdminSchema(AdminLoginRequestSchema):
    id = fields.Integer(dump_only=True, required=False)


class AdminResponseSchema(OkResponseSchema):
    data = fields.Nested(AdminSchema, only=("id", "email"))
