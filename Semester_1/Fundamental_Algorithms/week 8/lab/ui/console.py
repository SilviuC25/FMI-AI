from service.person_service import PersonService
from service.event_service import EventService
from service.registration_service import RegistrationService
from repository.registration_repo import RegistrationRepository
from repository.person_repo import PersonRepository
from repository.event_repo import EventRepository
from domain.person import Person
from domain.event import Event
from domain.validator import PersonValidator, EventValidator
from utils import str_to_datetime
import datetime
from typing import Optional, List

class Console:
    def __init__(self,
                 person_service: PersonService,
                 event_service: EventService,
                 registration_service: RegistrationService,
                 registration_repository: RegistrationRepository,
                 person_repository: PersonRepository,
                 event_repository: EventRepository):
        self.__person_service = person_service
        self.__event_service = event_service
        self.__registration_service = registration_service
        self.__registration_repository = registration_repository
        self.__person_repository = person_repository
        self.__event_repository = event_repository
        self.__person_validator = PersonValidator()
        self.__event_validator = EventValidator()

    def print_menu(self):
        print("\n" + "="*60)
        print("EVENT ORGANIZATION APPLICATION")
        print("="*60)
        print("1. Manage Persons")
        print("2. Manage Events")
        print("3. Manage Registrations")
        print("4. Display Reports")
        print("5. Exit")
        print("="*60)

    def print_person_menu(self):
        print("\n" + "-"*60)
        print("PERSON MANAGEMENT")
        print("-"*60)
        print("1. Add Person")
        print("2. Delete Person")
        print("3. Update Person")
        print("4. Search Person by ID")
        print("5. Display All Persons")
        print("6. Back to Main Menu")
        print("-"*60)

    def print_event_menu(self):
        print("\n" + "-"*60)
        print("EVENT MANAGEMENT")
        print("-"*60)
        print("1. Add Event")
        print("2. Delete Event")
        print("3. Update Event")
        print("4. Search Event by ID")
        print("5. Display All Events")
        print("6. Back to Main Menu")
        print("-"*60)

    def print_registrations_menu(self):
        print("\n" + "-"*60)
        print("REGISTRATION MANAGEMENT")
        print("-"*60)
        print("1. Add New Registration")
        print("2. Unregister Person from Event")
        print("3. Show All Registrations")
        print("4. Show Registrations For Person")
        print("5. Back to Main Menu")
        print("-"*60)

    def print_reports_menu(self):
        print("\n" + "-"*60)
        print("REPORTS")
        print("-"*60)
        print("1. Events for a Person (sorted by description)")
        print("2. Events for a Person (sorted by date)")
        print("3. Top 3 persons with most events")
        print("4. Top 20% events with most participants")
        print("5. Back to Main Menu")
        print("-"*60)

    def add_person(self):
        personal_id = input("Enter personal ID (CNP - 13 digits): ").strip()
        name = input("Enter name (minimum 2 characters): ").strip()
        try:
            self.__person_service.add_person(personal_id, name)
            print(f"✓ Person '{name}' added.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def delete_person(self):
        personal_id = input("Enter personal ID to delete: ").strip()
        try:
            self.__person_service.delete_person(personal_id)
            print(f"✓ Person '{personal_id}' deleted.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def update_person(self):
        personal_id = input("Enter personal ID to update: ").strip()
        person = self.__person_repository.get_person_by_id(personal_id)
        if person is None:
            print("✗ Person not found.")
            return
        print(f"Current: {person}")
        new_name = input("Enter new name (or Enter to keep): ").strip()
        if new_name == "":
            new_name = person.get_name()
        try:
            self.__person_service.update_person(personal_id, new_name)
            print("✓ Person updated.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def search_person(self):
        personal_id = input("Enter personal ID to search: ").strip()
        person = self.__person_repository.get_person_by_id(personal_id)
        if person is None:
            print("✗ Person not found.")
        else:
            print(f"✓ Found: {person}")

    def display_all_persons(self):
        people = self.__person_repository.get_all_people()
        if not people:
            print("No persons registered.")
            return
        for i, p in enumerate(people, 1):
            print(f"{i}. {p}")

    def manage_persons(self):
        while True:
            self.print_person_menu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.add_person()
            elif choice == "2":
                self.delete_person()
            elif choice == "3":
                self.update_person()
            elif choice == "4":
                self.search_person()
            elif choice == "5":
                self.display_all_persons()
            elif choice == "6":
                break
            else:
                print("✗ Invalid choice.")

    def add_event(self):
        event_id = input("Enter event ID (numeric, min 5 digits): ").strip()
        date = input("Enter date (YYYY-MM-DD): ").strip()
        time = input("Enter time (HH:MM): ").strip()
        description = input("Enter description (min 3 words): ").strip()
        try:
            self.__event_service.add_event(event_id, date, time, description)
            print(f"✓ Event '{description}' added.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def delete_event(self):
        event_id = input("Enter event ID to delete: ").strip()
        try:
            self.__event_service.delete_event(event_id)
            print(f"✓ Event '{event_id}' deleted.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def update_event(self):
        event_id = input("Enter event ID to update: ").strip()
        event = self.__event_repository.get_event_by_id(event_id)
        if event is None:
            print("✗ Event not found.")
            return
        print(f"Current: {event}")
        date = input("New date (YYYY-MM-DD) or Enter to keep: ").strip()
        time = input("New time (HH:MM) or Enter to keep: ").strip()
        description = input("New description or Enter to keep: ").strip()
        if date == "":
            date = event.get_date()
        if time == "":
            time = event.get_time()
        if description == "":
            description = event.get_description()
        try:
            self.__event_service.update_event(event_id, date, time, description)
            print("✓ Event updated.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def search_event(self):
        event_id = input("Enter event ID to search: ").strip()
        event = self.__event_repository.get_event_by_id(event_id)
        if event is None:
            print("✗ Event not found.")
        else:
            print(f"✓ Found: {event}")

    def display_all_events(self):
        events = self.__event_repository.get_all_events()
        if not events:
            print("No events available.")
            return
        for i, e in enumerate(events, 1):
            print(f"{i}. {e}")

    def manage_events(self):
        while True:
            self.print_event_menu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.add_event()
            elif choice == "2":
                self.delete_event()
            elif choice == "3":
                self.update_event()
            elif choice == "4":
                self.search_event()
            elif choice == "5":
                self.display_all_events()
            elif choice == "6":
                break
            else:
                print("✗ Invalid choice.")

    def add_registration(self):
        personal_id = input("Enter person's personal ID: ").strip()
        event_id = input("Enter event ID: ").strip()
        try:
            ok = self.__registration_service.register_person_to_event(personal_id, event_id)
            if ok:
                reg_date = self.__registration_service.get_registration_date(personal_id, event_id)
                ts = reg_date.strftime("%Y-%m-%d %H:%M:%S") if reg_date else "N/A"
                print(f"✓ Registration added at {ts}")
            else:
                print("✗ Registration failed (already exists).")
        except Exception as e:
            print(f"✗ Error: {e}")

    def unregister_registration(self):
        personal_id = input("Enter person's personal ID to unregister: ").strip()
        event_id = input("Enter event ID: ").strip()
        try:
            ok = self.__registration_service.unregister_person_from_event(personal_id, event_id)
            if ok:
                print("✓ Unregistered successfully.")
            else:
                print("✗ Not registered or already removed.")
        except Exception as e:
            print(f"✗ Error: {e}")

    def show_all_registrations(self):
        regs = self.__registration_service.get_all_registrations()
        if not regs:
            print("No registrations.")
            return
        for i, (pid, eid, rdate) in enumerate(regs, 1):
            person = self.__person_repository.get_person_by_id(pid)
            event = self.__event_repository.get_event_by_id(eid)
            pname = person.get_name() if person else pid
            edesc = event.get_description() if event else eid
            ts = rdate.strftime("%Y-%m-%d %H:%M:%S") if isinstance(rdate, datetime.datetime) else str(rdate)
            print(f"{i}. {pname} -> {edesc} at {ts}")

    def show_registrations_for_person(self):
        personal_id = input("Enter person's personal ID: ").strip()
        person = self.__person_repository.get_person_by_id(personal_id)
        if person is None:
            print("✗ Person not found.")
            return
        event_objs = self.__registration_service.get_events_for_person(personal_id)
        if not event_objs:
            print("No registrations for this person.")
            return
        for i, ev in enumerate(event_objs, 1):
            print(f"{i}. {ev}")

    def manage_registrations(self):
        while True:
            self.print_registrations_menu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.add_registration()
            elif choice == "2":
                self.unregister_registration()
            elif choice == "3":
                self.show_all_registrations()
            elif choice == "4":
                self.show_registrations_for_person()
            elif choice == "5":
                break
            else:
                print("✗ Invalid choice.")

    def display_events_for_person_by_description(self):
        personal_id = input("Enter person's personal ID: ").strip()
        person = self.__person_repository.get_person_by_id(personal_id)
        if person is None:
            print("✗ Person not found.")
            return
        events = self.__person_service.get_events_for_person_sorted_by_description(personal_id)
        if not events:
            print("No events for this person.")
            return
        for i, ev in enumerate(events, 1):
            print(f"{i}. {ev}")

    def display_events_for_person_by_date(self):
        personal_id = input("Enter person's personal ID: ").strip()
        person = self.__person_repository.get_person_by_id(personal_id)
        if person is None:
            print("✗ Person not found.")
            return
        events = self.__person_service.get_events_for_person_sorted_by_date(personal_id)
        if not events:
            print("No events for this person.")
            return
        for i, ev in enumerate(events, 1):
            print(f"{i}. {ev}")

    def display_top_3_participants(self):
        top3 = self.__person_service.get_top_3_participants()
        if not top3:
            print("No registrations.")
            return
        for i, (person, count) in enumerate(top3, 1):
            name = person.get_name() if person else "Unknown"
            print(f"{i}. {name} - {count} event(s)")

    def display_top_20_percent_events(self):
        top_events = self.__person_service.get_top_20_percent_events()
        if not top_events:
            print("No events.")
            return
        for i, (event, count) in enumerate(top_events, 1):
            desc = event.get_description() if event else "Unknown"
            date = event.get_date() if event else "N/A"
            time = event.get_time() if event else "N/A"
            print(f"{i}. {desc} - {count} participant(s) ({date} {time})")

    def display_reports(self):
        while True:
            self.print_reports_menu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.display_events_for_person_by_description()
            elif choice == "2":
                self.display_events_for_person_by_date()
            elif choice == "3":
                self.display_top_3_participants()
            elif choice == "4":
                self.display_top_20_percent_events()
            elif choice == "5":
                break
            else:
                print("✗ Invalid choice.")

    def run(self):
        print("\n" + "="*60)
        print("WELCOME TO EVENT ORGANIZATION APPLICATION")
        print("="*60)
        while True:
            self.print_menu()
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.manage_persons()
            elif choice == "2":
                self.manage_events()
            elif choice == "3":
                self.manage_registrations()
            elif choice == "4":
                self.display_reports()
            elif choice == "5":
                print("Goodbye.")
                break
            else:
                print("✗ Invalid choice.")