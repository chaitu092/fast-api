    # @field_validator("age", mode="before")
    # @classmethod
    # def validate_age(cls, value):
    #     """
    #     Validate the age field to check if the value is between 0 and 140.
    #     before validation: 30 means
    #     before says before type conversion
    #     it will take only int and if it is a string in the data
    #     it will throw an error
    #     """

    #     if 0 < value < 140:
    #         return value
    #     else:
    #         raise ValueError("Age must be between 0 and 140")
