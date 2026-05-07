"""
core/roadmap_data.py - Career roadmap definitions (Part 1: Full Stack, AI/ML, Cybersecurity, Data Science)
Additional tracks loaded from roadmap_data2.py
"""

ROADMAPS = {}

# ─── 1. FULL STACK DEVELOPMENT ────────────────────────────────────────────────
ROADMAPS["fullstack"] = {
    "title": "Full Stack Web Development",
    "icon": "🌐",
    "description": "Build complete web applications from frontend to backend and deployment.",
    "difficulty": "Intermediate",
    "duration": "12-18 months",
    "phases": [
        {
            "phase": "Phase 1: Foundations",
            "color": "#6C63FF",
            "topics": [
                {
                    "name": "HTML & CSS",
                    "required": True,
                    "description": "The building blocks of every web page. HTML provides structure while CSS handles presentation and layout.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "HTML Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=kUMe1FH4CHE", "type": "youtube"},
                            {"name": "CSS Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=OXGznpKZ_sA", "type": "youtube"},
                            {"name": "W3Schools HTML", "url": "https://www.w3schools.com/html/", "type": "website"},
                            {"name": "MDN Web Docs HTML", "url": "https://developer.mozilla.org/en-US/docs/Web/HTML", "type": "website"},
                            {"name": "CSS-Tricks", "url": "https://css-tricks.com/", "type": "website"},
                        ],
                        "paid": [
                            {"name": "The Web Developer Bootcamp - Colt Steele (Udemy)", "url": "https://www.udemy.com/course/the-web-developer-bootcamp/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "JavaScript Fundamentals",
                    "required": True,
                    "description": "Core JavaScript: variables, functions, DOM manipulation, async programming, ES6+.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "JavaScript Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=jS4aFq5-91M", "type": "youtube"},
                            {"name": "javascript.info", "url": "https://javascript.info/", "type": "website"},
                            {"name": "Eloquent JavaScript (free book)", "url": "https://eloquentjavascript.net/", "type": "website"},
                        ],
                        "paid": [
                            {"name": "JavaScript: The Complete Guide (Udemy)", "url": "https://www.udemy.com/course/javascript-the-complete-guide-2020-beginner-advanced/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Git & Version Control",
                    "required": True,
                    "description": "Track code changes, collaborate, and manage projects using Git and GitHub.",
                    "time_estimate": "1-2 weeks",
                    "resources": {
                        "free": [
                            {"name": "Git & GitHub Crash Course - Traversy Media", "url": "https://www.youtube.com/watch?v=SWYqp7iY_Tc", "type": "youtube"},
                            {"name": "Pro Git Book (free)", "url": "https://git-scm.com/book/en/v2", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 2: Frontend",
            "color": "#7C6FFF",
            "topics": [
                {
                    "name": "React.js",
                    "required": True,
                    "description": "Build dynamic UIs with component-based architecture, hooks, state management and React Router.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "React Full Course 2024 - freeCodeCamp", "url": "https://www.youtube.com/watch?v=x4rFhThSX04", "type": "youtube"},
                            {"name": "React Official Docs", "url": "https://react.dev/", "type": "website"},
                            {"name": "The Odin Project - React", "url": "https://www.theodinproject.com/paths/full-stack-javascript/courses/react", "type": "website"},
                        ],
                        "paid": [
                            {"name": "React - The Complete Guide (Udemy)", "url": "https://www.udemy.com/course/react-the-complete-guide-incl-redux/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "CSS Frameworks & Styling",
                    "required": False,
                    "description": "Tailwind CSS, styled-components, or Material UI for rapid, consistent UI development.",
                    "time_estimate": "2-3 weeks",
                    "resources": {
                        "free": [
                            {"name": "Tailwind CSS Crash Course", "url": "https://www.youtube.com/watch?v=UBOj6rqRUME", "type": "youtube"},
                            {"name": "Tailwind CSS Docs", "url": "https://tailwindcss.com/docs", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 3: Backend",
            "color": "#8C7FFF",
            "topics": [
                {
                    "name": "Node.js & Express",
                    "required": True,
                    "description": "Server-side JavaScript, RESTful APIs, middleware, routing, and HTTP handling.",
                    "time_estimate": "4-6 weeks",
                    "resources": {
                        "free": [
                            {"name": "Node.js Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=f2EqECiTBL8", "type": "youtube"},
                            {"name": "Node.js Docs", "url": "https://nodejs.org/en/docs/", "type": "website"},
                            {"name": "Express.js Docs", "url": "https://expressjs.com/", "type": "website"},
                        ],
                        "paid": [
                            {"name": "NodeJS - The Complete Guide (Udemy)", "url": "https://www.udemy.com/course/nodejs-the-complete-guide/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Databases: SQL & NoSQL",
                    "required": True,
                    "description": "PostgreSQL for relational data, MongoDB for document storage. Learn ORMs like Prisma/Mongoose.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "SQL Tutorial - W3Schools", "url": "https://www.w3schools.com/sql/", "type": "website"},
                            {"name": "MongoDB University (free)", "url": "https://learn.mongodb.com/", "type": "website"},
                            {"name": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "REST APIs & Authentication",
                    "required": True,
                    "description": "Design RESTful APIs, implement JWT authentication, OAuth2, and security best practices.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "REST API Crash Course - Traversy Media", "url": "https://www.youtube.com/watch?v=l8WPWK9mS5M", "type": "youtube"},
                            {"name": "JWT.io Introduction", "url": "https://jwt.io/introduction", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 4: DevOps & Deployment",
            "color": "#9A8FFF",
            "topics": [
                {
                    "name": "Docker & Containers",
                    "required": False,
                    "description": "Containerize applications for consistent deployments across environments.",
                    "time_estimate": "2-3 weeks",
                    "resources": {
                        "free": [
                            {"name": "Docker Tutorial for Beginners - TechWorld with Nana", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE", "type": "youtube"},
                            {"name": "Docker Docs", "url": "https://docs.docker.com/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Cloud Deployment (Vercel / AWS / Railway)",
                    "required": True,
                    "description": "Deploy frontend to Vercel/Netlify, backend to AWS EC2 or Railway/Render.",
                    "time_estimate": "2 weeks",
                    "resources": {
                        "free": [
                            {"name": "Deploy Node App to AWS - freeCodeCamp", "url": "https://www.youtube.com/watch?v=T-Pum2TraX4", "type": "youtube"},
                            {"name": "Vercel Docs", "url": "https://vercel.com/docs", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
    ]
}

# ─── 2. AI/ML ENGINEERING ─────────────────────────────────────────────────────
ROADMAPS["aiml"] = {
    "title": "AI / ML Engineering",
    "icon": "🤖",
    "description": "Build intelligent systems using machine learning, deep learning, and modern AI frameworks.",
    "difficulty": "Advanced",
    "duration": "18-24 months",
    "phases": [
        {
            "phase": "Phase 1: Math & Programming Foundations",
            "color": "#6C63FF",
            "topics": [
                {
                    "name": "Python for ML",
                    "required": True,
                    "description": "Python essentials: NumPy, Pandas, Matplotlib, data structures, and Pythonic coding.",
                    "time_estimate": "4-6 weeks",
                    "resources": {
                        "free": [
                            {"name": "Python for Everybody - freeCodeCamp", "url": "https://www.youtube.com/watch?v=8DvywoWv6fI", "type": "youtube"},
                            {"name": "NumPy Tutorial - freeCodeCamp", "url": "https://www.youtube.com/watch?v=QUT1VHiLmmI", "type": "youtube"},
                            {"name": "Kaggle Python Course (free)", "url": "https://www.kaggle.com/learn/python", "type": "website"},
                        ],
                        "paid": [
                            {"name": "Python Bootcamp - Jose Portilla (Udemy)", "url": "https://www.udemy.com/course/complete-python-bootcamp/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Linear Algebra & Calculus",
                    "required": True,
                    "description": "Vectors, matrices, dot products, gradients, partial derivatives — the backbone of ML.",
                    "time_estimate": "4-6 weeks",
                    "resources": {
                        "free": [
                            {"name": "3Blue1Brown - Essence of Linear Algebra", "url": "https://www.youtube.com/playlist?list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab", "type": "youtube"},
                            {"name": "Khan Academy Linear Algebra", "url": "https://www.khanacademy.org/math/linear-algebra", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Statistics & Probability",
                    "required": True,
                    "description": "Distributions, hypothesis testing, Bayes theorem, and statistical inference.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "Statistics for ML - StatQuest (YouTube)", "url": "https://www.youtube.com/@statquest", "type": "youtube"},
                            {"name": "Kaggle Intro to ML (free)", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 2: Core Machine Learning",
            "color": "#7C6FFF",
            "topics": [
                {
                    "name": "Scikit-learn & Classical ML",
                    "required": True,
                    "description": "Regression, classification, clustering, SVM, decision trees, ensemble methods.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "Scikit-learn Tutorial - Sentdex (YouTube)", "url": "https://www.youtube.com/watch?v=rvVkVsG49uU", "type": "youtube"},
                            {"name": "Scikit-learn Docs & User Guide", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "website"},
                            {"name": "Kaggle ML Courses", "url": "https://www.kaggle.com/learn", "type": "website"},
                        ],
                        "paid": [
                            {"name": "ML A-Z (Udemy)", "url": "https://www.udemy.com/course/machinelearning/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Deep Learning with PyTorch/TensorFlow",
                    "required": True,
                    "description": "Neural networks, CNNs, RNNs, Transformers; train on GPU using PyTorch or TensorFlow.",
                    "time_estimate": "8-10 weeks",
                    "resources": {
                        "free": [
                            {"name": "Deep Learning with PyTorch - freeCodeCamp", "url": "https://www.youtube.com/watch?v=V_xro1bcAuA", "type": "youtube"},
                            {"name": "Fast.ai Practical Deep Learning (free)", "url": "https://course.fast.ai/", "type": "website"},
                            {"name": "TensorFlow Tutorials", "url": "https://www.tensorflow.org/tutorials", "type": "website"},
                        ],
                        "paid": [
                            {"name": "Deep Learning Specialization - Coursera (Andrew Ng)", "url": "https://www.coursera.org/specializations/deep-learning", "type": "coursera"},
                        ]
                    }
                },
            ]
        },
        {
            "phase": "Phase 3: Advanced AI",
            "color": "#8C7FFF",
            "topics": [
                {
                    "name": "NLP & Large Language Models",
                    "required": True,
                    "description": "Hugging Face Transformers, BERT, GPT, fine-tuning, RAG, and prompt engineering.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "HuggingFace NLP Course (free)", "url": "https://huggingface.co/learn/nlp-course/", "type": "website"},
                            {"name": "Andrej Karpathy - Neural Nets: Zero to Hero", "url": "https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ", "type": "youtube"},
                        ],
                        "paid": [
                            {"name": "NLP with Transformers - O'Reilly Book", "url": "https://www.oreilly.com/library/view/natural-language-processing/9781098136789/", "type": "other"},
                        ]
                    }
                },
                {
                    "name": "MLOps & Model Deployment",
                    "required": True,
                    "description": "FastAPI, Docker, MLflow, model serving, monitoring in production.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "MLOps Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=Zd5d4xxzdiU", "type": "youtube"},
                            {"name": "Made With ML (free)", "url": "https://madewithml.com/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
    ]
}

# ─── 3. CYBERSECURITY ENGINEERING ─────────────────────────────────────────────
ROADMAPS["cybersecurity"] = {
    "title": "Cybersecurity Engineering",
    "icon": "🔐",
    "description": "Protect systems and networks. Master ethical hacking, threat analysis, and security architecture.",
    "difficulty": "Advanced",
    "duration": "18-24 months",
    "phases": [
        {
            "phase": "Phase 1: Networking & OS Fundamentals",
            "color": "#FF6B6B",
            "topics": [
                {
                    "name": "Networking Basics (TCP/IP, DNS, HTTP)",
                    "required": True,
                    "description": "OSI model, TCP/IP suite, DNS, HTTP/S, firewalls, VPNs, subnetting.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "Computer Networking - Professor Messer (YouTube)", "url": "https://www.youtube.com/@professormesser", "type": "youtube"},
                            {"name": "Cisco Networking Academy (free courses)", "url": "https://www.netacad.com/", "type": "website"},
                            {"name": "NetworkChuck (YouTube)", "url": "https://www.youtube.com/@NetworkChuck", "type": "youtube"},
                        ],
                        "paid": [
                            {"name": "CompTIA Network+ Study Guide", "url": "https://www.udemy.com/course/comptia-network-n10-008/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Linux for Security",
                    "required": True,
                    "description": "Command line mastery, file permissions, processes, bash scripting, and Kali Linux.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "Linux Command Line Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=sWbUDq4S6Y8", "type": "youtube"},
                            {"name": "OverTheWire Bandit (hands-on Linux wargames)", "url": "https://overthewire.org/wargames/bandit/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 2: Core Security Skills",
            "color": "#FF8080",
            "topics": [
                {
                    "name": "Ethical Hacking & Penetration Testing",
                    "required": True,
                    "description": "Reconnaissance, scanning, exploitation with Metasploit, Nmap, Burp Suite.",
                    "time_estimate": "8-10 weeks",
                    "resources": {
                        "free": [
                            {"name": "Ethical Hacking Full Course - freeCodeCamp", "url": "https://www.youtube.com/watch?v=3Kq1MIfTWCE", "type": "youtube"},
                            {"name": "HackTheBox (free tier)", "url": "https://www.hackthebox.com/", "type": "website"},
                            {"name": "TryHackMe (free rooms)", "url": "https://tryhackme.com/", "type": "website"},
                        ],
                        "paid": [
                            {"name": "Practical Ethical Hacking - TCM Security (Udemy)", "url": "https://www.udemy.com/course/practical-ethical-hacking/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Web Application Security (OWASP Top 10)",
                    "required": True,
                    "description": "SQL injection, XSS, CSRF, broken auth, insecure deserialization, and mitigations.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "OWASP Top 10 Explained - freeCodeCamp", "url": "https://www.youtube.com/watch?v=rWHvp7rUka8", "type": "youtube"},
                            {"name": "PortSwigger Web Security Academy (free)", "url": "https://portswigger.net/web-security", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Cryptography & PKI",
                    "required": True,
                    "description": "Symmetric/asymmetric encryption, TLS/SSL, hashing, digital signatures, PKI.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "Cryptography I - Coursera (Stanford, free to audit)", "url": "https://www.coursera.org/learn/crypto", "type": "coursera"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 3: Certifications & Specializations",
            "color": "#FF9595",
            "topics": [
                {
                    "name": "CompTIA Security+ / CEH",
                    "required": True,
                    "description": "Industry-recognized certifications validating core security skills.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "Security+ Study Guide - Professor Messer", "url": "https://www.professormesser.com/security-plus/sy0-701/sy0-701-video/sy0-701-comptia-security-plus-course/", "type": "website"},
                        ],
                        "paid": [
                            {"name": "CompTIA Security+ (SY0-701) - Udemy", "url": "https://www.udemy.com/course/comptia-security-sy0-701/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "SIEM, SOC & Incident Response",
                    "required": False,
                    "description": "Splunk, ELK Stack, threat hunting, log analysis, and IR playbooks.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "Splunk Free Training", "url": "https://www.splunk.com/en_us/training/free-courses.html", "type": "website"},
                            {"name": "Blue Team Labs Online (free tier)", "url": "https://blueteamlabs.online/", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
    ]
}

# ─── 4. DATA SCIENCE & ANALYTICS ─────────────────────────────────────────────
ROADMAPS["datascience"] = {
    "title": "Data Science & Analytics",
    "icon": "📊",
    "description": "Extract insights from data using statistics, machine learning, and powerful visualization tools.",
    "difficulty": "Intermediate",
    "duration": "12-18 months",
    "phases": [
        {
            "phase": "Phase 1: Foundations",
            "color": "#00D4AA",
            "topics": [
                {
                    "name": "Python & Data Libraries",
                    "required": True,
                    "description": "Python, NumPy, Pandas, Matplotlib, Seaborn for data manipulation and visualization.",
                    "time_estimate": "5-6 weeks",
                    "resources": {
                        "free": [
                            {"name": "Python for Data Analysis - freeCodeCamp", "url": "https://www.youtube.com/watch?v=r-uOLxNrNk8", "type": "youtube"},
                            {"name": "Kaggle Pandas Course (free)", "url": "https://www.kaggle.com/learn/pandas", "type": "website"},
                            {"name": "Kaggle Data Visualization (free)", "url": "https://www.kaggle.com/learn/data-visualization", "type": "website"},
                        ],
                        "paid": [
                            {"name": "Python for Data Science Bootcamp - Udemy", "url": "https://www.udemy.com/course/python-for-data-science-and-machine-learning-bootcamp/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "SQL for Data Analysis",
                    "required": True,
                    "description": "Advanced SQL: window functions, CTEs, subqueries, aggregations for analytics.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "SQL Tutorial - Mode Analytics", "url": "https://mode.com/sql-tutorial/", "type": "website"},
                            {"name": "SQL for Data Science - Kaggle", "url": "https://www.kaggle.com/learn/intro-to-sql", "type": "website"},
                        ],
                        "paid": []
                    }
                },
                {
                    "name": "Statistics for Data Science",
                    "required": True,
                    "description": "Descriptive stats, A/B testing, regression analysis, probability distributions.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "StatQuest with Josh Starmer (YouTube)", "url": "https://www.youtube.com/@statquest", "type": "youtube"},
                            {"name": "Khan Academy Statistics", "url": "https://www.khanacademy.org/math/statistics-probability", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
        {
            "phase": "Phase 2: Machine Learning for Data Science",
            "color": "#00E5BB",
            "topics": [
                {
                    "name": "Machine Learning Algorithms",
                    "required": True,
                    "description": "Supervised/unsupervised learning, model evaluation, cross-validation, feature engineering.",
                    "time_estimate": "6-8 weeks",
                    "resources": {
                        "free": [
                            {"name": "Kaggle Intro to ML & Intermediate ML", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "website"},
                            {"name": "ML Course - Andrew Ng (Coursera free audit)", "url": "https://www.coursera.org/learn/machine-learning", "type": "coursera"},
                        ],
                        "paid": [
                            {"name": "ML A-Z - Udemy", "url": "https://www.udemy.com/course/machinelearning/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Data Visualization & Storytelling",
                    "required": True,
                    "description": "Power BI, Tableau, Plotly Dash, and effective dashboard design for non-technical audiences.",
                    "time_estimate": "3-4 weeks",
                    "resources": {
                        "free": [
                            {"name": "Tableau Public Training (free)", "url": "https://www.tableau.com/learn/training/elearning", "type": "website"},
                            {"name": "Plotly & Dash Tutorial - Charming Data (YouTube)", "url": "https://www.youtube.com/@CharmingData", "type": "youtube"},
                        ],
                        "paid": [
                            {"name": "Power BI Desktop for Beginners - Udemy", "url": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/", "type": "udemy"},
                        ]
                    }
                },
            ]
        },
        {
            "phase": "Phase 3: Advanced Analytics & Big Data",
            "color": "#00F5CC",
            "topics": [
                {
                    "name": "Big Data: Spark & Hadoop",
                    "required": False,
                    "description": "PySpark, Hadoop ecosystem, Hive, distributed data processing at scale.",
                    "time_estimate": "4-6 weeks",
                    "resources": {
                        "free": [
                            {"name": "PySpark Tutorial - freeCodeCamp", "url": "https://www.youtube.com/watch?v=_C8kWso4ne4", "type": "youtube"},
                        ],
                        "paid": [
                            {"name": "Spark and Python for Big Data - Udemy", "url": "https://www.udemy.com/course/spark-and-python-for-big-data-with-pyspark/", "type": "udemy"},
                        ]
                    }
                },
                {
                    "name": "Cloud Data Platforms (AWS/GCP/Azure)",
                    "required": False,
                    "description": "S3, BigQuery, Azure Synapse — cloud-native tools for data warehousing and analytics.",
                    "time_estimate": "4-5 weeks",
                    "resources": {
                        "free": [
                            {"name": "Google BigQuery Tutorial - Google Cloud", "url": "https://cloud.google.com/bigquery/docs/tutorials", "type": "website"},
                            {"name": "AWS Data Analytics Fundamentals (free)", "url": "https://explore.skillbuilder.aws/learn/course/44/aws-data-analytics-fundamentals", "type": "website"},
                        ],
                        "paid": []
                    }
                },
            ]
        },
    ]
}
