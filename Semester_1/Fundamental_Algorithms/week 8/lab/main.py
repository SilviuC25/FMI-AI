from repository.person_repo import PersonRepository
from repository.event_repo import EventRepository
from repository.registration_repo import RegistrationRepository
from service.person_service import PersonService
from service.event_service import EventService
from service.registration_service import RegistrationService
from ui.console import Console
from domain.person import Person
from domain.event import Event
from domain.validator import PersonValidator, EventValidator
from tests.test_repo import run_all_repo_tests
from tests.test_service import run_all_service_tests
from tests.test_utils import run_all_utils_tests

def add_default_data(person_repository: PersonRepository, event_repository: EventRepository, registration_repository: RegistrationRepository):
    """
    Adds default data to the repositories for testing/demo purposes.
    Args:
      person_repository (PersonRepository): The person repository.
      event_repository (EventRepository): The event repository.
      registration_repo (RegistrationRepository): The registration repository.
    Returns:
      None
    """
    p1 = Person("1234567890123", "Alice Johnson")
    p2 = Person("9876543210987", "Bob Smith")
    p3 = Person("5555555555555", "Carol White")
    p4 = Person("1111111111111", "David Brown")
    p5 = Person("2222222222222", "Emma Davis")

    person_repository.add_person_to_repo(p1)
    person_repository.add_person_to_repo(p2)
    person_repository.add_person_to_repo(p3)
    person_repository.add_person_to_repo(p4)
    person_repository.add_person_to_repo(p5)

    e1 = Event("10001", "2025-03-15", "10:00", "Spring Conference Annual Meeting")
    e2 = Event("10002", "2025-04-20", "14:30", "Summer Workshop Training Session")
    e3 = Event("10003", "2025-05-10", "09:00", "Technology Summit Expo Event")
    e4 = Event("10004", "2025-06-01", "18:00", "Networking Gala Evening Party")
    e5 = Event("10005", "2025-07-25", "11:00", "Product Launch Special Announcement")

    event_repository.add_event_to_repo(e1)
    event_repository.add_event_to_repo(e2)
    event_repository.add_event_to_repo(e3)
    event_repository.add_event_to_repo(e4)
    event_repository.add_event_to_repo(e5)

    registration_repository.register_person_to_event("1234567890123", "10001")
    registration_repository.register_person_to_event("1234567890123", "10002")
    registration_repository.register_person_to_event("1234567890123", "10003")
    registration_repository.register_person_to_event("1234567890123", "10004")

    registration_repository.register_person_to_event("9876543210987", "10001")
    registration_repository.register_person_to_event("9876543210987", "10002")
    registration_repository.register_person_to_event("9876543210987", "10005")

    registration_repository.register_person_to_event("5555555555555", "10001")
    registration_repository.register_person_to_event("5555555555555", "10003")
    registration_repository.register_person_to_event("5555555555555", "10004")
    registration_repository.register_person_to_event("5555555555555", "10005")

    registration_repository.register_person_to_event("1111111111111", "10002")
    registration_repository.register_person_to_event("1111111111111", "10004")

    registration_repository.register_person_to_event("2222222222222", "10003")
    registration_repository.register_person_to_event("2222222222222", "10005")

    print("✓ Default data added successfully!")

if __name__ == "__main__":
    print("Running tests...\n")
    try:
        run_all_utils_tests()
        run_all_repo_tests()
        run_all_service_tests()
        print("\n✓ All tests passed!\n")
    except Exception as e:
        print(f"\n✗ Tests failed: {e}\n")

    person_repo = PersonRepository()
    event_repo = EventRepository()
    registration_repo = RegistrationRepository()
    person_validator = PersonValidator()
    event_validator = EventValidator()

    add_default_data(person_repo, event_repo, registration_repo)

    person_service = PersonService(person_repo, person_validator, registration_repo, event_repo)
    event_service = EventService(event_repo, event_validator, registration_repo, person_repo)
    registration_service = RegistrationService(registration_repo, person_repo, event_repo)

    console = Console(person_service, event_service, registration_service, registration_repo, person_repo, event_repo)
    console.run()