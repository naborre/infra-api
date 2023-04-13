from marshmallow import Schema, fields

class ChatGptAnswerSchema(Schema):
    id = fields.Int(dump_only=True)
    answer = fields.Str()

class PlainChatGptResponseSchema(Schema):
    id = fields.Int(dump_only=True)
    response = fields.Str()

class ChatGptResponseSchema(PlainChatGptResponseSchema):
    answer_id = fields.Int(required=True, load_only=True)
    answer = fields.Nested(ChatGptAnswerSchema(), dump_only=True)