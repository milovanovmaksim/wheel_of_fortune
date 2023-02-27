from marshmallow import Schema, fields


class OkResponseSchema(Schema):
    status = fields.Str(dump_default='ok')
    data = fields.Dict()

    class Meta:
        ordered = True
