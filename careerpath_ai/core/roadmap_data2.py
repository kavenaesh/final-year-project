"""
core/roadmap_data2.py - Roadmap data Part 2: DevOps, Android, ECE, Backend
Merged into ROADMAPS dict from roadmap_data.py
"""
from core.roadmap_data import ROADMAPS

# ─── 5. DEVOPS & CLOUD ENGINEERING ────────────────────────────────────────────
ROADMAPS["devops"] = {
    "title": "DevOps & Cloud Engineering",
    "icon": "☁️",
    "description": "Automate, scale, and manage infrastructure with CI/CD, containers, and cloud platforms.",
    "difficulty": "Advanced",
    "duration": "14-20 months",
    "phases": [
        {
            "phase": "Phase 1: Linux & Scripting",
            "color": "#F0A500",
            "topics": [
                {
                    "name": "Linux Administration",
                    "required": True,
                    "description": "File system, processes, networking, systemd, shell scripting, SSH, cron jobs.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "Linux for Beginners - NetworkChuck (YouTube)", "url": "https://www.youtube.com/watch?v=GE47s_VRWPg", "type": "youtube"},
                            {"name": "Linux Journey (interactive, free)", "url": "https://linuxjourney.com/", "type": "website"},
                            {"name": "The Linux Command Line (free book)", "url": "https://linuxcommand.org/tlcl.php", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Bash Scripting & Python Automation",
                    "required": True,
                    "description": "Automate repetitive tasks with shell scripts and Python. Key for CI/CD pipelines.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "Bash Scripting Tutorial - freeCodeCamp", "url": "https://www.youtube.com/watch?v=tK9Oc6AEnR4", "type": "youtube"},
                            {"name": "Python Automation Cookbook (free chapters)", "url": "https://www.packtpub.com/product/python-automation-cookbook/9781789133806", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 2: Containers & Orchestration",
            "color": "#F0B500",
            "topics": [
                {
                    "name": "Docker",
                    "required": True,
                    "description": "Images, containers, Dockerfile, Docker Compose, registries, multi-stage builds.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "Docker Tutorial for Beginners - TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "type": "youtube"},
                            {"name": "Play with Docker (free browser-based labs)", "url": "https://labs.play-with-docker.com/", "type": "website"},
                        ],
                        "paid": [
                            {"name": "Docker & Kubernetes: Complete Guide - Udemy", "url": "https://www.udemy.com/course/docker-and-kubernetes-the-complete-guide/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Kubernetes",
                    "required": True,
                    "description": "Pods, deployments, services, ConfigMaps, namespaces, Helm charts, and auto-scaling.",
                    "time_estimate": "5-6 weeks",
                    "resources": {
                        "free": [
                            {"name": "Kubernetes for Beginners - TechWorld with Nana", "url": "https://www.youtube.com/watch?v=X48VuDVv0do", "type": "youtube"},
                            {"name": "Kubernetes Official Docs + Interactive Tutorial", "url": "https://kubernetes.io/docs/tutorials/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 3: CI/CD & Cloud",
            "color": "#F0C500",
            "topics": [
                {
                    "name": "CI/CD Pipelines (GitHub Actions / Jenkins)",
                    "required": True,
                    "description": "Automate build, test, and deploy workflows with GitHub Actions, Jenkins, or GitLab CI.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "GitHub Actions Tutorial - TechWorld with Nana", "url": "https://www.youtube.com/watch?v=R8_veQiYBjI", "type": "youtube"},
                            {"name": "GitHub Actions Docs", "url": "https://docs.github.com/en/actions", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "AWS / GCP / Azure",
                    "required": True,
                    "description": "EC2, S3, RDS, IAM (AWS); Compute Engine, Cloud Run (GCP); cloud architecture and certifications.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "AWS Cloud Practitioner - freeCodeCamp", "url": "https://www.youtube.com/watch?v=SOTamWNgDKc", "type": "youtube"},
                            {"name": "AWS Skill Builder (free tier)", "url": "https://explore.skillbuilder.aws/", "type": "website"},
                        ],
                        "paid": [
                            {"name": "AWS Certified Solutions Architect - Udemy (Stephane Maarek)", "url": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Infrastructure as Code (Terraform)",
                    "required": True,
                    "description": "Provision and manage cloud resources declaratively with Terraform and Ansible.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "Terraform Tutorial - freeCodeCamp", "url": "https://www.youtube.com/watch?v=SLB_c_ayRMo", "type": "youtube"},
                            {"name": "Terraform Docs Getting Started", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 4: Monitoring & Security",
            "color": "#F0D500",
            "topics": [
                {
                    "name": "Monitoring: Prometheus & Grafana",
                    "required": True,
                    "description": "Metrics collection, alerting, and visualization for production systems.",
                    "time_estimate": "2-3 weeks",
                    "resources": {
                        "free": [
                            {"name": "Prometheus & Grafana Tutorial - TechWorld with Nana", "url": "https://www.youtube.com/watch?v=h4Sl21AKiDg", "type": "youtube"},
                            {"name": "Prometheus Docs", "url": "https://prometheus.io/docs/introduction/overview/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
    ]
}

# ─── 6. ANDROID DEVELOPMENT ───────────────────────────────────────────────────
ROADMAPS["android"] = {
    "title": "Android App Development",
    "icon": "📱",
    "description": "Build native Android apps with Kotlin, Jetpack Compose, and publish to the Play Store.",
    "difficulty": "Intermediate",
    "duration": "10-14 months",
    "phases": [
        {
            "phase": "Phase 1: Kotlin Fundamentals",
            "color": "#A100FF",
            "topics": [
                {
                    "name": "Kotlin Programming",
                    "required": True,
                    "description": "Data types, OOP, lambdas, coroutines, extension functions, and null safety.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "Kotlin Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=F9UC9DY-vIU", "type": "youtube"},
                            {"name": "Kotlin Docs Official", "url": "https://kotlinlang.org/docs/getting-started.html", "type": "website"},
                            {"name": "Kotlin Koans (interactive)", "url": "https://play.kotlinlang.org/koans/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Android Studio Setup & Project Structure",
                    "required": True,
                    "description": "IDE setup, Gradle build system, project structure, emulator, and ADB.",
                    "time_estimate": "1-2 weeks",
                    "resources": {
                        "free": [
                            {"name": "Android Developer Fundamentals (Google, free)", "url": "https://developer.android.com/courses/fundamentals-training/overview-v2", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 2: UI Development",
            "color": "#B020FF",
            "topics": [
                {
                    "name": "Jetpack Compose",
                    "required": True,
                    "description": "Modern declarative UI toolkit. Composables, state, theming, navigation.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "Jetpack Compose Tutorial - Philipp Lackner (YouTube)", "url": "https://www.youtube.com/@PhilippLackner", "type": "youtube"},
                            {"name": "Compose Pathway - Google Codelabs (free)", "url": "https://developer.android.com/courses/jetpack-compose/course", "type": "website"},
                        ],
                        "paid": [
                            {"name": "Android Jetpack Compose - Udemy", "url": "https://www.udemy.com/course/jetpack-compose-masterclass/", "type": "udemy"},
                        ]
                    }
                },
            ]
        },
        {
            "phase": "Phase 3: Architecture & Backend Integration",
            "color": "#C040FF",
            "topics": [
                {
                    "name": "MVVM Architecture & ViewModel",
                    "required": True,
                    "description": "Clean architecture with ViewModel, LiveData, StateFlow, Repository pattern.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "Android Architecture - Philipp Lackner", "url": "https://www.youtube.com/watch?v=dlGkNUxmQHU", "type": "youtube"},
                            {"name": "Android Guide to App Architecture", "url": "https://developer.android.com/topic/architecture", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Room Database & Retrofit",
                    "required": True,
                    "description": "Local SQLite via Room ORM, and network calls via Retrofit with Coroutines.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "Room Database Tutorial - CodinginFlow", "url": "https://www.youtube.com/watch?v=ONniq7-g-GE", "type": "youtube"},
                            {"name": "Retrofit Tutorial - Philipp Lackner", "url": "https://www.youtube.com/watch?v=t6Sql3WMAnk", "type": "youtube"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Firebase Integration",
                    "required": False,
                    "description": "Authentication, Firestore, Cloud Messaging (FCM), Crashlytics.",
                    "time_estimate": "2-3 weeks",
                    "resources": {
                        "free": [
                            {"name": "Firebase for Android - Google Codelabs", "url": "https://firebase.google.com/codelabs/firebase-android", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Publish to Google Play Store",
                    "required": True,
                    "description": "Signed APK/AAB, Play Console setup, app review process, release management.",
                    "time_estimate": "1 week",
                    "resources": {
                        "free": [
                            {"name": "Publish Android App to Play Store - Tutorial", "url": "https://www.youtube.com/watch?v=5GHT4M0Ug6g", "type": "youtube"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
    ]
}

# ─── 7. ECE (ELECTRONICS & COMMUNICATION ENGINEERING) ────────────────────────
ROADMAPS["ece"] = {
    "title": "Electronics & Communication Engineering",
    "icon": "⚡",
    "description": "Design circuits, embedded systems, and communication networks. Core engineering path.",
    "difficulty": "Advanced",
    "duration": "24-36 months",
    "phases": [
        {
            "phase": "Phase 1: Core Electronics",
            "color": "#FF8C00",
            "topics": [
                {
                    "name": "Circuit Analysis & Electronic Devices",
                    "required": True,
                    "description": "KVL/KCL, Thevenin/Norton, diodes, BJT, MOSFET, op-amps, AC/DC circuits.",
                    "time_estimate": "8-10 weeks",
                    "resources": {
                        "free": [
                            {"name": "Circuit Analysis - Neso Academy (YouTube)", "url": "https://www.youtube.com/@nesoacademy", "type": "youtube"},
                            {"name": "All About Circuits (free textbook)", "url": "https://www.allaboutcircuits.com/textbook/", "type": "website"},
                            {"name": "MIT OpenCourseWare - Circuits & Electronics", "url": "https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Digital Electronics & Logic Design",
                    "required": True,
                    "description": "Boolean algebra, logic gates, combinational/sequential circuits, Karnaugh maps, FPGAs.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "Digital Electronics - Neso Academy", "url": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRjMH3mWf6kwqiTbT798eAOm", "type": "youtube"},
                            {"name": "DigitalLogic Tutorial - GeeksforGeeks", "url": "https://www.geeksforgeeks.org/digital-electronics-logic-design-tutorials/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Signals & Systems",
                    "required": True,
                    "description": "Fourier transforms, Laplace transforms, convolution, LTI systems, sampling theorem.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "Signals & Systems - Neso Academy", "url": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRhG6s3jYIU48CqsT5cyiDTO", "type": "youtube"},
                            {"name": "MIT 6.003 Signals & Systems (OCW)", "url": "https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 2: Embedded Systems",
            "color": "#FF9C00",
            "topics": [
                {
                    "name": "C for Embedded Systems",
                    "required": True,
                    "description": "Pointers, memory management, bitwise ops, hardware register access in C.",
                    "time_estimate": "4-6 weeks",
                    "resources": {
                        "free": [
                            {"name": "C Programming Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=KJgsSFOSQv0", "type": "youtube"},
                            {"name": "Embedded C - EmbeddedGurus", "url": "https://barrgroup.com/embedded-systems/books/programming-embedded-systems", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Microcontrollers: ARM / Arduino / STM32",
                    "required": True,
                    "description": "GPIO, timers, ADC, UART/SPI/I2C, interrupts, RTOS basics on STM32/ESP32/Arduino.",
                    "time_estimate": "8-10 weeks",
                    "resources": {
                        "free": [
                            {"name": "STM32 Tutorial - Controllerstech (YouTube)", "url": "https://www.youtube.com/@controllerstech", "type": "youtube"},
                            {"name": "Arduino Official Tutorials", "url": "https://docs.arduino.cc/learn/starting-guide/getting-started-arduino/", "type": "website"},
                            {"name": "ESP32 Programming - Random Nerd Tutorials", "url": "https://randomnerdtutorials.com/esp32/", "type": "website"},
                        ],
                        "paid": [
                            {"name": "Embedded Systems Bare-to-Metal - Udemy", "url": "https://www.udemy.com/course/embedded-systems-bare-to-metal-programming-in-c/", "type": "udemy"},
                        ]
                    }
                },
            ]
        },
        {
            "phase": "Phase 3: Communications & RF",
            "color": "#FFAC00",
            "topics": [
                {
                    "name": "Communication Systems",
                    "required": True,
                    "description": "AM/FM/PM modulation, digital comms (ASK/FSK/PSK/QAM), channel coding, OFDM.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "Communication Systems - Neso Academy", "url": "https://www.youtube.com/playlist?list=PLBlnK6fEyqRhztGPmpkdFNDM_8K0vLAJC", "type": "youtube"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "VLSI Design & HDL",
                    "required": False,
                    "description": "Verilog/VHDL, synthesis, timing analysis, CMOS design, FPGA implementation.",
                    "time_estimate": "8-10 weeks",
                    "resources": {
                        "free": [
                            {"name": "Verilog Tutorial - NPTEL", "url": "https://nptel.ac.in/courses/117/105/117105146/", "type": "website"},
                            {"name": "FPGA Design - EEVblog YouTube", "url": "https://www.youtube.com/@EEVblog", "type": "youtube"},
                        ],
                        "paid": [
                            {"name": "VLSI: From Basics to IC Design - Udemy", "url": "https://www.udemy.com/course/analog-vlsi-design/", "type": "udemy"},
                        ]
                    }
                },
            ]
        },
    ]
}

# ─── 8. BACKEND DEVELOPMENT ───────────────────────────────────────────────────
ROADMAPS["backend"] = {
    "title": "Backend Development",
    "icon": "⚙️",
    "description": "Build scalable server-side systems, APIs, and databases powering modern applications.",
    "difficulty": "Intermediate",
    "duration": "10-14 months",
    "phases": [
        {
            "phase": "Phase 1: Programming & Fundamentals",
            "color": "#00A8FF",
            "topics": [
                {
                    "name": "Python or Node.js",
                    "required": True,
                    "description": "Choose one: Python (Django/FastAPI) or Node.js (Express/NestJS) as your primary backend language.",
                    "time_estimate": "4-6 weeks",
                    "resources": {
                        "free": [
                            {"name": "Python Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=eWRfhZUzrAc", "type": "youtube"},
                            {"name": "Node.js Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=f2EqECiTBL8", "type": "youtube"},
                        ],
                        "paid": [
                            {"name": "Complete Python Bootcamp (Udemy)", "url": "https://www.udemy.com/course/complete-python-bootcamp/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Data Structures & Algorithms",
                    "required": True,
                    "description": "Arrays, linked lists, trees, graphs, sorting/searching, big-O analysis — essential for interviews.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "DSA Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=pkYVOmU3MgA", "type": "youtube"},
                            {"name": "LeetCode (free problems)", "url": "https://leetcode.com/", "type": "website"},
                            {"name": "NeetCode Roadmap", "url": "https://neetcode.io/roadmap", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 2: Web Frameworks & APIs",
            "color": "#00B8FF",
            "topics": [
                {
                    "name": "Django or FastAPI (Python) / Express or NestJS (Node)",
                    "required": True,
                    "description": "Build production-ready REST APIs with routing, middleware, validation, and authentication.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "Django Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=F5mRW0jo-U4", "type": "youtube"},
                            {"name": "FastAPI Official Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "website"},
                            {"name": "NestJS Crash Course - Traversy Media", "url": "https://www.youtube.com/watch?v=wqhNoDE6pb4", "type": "youtube"},
                        ],
                        "paid": [
                            {"name": "Django & Django REST Framework - Udemy", "url": "https://www.udemy.com/course/django-3-make-websites-with-python-tutorial-beginner-learn-bootstrap/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Database Design & ORMs",
                    "required": True,
                    "description": "ER modeling, normalization, PostgreSQL, SQLAlchemy / Prisma, migrations, indexing.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "PostgreSQL Tutorial - freeCodeCamp", "url": "https://www.youtube.com/watch?v=qw--VYLpxG4", "type": "youtube"},
                            {"name": "SQLAlchemy Docs", "url": "https://docs.sqlalchemy.org/en/14/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 3: Scalability & Production",
            "color": "#00C8FF",
            "topics": [
                {
                    "name": "Caching: Redis & Memcached",
                    "required": True,
                    "description": "Cache API responses, session data, rate limiting using Redis. Reduces DB load significantly.",
                    "time_estimate": "2-3 weeks",
                    "resources": {
                        "free": [
                            {"name": "Redis Crash Course - Traversy Media", "url": "https://www.youtube.com/watch?v=Hbt56gFj998", "type": "youtube"},
                            {"name": "Redis Docs", "url": "https://redis.io/docs/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Message Queues: RabbitMQ / Kafka",
                    "required": False,
                    "description": "Async task processing, event-driven architecture, microservices communication.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "RabbitMQ Tutorial - freeCodeCamp", "url": "https://www.youtube.com/watch?v=nFxjaVmFj5E", "type": "youtube"},
                            {"name": "Apache Kafka Docs", "url": "https://kafka.apache.org/documentation/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "API Security & Testing",
                    "required": True,
                    "description": "JWT, OAuth2, rate limiting, input validation, unit/integration testing with pytest.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "API Security Best Practices - OWASP", "url": "https://owasp.org/www-project-api-security/", "type": "website"},
                            {"name": "pytest Tutorial - freeCodeCamp", "url": "https://www.youtube.com/watch?v=cHYq1MRoyI0", "type": "youtube"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
    ]
}

# ─── ADDITIONAL CAREER TRACKS (cards only, no detailed roadmap) ───────────────
ROADMAPS["cse"] = {
    "title": "Computer Science Engineering",
    "icon": "💻",
    "description": "Core CS fundamentals: algorithms, OS, networks, databases, and software engineering.",
    "difficulty": "Intermediate",
    "duration": "48 months (degree)",
    "phases": ROADMAPS["fullstack"]["phases"]  # Use fullstack as base
}

ROADMAPS["it"] = {
    "title": "Information Technology",
    "icon": "🖥️",
    "description": "IT infrastructure, networking, system administration, and enterprise solutions.",
    "difficulty": "Beginner",
    "duration": "12-18 months",
    "phases": ROADMAPS["devops"]["phases"]
}

ROADMAPS["blockchain"] = {
    "title": "Blockchain Development",
    "icon": "⛓️",
    "description": "Build decentralized apps, smart contracts, and Web3 solutions on Ethereum and beyond.",
    "difficulty": "Advanced",
    "duration": "12-16 months",
    "phases": ROADMAPS["backend"]["phases"]
}

ROADMAPS["gamedev"] = {
    "title": "Game Development",
    "icon": "🎮",
    "description": "Create 2D/3D games using Unity, Unreal Engine, or Godot with C# or C++.",
    "difficulty": "Intermediate",
    "duration": "12-18 months",
    "phases": ROADMAPS["android"]["phases"]
}

ROADMAPS["mobile"] = {
    "title": "Mobile App Development",
    "icon": "📲",
    "description": "Build cross-platform mobile apps with React Native or Flutter for iOS and Android.",
    "difficulty": "Intermediate",
    "duration": "10-14 months",
    "phases": ROADMAPS["android"]["phases"]
}

# All available career tracks for the browser grid
CAREER_TRACKS = [
    {"key": "fullstack", "category": "IT & Software"},
    {"key": "aiml", "category": "Engineering & CS"},
    {"key": "cybersecurity", "category": "Engineering & CS"},
    {"key": "datascience", "category": "Engineering & CS"},
    {"key": "devops", "category": "IT & Software"},
    {"key": "android", "category": "IT & Software"},
    {"key": "ece", "category": "Electronics & Core"},
    {"key": "backend", "category": "IT & Software"},
    {"key": "cse", "category": "Engineering & CS"},
    {"key": "it", "category": "IT & Software"},
    {"key": "blockchain", "category": "IT & Software"},
    {"key": "gamedev", "category": "IT & Software"},
    {"key": "mobile", "category": "IT & Software"},
]
