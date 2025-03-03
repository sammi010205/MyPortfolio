#!/usr/bin/env python
# coding: utf-8

# In[31]:


from heapq import heappop, heappush
from collections import deque, defaultdict
import pandas as pd

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


# Step 6: Parse the dataset into Task objects
def parse_task_data(data):
    task_list = []
    for row in data:
        task_name = row.get('Task_1') or f"Task {len(task_list) + 1}"
        value = float(row.get('Q4', 0))  # Benefit
        duration = float(row.get('Q3', 0))  # Estimated time
        dependencies = row.get('Q2', "").split(",") if row.get('Q2') else []
        mandatory = row.get('Q1', "").strip().lower() == "yes"
        fractionable = row.get('Q5', "").strip().lower() == "yes"

        task = Task(task_name, value, duration, dependencies, mandatory, fractionable)
        task_list.append(task)

    return task_list


# Step 7: Main function
def main():
    # Load your dataset
    file_path = '/path/to/Cleaned_Task_Dataset.csv'  # Replace with the actual dataset file path
    new_data = pd.read_csv(file_path)

    # Parse tasks from the dataset
    task_list = parse_task_data(new_data.to_dict('records'))

    available_time = 100  # Total time available for the month
    sorted_tasks = topological_sort(task_list)
    max_heap = create_max_heap(sorted_tasks, available_time)
    prioritized_tasks = prioritize_tasks(max_heap, available_time)

    print("Prioritized tasks:")
    print_tasks(prioritized_tasks)


if __name__ == "__main__":
    main()


# In[ ]:


from flask import Flask, render_template, request, jsonify
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
        Task("2024 Fall class", 10, 24, ["Leetcode"], mandatory=True, fractionable=False),
        Task("Leetcode", 6, 6, [], mandatory=False, fractionable=True),
        Task("Assignments and Exams", 10, 80, ["2024 Fall class"], mandatory=True, fractionable=False),
        Task("Networking event", 7, 9, [], mandatory=False, fractionable=False),
        Task("Job Searching and Preparation", 10, 30, ["Leetcode"], mandatory=True, fractionable=False),
        Task("Shopping and Household", 10, 5, [], mandatory=False, fractionable=False),
        Task("Exercise and Outdoor Activity", 10, 20, [], mandatory=False, fractionable=False)
    ],
    [
        Task("Leetcode", 6, 48, [], mandatory=False, fractionable=True),
        Task("2024 Fall class", 7, 24, [], mandatory=False, fractionable=False),
        Task("Assignments and Exams", 7, 80, ["2024 Fall class"], mandatory=True, fractionable=False),
        Task("Job Searching and Preparation", 5, 20, [], mandatory=False, fractionable=True),
        Task("Exercise and Outdoor Activity", 5, 20, [], mandatory=False, fractionable=True),
        Task("Shopping and Household", 5, 20, [], mandatory=False, fractionable=False),
        Task("Networking event", 6, 10, [], mandatory=False, fractionable=False)
    ],
    
    [
        Task("Leetcode", 10, 11, [], mandatory=False, fractionable=True),
        Task("2024 Fall class", 10, 24, [], mandatory=False, fractionable=False),
        Task("Assignments and Exams", 10, 90, ["2024 Fall class"], mandatory=True, fractionable=False),
        Task("Networking event", 10, 7, [], mandatory=False, fractionable=True),
        Task("Job Searching and Preparation", 10, 30, [], mandatory=False, fractionable=True),
        Task("Exercise and Outdoor Activity", 10, 30, [], mandatory=False, fractionable=False),
        Task("Shopping and Household", 5, 15, [], mandatory=False, fractionable=False)
    ],
    [
        Task("Shopping and Household", 4, 12, [], mandatory=False, fractionable=False),
        Task("Assignments and Exams", 5, 30, ["2024 Fall class"], mandatory=False, fractionable=False),
        Task("2024 Fall class", 5, 24, [], mandatory=False, fractionable=False),
        Task("Leetcode", 3, 20, [], mandatory=False, fractionable=True),
        Task("Networking event", 3, 5, [], mandatory=False, fractionable=False),
        Task("Exercise and Outdoor Activity", 4, 50, [], mandatory=False, fractionable=False),
        Task("Job Searching and Preparation", 5, 20, [], mandatory=False, fractionable=False)
    ],
    [
        Task("Leetcode", 6, 60, [], mandatory=False, fractionable=True),
        Task("2024 Fall class", 6, 20, [], mandatory=False, fractionable=False),
        Task("Networking event", 5, 20, [], mandatory=False, fractionable=False),
        Task("Job Searching and Preparation", 7, 50, [], mandatory=False, fractionable=True),
        Task("Shopping and Household", 7, 40, [], mandatory=False, fractionable=True),
        Task("Assignments and Exams", 8, 60, [], mandatory=False, fractionable=False),
        Task("Exercise and Outdoor Activity", 5, 15, [], mandatory=False, fractionable=False)
    ],
    [
        Task("2024 Fall class", 8, 24, [], mandatory=False, fractionable=False),
        Task("Leetcode", 10, 10, ["2024 Fall class"], mandatory=True, fractionable=False),
        Task("Assignments and Exams", 10, 80, ["2024 Fall class"], mandatory=True, fractionable=False),
        Task("Networking event", 9, 30, [], mandatory=False, fractionable=False),
        Task("Job Searching and Preparation", 10, 40, [], mandatory=False, fractionable=False),
        Task("Exercise and Outdoor Activity", 10, 30, [], mandatory=False, fractionable=False),
        Task("Shopping and Household", 7, 8, [], mandatory=False, fractionable=False)
    ],
    [
        Task("2024 Fall class", 7, 24, ["Assignments and Exams"], mandatory=True, fractionable=False),
        Task("Leetcode", 7, 9, [], mandatory=False, fractionable=False),
        Task("Assignments and Exams", 6, 40, [], mandatory=False, fractionable=False),
        Task("Networking event", 8, 8, [], mandatory=False, fractionable=False),
        Task("Exercise and Outdoor Activity", 7, 15, [], mandatory=False, fractionable=True),
        Task("Job Searching and Preparation", 7, 70, [], mandatory=False, fractionable=False),
        Task("Shopping and Household", 5, 10, [], mandatory=False, fractionable=False)
    ],
    [
        Task("Leetcode", 10, 90, [], mandatory=False, fractionable=True),
        Task("Job Searching and Preparation", 10, 45, ["Leetcode"], mandatory=True, fractionable=False),
        Task("Networking event", 8, 7, [], mandatory=False, fractionable=False),
        Task("Shopping and Household", 2, 7, [], mandatory=False, fractionable=False),
        Task("2024 Fall class", 9, 45, [], mandatory=False, fractionable=False),
        Task("Exercise and Outdoor Activity", 8, 7, [], mandatory=False, fractionable=False),
        Task("Assignments and Exams", 7, 30, [], mandatory=False, fractionable=False)
    ],
    [
        Task("Leetcode", 10, 90, [], mandatory=False, fractionable=True),
        Task("Networking event", 10, 34, ["Job Searching and Preparation"], mandatory=True, fractionable=False),
        Task("Exercise and Outdoor Activity", 10, 10, ["Shopping and Household"], mandatory=True, fractionable=False),
        Task("Assignments and Exams", 10, 60, ["2024 Fall class"], mandatory=True, fractionable=False),
        Task("2024 Fall class", 10, 25, ["Exercise and Outdoor Activity"], mandatory=True, fractionable=True),
        Task("Shopping and Household", 10, 30, [], mandatory=False, fractionable=False),
        Task("Job Searching and Preparation", 8, 30, [], mandatory=False, fractionable=False)
    ],
    [
        Task("2024 Fall class", 10, 24, [], mandatory=False, fractionable=False),
        Task("Leetcode", 10, 40, [], mandatory=False, fractionable=True),
        Task("Assignments and Exams", 10, 80, ["2024 Fall class"], mandatory=True, fractionable=True),
        Task("Exercise and Outdoor Activity", 7, 30, [], mandatory=False, fractionable=True),
        Task("Networking event", 6, 15, [], mandatory=False, fractionable=False),
        Task("Job Searching and Preparation", 8, 45, [], mandatory=False, fractionable=True),
        Task("Shopping and Household", 10, 24, [], mandatory=False, fractionable=False)
    ],
    [
        Task("Assignments", 7, 90, ["2024 Fall class"], mandatory=True, fractionable=True),
        Task("Leetcode", 6, 10, [], mandatory=False, fractionable=True),
        Task("Shopping and Household", 8, 12, [], mandatory=False, fractionable=True),
        Task("2024 Fall class", 4, 30, [], mandatory=False, fractionable=True),
        Task("Exercise and Outdoor Activity", 7, 15, [], mandatory=False, fractionable=True),
        Task("Networking event", 3, 40, [], mandatory=False, fractionable=True),
        Task("Leetcode", 7, 17, [], mandatory=False, fractionable=True)
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


# In[5]:


import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

# Define the Task class
class Task:
    def __init__(self, name, priority, duration, dependencies, mandatory, fractionable):
        self.name = name
        self.priority = priority
        self.duration = duration
        self.dependencies = dependencies
        self.mandatory = mandatory
        self.fractionable = fractionable

# Example tasks list
tasks = [
    Task("2024 Fall class", 10, 26, ["Leetcode"], mandatory=True, fractionable=False),
    Task("Leetcode", 6, 5, [], mandatory=False, fractionable=True),
    Task("Assignments and Exams", 10, 90, ["2024 Fall class"], mandatory=True, fractionable=False),
    Task("Networking event", 7, 10, [], mandatory=False, fractionable=False),
    Task("Job Searching and Preparation", 10, 25, ["Leetcode"], mandatory=True, fractionable=False),
    Task("Shopping and Household", 10, 8, [], mandatory=False, fractionable=False),
    Task("Exercise and Outdoor Activity", 10, 27, [], mandatory=False, fractionable=False)
]

# Function to build the graph and in-degree dictionary
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

graph, in_degree = build_graph(tasks)

# Visualize using networkx
G = nx.DiGraph()

# Add edges to the graph
for dependency, dependents in graph.items():
    for dependent in dependents:
        G.add_edge(dependency, dependent)

# Draw the graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G)  # Layout for better visualization
nx.draw(
    G, pos, with_labels=True, node_color="lightgreen", edge_color="blue",
    node_size=3000, font_size=10, font_weight="bold", arrowsize=15
)
plt.title("Directed Task Dependency Graph")
plt.show()


# In[14]:


import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict, deque

# Define the Task class
class Task:
    def __init__(self, name, priority, duration, dependencies, mandatory, fractionable):
        self.name = name
        self.priority = priority
        self.duration = duration
        self.dependencies = dependencies
        self.mandatory = mandatory
        self.fractionable = fractionable
        self.value = self.priority  # Assuming priority as value for sorting

# Example tasks list
tasks = [
    Task("2024 Fall class", 10, 26, [], mandatory=True, fractionable=False),
    Task("Leetcode", 6, 5, [], mandatory=True, fractionable=True),
    Task("Assignments and Exams", 10, 90, ["2024 Fall class"], mandatory=True, fractionable=False),
    Task("Networking event", 7, 10, [], mandatory=False, fractionable=False),
    Task("Job Searching and Preparation", 10, 25, ["Leetcode"], mandatory=True, fractionable=False),
    Task("Shopping and Household", 7, 8, [], mandatory=False, fractionable=False),
    Task("Exercise and Outdoor Activity", 10, 27, [], mandatory=False, fractionable=False)
]

# Step 1: Build the dependency graph
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

# Step 2: Perform topological sort with prioritization
def topological_sort(tasks):
    graph, in_degree = build_graph(tasks)
    task_map = {task.name: task for task in tasks}
    queue = deque([task.name for task in tasks if in_degree[task.name] == 0])
    sorted_tasks = []

    # Topological sort
    while queue:
        current = queue.popleft()
        sorted_tasks.append(task_map[current])
        for dependent in graph[current]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # Final sorting: Mandatory tasks first, then by value/duration ratio
    sorted_tasks = sorted(
        sorted_tasks,
        key=lambda t: (-t.mandatory, -(t.value / t.duration))
    )
    return sorted_tasks

# Step 3: Visualization
def visualize_sorted_tasks(graph, sorted_tasks):
    G = nx.DiGraph()

    # Add edges for the dependency graph
    for dependency, dependents in graph.items():
        for dependent in dependents:
            G.add_edge(dependency, dependent)

    # Plot the dependency graph
    plt.figure(figsize=(12, 6))
    pos = nx.spring_layout(G)  # Layout for better visualization
    nx.draw(
        G, pos, with_labels=True, node_color="lightblue", edge_color="gray",
        node_size=3000, font_size=10, font_weight="bold", arrowsize=15
    )
    plt.title("Dependency Graph")
    plt.show()

    # Plot the sorted task order
    task_names = [task.name for task in sorted_tasks]
    plt.figure(figsize=(12, 2))
    plt.plot(task_names, [1] * len(task_names), 'o-', markersize=10, label="Task Order")
    plt.xticks(range(len(task_names)), task_names, fontsize=10)
    plt.title("Topologically Sorted Task Order (With Priority)")
    plt.gca().axes.get_yaxis().set_visible(False)  # Hide y-axis
    plt.legend()
    plt.show()

# Execute the sorting and visualize
graph, _ = build_graph(tasks)
sorted_tasks = topological_sort(tasks)
visualize_sorted_tasks(graph, sorted_tasks)



# In[16]:


import heapq
from heapq import heappush, heappop
import matplotlib.pyplot as plt
from collections import defaultdict, deque

# Define the Task class
class Task:
    def __init__(self, name, value, duration, dependencies, mandatory, fractionable):
        self.name = name
        self.value = value
        self.duration = duration
        self.dependencies = dependencies
        self.mandatory = mandatory
        self.fractionable = fractionable

# Example tasks list
tasks = [
    Task("2024 Fall class", 10, 26, [], mandatory=True, fractionable=False),
    Task("Leetcode", 6, 5, [], mandatory=True, fractionable=True),
    Task("Assignments and Exams", 10, 90, ["2024 Fall class"], mandatory=True, fractionable=False),
    Task("Networking event", 7, 10, [], mandatory=False, fractionable=False),
    Task("Job Searching and Preparation", 10, 25, ["Leetcode"], mandatory=True, fractionable=False),
    Task("Shopping and Household", 7, 8, [], mandatory=False, fractionable=False),
    Task("Exercise and Outdoor Activity", 10, 27, [], mandatory=False, fractionable=False)
]

# Build the dependency graph
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

# Perform topological sort with prioritization
def topological_sort(tasks):
    graph, in_degree = build_graph(tasks)
    task_map = {task.name: task for task in tasks}
    queue = deque([task.name for task in tasks if in_degree[task.name] == 0])
    sorted_tasks = []

    # Topological sort
    while queue:
        current = queue.popleft()
        sorted_tasks.append(task_map[current])
        for dependent in graph[current]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # Final sorting: Mandatory tasks first, then by value/duration ratio
    sorted_tasks = sorted(
        sorted_tasks,
        key=lambda t: (-t.mandatory, -(t.value / t.duration))
    )
    return sorted_tasks

# Create a max heap for prioritizing tasks
def create_max_heap(sorted_tasks, available_time):
    max_heap = []
    for task in sorted_tasks:
        # Ensure the task meets the available time condition and prerequisites are handled
        if task.duration > 0 and (task.mandatory or available_time >= task.duration):
            heappush(max_heap, (-task.mandatory, -(task.value / task.duration), task))
    return max_heap

# Visualize the max heap
def visualize_max_heap(max_heap):
    # Extract and sort tasks from the heap for visualization
    heap_data = []
    while max_heap:
        mandatory, value_ratio, task = heappop(max_heap)
        heap_data.append((task.name, -mandatory, -value_ratio))

    # Prepare the heap for reuse
    for data in heap_data:
        heappush(max_heap, (-data[1], -data[2], task))

    # Create visualization
    task_names = [data[0] for data in heap_data]
    value_ratios = [round(data[2], 2) for data in heap_data]

    plt.figure(figsize=(10, 5))
    plt.barh(task_names, value_ratios, color='skyblue')
    plt.xlabel("Value/Duration Ratio")
    plt.ylabel("Tasks")
    plt.title("Max Heap Tasks Ordered by mandatory and Value/Duration Ratio")
    plt.gca().invert_yaxis()  # Invert y-axis for priority order
    plt.show()

# Example sorted tasks and available time
sorted_tasks = topological_sort(tasks)  # Tasks sorted by dependencies and priorities
available_time = 40  # Example available time
max_heap = create_max_heap(sorted_tasks, available_time)

# Visualize the max heap
visualize_max_heap(max_heap)


# In[30]:


import heapq
from heapq import heappush, heappop
import matplotlib.pyplot as plt
from collections import defaultdict, deque

# Define the Task class
class Task:
    def __init__(self, name, value, duration, dependencies, mandatory, fractionable):
        self.name = name
        self.value = value
        self.duration = duration
        self.dependencies = dependencies
        self.mandatory = mandatory
        self.fractionable = fractionable

# Example tasks list
tasks = [
    Task("2024 Fall class", 10, 26, [], mandatory=True, fractionable=False),
    Task("Leetcode", 6, 5, [], mandatory=True, fractionable=True),
    Task("Assignments and Exams", 10, 90, ["2024 Fall class"], mandatory=True, fractionable=False),
    Task("Networking event", 7, 10, [], mandatory=False, fractionable=False),
    Task("Job Searching and Preparation", 10, 25, ["Leetcode"], mandatory=True, fractionable=False),
    Task("Shopping and Household", 7, 8, [], mandatory=False, fractionable=False),
    Task("Exercise and Outdoor Activity", 10, 27, [], mandatory=False, fractionable=False)
]

# Step 1: Build the dependency graph
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

# Step 2: Perform topological sort with prioritization
def topological_sort(tasks):
    graph, in_degree = build_graph(tasks)
    task_map = {task.name: task for task in tasks}
    queue = deque([task.name for task in tasks if in_degree[task.name] == 0])
    sorted_tasks = []

    # Topological sort
    while queue:
        current = queue.popleft()
        sorted_tasks.append(task_map[current])
        for dependent in graph[current]:
            in_degree[dependent] -= 1
            if in_degree[dependent] == 0:
                queue.append(dependent)

    # Final sorting: Mandatory tasks first, then by value/duration ratio
    sorted_tasks = sorted(
        sorted_tasks,
        key=lambda t: (-t.mandatory, -(t.value / t.duration))
    )
    return sorted_tasks

# Step 3: Create a max heap for prioritizing tasks
def create_max_heap(sorted_tasks, available_time):
    max_heap = []
    for task in sorted_tasks:
        # Ensure the task meets the available time condition and prerequisites are handled
        if task.duration > 0 and (task.mandatory or available_time >= task.duration):
            heappush(max_heap, (-task.mandatory, -(task.value / task.duration), task))
    return max_heap

# Step 4: Prioritize tasks using a max heap
def prioritize_tasks(max_heap, available_time):
    selected_tasks = []
    current_time = 0

    while max_heap:
        _, _, task = heappop(max_heap)  # Updated to handle extra tuple field for mandatory flag

        if current_time + task.duration <= available_time:
            # Fully pick the task if it fits within the available time
            selected_tasks.append(task)
            current_time += task.duration
        elif task.fractionable:
            # Handle fractionable tasks by taking as much as possible
            fraction = (available_time - current_time) / task.duration if current_time < available_time else 0
            selected_tasks.append(
                Task(f"{task.name} (Partial)", task.value * fraction, available_time - current_time, [], task.mandatory, task.fractionable)
            )
            current_time = available_time  # Exhaust available time
        else:
            # Include non-fractionable tasks regardless of available time
            selected_tasks.append(Task(f"{task.name} (Exceeds Time)", task.value, task.duration, [], task.mandatory, task.fractionable))
            break

    return selected_tasks

# Visualize prioritized tasks
def visualize_prioritized_tasks(selected_tasks):
    task_names = [task.name for task in selected_tasks]
    task_durations = [task.duration for task in selected_tasks]

    plt.figure(figsize=(10, 5))
    plt.barh(task_names, task_durations, color='lightcoral')
    plt.xlabel("Time (hours)")
    plt.ylabel("Tasks")
    plt.title("Prioritized Tasks Including High-Priority Overflow")
    plt.gca().invert_yaxis()  # Invert y-axis for priority order
    plt.show()

# Main execution
available_time = 69 # Update available time
sorted_tasks = topological_sort(tasks)  # Topologically sorted tasks
max_heap = create_max_heap(sorted_tasks, available_time)  # Max heap of tasks
selected_tasks = prioritize_tasks(max_heap, available_time)  # Prioritize tasks

# Visualize the prioritized tasks
visualize_prioritized_tasks(selected_tasks)



# In[ ]:




