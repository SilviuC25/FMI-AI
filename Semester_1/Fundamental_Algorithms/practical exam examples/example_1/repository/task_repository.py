from domain.task import Task

class TaskRepository:
  def __init__(self, filename: str):
    self.__tasks = []
    self.__filename = filename
    self.__load_from_file()

  def add_task(self, task: Task):
    self.__tasks.append(task)
    self.__save_to_file()

  def get_all_task(self):
    return self.__tasks()

  def __load_from_file(self):
    with open(self.__filename, "r") as file:
      for line in file:
        line = line.strip()
        parts = line.split("; ")
        id = int(line[0])
        title = line[1]
        programmer = line[2]
        status = line[3]
        priority = int(line[4])

        task = Task(id, title, programmer, status, priority)
        self.__tasks.append(task)

  def __save_to_file(self):
    with open(self.__filename, "w") as file:
      for task in self.__tasks:
        id = task.get_id()
        title = task.get_title()
        programmer = task.get_programmer()
        status = task.get_status()
        priority = task.get_priority()

        line = (
          f"{id}; "
          f"{title}; "
          f"{programmer}; "
          f"{status}; "
          f"{priority}\n"
        )

        file.write(line)


