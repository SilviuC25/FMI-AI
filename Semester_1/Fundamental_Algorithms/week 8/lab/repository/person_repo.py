from domain.person import Person

class PersonRepository:
	def __init__(self):
		self.__people = []
	
	def get_all_people(self) -> list:
		"""
		Gets all people from the people list.
		Returns:
		  list: A list of all people.
		"""
		return self.__people

	def get_person_by_id(self, personal_id: str) -> Person | None:
		"""
		Finds a person by their personal ID.
		Args:
		  personal_id (str): The personal ID of the person to find.
		Returns:
		  Person | None: The person if found, None otherwise.
		"""
		for person in self.__people:
			if person.get_personal_id() == personal_id:
				return person
		return None
	
	def add_person_to_repo(self, person: Person):
		"""
		Adds a person to the people list.
		Args:
		  person (Person): The person to add.
		Returns:
		  None
		"""
		for p in self.__people:
			if p.get_personal_id() == person.get_personal_id():
				raise ValueError(f"Person with ID {person.get_personal_id()} already exists.")
			
		self.__people.append(person)

	def delete_person_by_id(self, personal_id: str) -> bool:
		"""
		Deletes a person by their personal ID.
		Args:
		  personal_id (str): The personal ID of the person to delete.
		Returns:
		  bool: True if the person was deleted, raises ValueError otherwise.
		"""
		person_to_delete = self.get_person_by_id(personal_id)
		if person_to_delete is not None:
			self.__people.remove(person_to_delete)
			return True
		else:
			raise ValueError(f"Person with ID {personal_id} does not exist.")
	
	def update_person_by_id(self, updated_person: Person) -> bool:
		"""
		Updates an existing person.
		Args:
		  personal_id (str): The personal ID of the person to update.
		  new_name (str): The new name for the person.
		Returns:
		  bool: True if the person was updated, raises ValueError otherwise.
		"""
		personal_id = updated_person.get_personal_id()

		for p in self.__people:
			if p.get_personal_id() == personal_id:
				p.set_name(updated_person.get_name())
				return True
		else:
			raise ValueError(f"Person with ID {personal_id} does not exist.")

	def get_size(self) -> int:
		"""
		Gets the number of people in the repository.
		Returns:
		  int: The number of people.
		"""
		return len(self.__people)
