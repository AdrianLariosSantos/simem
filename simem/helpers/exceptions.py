from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException




class BadRequest(APIException):
    #Error de analisis o ParseError
    status_code = 400
    default_code = 'peticion mala'
    default_detail = 'data'
    message="Ha ocurrido un error, valida los campos"

    def __init__(self, detail=None, code=None):
        if detail is not None:
            self.detail = {
                'error':self.default_code,
                'message': self.message,
                'detail': detail,
                'code':self.status_code
                }
                
        else:
            self.detail={ 'detail': 'Validar algunos campos pero no se especificaron cuales'}

class Unauthorized(APIException):
    status_code = 401
    default_code = 'Autenticacion fallida'
    message="No tiene las credenciales válidas de autenticación para acceder al recurso"

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = {
                'error':self.default_code,
                'message': self.message,
                'detail': detail,
                'code':self.status_code
                }           
        else:
            self.detail={ 'detail': self.message }

class PermissionDenied(APIException):
    status_code = 403
    default_code = 'Acceso denegado'
    message="El acceso esta prohibido"

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = {
                'error':self.default_code,
                'message': self.message,
                'detail': detail,
                'code':self.status_code
                }           
        else:
            self.detail={ 'detail': self.message }

class NotFound(APIException):
    status_code = 404
    default_code = 'No encontrado'
    message="Ha ocurrido un error, el objeto no existe"

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = {
                'error':self.default_code,
                'message': self.message,
                'detail': detail,
                'code':self.status_code
                }
                
        else:
            self.detail={ 'detail': self.message }

class MethodNotAllowed(APIException):
    status_code = 405
    default_code = 'Metodo no permitido'
    message="El servidor no conoce el metodo de solicitud"

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = {
                'error':self.default_code,
                'message': self.message,
                'detail': detail,
                'code':self.status_code
                }
                
        else:
            self.detail={ 'detail': self.message }
class InternalError(APIException):
    status_code = 500
    default_code = 'Error servidor'
    message="Ha ocurrido un error inesperado al procesar la petición"

    def __init__(self, detail=None, code=None):
        if detail is None:
            self.detail = {
                'error':self.default_code,
                'message': self.message,
                'detail': detail,
                'code':self.status_code
                }           
        else:
            self.detail={ 'detail': self.message }