# src/utils/logger.py

import logging
import os

def setup_logging(log_level=logging.INFO, log_file="etl_process.log"):
    """
    Configura el sistema de logging para el proyecto.

    Args:
        log_level (int): Nivel mínimo de mensajes a registrar (ej. logging.INFO, logging.DEBUG).
        log_file (str): Nombre del archivo donde se guardarán los logs.
    """
    # Crear el directorio de logs si no existe
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, log_file)

    # Obtener el logger raíz
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Limpiar handlers existentes para evitar duplicados si se llama varias veces
    if root_logger.handlers:
        for handler in root_logger.handlers:
            root_logger.removeHandler(handler)

    # Formateador para los mensajes de log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler para la consola (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Handler para el archivo de log
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.info(f"Logging configurado. Nivel: {logging.getLevelName(log_level)}. Los logs se guardarán en: {log_file_path}")

