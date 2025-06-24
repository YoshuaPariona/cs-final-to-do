// ===== APPLICATION STATE MANAGEMENT =====
const AppState = {
    currentUser: null,
    currentPage: 'dashboard',
    users: [],
    tasks: [],
    events: [],
    settings: {}
};

// ===== USER AUTHENTICATION MODULE =====
const UserAuth = {
    // Initialize authentication system
    init() {
        this.checkExistingSession();
        this.setupEventListeners();
    },

    // Check for existing user session
    checkExistingSession() {
        const savedUser = localStorage.getItem('currentUser');
        if (savedUser) {
            try {
                AppState.currentUser = JSON.parse(savedUser);
                this.showApp();
            } catch (error) {
                console.error('Error parsing saved user:', error);
                this.showLogin();
            }
        } else {
            this.showLogin();
        }
    },

    // Setup authentication event listeners
    setupEventListeners() {
        // Login form events
        const loginForm = document.getElementById('loginForm');
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');

        loginForm.addEventListener('submit', this.handleLogin.bind(this));
        emailInput.addEventListener('blur', this.validateEmail.bind(this));
        passwordInput.addEventListener('blur', this.validatePassword.bind(this));
        emailInput.addEventListener('input', this.clearEmailError.bind(this));
        passwordInput.addEventListener('input', this.clearPasswordError.bind(this));

        // Signup form events
        const signupForm = document.getElementById('signupForm');
        if (signupForm) {
            signupForm.addEventListener('submit', this.handleSignup.bind(this));
            document.getElementById('signupName').addEventListener('input', this.clearSignupNameError.bind(this));
            document.getElementById('signupEmail').addEventListener('input', this.clearSignupEmailError.bind(this));
            document.getElementById('signupPassword').addEventListener('input', this.clearSignupPasswordError.bind(this));
        }

        // Switch between login and signup
        const switchToSignup = document.querySelectorAll('.btn-link[onclick="showSignup()"]');
        switchToSignup.forEach(btn => btn.addEventListener('click', showSignup));
        const switchToLogin = document.querySelectorAll('.btn-link[onclick="showLogin()"]');
        switchToLogin.forEach(btn => btn.addEventListener('click', showLogin));
    },

    // Handle login form submission
    async handleLogin(event) {
        event.preventDefault();
        
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();
        
        // Validate inputs
        const isEmailValid = this.validateEmail();
        const isPasswordValid = this.validatePassword();
        
        if (!isEmailValid || !isPasswordValid) {
            return;
        }
        
        // Show loading state
        this.showLoadingState();
        
        const response = await window.pywebview.api.get_item("get_user", {email, password});
        const data = response.user;

        if (response.success && data) {
            AppState.currentUser = {
                email: data.email,
                name: data.name,
                role: data.role || "user",
                loginTime: new Date().toISOString()
            };
            // Cargar tareas desde backend
            const tasksResp = await window.pywebview.api.get_item('get_tasks', {});
            if (tasksResp.success) {
                // Usar los campos tal como los entrega el backend: id, name, description, priority, status, start_date, end_date, created_at, completed_at
                AppState.tasks = (tasksResp.tasks || []).map(t => ({
                    id: t.id,
                    name: t.name, // Usar 'name' en vez de 'title' para consistencia con backend
                    description: t.description,
                    priority: t.priority,
                    status: t.status,
                    start_date: t.start_date,
                    end_date: t.end_date,
                    created_at: t.created_at,
                    completed_at: t.completed_at
                }));
            } else {
                AppState.tasks = [];
            }
            this.showApp();
        } else {
            this.showLoginError('Invalid email or password. Please try again.');
        }
        
        this.hideLoadingState();
    },

    // Handle signup form submission
    async handleSignup(event) {
        event.preventDefault();

        const name = document.getElementById('signupName').value.trim();
        const email = document.getElementById('signupEmail').value.trim();
        const password = document.getElementById('signupPassword').value.trim();

        let valid = true;
        if (!name) {
            this.showFieldError('signupName', document.getElementById('signupNameError'), 'Name is required');
            valid = false;
        }
        if (!this.validateSignupEmail()) valid = false;
        if (!this.validateSignupPassword()) valid = false;
        if (!valid) return;

        // Check if user already exists
        const response = await window.pywebview.api.add_item("create_user", {name, email, password})

        if (!response.success) {
            this.showFieldError('signupEmail', document.getElementById('signupPasswordError'), response.message);
            return;
        }

        showLogin();
    },

    // Email validation
    validateEmail() {
        const email = document.getElementById('email').value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const errorElement = document.getElementById('emailError');
        
        if (!email) {
            this.showFieldError('email', errorElement, 'Email is required');
            return false;
        } else if (!emailRegex.test(email)) {
            this.showFieldError('email', errorElement, 'Please enter a valid email address');
            return false;
        } else {
            this.hideFieldError('email', errorElement);
            return true;
        }
    },

    // Password validation
    validatePassword() {
        const password = document.getElementById('password').value.trim();
        const errorElement = document.getElementById('passwordError');
        
        if (!password) {
            this.showFieldError('password', errorElement, 'Password is required');
            return false;
        } else {
            this.hideFieldError('password', errorElement);
            return true;
        }
    },

    // Signup email validation
    validateSignupEmail() {
        const email = document.getElementById('signupEmail').value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const errorElement = document.getElementById('signupEmailError');
        if (!email) {
            this.showFieldError('signupEmail', errorElement, 'Email is required');
            return false;
        } else if (!emailRegex.test(email)) {
            this.showFieldError('signupEmail', errorElement, 'Please enter a valid email address');
            return false;
        } else {
            this.hideFieldError('signupEmail', errorElement);
            return true;
        }
    },

    // Signup password validation
    validateSignupPassword() {
        const password = document.getElementById('signupPassword').value.trim();
        const errorElement = document.getElementById('signupPasswordError');
        if (!password) {
            this.showFieldError('signupPassword', errorElement, 'Password is required');
            return false;
        } else if (password.length < 6) {
            this.showFieldError('signupPassword', errorElement, 'Password must be at least 6 characters');
            return false;
        } else {
            this.hideFieldError('signupPassword', errorElement);
            return true;
        }
    },

    // Clear email error
    clearEmailError() {
        const errorElement = document.getElementById('emailError');
        this.hideFieldError('email', errorElement);
    },

    // Clear password error
    clearPasswordError() {
        const errorElement = document.getElementById('passwordError');
        this.hideFieldError('password', errorElement);
    },

    // Clear signup errors
    clearSignupNameError() {
        this.hideFieldError('signupName', document.getElementById('signupNameError'));
    },
    clearSignupEmailError() {
        this.hideFieldError('signupEmail', document.getElementById('signupEmailError'));
    },
    clearSignupPasswordError() {
        this.hideFieldError('signupPassword', document.getElementById('signupPasswordError'));
    },

    // Show field error
    showFieldError(fieldId, errorElement, message) {
        const input = document.getElementById(fieldId);
        input.classList.add('error');
        errorElement.textContent = message;
    },

    // Hide field error
    hideFieldError(fieldId, errorElement) {
        const input = document.getElementById(fieldId);
        input.classList.remove('error');
        errorElement.textContent = '';
    },

    // Show login error
    showLoginError(message) {
        alert(message); // In production, use a better notification system
    },

    // Show loading state
    showLoadingState() {
        const button = document.getElementById('loginButton');
        const buttonText = button.querySelector('.button-text');
        const spinner = button.querySelector('.loading-spinner');
        
        button.disabled = true;
        buttonText.style.display = 'none';
        spinner.style.display = 'block';
    },
    showSignup() {
        document.getElementById('loginPage').style.display = 'none';
        document.getElementById('signupPage').style.display = 'flex';
        document.getElementById('signupForm').reset();
        // Limpia errores si tienes funciones para ello
    },

    showLogin() {
        document.getElementById('signupPage').style.display = 'none';
        document.getElementById('loginPage').style.display = 'flex';
        document.getElementById('loginForm').reset();
        this.clearEmailError();
        this.clearPasswordError();
        this.hideLoadingState();
    },
    // Hide loading state
    hideLoadingState() {
        const button = document.getElementById('loginButton');
        const buttonText = button.querySelector('.button-text');
        const spinner = button.querySelector('.loading-spinner');
        
        button.disabled = false;
        buttonText.style.display = 'block';
        spinner.style.display = 'none';
    },

    // Load user-specific data
    loadUserData() {
        // Ya no se usa localStorage para tareas
        // Las tareas se cargan desde el backend al iniciar sesión
        // Esta función puede quedar vacía o solo para settings/eventos si se desea
    },

    // Initialize default tasks
    initializeDefaultTasks() {
        AppState.tasks = [
            {
                id: 1,
                title: 'Fix Critical Bug in Payment System',
                description: 'Resolve the payment processing error that\'s affecting customer transactions.',
                priority: 'high',
                status: 'new',
                createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString() // 2 hours ago
            },
        ];
    },

    // Initialize default events
    initializeDefaultEvents() {
        AppState.events = [
            {
                id: 1,
                title: 'Project Deadline',
                description: 'Website redesign completion',
                date: '2024-12-15',
                time: '23:59',
                priority: 'high'
            },
        ];
    },

    // Save user-specific data
    saveUserData() {
        if (!AppState.currentUser) return;
        
        const userKey = `userData_${AppState.currentUser.email}`;
        const userData = {
            tasks: AppState.tasks,
            events: AppState.events,
            settings: AppState.settings
        };
        
        localStorage.setItem(userKey, JSON.stringify(userData));
    },

    // Show login page
    showLogin() {
        document.getElementById('loginPage').style.display = 'flex';
        document.getElementById('appContainer').style.display = 'none';
        
        // Clear form
        document.getElementById('loginForm').reset();
        this.clearEmailError();
        this.clearPasswordError();
    },

    // Show main application
    showApp() {
        document.getElementById('loginPage').style.display = 'none';
        document.getElementById('appContainer').style.display = 'flex';
        
        // Update user profile display
        this.updateUserProfile();
        
        // Initialize other modules
        Navigation.init();
        TaskManager.init();
        CalendarManager.init();
        SettingsManager.init();
    },

    // Update user profile display
    updateUserProfile() {
        if (!AppState.currentUser) return;
        
        const userAvatar = document.getElementById('userAvatar');
        const userName = document.getElementById('userName');
        const userEmail = document.getElementById('userEmail');
        
        userAvatar.textContent = AppState.currentUser.name.charAt(0).toUpperCase();
        userName.textContent = AppState.currentUser.name;
        userEmail.textContent = AppState.currentUser.email;
    },

    // Logout function
    logout() {
        // Clear session
        AppState.currentUser = null;
        localStorage.removeItem('currentUser');
        this.showLogin();
        this.hideLoadingState();
    }
};

// ===== NAVIGATION MODULE =====
const Navigation = {
    // Initialize navigation system
    init() {
        this.setupEventListeners();
        this.showPage('dashboard'); // Default page
    },

    // Setup navigation event listeners
    setupEventListeners() {
        const navItems = document.querySelectorAll('.nav-item');
        navItems.forEach(item => {
            item.addEventListener('click', this.handleNavigation.bind(this));
        });
    },

    // Handle navigation between pages
    handleNavigation(event) {
        event.preventDefault();
        
        const clickedItem = event.currentTarget;
        const page = clickedItem.dataset.page;
        
        // Update active navigation item
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.remove('active');
        });
        clickedItem.classList.add('active');
        
        // Show selected page
        this.showPage(page);
        
        AppState.currentPage = page;
    },

    // Show specific page content
    async showPage(pageId) {
        // Hide all pages
        document.querySelectorAll('.page-content').forEach(page => {
            page.classList.remove('active');
        });
        
        // Show selected page
        const targetPage = document.getElementById(`${pageId}Page`);
        if (targetPage) {
            targetPage.classList.add('active');
        }
        
        // Update page-specific content
        await this.updatePageContent(pageId);
    },

    // Update page-specific content
    async updatePageContent(pageId) {
        switch(pageId) {
            case 'dashboard':
                this.updateDashboard();
                break;
            case 'tasks':
                await TaskManager.loadTasksFromBackend();
                TaskManager.renderTasks();
                break;
            case 'calendar':
                CalendarManager.render();
                break;
            case 'settings':
                SettingsManager.loadSettings();
                break;
        }
    },

    // Update dashboard content
    updateDashboard() {
        // Update dashboard stats
        const stats = TaskManager.getTaskStats();
        const statCards = document.querySelectorAll('.stat-card');
        if (statCards.length >= 4) {
            statCards[0].querySelector('.stat-number').textContent = stats.total;
            statCards[1].querySelector('.stat-number').textContent = stats.completed;
            statCards[2].querySelector('.stat-number').textContent = stats.inProgress;
            statCards[3].querySelector('.stat-number').textContent = stats.new;
        }
        // Render recent tasks
        TaskManager.renderRecentTasks();
        console.log('Dashboard updated for user:', AppState.currentUser.email);
    }
};

// ===== TASK MANAGER MODULE =====
const TaskManager = {
    currentEditingTask: null,

    // Inicializar y cargar tareas desde backend
    async init() {
        await this.loadTasksFromBackend();
        this.setupEventListeners();
        this.renderTasks();
    },

    async loadTasksFromBackend() {
        const response = await window.pywebview.api.get_item('get_tasks', {});
        if (response.success) {
            AppState.tasks = (response.tasks || []).map(t => ({
                id: t.id,
                title: t.name,
                description: t.description,
                priority: t.priority,
                status: t.status,
                start_date: t.start_date,
                end_date: t.end_date,
                createdAt: t.created_at,
                completedAt: t.completed_at
            }));
        } else {
            AppState.tasks = [];
        }
    },

    // Setup task event listeners
    setupEventListeners() {
        // Close modals when clicking outside
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal();
            }
        });
        // Close task menus when clicking outside
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.task-actions-menu')) {
                document.querySelectorAll('.task-menu').forEach(menu => {
                    menu.classList.remove('show');
                });
            }
        });
    },

    // Get task statistics
    getTaskStats() {
        const total = AppState.tasks.length;
        const completed = AppState.tasks.filter(task => task.status === 'completed').length;
        const inProgress = AppState.tasks.filter(task => task.status === 'progress').length;
        const newTasks = AppState.tasks.filter(task => task.status === 'new').length;
        return { total, completed, inProgress, new: newTasks };
    },

    // Render all tasks
    renderTasks() {
        // Render encabezados y tareas por estado
        this.renderSectionWithHeader('new', 'Nuevas');
        this.renderSectionWithHeader('progress', 'En Proceso');
        this.renderSectionWithHeader('completed', 'Completadas');
        this.updateTaskCounts();
        // Sincronizar dashboard
        if (typeof TaskManager.renderRecentTasks === 'function') {
            TaskManager.renderRecentTasks();
        }
    },

    renderSectionWithHeader(status, label) {
        const container = document.getElementById(`${status}TasksContainer`);
        if (!container) return;
        // Encabezado: buscar el .section-title dentro del .section-header padre
        const sectionHeader = container.parentElement.querySelector('.section-header');
        if (sectionHeader) {
            const titleElem = sectionHeader.querySelector('.section-title');
            if (titleElem) titleElem.textContent = label;
        }
        // Render tareas
        const tasks = AppState.tasks.filter(task => task.status === status);
        this.renderTaskCards(tasks, container, status);
        console.log(`[TaskManager] Rendered ${tasks.length} tasks for status: ${status}`);
    },

    // Render tasks by status
    renderTasksByStatus(status) {
        const container = document.getElementById(`${status}TasksContainer`);
        if (!container) return;
        const tasks = AppState.tasks.filter(task => task.status === status);
        this.renderTaskCards(tasks, container, status);
        console.log(`[TaskManager] Rendered ${tasks.length} tasks for status: ${status}`);
    },

    // Render a list of tasks in a given container (dashboard style)
    renderTaskCards(tasks, container, status = null) {
        container.innerHTML = '';
        if (tasks.length === 0) {
            let label = 'tasks';
            if (status === 'new') label = 'new tasks';
            else if (status === 'progress') label = 'in progress tasks';
            else if (status === 'completed') label = 'completed tasks';
            container.innerHTML = `<div style='color:#64748b;'>No ${label}.</div>`;
            return;
        }
        tasks.forEach(task => {
            const card = document.createElement('div');
            card.className = `task-card ${task.status}`;
            card.dataset.taskId = task.id;
            // Botones de acción según el estado
            let actions = '';
            if (status === 'new') {
                actions = `
                    <button class="btn-move-progress" onclick="TaskManager.moveTask(${task.id}, 'progress')">Mover a En Proceso</button>
                    <button class="btn-move-completed" onclick="TaskManager.moveTask(${task.id}, 'completed')">Completar</button>
                `;
            } else if (status === 'progress') {
                actions = `
                    <button class="btn-move-new" onclick="TaskManager.moveTask(${task.id}, 'new')">Mover a Nuevas</button>
                    <button class="btn-move-completed" onclick="TaskManager.moveTask(${task.id}, 'completed')">Completar</button>
                `;
            } else if (status === 'completed') {
                actions = `
                    <button class="btn-move-new" onclick="TaskManager.moveTask(${task.id}, 'new')">Mover a Nuevas</button>
                    <button class="btn-move-progress" onclick="TaskManager.moveTask(${task.id}, 'progress')">Mover a En Proceso</button>
                `;
            }
            card.innerHTML = `
                <div class="task-header">
                    <h3 class="task-title">${task.title}</h3>
                    ${task.status === 'completed' ? '<span class="task-status">✓</span>' : ''}
                </div>
                <p class="task-description">${task.description || ''}</p>
                <div class="task-footer">
                    <span class="task-time">${task.status === 'completed' ? 'Completed ' + Utils.formatDate(task.completedAt) : task.status === 'progress' ? 'Started ' + Utils.formatDate(task.createdAt) : 'Created ' + Utils.formatDate(task.createdAt)}</span>
                    <span class="task-priority ${task.priority}">${this.getPriorityLabel(task.priority)}</span>
                </div>
                <div class="task-actions">${actions}</div>
            `;
            container.appendChild(card);
        });
    },

    // Get priority label
    getPriorityLabel(priority) {
        const labels = {
            'high': 'High Priority',
            'normal': 'Normal Priority',
            'postponable': 'Low Priority'
        };
        return labels[priority] || 'Normal Priority';
    },

    // Toggle task menu
    toggleTaskMenu(button) {
        const menu = button.nextElementSibling;
        const isVisible = menu.classList.contains('show');
        document.querySelectorAll('.task-menu').forEach(m => m.classList.remove('show'));
        if (!isVisible) {
            menu.classList.add('show');
        }
    },

    // Move task to different status
    async moveTask(taskId, newStatus) {
        let statusMsg = '';
        let cardElem = document.querySelector(`.task-card[data-task-id='${taskId}']`);
        // Realizar el cambio de estado
        let response;
        if (newStatus === 'completed') {
            response = await window.pywebview.api.toggle_item('complete_task', { task_id: taskId });
        } else {
            const task = AppState.tasks.find(t => t.id === taskId);
            if (!task) return;
            response = await window.pywebview.api.update_item('update_task', {
                task_id: taskId,
                name: task.title,
                description: task.description,
                start_date: task.start_date,
                end_date: task.end_date,
                priority: task.priority,
                status: newStatus
            });
        }
        // Usar el status retornado si está disponible
        const updatedStatus = response && response.updated_status ? response.updated_status : newStatus;
        if (updatedStatus === 'completed') statusMsg = 'Tarea completada';
        else if (updatedStatus === 'progress') statusMsg = 'Tarea movida a En Proceso';
        else if (updatedStatus === 'new') statusMsg = 'Tarea movida a Nuevas';
        if (response && response.success) {
            await this.loadTasksFromBackend();
            this.renderTasks();
        }
        document.querySelectorAll('.task-menu').forEach(menu => menu.classList.remove('show'));
        // Mostrar mensaje de actualización de estado
        if (cardElem && statusMsg) {
            const msg = document.createElement('div');
            msg.className = 'status-update-msg';
            msg.textContent = statusMsg;
            cardElem.insertAdjacentElement('afterend', msg);
            setTimeout(() => { msg.remove(); }, 2000);
        }
    },

    // Edit task
    editTask(taskId) {
        const task = AppState.tasks.find(t => t.id === taskId);
        if (!task) return;
        this.currentEditingTask = task;
        document.getElementById('taskTitle').value = task.title;
        document.getElementById('taskDescription').value = task.description;
        document.getElementById('taskPriority').value = task.priority;
        document.getElementById('taskStatus').value = task.status;
        document.getElementById('modalTitle').textContent = 'Edit Task';
        document.getElementById('taskModal').style.display = 'flex';
        document.querySelectorAll('.task-menu').forEach(menu => menu.classList.remove('show'));
    },

    // Delete task
    async deleteTask(taskId) {
        if (confirm('Are you sure you want to delete this task?')) {
            const response = await window.pywebview.api.remove_item('delete_task', { task_id: taskId });
            if (response.success) {
                await this.loadTasksFromBackend();
                this.renderTasks();
            }
        }
        document.querySelectorAll('.task-menu').forEach(menu => menu.classList.remove('show'));
    },

    // Show add task modal
    showAddTaskModal() {
        this.currentEditingTask = null;
        document.getElementById('taskForm').reset();
        document.getElementById('modalTitle').textContent = 'Add New Task';
        document.getElementById('taskModal').style.display = 'flex';
    },

    // Close task modal
    closeModal() {
        document.getElementById('taskModal').style.display = 'none';
        this.currentEditingTask = null;
    },

    // Save task
    async saveTask() {
        const title = document.getElementById('taskTitle').value.trim();
        const description = document.getElementById('taskDescription').value.trim();
        const priority = document.getElementById('taskPriority').value;
        const status = document.getElementById('taskStatus').value;
        const now = new Date().toISOString();
        let start_date = now;
        let end_date = now;
        if (this.currentEditingTask) {
            start_date = this.currentEditingTask.start_date || now;
            end_date = this.currentEditingTask.end_date || now;
        }
        if (!title) {
            alert('Please enter a task title');
            return;
        }
        let response;
        if (this.currentEditingTask) {
            response = await window.pywebview.api.update_item('update_task', {
                task_id: this.currentEditingTask.id,
                name: title,
                description,
                start_date,
                end_date,
                priority,
                status
            });
        } else {
            response = await window.pywebview.api.add_item('create_task', {
                name: title,
                description,
                start_date,
                end_date,
                priority,
                status
            });
        }
        if (response && response.success) {
            await this.loadTasksFromBackend();
            this.renderTasks();
            // Mostrar mensaje de estado si está disponible
            let statusMsg = '';
            const createdStatus = response.created_status;
            if (createdStatus === 'completed') statusMsg = 'Tarea creada como completada';
            else if (createdStatus === 'progress') statusMsg = 'Tarea creada en En Proceso';
            else if (createdStatus === 'new') statusMsg = 'Tarea creada como Nueva';
            if (statusMsg) {
                const msg = document.createElement('div');
                msg.className = 'status-update-msg';
                msg.textContent = statusMsg;
                // Insertar mensaje al inicio del contenedor correspondiente
                const container = document.getElementById(`${createdStatus}TasksContainer`);
                if (container) {
                    container.insertAdjacentElement('afterbegin', msg);
                    setTimeout(() => { msg.remove(); }, 2000);
                }
            }
        }
        this.closeModal();
    },

    // Update task counts
    updateTaskCounts() {
        const stats = this.getTaskStats();
        const newCount = document.getElementById('newTasksCount');
        const progressCount = document.getElementById('progressTasksCount');
        const completedCount = document.getElementById('completedTasksCount');
        if (newCount) newCount.textContent = stats.new;
        if (progressCount) progressCount.textContent = stats.inProgress;
        if (completedCount) completedCount.textContent = stats.completed;
    },

    renderRecentTasks() {
        const container = document.getElementById('recentTasksGrid');
        if (!container) return;
        // Ordenar por fecha de creación o completado (la más reciente primero)
        const tasksSorted = [...AppState.tasks].sort((a, b) => {
            const dateA = a.completedAt || a.createdAt;
            const dateB = b.completedAt || b.createdAt;
            return new Date(dateB) - new Date(dateA);
        });
        // Tomar las 3 más recientes
        const recentTasks = tasksSorted.slice(0, 3);
        container.innerHTML = '';
        if (recentTasks.length === 0) {
            container.innerHTML = '<div style="color:#64748b;">No recent tasks.</div>';
            return;
        }
        recentTasks.forEach(task => {
            const card = document.createElement('div');
            card.className = `task-card ${task.status}`;
            card.innerHTML = `
                <div class="task-header">
                    <h3 class="task-title">${task.title}</h3>
                    ${task.status === 'completed' ? '<span class="task-status">✓</span>' : ''}
                </div>
                <p class="task-description">${task.description || ''}</p>
                <div class="task-footer">
                    <span class="task-time">${task.status === 'completed' ? 'Completed ' + Utils.formatDate(task.completedAt) : 'Created ' + Utils.formatDate(task.createdAt)}</span>
                    <span class="task-priority ${task.priority}">${this.getPriorityLabel(task.priority)}</span>
                </div>
            `;
            container.appendChild(card);
        });
    }
};

// ===== CALENDAR MANAGER MODULE =====
const CalendarManager = {
    currentDate: new Date(),
    events: [],
    
    init() {
        this.loadEvents();
        this.renderCalendar();
        this.renderMiniCalendar();
        this.setupEventListeners();
    },
    
    loadEvents() {
        // Ejemplo de eventos (luego se pueden cargar desde localStorage o API)
        this.events = [
            {
                title: 'Project Deadline',
                date: '2024-12-15',
                time: '23:59',
                priority: 'high'
            },
            {
                title: 'Team Meeting',
                date: '2024-12-20',
                time: '14:00',
                priority: 'normal'
            },
            {
                title: 'Code Review Session',
                date: '2024-12-22',
                time: '10:00',
                priority: 'low'
            }
        ];
    },

    renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();
        
        // Actualizar título del mes
        document.getElementById('currentMonth').textContent = 
            this.currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
        
        const firstDay = new Date(year, month, 1);
        const lastDay = new Date(year, month + 1, 0);
        const daysContainer = document.getElementById('calendarDays');
        daysContainer.innerHTML = '';
        
        // Agregar días vacíos al inicio
        for (let i = 0; i < firstDay.getDay(); i++) {
            daysContainer.appendChild(this.createDayElement(''));
        }
        
        // Agregar días del mes
        for (let day = 1; day <= lastDay.getDate(); day++) {
            const dateStr = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const dayEvents = this.events.filter(event => event.date === dateStr);
            
            const dayElement = this.createDayElement(day, dayEvents);
            daysContainer.appendChild(dayElement);
        }
    },

    createDayElement(day, events = []) {
        const div = document.createElement('div');
        div.className = 'calendar-day';
        
        if (day !== '') {
            div.innerHTML = `
                <span class="day-number">${day}</span>
                ${events.length > 0 ? this.createEventIndicators(events) : ''}
            `;
            
            if (events.length > 0) {
                div.classList.add('has-events');
            }
        }
        
        return div;
    },

    createEventIndicators(events) {
        return `
            <div class="event-indicators">
                ${events.map(event => `
                    <div class="event-dot ${event.priority}-priority" 
                         title="${event.title}"></div>
                `).join('')}
            </div>
        `;
    }
};

// ===== SETTINGS MANAGER MODULE =====
const SettingsManager = {
    // Initialize settings manager
    init() {
        this.loadSettings();
    },

    // Load user settings
    loadSettings() {
        const displayName = document.getElementById('displayName');
        const userEmailSetting = document.getElementById('userEmailSetting');
        if (AppState.currentUser) {
            if (displayName) displayName.value = AppState.settings.displayName || AppState.currentUser.name;
            if (userEmailSetting) userEmailSetting.value = AppState.currentUser.email;
        }
    },

    // Save user settings
    saveSettings() {
        const displayName = document.getElementById('displayName');
        if (displayName) {
            AppState.settings.displayName = displayName.value;
            AppState.currentUser.name = displayName.value;
        }
        UserAuth.saveUserData();
        UserAuth.updateUserProfile();
        alert('Settings saved successfully!');
    }
};

// ===== UTILITY FUNCTIONS =====
const Utils = {
    // Format date for display
    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diffTime = Math.abs(now - date);
        const diffHours = Math.floor(diffTime / (1000 * 60 * 60));
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        
        if (diffHours < 1) {
            return 'Just now';
        } else if (diffHours < 24) {
            return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
        } else if (diffDays === 1) {
            return 'Yesterday';
        } else if (diffDays < 7) {
            const weeks = Math.floor(diffDays / 7);
            return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
        } else if (diffDays < 30) {
            const months = Math.floor(diffDays / 30);
            return `${months} month${months > 1 ? 's' : ''} ago`;
        } else {
            const years = Math.floor(diffDays / 365);
            return `${years} year${years > 1 ? 's' : ''} ago`;
        }
    },

    // Generate unique ID
    generateId() {
        return Date.now() + Math.random().toString(36).substr(2, 9);
    },

    // Debounce function for performance
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
};

// ===== PYWEBVIEW INTEGRATION API =====
window.PyWebViewAPI = {
    // Get current user information
    getCurrentUser() {
        return AppState.currentUser;
    },

    // Get all user data
    getUserData() {
        return {
            user: AppState.currentUser,
            tasks: AppState.tasks,
            events: AppState.events,
            settings: AppState.settings
        };
    },

    // Set user data from Python
    setUserData(userData) {
        if (userData.tasks) AppState.tasks = userData.tasks;
        if (userData.events) AppState.events = userData.events;
        if (userData.settings) AppState.settings = userData.settings;
        
        // Refresh current page
        Navigation.updatePageContent(AppState.currentPage);
    },

    // Navigate to specific page
    navigateToPage(pageId) {
        Navigation.showPage(pageId);
    },

    // Add new task from Python
    addTask(taskData) {
        const newTask = {
            id: Utils.generateId(),
            title: taskData.title,
            description: taskData.description || '',
            priority: taskData.priority || 'normal',
            status: taskData.status || 'new',
            createdAt: new Date().toISOString(),
            ...taskData
        };
        
        if (newTask.status === 'progress' && !newTask.progress) {
            newTask.progress = 0;
        } else if (newTask.status === 'completed') {
            newTask.completedAt = new Date().toISOString();
            newTask.progress = 100;
        }
        
        AppState.tasks.push(newTask);
        UserAuth.saveUserData();
        
        if (AppState.currentPage === 'tasks') {
            TaskManager.renderTasks();
        }
    },

    // Add new event from Python
    addEvent(eventData) {
        const newEvent = {
            id: Utils.generateId(),
            title: eventData.title,
            description: eventData.description || '',
            date: eventData.date,
            time: eventData.time,
            priority: eventData.priority || 'normal',
            ...eventData
        };
        
        AppState.events.push(newEvent);
        UserAuth.saveUserData();
        
        if (AppState.currentPage === 'calendar') {
            CalendarManager.render();
        }
    },

    // Update settings from Python
    updateSettings(newSettings) {
        AppState.settings = { ...AppState.settings, ...newSettings };
        UserAuth.saveUserData();
        
        if (AppState.currentPage === 'settings') {
            SettingsManager.loadSettings();
        }
    },

    // Force logout
    forceLogout() {
        UserAuth.logout();
    },

    // Get application state
    getAppState() {
        return {
            currentUser: AppState.currentUser,
            currentPage: AppState.currentPage,
            isLoggedIn: !!AppState.currentUser
        };
    },

    // Get task statistics
    getTaskStats() {
        return TaskManager.getTaskStats();
    },

    // Update task progress
    updateTaskProgress(taskId, progress) {
        const task = AppState.tasks.find(t => t.id === taskId);
        if (task && task.status === 'progress') {
            task.progress = Math.min(100, Math.max(0, progress));
            
            if (task.progress === 100) {
                task.status = 'completed';
                task.completedAt = new Date().toISOString();
            }
            
            UserAuth.saveUserData();
            
            if (AppState.currentPage === 'tasks') {
                TaskManager.renderTasks();
            }
        }
    }
};

// ===== APPLICATION INITIALIZATION =====
document.addEventListener('DOMContentLoaded', function() {
    console.log('Todo App initializing...');
    
    // Initialize authentication system
    UserAuth.init();
    
    // Log successful initialization
    console.log('Todo App initialized successfully');
    console.log('PyWebView API available at window.PyWebViewAPI');
});

// ===== ERROR HANDLING =====
window.addEventListener('error', function(event) {
    console.error('Application error:', event.error);
    // In production, you might want to send this to your Python backend
});

// ===== EXPORT FOR PYTHON INTEGRATION =====
// Make modules available globally for Python integration
window.TodoApp = {
    UserAuth,
    Navigation,
    TaskManager,
    CalendarManager,
    SettingsManager,
    Utils,
    AppState
};

// ====== UI SWITCH FUNCTIONS ======
function showSignup() {
    document.getElementById('loginPage').style.display = 'none';
    document.getElementById('signupPage').style.display = 'flex';
    // Optionally reset the form and errors
    document.getElementById('signupForm').reset();
    UserAuth.clearSignupNameError();
    UserAuth.clearSignupEmailError();
    UserAuth.clearSignupPasswordError();
}
function showLogin() {
    document.getElementById('signupPage').style.display = 'none';
    document.getElementById('loginPage').style.display = 'flex';
    document.getElementById('loginForm').reset();
    UserAuth.clearEmailError();
    UserAuth.clearPasswordError();
}

// NOTA: El backend ahora entrega los campos de tarea como:
// id, name, description, priority, status, start_date, end_date, created_at, completed_at
// El mapeo de estados es: 'todo' → 'new', 'pending' → 'progress', 'completed' → 'completed'.
// Si necesitas agregar más mapeos, hazlo aquí o en el backend.
