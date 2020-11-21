from marshmallow import Schema, fields

class InfoQR_Code_Schema(Schema):
    qr_nom = fields.String(dump_only=True)
    qr_date = fields.DateTime(dump_only=True)
    qr_sum = fields.Decimal(as_string=True, dump_only=True)
    qr_uid = fields.String(dump_only=True)
    qr_uid_client = fields.String(dump_only=True)

class User_Schemma(Schema):
    user_id = fields.Integer(dump_only=True)
    name = fields.String(dump_only=True)
    telephone = fields.String(dump_only=True)


class  QR_Schema(Schema):
    id = fields.String(dump_only=True)
    file_id = fields.String(dump_only=True)

    date = fields.DateTime(dump_only=True)

    file_size = fields.Integer(dump_only=True)
    file_path = fields.String(dump_only=True)
    mime_type = fields.String(dump_only=True)
    file_name = fields.String(dump_only=True)

    auto_determination = fields.Boolean(dump_only=True)
    user = fields.Nested(User_Schemma)
    info_qr_code = fields.Nested(InfoQR_Code_Schema)






