from domain.task import Task

class TaskValidator:
  def validate_task(self, task: Task):
    title = task.get_title()
    status = task.get_status()
    priority = task.get_priority()

    if len(title) < 1:
      raise ValueError("Title cannot be empty string")
    
    if status not in ["in progress", "open", "closed"]:
      raise ValueError("Status must be one of: open, in progress, closed")
    
    if priority < 1 or priority > 5:
      raise ValueError("Priority must be between 1 and 5")
    