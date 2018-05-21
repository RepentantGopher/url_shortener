from marshmallow import Schema, fields


class IndexSchema(Schema):
    class Meta:
        strict = True

    url = fields.URL(required=True)
