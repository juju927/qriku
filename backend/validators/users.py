
from marshmallow import Schema, fields, validate

# "This class defines the input schema for the CreateSignup mutation.
# The input schema is used to validate the input data before it is passed to the mutation
class CreateSignupInputSchema(Schema):
    # the 'required' argument ensures the field exists
    username = fields.Str(required=True, validate=validate.Length(min=4, max=25))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))
    is_performer = fields.Bool(required=True)

# The above class is a subclass of the Schema class from the marshmallow library. The Schema class is
# a class that validates dictionaries. The Schema class has a class attribute called fields which is a
# dictionary. The keys of the fields dictionary are the keys of the dictionary that the Schema class
# validates. The values of the fields dictionary are instances of the Field class from the marshmallow
# library. The Field class is a class that validates values
class CreateLoginInputSchema(Schema):
    # the 'required' argument ensures the field exists
    username = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=8))




