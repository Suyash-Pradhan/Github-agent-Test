(() => {
  const form = document.getElementById('todo-form');
  const input = document.getElementById('todo-input');
  const list = document.getElementById('todo-list');

  function loadTodos() {
    try {
      return JSON.parse(localStorage.getItem('todos') || '[]');
    } catch (e) {
      return [];
    }
  }

  function saveTodos(todos) {
    localStorage.setItem('todos', JSON.stringify(todos));
  }

  function render() {
    const todos = loadTodos();
    list.innerHTML = '';
    if (todos.length === 0) {
      const el = document.createElement('div');
      el.className = 'empty';
      el.textContent = 'No todos yet — add one!';
      list.appendChild(el);
      return;
    }

    todos.forEach((t, idx) => {
      const li = document.createElement('li');
      li.className = 'todo-item' + (t.done ? ' completed' : '');

      const left = document.createElement('div');
      left.className = 'left';

      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = !!t.done;
      cb.addEventListener('change', () => toggleDone(idx));

      const span = document.createElement('div');
      span.className = 'text';
      span.textContent = t.text;

      left.appendChild(cb);
      left.appendChild(span);

      const actions = document.createElement('div');
      actions.className = 'todo-actions';
      const del = document.createElement('button');
      del.textContent = 'Delete';
      del.addEventListener('click', () => deleteTodo(idx));

      actions.appendChild(del);

      li.appendChild(left);
      li.appendChild(actions);
      list.appendChild(li);
    });
  }

  function addTodo(text) {
    if (!text || !text.trim()) return;
    const todos = loadTodos();
    todos.unshift({text: text.trim(), done: false});
    saveTodos(todos);
    render();
  }

  function toggleDone(index) {
    const todos = loadTodos();
    if (!todos[index]) return;
    todos[index].done = !todos[index].done;
    saveTodos(todos);
    render();
  }

  function deleteTodo(index) {
    const todos = loadTodos();
    todos.splice(index, 1);
    saveTodos(todos);
    render();
  }

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    addTodo(input.value);
    input.value = '';
    input.focus();
  });

  // initial render
  render();
})();
