def error(default_errors):
    new_error = {}
    for field_name, field_errors in default_errors.items():
        new_error[field_name] = field_errors[0]
        return new_error