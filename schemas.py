from marshmallow import Schema, fields

class ChatGptRequestSchema(Schema):
    id = fields.Int(dump_only=True)
    request = fields.Str()

class PlainChatGptResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    response = fields.Str()

class ChatGptResponseSchema(PlainChatGptResponseSchema):
    request_id = fields.Int(required=True, load_only=True)
    request = fields.Nested(ChatGptRequestSchema(), dump_only=True)

class ChatGptResponseUpdateSchema(Schema):
    response = fields.Str()