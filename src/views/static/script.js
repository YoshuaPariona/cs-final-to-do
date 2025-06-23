// ===== APPLICATION STATE MANAGEMENT =====
const AppState = {
    currentUser: null,
    currentPage: 'dashboard',
    users: [
        { email: 'admin@gmail.com', password: 'admin', name: 'Admin User', role: 'admin' },
        { email: 'user@example.com', password: 'user123', name: 'Regular User', role: 'user' }
    ],
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
        
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Check credentials against user database
        const user = AppState.users.find(u => u.email === email && u.password === password);
        
        if (user) {
            // Successful login
            AppState.currentUser = {
                email: user.email,
                name: user.name,
                role: user.role,
                loginTime: new Date().toISOString()
            };
            
            // Save session
            localStorage.setItem('currentUser', JSON.stringify(AppState.currentUser));
            
            // Load user-specific data
            this.loadUserData();
            
            // Show application
            this.showApp();
        } else {
            // Failed login
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
        if (AppState.users.some(u => u.email === email)) {
            this.showFieldError('signupEmail', document.getElementById('signupEmailError'), 'Email already registered');
            return;
        }

        // Add new user
        AppState.users.push({
            email,
            password,
            name,
            role: 'user'
        });

        alert('Account created successfully! You can now log in.');
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
        // Limpia errores si tienes funciones para ello
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
        const userKey = `userData_${AppState.currentUser.email}`;
        const savedData = localStorage.getItem(userKey);
        
        if (savedData) {
            try {
                const userData = JSON.parse(savedData);
                AppState.tasks = userData.tasks || [];
                AppState.events = userData.events || [];
                AppState.settings = userData.settings || {};
            } catch (error) {
                console.error('Error loading user data:', error);
            }
        }
        
        // Initialize with default data if empty
        if (AppState.tasks.length === 0) {
            this.initializeDefaultTasks();
        }
        
        if (AppState.events.length === 0) {
            this.initializeDefaultEvents();
        }
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
            {
                id: 2,
                title: 'Update API Documentation',
                description: 'Update API documentation with new endpoints and examples for the latest version.',
                priority: 'normal',
                status: 'new',
                createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString() // 1 day ago
            },
            {
                id: 3,
                title: 'Organize Team Building Event',
                description: 'Plan and organize the quarterly team building event for all departments.',
                priority: 'postponable',
                status: 'new',
                createdAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString() // 3 days ago
            },
            {
                id: 4,
                title: 'Security Audit Report',
                description: 'Complete the quarterly security audit and submit findings to management.',
                priority: 'high',
                status: 'progress',
                progress: 65,
                createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString() // 2 days ago
            },
            {
                id: 5,
                title: 'Mobile App Testing',
                description: 'Conduct comprehensive testing of the new mobile application features.',
                priority: 'normal',
                status: 'progress',
                progress: 40,
                createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString() // 1 week ago
            },
            {
                id: 6,
                title: 'Website Redesign',
                description: 'Complete the new landing page design and implement responsive layout for mobile devices.',
                priority: 'high',
                status: 'completed',
                completedAt: new Date(Date.now() - 60 * 24 * 60 * 60 * 1000).toISOString() // 2 months ago
            },
            {
                id: 7,
                title: 'Database Migration',
                description: 'Migrate user data from old database system to new PostgreSQL setup with improved performance.',
                priority: 'normal',
                status: 'completed',
                completedAt: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString() // 3 days ago
            },
            {
                id: 8,
                title: 'Code Review',
                description: 'Review pull requests for the authentication module and provide feedback to team members.',
                priority: 'postponable',
                status: 'completed',
                completedAt: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString() // 2 hours ago
            },
            {
                id: 9,
                title: 'Client Presentation',
                description: 'Prepare and deliver project presentation to client stakeholders.',
                priority: 'high',
                status: 'completed',
                completedAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000).toISOString() // 1 week ago
            }
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
            {
                id: 2,
                title: 'Team Meeting',
                description: 'Quarterly review meeting',
                date: '2024-12-20',
                time: '14:00',
                priority: 'normal'
            },
            {
                id: 3,
                title: 'Code Review Session',
                description: 'Weekly code review with team',
                date: '2024-12-22',
                time: '10:00',
                priority: 'low'
            }
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
        // Save current user data before logout
        this.saveUserData();
        
        // Clear session
        AppState.currentUser = null;
        localStorage.removeItem('currentUser');
        
        // Show login page
        this.showLogin();
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
    showPage(pageId) {
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
        this.updatePageContent(pageId);
    },

    // Update page-specific content
    updatePageContent(pageId) {
        switch(pageId) {
            case 'dashboard':
                this.updateDashboard();
                break;
            case 'tasks':
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
        
        console.log('Dashboard updated for user:', AppState.currentUser.email);
    }
};

// ===== TASK MANAGER MODULE =====
const TaskManager = {
    currentEditingTask: null,

    // Initialize task manager
    init() {
        this.setupEventListeners();
        this.renderTasks();
    },

    // Setup task event listeners
    setupEventListeners() {
        // Close modals when clicking outside
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal();
                this.closeEventModal();
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
        this.renderTasksByStatus('new');
        this.renderTasksByStatus('progress');
        this.renderTasksByStatus('completed');
        this.updateTaskCounts();
    },

    // Render tasks by status
    renderTasksByStatus(status) {
        const container = document.getElementById(`${status}TasksContainer`) || 
                         document.getElementById(`${status === 'progress' ? 'progress' : status}TasksContainer`);
        
        if (!container) return;
        
        const tasks = AppState.tasks.filter(task => task.status === status);
        container.innerHTML = '';
        
        tasks.forEach(task => {
            const taskCard = this.createTaskCard(task);
            container.appendChild(taskCard);
        });
    },

    // Create task card element
    createTaskCard(task) {
        const card = document.createElement('div');
        card.className = `task-card ${task.status}`;
        card.dataset.taskId = task.id;
        
        const timeText = task.status === 'completed' 
            ? `Completed ${Utils.formatDate(task.completedAt)}`
            : task.status === 'progress' 
                ? `Started ${Utils.formatDate(task.createdAt)}`
                : `Created ${Utils.formatDate(task.createdAt)}`;
        
        card.innerHTML = `
            <div class="task-header">
                <h3 class="task-title">${task.title}</h3>
                ${task.status === 'completed' 
                    ? '<span class="task-status">✓</span>'
                    : `<div class="task-actions-menu">
                        <button class="btn-menu" onclick="TaskManager.toggleTaskMenu(this)">⋮</button>
                        <div class="task-menu">
                            ${this.getTaskMenuItems(task)}
                        </div>
                    </div>`
                }
            </div>
            <p class="task-description">${task.description}</p>
            <div class="task-footer">
                <span class="task-time">${timeText}</span>
                <span class="task-priority ${task.priority}">${this.getPriorityLabel(task.priority)}</span>
            </div>
            ${task.status === 'progress' && task.progress ? `
                <div class="task-progress">
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: ${task.progress}%"></div>
                    </div>
                    <span class="progress-text">${task.progress}% Complete</span>
                </div>
            ` : ''}
        `;
        
        return card;
    },

    // Get task menu items based on status
    getTaskMenuItems(task) {
        const items = [];
        
        if (task.status === 'new') {
            items.push(`<button onclick="TaskManager.moveTask(${task.id}, 'progress')">Move to Progress</button>`);
        } else if (task.status === 'progress') {
            items.push(`<button onclick="TaskManager.moveTask(${task.id}, 'completed')">Mark Complete</button>`);
            items.push(`<button onclick="TaskManager.moveTask(${task.id}, 'new')">Move to New</button>`);
        }
        
        items.push(`<button onclick="TaskManager.editTask(${task.id})">Edit</button>`);
        items.push(`<button onclick="TaskManager.deleteTask(${task.id})">Delete</button>`);
        
        return items.join('');
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
        
        // Close all other menus
        document.querySelectorAll('.task-menu').forEach(m => m.classList.remove('show'));
        
        // Toggle current menu
        if (!isVisible) {
            menu.classList.add('show');
        }
    },

    // Move task to different status
    moveTask(taskId, newStatus) {
        const task = AppState.tasks.find(t => t.id === taskId);
        if (!task) return;
        
        task.status = newStatus;
        
        if (newStatus === 'completed') {
            task.completedAt = new Date().toISOString();
            task.progress = 100;
        } else if (newStatus === 'progress' && !task.progress) {
            task.progress = 0;
        }
        
        this.renderTasks();
        UserAuth.saveUserData();
        
        // Close menu
        document.querySelectorAll('.task-menu').forEach(menu => {
            menu.classList.remove('show');
        });
    },

    // Edit task
    editTask(taskId) {
        const task = AppState.tasks.find(t => t.id === taskId);
        if (!task) return;
        
        this.currentEditingTask = task;
        
        // Populate form with task data
        document.getElementById('taskTitle').value = task.title;
        document.getElementById('taskDescription').value = task.description;
        document.getElementById('taskPriority').value = task.priority;
        document.getElementById('taskStatus').value = task.status;
        document.getElementById('modalTitle').textContent = 'Edit Task';
        
        // Show modal
        document.getElementById('taskModal').style.display = 'flex';
        
        // Close menu
        document.querySelectorAll('.task-menu').forEach(menu => {
            menu.classList.remove('show');
        });
    },

    // Delete task
    deleteTask(taskId) {
        if (confirm('Are you sure you want to delete this task?')) {
            AppState.tasks = AppState.tasks.filter(t => t.id !== taskId);
            this.renderTasks();
            UserAuth.saveUserData();
        }
        
        // Close menu
        document.querySelectorAll('.task-menu').forEach(menu => {
            menu.classList.remove('show');
        });
    },

    // Show add task modal
    showAddTaskModal() {
        this.currentEditingTask = null;
        
        // Clear form
        document.getElementById('taskForm').reset();
        document.getElementById('modalTitle').textContent = 'Add New Task';
        
        // Show modal
        document.getElementById('taskModal').style.display = 'flex';
    },

    // Show add event modal
    showAddEventModal() {
        // Clear form
        document.getElementById('eventForm').reset();
        
        // Set default date to today
        const today = new Date().toISOString().split('T')[0];
        document.getElementById('eventDate').value = today;
        
        // Show modal
        document.getElementById('eventModal').style.display = 'flex';
    },

    // Close task modal
    closeModal() {
        document.getElementById('taskModal').style.display = 'none';
        this.currentEditingTask = null;
    },

    // Close event modal
    closeEventModal() {
        document.getElementById('eventModal').style.display = 'none';
    },

    // Save task
    saveTask() {
        const title = document.getElementById('taskTitle').value.trim();
        const description = document.getElementById('taskDescription').value.trim();
        const priority = document.getElementById('taskPriority').value;
        const status = document.getElementById('taskStatus').value;
        
        if (!title) {
            alert('Please enter a task title');
            return;
        }
        
        if (this.currentEditingTask) {
            // Update existing task
            this.currentEditingTask.title = title;
            this.currentEditingTask.description = description;
            this.currentEditingTask.priority = priority;
            this.currentEditingTask.status = status;
        } else {
            // Create new task
            const newTask = {
                id: Utils.generateId(),
                title,
                description,
                priority,
                status,
                createdAt: new Date().toISOString()
            };
            
            if (status === 'progress') {
                newTask.progress = 0;
            } else if (status === 'completed') {
                newTask.completedAt = new Date().toISOString();
                newTask.progress = 100;
            }
            
            AppState.tasks.push(newTask);
        }
        
        this.renderTasks();
        UserAuth.saveUserData();
        this.closeModal();
    },

    // Save event
    saveEvent() {
        const title = document.getElementById('eventTitle').value.trim();
        const description = document.getElementById('eventDescription').value.trim();
        const date = document.getElementById('eventDate').value;
        const time = document.getElementById('eventTime').value;
        const priority = document.getElementById('eventPriority').value;
        
        if (!title || !date || !time) {
            alert('Please fill in all required fields');
            return;
        }
        
        const newEvent = {
            id: Utils.generateId(),
            title,
            description,
            date,
            time,
            priority
        };
        
        AppState.events.push(newEvent);
        UserAuth.saveUserData();
        this.closeEventModal();
        
        // Refresh calendar if on calendar page
        if (AppState.currentPage === 'calendar') {
            CalendarManager.render();
        }
        
        alert('Event added successfully!');
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
        const timezone = document.getElementById('timezone');
        const emailNotifications = document.getElementById('emailNotifications');
        const darkMode = document.getElementById('darkMode');
        const autoSave = document.getElementById('autoSave');
        
        if (AppState.currentUser) {
            if (displayName) displayName.value = AppState.settings.displayName || AppState.currentUser.name;
            if (userEmailSetting) userEmailSetting.value = AppState.currentUser.email;
            if (timezone) timezone.value = AppState.settings.timezone || 'UTC';
            if (emailNotifications) emailNotifications.checked = AppState.settings.emailNotifications !== false;
            if (darkMode) darkMode.checked = AppState.settings.darkMode || false;
            if (autoSave) autoSave.checked = AppState.settings.autoSave !== false;
        }
        
        // Apply current theme
        this.applyTheme();
    },

    // Save user settings
    saveSettings() {
        const displayName = document.getElementById('displayName');
        const timezone = document.getElementById('timezone');
        const emailNotifications = document.getElementById('emailNotifications');
        const darkMode = document.getElementById('darkMode');
        const autoSave = document.getElementById('autoSave');
        
        AppState.settings = {
            displayName: displayName ? displayName.value : AppState.currentUser.name,
            timezone: timezone ? timezone.value : 'UTC',
            emailNotifications: emailNotifications ? emailNotifications.checked : true,
            darkMode: darkMode ? darkMode.checked : false,
            autoSave: autoSave ? autoSave.checked : true
        };
        
        // Save to localStorage
        UserAuth.saveUserData();
        
        // Apply theme
        this.applyTheme();
        
        // Show success message
        alert('Settings saved successfully!');
    },

    // Reset settings to default
    resetSettings() {
        if (confirm('Are you sure you want to reset all settings to default?')) {
            AppState.settings = {};
            this.loadSettings();
            UserAuth.saveUserData();
            alert('Settings reset to default values.');
        }
    },

    // Apply theme based on settings
    applyTheme() {
        if (AppState.settings.darkMode) {
            document.body.classList.add('dark-theme');
        } else {
            document.body.classList.remove('dark-theme');
        }
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
            return `${diffDays} days ago`;
        } else if (diffDays < 30) {
            const weeks = Math.floor(diffDays / 7);
            return `${weeks} week${weeks > 1 ? 's' : ''} ago`;
        } else if (diffDays < 365) {
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
