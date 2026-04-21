from tests.test_repo import run_all_repo_tests
from tests.test_service import run_all_service_tests
from tests.test_utils import run_all_utils_tests

def run_all_tests():
    """
    Runs all tests from repo, service, and utils modules.
    """
    run_all_repo_tests()
    run_all_service_tests()
    run_all_utils_tests()
    print("\nAll tests passed!")