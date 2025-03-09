import logging

# Configuración del logger principal
app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)

# Logger de seguridad
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.WARNING)

# Logger de validación
validation_logger = logging.getLogger("validation")
validation_logger.setLevel(logging.ERROR)