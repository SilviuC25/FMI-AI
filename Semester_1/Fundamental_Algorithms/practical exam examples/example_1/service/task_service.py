from domain.task import Task
from domain.validator import TaskValidator
from repository.task_repository import TaskRepository

class TaskService:
  def __init__(self, task_repository: TaskRepository, task_validator: TaskRepository):
    self.__task_reposiotry = task_repository
    self.__task_validator = task_validator

  def add_task(self, task: Task):
    self.__task_validator(task)
    self.__task_reposiotry.add_task(task)
  
  def view_tasks(self, programmer_to_display: str):
    