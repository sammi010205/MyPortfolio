from heapq import heappop, heappush
from collections import deque, defaultdict

class Task:
  def __init__(self, name, value, duration, dependencies=None, mandatory=False, fractionable=False):
    self.name = name
    self.value = value
    self.duration = duration
    self.dependencies = dependencies if dependencies else []
    self.mandatory = mandatory
    self.fractionable = fractionable

  # Implementing the __lt__ method to avoid TypeError when comparing Task instances in a heap
  def __lt__(self, other):
    return (self.value / self.duration) > (other.value / other.duration)


# Step 1: Build a directed graph from the task list
def build_graph(tasks):
  graph = defaultdict(list)
  in_degree = defaultdict(int)

  # Initialize in-degrees for all tasks
  for task in tasks:
    in_degree[task.name] = 0

  for task in tasks:
    for dependency in task.dependencies:
      graph[dependency].append(task.name)
      in_degree[task.name] += 1

  return graph, in_degree


# Step 2: Topological sort to find a valid task order considering dependencies
def topological_sort(tasks):
  graph, in_degree = build_graph(tasks)
  task_map = {task.name: task for task in tasks}
  queue = deque([task.name for task in tasks if in_degree[task.name] == 0])
  sorted_tasks = []

  while queue:
    current = queue.popleft()
    sorted_tasks.append(task_map[current])
    for dependent in graph[current]:
      in_degree[dependent] -= 1
      if in_degree[dependent] == 0:
        queue.append(dependent)

  return sorted_tasks


# Step 3: Create a max heap for prioritizing tasks by value/duration ratio
def create_max_heap(sorted_tasks, available_time):
  max_heap = []
  for task in sorted_tasks:
    if task.mandatory or (available_time >= task.duration):
      heappush(max_heap, (-task.value / task.duration, task))  # Max heap by value/time ratio (Fractional Knapsack concept)
  return max_heap


# Step 4: Implement Fractional Knapsack Algorithm to prioritize tasks from the max heap until time runs out
def prioritize_tasks(max_heap, available_time):
  selected_tasks = []
  current_time = 0

 # Implement fractional knapsack algorithm:

  while max_heap and current_time < available_time:
    _, task = heappop(max_heap)
    if current_time + task.duration <= available_time:
      selected_tasks.append(task)
      current_time += task.duration
    elif task.fractionable:
      # Handle fractionable tasks using the Fractional Knapsack Algorithm
      fraction = (available_time - current_time) / task.duration
      selected_tasks.append(Task(f"{task.name} (Partial)", task.value * fraction, available_time - current_time))
      break

  return selected_tasks


# Step 5: Print task details
def print_tasks(tasks):
  for task in tasks:
    print(f"Task Name: {task.name}, Value: {task.value}, Duration: {task.duration}, Dependencies: {task.dependencies}, Mandatory: {task.mandatory}, Fractionable: {task.fractionable}")


# Step 6: Main function with a complete set of 18 task examples
def main():
  task_list = [
    Task("Assignment 1 - 5002", 85, 10, [], mandatory=True, fractionable=False),
    Task("LeetCode", 60, 5, [], mandatory=False, fractionable=False),
    Task("Assignment 1 - 5001", 100, 8, ["LeetCode"], mandatory=False, fractionable=False),
    Task("Quiz 1 - 5002", 40, 3, [], mandatory=True, fractionable=False),
    Task("Assignment 2 - 5001", 70, 6, ["Assignment 1 - 5001"], mandatory=False, fractionable=True),
    Task("Assignment 3 - 5002", 90, 10, ["LeetCode", "Quiz 1 - 5002"], mandatory=False, fractionable=False),
    Task("Interview Preparation", 120, 15, [], mandatory=False, fractionable=True),
    Task("Quiz 2 - 5001", 110, 12, ["Assignment 3 - 5002"], mandatory=True, fractionable=False),
    Task("Conference Call", 130, 20, [], mandatory=False, fractionable=False),
    Task("Doctor's Appointment", 50, 4, ["Quiz 1 - 5002"], mandatory=False, fractionable=True),
    Task("Assignment 4 - 5002", 95, 7, ["Conference Call"], mandatory=True, fractionable=False),
    Task("Movie Night", 60, 5, ["Interview Preparation"], mandatory=False, fractionable=True),
    Task("Quiz 3 - 5002", 150, 18, ["Quiz 2 - 5001"], mandatory=False, fractionable=False),
    Task("Assignment 5 - 5001", 80, 9, [], mandatory=False, fractionable=True),
    Task("Meet Friend", 65, 8, ["Assignment 5 - 5001"], mandatory=False, fractionable=False),
    Task("Project Submission - 5001", 140, 22, ["Assignment 1 - 5001"], mandatory=True, fractionable=False),
    Task("Assignment 6 - 5002", 105, 11, ["Quiz 3 - 5002"], mandatory=False, fractionable=False),
    Task("Exam - 5002", 75, 5, [], mandatory=True, fractionable=False),
    Task("Internship Application", 160, 25, ["Assignment 2 - 5001"], mandatory=False, fractionable=True),
    Task("Assignment 7 - 5001", 115, 14, ["Exam - 5002"], mandatory=False, fractionable=False),
    Task("Final Project - 5002", 135, 16, ["Meet Friend"], mandatory=True, fractionable=False)
  ]

  available_time = 100  # Total time available for the month
  sorted_tasks = topological_sort(task_list)
  max_heap = create_max_heap(sorted_tasks, available_time)
  prioritized_tasks = prioritize_tasks(max_heap, available_time)

  print("Prioritized tasks:")
  print_tasks(prioritized_tasks)

if __name__ == "__main__":
  main()
