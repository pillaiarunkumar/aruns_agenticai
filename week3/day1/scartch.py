# tags: list[str] = [1, "pydantic", "fastapi"]
# quantities: list[int] = [1, 5, 3, 2,"a"]
# word_counts: dict[str, int] = {"error": 12, "warning": 5}
# settings: dict[str, str] = {"theme": "dark", "language": "en"}

# print(tags, quantities, word_counts, settings)


# class FormData():
#     def __init__(self, name, email, message):
#         self.name = name
#         self.email = email
#         self.message = message


# mayankForm = FormData('mayank','abc@gmail.com','I am goi')


# print(mayankForm.name, mayankForm.email, mayankForm.message)

# from dataclasses import dataclass

# @dataclass
# class UserDataclass:
#     name: str
#     email: str
#     age: int

# from pydantic import BaseModel, ValidationError


# class SignupForm(BaseModel):
#     username: str
#     email: str
#     age: int
#     newsletter_opt_in: bool = False   # has a default -> OPTIONAL field


from pydantic import BaseModel, EmailStr, ValidationError,Field, computed_field, field_validator, model_validator

# # #user_pydantic = UserModel(name="Alice", email="alice@example.com", age="not a number")
# # incoming_data = {"username": "aditi28", "email": "aditi@example.com", "age": 28}
# # user_a = SignupForm(**incoming_data)
# # dump_data = user_a.model_dump()  # returns a dict
# # print(user_a.username, user_a.email, user_a.age, user_a.newsletter_opt_in)
# # print(dump_data)

# class person(BaseModel):
#     full_name: str=Field(min_length=1, max_length=50)
#     years_of_experience: Field(ge=0, le=50)
#     email: EmailStr

#     @field_validator("years_of_experience")
#     def check_years_of_experience(cls, value):
#         if value < 0:
#             raise ValueError("Years of experience must be a non-negative integer")
#         return value
    
# person_data = {"full_name": "John Doe", "years_of_experience": 10, "email": "john.1doeexample.com"}
# dump_data = person(**person_data).model_dump()  # returns a dict
# print(dump_data)

# class JobApplication(BaseModel):
#     full_name: str
#     email: str
#     years_experience: int
#     company: str = Field(default="Unknown", max_length=50)

#     @field_validator('email')
#     @classmethod
#     def reject_disposable_domains(cls,value:str)->str:
#       blocked_domain = {'yopmail.com'}
#       user_domain = value.split('@')[-1].lower()
#       if user_domain in blocked_domain:
#             raise ValueError(f"disposable email domains are not accepted ({user_domain})")
#       return value.lower()
    
#     @model_validator(mode='before')
#     @classmethod
#     def validate_application(cls, values):
#         if values['years_experience'] < 5 and values['company'] == "infy":
#             raise ValueError("Years of experience must be a non-negative integer")
#         return values

# ##validate_application = JobApplication(full_name="John Doe", email="test@yopmail.com", years_experie
# # nce=4, company="infy")
# validate_application = JobApplication(full_name="John Doe", email="test@mail.com", years_experience=6, company="infy")


# class SignupForm(BaseModel):
#     username: str
#     email: EmailStr
#     age: int
#     newsletter_opt_in: bool = False   # has a default -> OPTIONAL field
#     password: str = Field(min_length=8, max_length=20)

#     @field_validator('username')
#     @classmethod
#     def validate_username(cls, value: str) -> str:
#         if len(value) < 3:
#             raise ValueError("Username must be at least 3 characters long")
#         return value

#     @field_validator('password')
#     @classmethod
#     def validate_password(cls, value: str) -> str:
#         if len(value) < 8:
#             raise ValueError("Password must be at least 8 characters long")
#         return value
#     model_validat')


# class SignupForm(BaseModel):
#     username: str
#     password: str
#     confirm_password: str


#     @field_validator('password')
#     @classmethod
#     def reject_disposable_domains(cls,value:str)->str:
#       if len(value)<8:
#         raise ValidationError

#       return value.lower()



#     @model_validator(mode='after')
#     def passwords_must_match(self):
#         """
#         Cross-field rule: password and confirm_password must be
#         identical. This is IMPOSSIBLE to express with field_validator
#         alone, because a single field_validator only ever sees one
#         field's value — it has no visibility into any other field.
#         """
#         if self.password != self.confirm_password:
#             raise ValueError("password and confirm_password do not match")
#         return self

# signup_data = {"username": "aditi28", "password": "mypassword", "confirm_password": "mypassword"} 
# signup_form = SignupForm(**signup_data)
# signup_data = {"username": "aditi28", "password": "mypassword", "confirm_password": "mypassword1"} 
# signup_form = SignupForm(**signup_data)

# class SignupForm(BaseModel):
#    full_name: str
#    years_of_experience: int
#    @computed_field
#    @property
#    def is_senior(self) -> str:
#          if self.years_of_experience < 2:
#              return "junior"
#          else:
#              return "mid-level"
         
# user_data = {"full_name": "John Doe", "years_of_experience": 3}
# signup_form = SignupForm(**user_data)
# print(signup_form.full_name, signup_form.years_of_experience, signup_form.is_senior)


#Nested model

from pydantic import BaseModel, Field, EmailStr, ValidationError, model_validator,email_validator
from typing import List

class Address(BaseModel):
    street: str
    city: str
    postal_code: str = Field(..., min_length=3)

class User(BaseModel):
    name: str
    email: EmailStr
    age: int = Field(ge=0)
    address: Address
    previous_addresses: List[Address] = []

    @model_validator(mode="after")
    def check_age_and_address(cls, values):
        age = values.get("age")
        addr: Address = values.get("address")
        if age is not None and addr and age < 18 and addr.city == "Restricted":
            raise ValueError("Under-18 users cannot be from 'Restricted' city")
        return values

# Construct from nested dicts
data = {
    "name": "Alice",
    "email": "alice@example.com",
    "age": 25,
    "address": {"street": "1 Main St", "city": "Springfield", "postal_code": "12345"},
    "previous_addresses": [
        {"street": "2 Old Rd", "city": "Springfield", "postal_code": "54321"}
    ],
}

user = User(**data)
print(user.model_dump())