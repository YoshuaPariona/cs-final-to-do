"""
Archivo principal para ejecutar la suite de tests unitarios de TodoApp.

Carga y ejecuta todas las pruebas definidas en los módulos individuales,
mostrando un resumen al finalizar.
"""

import sys
import os
import unittest

# Agrega el directorio raíz del proyecto al sys.path para importar módulos correctamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar todas las clases de test individuales
from test_01_register_user_success import TestRegisterUserSuccess
from test_02_register_user_duplicate import TestRegisterUserDuplicate
from test_03_login_success import TestLoginSuccess
from test_04_login_wrong_password import TestLoginWrongPassword
from test_05_login_nonexistent_user import TestLoginNonexistentUser
from test_06_logout import TestLogout
from test_07_cleanup_completed_tasks import TestCleanupCompletedTasks
from test_08_create_task_important import TestCreateTaskImportant
from test_09_create_task_normal import TestCreateTaskNormal
from test_10_create_task_postponable import TestCreateTaskPostponable
from test_11_read_tasks import TestReadTasks
from test_12_update_task import TestUpdateTask
from test_13_delete_task import TestDeleteTask


if __name__ == "__main__":
    # Crear el cargador y la suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Lista de clases de test a ejecutar
    test_classes = [
        TestRegisterUserSuccess,
        TestRegisterUserDuplicate,
        TestLoginSuccess,
        TestLoginWrongPassword,
        TestLoginNonexistentUser,
        TestLogout,
        TestCleanupCompletedTasks,
        TestCreateTaskImportant,
        TestCreateTaskNormal,
        TestCreateTaskPostponable,
        TestReadTasks,
        TestUpdateTask,
        TestDeleteTask
    ]

    # Cargar y agregar los tests de cada clase a la suite
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)

    # Ejecutar la suite de tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Mostrar resumen de resultados
    print(f"\n{'=' * 50}")
    print(f"Tests ejecutados : {result.testsRun}")
    print(f"Errores          : {len(result.errors)}")
    print(f"Fallos           : {len(result.failures)}")
    print(f"Éxito total      : {result.wasSuccessful()}")
