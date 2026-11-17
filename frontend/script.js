const API = "/api/tasks";

const taskForm = document.getElementById("taskForm");
const taskList = document.getElementById("taskList");
const message = document.getElementById("message");

function showMessage(text) {
    message.textContent = text;
}

async function loadTasks() {
    try {
        const response = await fetch(API);

        if (!response.ok) {
            throw new Error("Unable to load tasks");
        }

        const tasks = await response.json();

        taskList.replaceChildren();

        tasks.forEach(task => {
            const card = document.createElement("div");
            card.className = "task";

            const title = document.createElement("h3");
            title.textContent = task.title;

            const description = document.createElement("p");
            description.textContent = task.description || "";

            const status = document.createElement("p");
            status.textContent = `Status: ${task.status}`;

            const actions = document.createElement("div");
            actions.className = "task-actions";

            const select = document.createElement("select");

            ["Pending", "In Progress", "Completed"].forEach(value => {
                const option = document.createElement("option");
                option.value = value;
                option.textContent = value;
                option.selected = task.status === value;
                select.appendChild(option);
            });

            select.addEventListener("change", async () => {
                await fetch(`${API}/${task.id}`, {
                    method: "PATCH",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify({status: select.value})
                });
                loadTasks();
            });

            const deleteButton = document.createElement("button");
            deleteButton.className = "delete";
            deleteButton.textContent = "Delete";

            deleteButton.addEventListener("click", async () => {
                await fetch(`${API}/${task.id}`, {
                    method: "DELETE"
                });
                loadTasks();
            });

            actions.append(select, deleteButton);
            card.append(title, description, status, actions);
            taskList.appendChild(card);
        });

        if (tasks.length === 0) {
            showMessage("No tasks available. Create your first task!");
        } else {
            showMessage(`${tasks.length} task(s) found.`);
        }

    } catch (error) {
        showMessage(error.message);
    }
}

taskForm.addEventListener("submit", async event => {
    event.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    try {
        const response = await fetch(API, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({title, description})
        });

        if (!response.ok) {
            throw new Error("Unable to create task");
        }

        taskForm.reset();
        showMessage("Task created successfully!");
        await loadTasks();

    } catch (error) {
        showMessage(error.message);
    }
});

loadTasks();
