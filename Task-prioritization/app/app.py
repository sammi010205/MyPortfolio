from flask import Flask, request, jsonify, render_template
from heapq import heappop, heappush
from collections import deque, defaultdict

# Use your Task class and functions from the original script
class Task:
    def __init__(self, name, value, duration, dependencies=None, mandatory=False, fractionable=False):
        self.name = name
        self.value = value
        self.duration = duration
        self.dependencies = dependencies if dependencies else []
        self.mandatory = mandatory
        self.fractionable = fractionable

    def to_dict(self):
        return {
            "name": self.name,
            "value": self.value,
            "duration": self.duration,
            "dependencies": self.dependencies,
            "mandatory": self.mandatory,
            "fractionable": self.fractionable,
        }

def build_graph(tasks):
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for task in tasks:
        in_degree[task.name] = 0

    for task in tasks:
        for dependency in task.dependencies:
            graph[dependency].append(task.name)
            in_degree[task.name] += 1

    return graph, in_degree

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

def create_max_heap(sorted_tasks, available_time):
    max_heap = []
    for task in sorted_tasks:
        if task.mandatory or (available_time >= task.duration):
            if task.duration > 0:  # Avoid division by zero
                heappush(max_heap, (-task.value / task.duration, task))
    return max_heap

def prioritize_tasks(max_heap, available_time):
    selected_tasks = []
    current_time = 0

    while max_heap and current_time < available_time:
        _, task = heappop(max_heap)
        if current_time + task.duration <= available_time:
            selected_tasks.append(task)
            current_time += task.duration
        elif task.fractionable:
            fraction = (available_time - current_time) / task.duration
            selected_tasks.append(Task(f"{task.name} (Partial)", task.value * fraction, available_time - current_time))
            break

    return selected_tasks


# Flask Application
app = Flask(__name__)

# Sample Task Data
task_lists = [
    [
        Task("2024 Fall class", 10, 12, ["Leetcode"], mandatory=True, fractionable=False),
        Task("Leetcode", 6, 3, [], mandatory=False, fractionable=True),
        Task("Assignments and Exams", 10, 14, ["2024 Fall class"], mandatory=True, fractionable=False),
        Task("Networking event", 7, 14, [], mandatory=False, fractionable=False),
    ],
    [
        Task("Leetcode", 10, 15, [], mandatory=False, fractionable=True),
        Task("Job Searching and Preparation", 10, 30, ["Leetcode"], mandatory=True, fractionable=False),
        Task("Networking event", 8, 1, [], mandatory=False, fractionable=False),
    ]
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/prioritize', methods=['POST'])
def prioritize():
    participant_index = int(request.form.get('participant'))  # Index of task list
    available_time = int(request.form.get('time'))  # Time input

    # Process tasks for the selected participant
    tasks = task_lists[participant_index]
    sorted_tasks = topological_sort(tasks)
    max_heap = create_max_heap(sorted_tasks, available_time)
    prioritized_tasks = prioritize_tasks(max_heap, available_time)

    # Convert to dictionary for JSON response
    result = [task.to_dict() for task in prioritized_tasks]
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
