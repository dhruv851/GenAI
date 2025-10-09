let isDarkMode = false;
const toggleDarkMode = () => {
  document.body.classList.toggle("dark-mode", isDarkMode);
  isDarkMode = !isDarkMode;
};
document.getElementById("add-todo").addEventListener("click", function() {
  const todoText = document.getElementById("new-todo").value;
  if (todoText) {
    const li = document.createElement("li");
    li.textContent = todoText;
    const removeBtn = document.createElement("button");
    removeBtn.textContent = "Remove";
    removeBtn.addEventListener("click", function() {
      li.remove();
    });
    li.appendChild(removeBtn);
    document.getElementById("todo-list").appendChild(li);
    document.getElementById("new-todo").value = "";
  }
});

const darkModeToggle = document.createElement("button");
darkModeToggle.textContent = "Toggle Dark Mode";
darkModeToggle.style.marginTop = "10px";
darkModeToggle.addEventListener("click", toggleDarkMode);
document.getElementById("app").appendChild(darkModeToggle);
