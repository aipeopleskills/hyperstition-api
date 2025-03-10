import logging
import os

# Directorio de logs
LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configuración del formato de logs
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Configuración del logger principal
app_logger = logging.getLogger("app")
app_logger.setLevel(logging.INFO)
app_handler = logging.FileHandler(os.path.join(LOG_DIR, "app.log"))
app_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
app_logger.addHandler(app_handler)

# Logger de seguridad
security_logger = logging.getLogger("security")
security_logger.setLevel(logging.WARNING)
security_handler = logging.FileHandler(os.path.join(LOG_DIR, "security.log"))
security_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
security_logger.addHandler(security_handler)

# Logger de validación
validation_logger = logging.getLogger("validation")
validation_logger.setLevel(logging.ERROR)
validation_handler = logging.FileHandler(os.path.join(LOG_DIR, "validation.log"))
validation_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
validation_logger.addHandler(validation_handler)

# Logger de análisis hipersticioso
analysis_logger = logging.getLogger("analysis")
analysis_logger.setLevel(logging.INFO)
analysis_handler = logging.FileHandler(os.path.join(LOG_DIR, "analysis.log"))
analysis_handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))
analysis_logger.addHandler(analysis_handler)

# Mensajes de inicialización de logs
app_logger.info("Logger de aplicación inicializado correctamente.")
security_logger.warning("Logger de seguridad activo.")
validation_logger.error("Logger de validación activo.")
analysis_logger.info("Logger de análisis hipersticioso listo para uso.")
