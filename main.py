import streamlit as st
import pandas as pd
import os

# Initialize session state
if 'job_list' not in st.session_state:
    st.session_state.job_list = []

# ===== LOAD EXTERNAL FILES =====
def load_css(file_path):
    """Load external CSS file"""
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            css = f.read()
            st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    else:
        st.warning(f"CSS file not found: {file_path}")

def load_html_template(file_path):
    """Load HTML template file"""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    return None

def create_job_card_html(job, details):
    """Create HTML job card using template"""
    template = load_html_template("job_card.html")
    if not template:
        return None
    
    # Determine AI impact colors and icons
    ai_impact = details["ai_impact"]
    if ai_impact == "High":
        ai_color = "#ff6b6b"
        ai_icon = "🔴"
    elif ai_impact == "Medium":
        ai_color = "#ffa726"
        ai_icon = "🟠"
    else:
        ai_color = "#4CAF50"
        ai_icon = "🟢"
    
    # Calculate salary percentage for progress bar
    min_salary, max_salary = details["salary"]
    avg_salary = (min_salary + max_salary) // 2
    salary_percentage = min(100, int((avg_salary / 150000) * 100))
    
    # Replace placeholders in template
    replacements = {
        "JOB_TITLE_PLACEHOLDER": job,
        "JOB_DESCRIPTION_PLACEHOLDER": details["description"],
        "MIN_SALARY_PLACEHOLDER": f"{min_salary:,}",
        "MAX_SALARY_PLACEHOLDER": f"{max_salary:,}",
        "SALARY_PERCENTAGE_PLACEHOLDER": str(salary_percentage),
        "CERTIFICATES_PLACEHOLDER": ", ".join(details["certificates"]),
        "AI_IMPACT_PLACEHOLDER": ai_impact,
        "AI_COLOR_PLACEHOLDER": ai_color,
        "AI_ICON_PLACEHOLDER": ai_icon,
        "CAREER_LEVEL_PLACEHOLDER": "Intermediate",
        "LOCATION_PLACEHOLDER": "UAE (Remote/On-site)"
    }
    
    html = template
    for key, value in replacements.items():
        html = html.replace(key, str(value))
    
    return html

# ===== HELPER FUNCTION FOR STREAMLIT DISPLAY =====
def display_job_streamlit(job, details):
    """Fallback function to display job using Streamlit components"""
    desc = details["description"]
    min_salary, max_salary = details["salary"]
    avg_salary = (min_salary + max_salary) // 2
    certs = ", ".join(details["certificates"])
    ai_impact = details["ai_impact"]

    # Color coding AI impact
    if ai_impact == "High":
        impact_color = "🔴 High"
    elif ai_impact == "Medium":
        impact_color = "🟠 Medium"
    else:
        impact_color = "🟢 Low"

    # Salary bar
    max_possible_salary = 150000
    salary_bar = min(100, int((avg_salary / max_possible_salary) * 100))

    # Display
    with st.container():
        col1, col2, col3, col4 = st.columns([3, 2, 3, 2])
        with col1:
            st.markdown(f"**{job}**")
            st.write(desc)
        with col2:
            st.progress(salary_bar/100)
            st.markdown(f"💰 AED {min_salary:,} - {max_salary:,}")
        with col3:
            st.markdown(f"📜 Certificates: {certs}")
        with col4:
            st.markdown(f"🤖 AI Impact: {impact_color}")
        st.markdown("---")

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title="AI Job Recommender",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ===== LOAD EXTERNAL CSS =====
load_css("styles.css")

# ===== CUSTOM HEADER WITH HTML =====
st.markdown("""
<div class="main-header">
    <h1>🚀 AI Job Recommender</h1>
    <h2>Get personalized job recommendations with salaries, certificates, and AI impact visualization!</h2>
</div>
""", unsafe_allow_html=True)

# ===== SKILL INPUT SECTION =====
with st.container():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        skills = st.text_input(
            "Enter your skills (comma-separated, e.g., Python, Excel, Design)",
            key="skills_input"
        )



# ===== SKILL MAP DICTIONARY =====
skill_map = {
    # Technical Skills
    "python": ["Data Analyst", "Software Developer", "Data Scientist", "AI Researcher", "ML Engineer"],
    "java": ["Software Developer", "Backend Engineer", "Android Developer"],
    "javascript": ["Frontend Developer", "Full Stack Developer"],
    "c++": ["Software Developer", "Systems Engineer", "Game Developer"],
    "excel": ["Business Analyst", "Financial Analyst", "Data Analyst", "Operations Manager"],
    "design": ["UI/UX Designer", "Graphic Designer", "Product Designer"],
    "marketing": ["Digital Marketing Specialist", "SEO Specialist", "Marketing Manager", "Brand Manager"],
    "communication": ["Project Manager", "Business Analyst", "HR Manager", "Sales Manager"],
    "sql": ["Data Analyst", "Database Administrator", "Business Intelligence Analyst"],
    "cloud": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect"],
    "machine learning": ["ML Engineer", "Data Scientist", "AI Researcher"],
    "ai": ["AI Researcher", "ML Engineer", "AI Product Manager"],
    "html": ["Frontend Developer", "Web Developer", "Full Stack Developer", "UI/UX Designer"],
    "css": ["Frontend Developer", "Web Developer", "Full Stack Developer", "UI/UX Designer"],
    
    # Cybersecurity Skills
    "cybersecurity": ["Cybersecurity Analyst", "Security Engineer", "Penetration Tester", "Security Architect"],
    "security": ["Cybersecurity Analyst", "Security Engineer", "Penetration Tester", "Security Architect"],
    "penetration testing": ["Penetration Tester", "Ethical Hacker"],
    "ethical hacking": ["Penetration Tester", "Ethical Hacker"],
    "network security": ["Network Security Engineer", "Security Engineer"],
    "cloud security": ["Cloud Security Engineer", "Security Architect"],
    
        # Database Skills
    "database": ["Database Administrator", "Data Engineer", "Database Developer"],
    "oracle": ["Database Administrator", "ERP Consultant"],
    "mysql": ["Database Administrator", "Backend Engineer"],
    "postgresql": ["Database Administrator", "Backend Engineer"],
    "mongodb": ["Database Administrator", "Backend Engineer", "Full Stack Developer"],
    "nosql": ["Database Administrator", "Backend Engineer", "Data Engineer", "Full Stack Developer"],
    
    
    # AI/ML Skills
    "deep learning": ["ML Engineer", "AI Researcher", "Data Scientist"],
    "nlp": ["ML Engineer", "AI Researcher", "Data Scientist"],
    "tensorflow": ["ML Engineer", "AI Researcher"],
    "pytorch": ["ML Engineer", "AI Researcher"],
    
    # Game Development Skills
    "game development": ["Game Developer", "Game Designer", "Game Programmer"],
    "unity": ["Game Developer", "AR/VR Developer"],
    "unreal": ["Game Developer", "Game Programmer"],
    
    # Business Skills
    "leadership": ["Project Manager", "Product Manager", "Operations Manager", "HR Director"],
    "strategy": ["Strategy Consultant", "Business Development Manager", "Product Manager"],
    "sales": ["Sales Manager", "Account Executive", "Business Development Manager"],
    "finance": ["Financial Analyst", "Investment Banker", "Financial Controller", "CFO"],
    "accounting": ["Accountant", "Financial Controller", "Auditor"],
    "management": ["Project Manager", "Operations Manager", "Product Manager"],
    
    # Web Development Skills
    "react": ["Frontend Developer", "Full Stack Developer"],
    "angular": ["Frontend Developer", "Full Stack Developer"],
    "vue": ["Frontend Developer"],
    "node.js": ["Backend Engineer", "Full Stack Developer"],
    "docker": ["DevOps Engineer", "Cloud Engineer"],
    "aws": ["Cloud Engineer", "DevOps Engineer", "Solutions Architect"],
}

# ===== JOB DETAILS DICTIONARY - COMPLETE VERSION =====
job_details = {
    "Data Analyst": {
        "description": "Analyze datasets to extract actionable insights for business decisions.",
        "salary": (8000, 15000),
        "certificates": ["Google Data Analytics", "Microsoft Excel Expert", "Tableau Desktop Specialist"],
        "ai_impact": "Medium"
    },
    "Software Developer": {
        "description": "Design, develop, and maintain software applications and systems.",
        "salary": (10000, 20000),
        "certificates": ["AWS Developer", "Oracle Java Certification", "Microsoft Certified: Azure Developer"],
        "ai_impact": "Low"
    },
    "UI/UX Designer": {
        "description": "Create user-centered designs for digital products and improve user experience.",
        "salary": (9000, 16000),
        "certificates": ["Adobe XD Certification", "Google UX Design Professional", "Figma UI/UX Design"],
        "ai_impact": "Medium"
    },
    "Digital Marketing Specialist": {
        "description": "Plan and execute online marketing campaigns across various digital channels.",
        "salary": (8000, 14000),
        "certificates": ["Google Ads Certification", "HubSpot Content Marketing", "Facebook Blueprint"],
        "ai_impact": "High"
    },
    "Business Analyst": {
        "description": "Analyze business processes and recommend solutions to improve efficiency.",
        "salary": (9000, 17000),
        "certificates": ["IIBA ECBA", "PMI-PBA", "CBAP"],
        "ai_impact": "Medium"
    },
    "Financial Analyst": {
        "description": "Analyze financial data to support investment decisions and financial planning.",
        "salary": (10000, 18000),
        "certificates": ["CFA Level 1", "CPA", "Financial Modeling & Valuation Analyst"],
        "ai_impact": "High"
    },
    "Frontend Developer": {
        "description": "Build responsive and interactive user interfaces for web applications.",
        "salary": (9000, 17000),
        "certificates": ["React Certification", "Google IT Automation", "Frontend Developer Nanodegree"],
        "ai_impact": "Low"
    },
    "Backend Engineer": {
        "description": "Develop server-side logic, APIs, and database architecture.",
        "salary": (10000, 20000),
        "certificates": ["AWS Developer", "Node.js Certification", "Spring Professional"],
        "ai_impact": "Low"
    },
    "Full Stack Developer": {
        "description": "Work on both client-side and server-side development of web applications.",
        "salary": (12000, 22000),
        "certificates": ["Full Stack Web Developer", "Microsoft Azure Developer", "MERN Stack Developer"],
        "ai_impact": "Low"
    },
    "Cybersecurity Analyst": {
        "description": "Monitor networks for security breaches and investigate security incidents.",
        "salary": (13000, 26000),
        "certificates": ["CEH", "CompTIA Security+", "CySA+", "GSEC"],
        "ai_impact": "Medium"
    },
    "Security Engineer": {
        "description": "Design and implement security systems to protect organizational data.",
        "salary": (14000, 27000),
        "certificates": ["CISSP", "CCSP", "SANS GIAC", "OSCP"],
        "ai_impact": "Medium"
    },
    "Penetration Tester": {
        "description": "Ethically hack systems to identify vulnerabilities before malicious attackers.",
        "salary": (15000, 30000),
        "certificates": ["OSCP", "GPEN", "CEH Master", "Pentest+"],
        "ai_impact": "Low"
    },
    "ML Engineer": {
        "description": "Build, deploy, and maintain machine learning models in production.",
        "salary": (15000, 28000),
        "certificates": ["TensorFlow Developer", "AWS ML Specialty", "Google Professional ML Engineer"],
        "ai_impact": "Low"
    },
    "Data Scientist": {
        "description": "Extract insights from complex data using statistical analysis and machine learning.",
        "salary": (16000, 30000),
        "certificates": ["Data Science Professional Certificate", "IBM Data Science", "Microsoft Certified: Data Scientist"],
        "ai_impact": "Medium"
    },
    "AI Researcher": {
        "description": "Research and develop new AI algorithms and models.",
        "salary": (18000, 35000),
        "certificates": ["DeepLearning.AI Specialization", "Stanford AI Graduate Certificate", "MIT AI Research"],
        "ai_impact": "Low"
    },
    "Game Developer": {
        "description": "Create video games and interactive entertainment experiences.",
        "salary": (12000, 25000),
        "certificates": ["Unity Certified Developer", "Unreal Engine Certification", "Game Development Specialization"],
        "ai_impact": "Medium"
    },
    "Product Manager": {
        "description": "Define product vision, strategy, and roadmap for successful product delivery.",
        "salary": (20000, 40000),
        "certificates": ["Pragmatic Marketing", "Product School Certification", "PMI-ACP"],
        "ai_impact": "Medium"
    },
    "Sales Manager": {
        "description": "Lead sales team, develop strategies, and drive revenue growth.",
        "salary": (18000, 35000),
        "certificates": ["Salesforce Certified", "SPIN Selling", "Professional Sales Certificate"],
        "ai_impact": "Medium"
    },
    "HR Manager": {
        "description": "Manage human resources functions including recruitment and employee relations.",
        "salary": (14000, 28000),
        "certificates": ["SHRM-CP", "PHR", "HR Management Certificate"],
        "ai_impact": "High"
    },
    "Cloud Engineer": {
        "description": "Design, deploy, and maintain cloud infrastructure and services.",
        "salary": (15000, 25000),
        "certificates": ["AWS Solutions Architect", "Google Cloud Professional", "Azure Solutions Architect"],
        "ai_impact": "Low"
    },
    "Database Administrator": {
        "description": "Install, configure, and maintain database management systems.",
        "salary": (10000, 18000),
        "certificates": ["Oracle DBA", "SQL Server Certification", "MySQL Database Administration"],
        "ai_impact": "Medium"
    },
    "Systems Engineer": {
        "description": "Design and maintain IT systems infrastructure and network architecture.",
        "salary": (11000, 19000),
        "certificates": ["Cisco CCNA", "Microsoft Azure Admin", "Red Hat Certified Engineer"],
        "ai_impact": "Medium"
    },
    "Graphic Designer": {
        "description": "Create visual concepts and designs for digital and print media.",
        "salary": (8000, 14000),
        "certificates": ["Adobe Creative Cloud Certified", "Graphic Design Specialization", "Digital Arts Certificate"],
        "ai_impact": "High"
    },
    "SEO Specialist": {
        "description": "Optimize websites to improve search engine rankings and organic traffic.",
        "salary": (8000, 13000),
        "certificates": ["Google Analytics Certification", "HubSpot SEO", "SEMrush SEO Toolkit"],
        "ai_impact": "High"
    },
    "Project Manager": {
        "description": "Plan, execute, and close projects while managing teams and resources.",
        "salary": (12000, 25000),
        "certificates": ["PMP", "PRINCE2", "Certified Scrum Master"],
        "ai_impact": "Medium"
    },
    "DevOps Engineer": {
        "description": "Automate and optimize software development and deployment processes.",
        "salary": (14000, 24000),
        "certificates": ["Docker Certified Associate", "AWS DevOps Engineer", "Kubernetes Administrator"],
        "ai_impact": "Low"
    },
    "AI Product Manager": {
        "description": "Manage AI/ML product development from conception to launch.",
        "salary": (25000, 50000),
        "certificates": ["AI Product Management", "Machine Learning Basics", "Product Strategy for AI"],
        "ai_impact": "Low"
    },
    "Security Architect": {
        "description": "Design comprehensive security frameworks and solutions for organizations.",
        "salary": (20000, 40000),
        "certificates": ["CISSP-ISSAP", "SABSA", "TOGAF", "CISSP"],
        "ai_impact": "Low"
    },
    "Ethical Hacker": {
        "description": "Perform authorized penetration testing to identify system vulnerabilities.",
        "salary": (14000, 30000),
        "certificates": ["CEH", "OSCP", "Pentest+", "GPEN"],
        "ai_impact": "Low"
    },
    "Database Developer": {
        "description": "Design and implement database solutions and optimize queries.",
        "salary": (12000, 24000),
        "certificates": ["Oracle Database Developer", "SQL Server Developer", "PostgreSQL Certification"],
        "ai_impact": "Medium"
    },
    "Game Designer": {
        "description": "Design game mechanics, storylines, and user experiences.",
        "salary": (11000, 22000),
        "certificates": ["Game Design Specialization", "Level Design Certificate", "Narrative Design"],
        "ai_impact": "Medium"
    },
    "Game Programmer": {
        "description": "Write code for game functionality, physics, and AI behavior.",
        "salary": (13000, 27000),
        "certificates": ["C++ Game Development", "Unity Scripting", "Unreal Engine C++ Developer"],
        "ai_impact": "Low"
    },
    "AR/VR Developer": {
        "description": "Develop augmented and virtual reality applications and experiences.",
        "salary": (15000, 30000),
        "certificates": ["Unity XR Development", "Oculus Developer", "AR Core/ARKit Certification"],
        "ai_impact": "Low"
    },
    "Android Developer": {
        "description": "Develop mobile applications for Android devices.",
        "salary": (12000, 23000),
        "certificates": ["Google Android Developer", "Kotlin Certification", "Android Development Nanodegree"],
        "ai_impact": "Low"
    },
    "Solutions Architect": {
        "description": "Design comprehensive technology solutions for business problems.",
        "salary": (20000, 40000),
        "certificates": ["AWS Solutions Architect Pro", "TOGAF", "Azure Solutions Architect Expert"],
        "ai_impact": "Low"
    },
    "Marketing Manager": {
        "description": "Develop and execute marketing strategies to promote products/services.",
        "salary": (15000, 30000),
        "certificates": ["Digital Marketing Pro", "Google Marketing Platform", "HubSpot Marketing"],
        "ai_impact": "High"
    },
    "Brand Manager": {
        "description": "Develop and maintain brand strategy, identity, and positioning.",
        "salary": (15000, 30000),
        "certificates": ["Brand Management", "Marketing Strategy", "Digital Brand Management"],
        "ai_impact": "Medium"
    },
    "Business Development Manager": {
        "description": "Identify and pursue new business opportunities and partnerships.",
        "salary": (17000, 35000),
        "certificates": ["Business Development Professional", "Strategic Partnerships", "Sales Strategy"],
        "ai_impact": "Low"
    },
    "Strategy Consultant": {
        "description": "Advise companies on strategic decisions and business transformation.",
        "salary": (25000, 50000),
        "certificates": ["Management Consulting", "Strategic Planning", "Business Strategy Specialization"],
        "ai_impact": "Medium"
    },
    "Account Executive": {
        "description": "Manage client accounts and drive sales through relationship building.",
        "salary": (15000, 30000),
        "certificates": ["Sales Certification", "Account Management", "CRM Specialist"],
        "ai_impact": "Low"
    },
    "Financial Controller": {
        "description": "Manage accounting operations and financial reporting for organizations.",
        "salary": (22000, 45000),
        "certificates": ["CPA", "CMA", "Chartered Accountant"],
        "ai_impact": "High"
    },
    "Management Consultant": {
        "description": "Provide expert advice to improve business performance and operations.",
        "salary": (25000, 55000),
        "certificates": ["McKinsey Problem Solving", "BCG Strategy", "Bain Certificate"],
        "ai_impact": "Medium"
    },
    "Supply Chain Manager": {
        "description": "Manage logistics, inventory, and supply chain operations.",
        "salary": (16000, 32000),
        "certificates": ["CSCP", "SCPro", "Logistics Management"],
        "ai_impact": "High"
    },
    "Investment Banker": {
        "description": "Advise on financial transactions, mergers, and capital raising.",
        "salary": (30000, 80000),
        "certificates": ["CFA", "Series 7", "Investment Banking Certificate"],
        "ai_impact": "High"
    },
    "Business Intelligence Analyst": {
        "description": "Analyze business data to support decision making with insights.",
        "salary": (12000, 25000),
        "certificates": ["Tableau Desktop Specialist", "Power BI Certification", "Qlik Sense Business Analyst"],
        "ai_impact": "Medium"
    },
    "Talent Acquisition Specialist": {
        "description": "Source, recruit, and hire top talent for organizations.",
        "salary": (10000, 20000),
        "certificates": ["Talent Acquisition", "Recruitment Certification", "LinkedIn Recruiter"],
        "ai_impact": "High"
    },
    "Risk Analyst": {
        "description": "Identify and analyze potential business and financial risks.",
        "salary": (14000, 28000),
        "certificates": ["FRM", "Risk Management Professional", "Operational Risk Management"],
        "ai_impact": "High"
    },
    "Compliance Officer": {
        "description": "Ensure company compliance with laws, regulations, and standards.",
        "salary": (15000, 30000),
        "certificates": ["Compliance Certification", "Regulatory Affairs", "AML/KYC Certification"],
        "ai_impact": "High"
    },
    "Startup Founder": {
        "description": "Establish and grow a new business venture from concept to scale.",
        "salary": (0, 100000),
        "certificates": ["Entrepreneurship", "Venture Capital", "Startup Management"],
        "ai_impact": "Medium"
    },
    "Scrum Master": {
        "description": "Facilitate agile development processes and remove team impediments.",
        "salary": (13000, 26000),
        "certificates": ["CSM", "PSM", "SAFe Scrum Master"],
        "ai_impact": "Low"
    },
    "Accountant": {
        "description": "Prepare and examine financial records and ensure accuracy.",
        "salary": (9000, 18000),
        "certificates": ["CPA", "ACCA", "Chartered Accountant"],
        "ai_impact": "High"
    },
    "Auditor": {
        "description": "Examine financial statements for accuracy and compliance.",
        "salary": (11000, 22000),
        "certificates": ["CIA", "Internal Audit", "ISO Auditor"],
        "ai_impact": "High"
    },
    "Market Research Analyst": {
        "description": "Study market conditions to inform business decisions and strategy.",
        "salary": (10000, 20000),
        "certificates": ["Market Research", "Data Analysis", "Qualitative Research"],
        "ai_impact": "High"
    },
    "Learning & Development Specialist": {
        "description": "Design and implement employee training and development programs.",
        "salary": (11000, 22000),
        "certificates": ["ATD Certification", "Training Professional", "Instructional Design"],
        "ai_impact": "Medium"
    },
    "Content Manager": {
        "description": "Develop and manage digital content strategy across platforms.",
        "salary": (10000, 20000),
        "certificates": ["Content Marketing", "SEO Writing", "Digital Content Strategy"],
        "ai_impact": "High"
    },
    "Procurement Manager": {
        "description": "Manage purchasing processes and supplier relationships.",
        "salary": (14000, 28000),
        "certificates": ["CPSM", "Procurement Professional", "Supply Chain Management"],
        "ai_impact": "Medium"
    },
    "Innovation Manager": {
        "description": "Drive innovation and new product development initiatives.",
        "salary": (18000, 35000),
        "certificates": ["Innovation Management", "Design Thinking", "Product Innovation"],
        "ai_impact": "Medium"
    },
    "Web Developer": {
        "description": "Build and maintain websites and web applications.",
        "salary": (10000, 20000),
        "certificates": ["Web Development", "Frontend Technologies", "Full Stack Web Dev"],
        "ai_impact": "Low"
    },
    "ERP Consultant": {
        "description": "Implement and customize ERP systems for businesses.",
        "salary": (15000, 30000),
        "certificates": ["SAP Certification", "Oracle ERP", "Microsoft Dynamics"],
        "ai_impact": "Medium"
    },
    "HR Director": {
        "description": "Lead human resources department and develop HR strategy.",
        "salary": (30000, 60000),
        "certificates": ["SHRM-SCP", "HR Executive", "Strategic HR Management"],
        "ai_impact": "Medium"
    },
    "CFO": {
        "description": "Oversee financial operations, strategy, and planning.",
        "salary": (50000, 150000),
        "certificates": ["CPA", "MBA Finance", "Chartered Financial Analyst"],
        "ai_impact": "High"
    },
    "Recruitment Consultant": {
        "description": "Connect employers with qualified candidates for job placements.",
        "salary": (10000, 25000),
        "certificates": ["Recruitment Professional", "Talent Sourcing", "Executive Search"],
        "ai_impact": "Medium"
    },
    "Corporate Trainer": {
        "description": "Deliver training programs to employees on various topics.",
        "salary": (11000, 22000),
        "certificates": ["Training Delivery", "Instructional Design", "Corporate Education"],
        "ai_impact": "Medium"
    },
    "Logistics Manager": {
        "description": "Manage transportation, distribution, and logistics operations.",
        "salary": (14000, 28000),
        "certificates": ["CLTD", "Logistics Management", "Supply Chain Operations"],
        "ai_impact": "High"
    },
    "Business Consultant": {
        "description": "Provide specialized business advice and solutions to clients.",
        "salary": (20000, 45000),
        "certificates": ["Business Consulting", "Industry Specialization", "Management Advisory"],
        "ai_impact": "Medium"
    },
    "Product Designer": {
        "description": "Design user experiences and interfaces for products and services.",
        "salary": (15000, 30000),
        "certificates": ["Product Design", "User Research", "Interaction Design"],
        "ai_impact": "Medium"
    },
    "Operations Manager": {
        "description": "Oversee daily business operations and improve efficiency.",
        "salary": (16000, 32000),
        "certificates": ["Six Sigma", "Operations Management", "Lean Management"],
        "ai_impact": "Medium"
    },
    "Network Security Engineer": {
        "description": "Secure network infrastructure and manage security systems.",
        "salary": (14000, 28000),
        "certificates": ["CCNP Security", "Palo Alto Networks", "Checkpoint CCSA"],
        "ai_impact": "Medium"
    },
    "Cloud Security Engineer": {
        "description": "Secure cloud environments and implement cloud security controls.",
        "salary": (16000, 35000),
        "certificates": ["CCSP", "AWS Security Specialty", "Azure Security Engineer"],
        "ai_impact": "Medium"
    },
    "3D Artist": {
        "description": "Create 3D models, textures, and animations for games/media.",
        "salary": (10000, 20000),
        "certificates": ["Autodesk Maya", "Blender", "Substance Painter"],
        "ai_impact": "High"
    },
    "Mobile App Developer": {
        "description": "Develop applications for iOS and Android mobile devices.",
        "salary": (12000, 25000),
        "certificates": ["Google Mobile Web Specialist", "Apple Developer", "React Native"],
        "ai_impact": "Low"
    },
    "Computer Vision Engineer": {
        "description": "Develop AI systems that can interpret and understand visual information.",
        "salary": (17000, 32000),
        "certificates": ["OpenCV Certification", "Computer Vision Specialization", "Deep Learning for CV"],
        "ai_impact": "Low"
    },
    "CISO": {
        "description": "Executive responsible for organization's information security program.",
        "salary": (50000, 150000),
        "certificates": ["CISSP", "CISM", "CRISC", "CISA"],
        "ai_impact": "Low"
    }
}

# ===== RECOMMENDATION BUTTON =====
# Center just the button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    button_clicked = st.button("🚀 Get AI-Powered Recommendations", 
                               key="recommend_button",
                               use_container_width=True)

# The rest of the logic stays outside columns
if button_clicked:
    if skills.strip() == "":
        st.warning("⚠️ Please enter at least one skill!")
    else:
        with st.spinner("🤖 AI is analyzing your skills and finding perfect matches..."):
            # Process input
            recommended = []
            unknown_skills = []
            for s in skills.split(","):
                skill = s.strip().lower()
                if skill in skill_map:
                    recommended.extend(skill_map[skill])
                else:
                    unknown_skills.append(s.strip())

            # Remove duplicates
            recommended = list(dict.fromkeys(recommended))
            
            if recommended:
                st.success(f"✅ Found {len(recommended)} Recommended Jobs:")
                job_list = []
                
                # Use HTML job cards if template exists
                html_template_exists = os.path.exists("job_card.html")
                
                for job in recommended:
                    if job in job_details:
                        details = job_details[job]
                        
                        if html_template_exists:
                            # Display using HTML template
                            html_card = create_job_card_html(job, details)
                            if html_card:
                                st.markdown(html_card, unsafe_allow_html=True)
                            else:
                                # Fallback to Streamlit display
                                display_job_streamlit(job, details)
                        else:
                            # Use Streamlit display
                            display_job_streamlit(job, details)
                        
                        # Collect for download
                        job_list.append({
                            "Job": job,
                            "Description": details["description"],
                            "Min Salary AED": details["salary"][0],
                            "Max Salary AED": details["salary"][1],
                            "Certificates": ", ".join(details["certificates"]),
                            "AI Impact": details["ai_impact"]
                        })
                    else:
                        # Remove this warning to clean up the output
                        # st.warning(f"Job details not found for: {job}")
                        pass

                # Store job list in session state for download
                st.session_state.job_list = job_list

                # ===== DOWNLOAD SECTION =====
                if job_list:
                    df = pd.DataFrame(job_list)
                    csv_data = df.to_csv(index=False)
                    
                    st.markdown("---")
                    # Center the download button too
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col2:
                        st.download_button(
                            label="📥 Download All Recommendations (CSV)",
                            data=csv_data,
                            file_name="AI_Job_Recommender_Recommendations.csv",
                            mime="text/csv",
                            key="download_csv",
                            use_container_width=True
                        )
                        st.success(f"✅ Ready to download {len(job_list)} recommendations!")

            if unknown_skills:
                st.warning(f"⚠️ Skills not recognized: {', '.join(unknown_skills)}")
                st.info("💡 Try using skills from the list above or check your spelling.")  


# ===== CAREER PATHS TABS =====
st.markdown("---")
st.markdown("### 🎯 Explore Career Paths")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🔒 Cybersecurity", "🤖 AI/ML", "🗄️ Database", "🎮 Game Dev", "💼 Business"])

with tab1:
    st.subheader("🔒 Cybersecurity Career Paths")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Entry Level:**")
        st.markdown("""
        - Security Operations Center (SOC) Analyst
        - Cybersecurity Analyst
        - Vulnerability Analyst
        - IT Security Specialist
        """)
    
    with col2:
        st.markdown("**Mid Level:**")
        st.markdown("""
        - Penetration Tester
        - Security Engineer
        - Incident Responder
        - Network Security Engineer
        - Security Auditor
        """)
    
    with col3:
        st.markdown("**Senior Level:**")
        st.markdown("""
        - Security Architect
        - Security Consultant
        - Cloud Security Engineer
        - Threat Hunter
        - Digital Forensics Analyst
        """)
    
    with col4:
        st.markdown("**Executive Level:**")
        st.markdown("""
        - CISO (Chief Information Security Officer)
        - Head of Security
        - Security Director
        - VP of Cybersecurity
        """)
    
    st.markdown("**Key Certifications:** CEH, CISSP, CISM, OSCP, CompTIA Security+, CCSP, CISA")

with tab2:
    st.subheader("🤖 AI/ML Career Paths")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Entry Level:**")
        st.markdown("""
        - Data Analyst
        - AI/ML Engineer (Junior)
        - Business Intelligence Analyst
        - Data Annotator
        """)
    
    with col2:
        st.markdown("**Mid Level:**")
        st.markdown("""
        - Machine Learning Engineer
        - Data Scientist
        - NLP Specialist
        - Computer Vision Engineer
        - AI Developer
        """)
    
    with col3:
        st.markdown("**Senior Level:**")
        st.markdown("""
        - Senior ML Engineer
        - Lead Data Scientist
        - AI Researcher
        - ML Architect
        - AI Product Manager
        """)
    
    with col4:
        st.markdown("**Executive Level:**")
        st.markdown("""
        - Chief AI Officer
        - Head of AI/ML
        - VP of Data Science
        - Director of AI Research
        """)
    
    st.markdown("**Key Certifications:** TensorFlow Developer, AWS ML Specialty, Google Cloud AI, DeepLearning.AI, Data Science Professional")

with tab3:
    st.subheader("🗄️ Database Career Paths")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Entry Level:**")
        st.markdown("""
        - Database Administrator (Junior)
        - SQL Developer
        - Data Entry Specialist
        - Database Support Specialist
        """)
    
    with col2:
        st.markdown("**Mid Level:**")
        st.markdown("""
        - Database Administrator
        - Database Developer
        - ETL Developer
        - Data Warehouse Analyst
        - Business Intelligence Developer
        """)
    
    with col3:
        st.markdown("**Senior Level:**")
        st.markdown("""
        - Senior Database Administrator
        - Database Architect
        - Data Architect
        - Data Engineer
        - Big Data Specialist
        """)
    
    with col4:
        st.markdown("**Executive Level:**")
        st.markdown("""
        - Chief Data Officer
        - Director of Data Management
        - Head of Database Engineering
        - VP of Data Infrastructure
        """)
    
    st.markdown("**Key Certifications:** Oracle DBA, SQL Server, MySQL, AWS Database Specialty, Google Cloud Database")

with tab4:
    st.subheader("🎮 Game Development Career Paths")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Entry Level:**")
        st.markdown("""
        - Game Tester/QA Tester
        - Junior Game Developer
        - Game Programmer (Junior)
        - Technical Artist (Junior)
        """)
    
    with col2:
        st.markdown("**Mid Level:**")
        st.markdown("""
        - Game Developer
        - Game Programmer
        - Game Designer
        - Level Designer
        - Technical Artist
        - 3D Artist
        """)
    
    with col3:
        st.markdown("**Senior Level:**")
        st.markdown("""
        - Senior Game Developer
        - Lead Game Programmer
        - Lead Game Designer
        - Technical Director
        - Art Director
        - AR/VR Developer
        """)
    
    with col4:
        st.markdown("**Executive Level:**")
        st.markdown("""
        - Game Director
        - Studio Head
        - Creative Director
        - Executive Producer
        - CTO (Gaming Studio)
        """)
    
    st.markdown("**Key Certifications:** Unity Certified, Unreal Engine, Game Design, 3D Modeling, AR/VR Development")

with tab5:
    st.subheader("💼 Business Career Paths")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Entry Level:**")
        st.markdown("""
        - Business Analyst
        - Marketing Associate
        - Sales Representative
        - HR Coordinator
        - Financial Analyst (Junior)
        """)
    
    with col2:
        st.markdown("**Mid Level:**")
        st.markdown("""
        - Product Manager
        - Marketing Manager
        - Sales Manager
        - HR Manager
        - Operations Manager
        - Business Development Manager
        """)
    
    with col3:
        st.markdown("**Senior Level:**")
        st.markdown("""
        - Senior Product Manager
        - Director of Marketing
        - Sales Director
        - HR Director
        - Operations Director
        - Strategy Consultant
        - Management Consultant
        """)
    
    with col4:
        st.markdown("**Executive Level:**")
        st.markdown("""
        - CEO
        - CFO
        - CMO
        - CHRO
        - COO
        - General Manager
        - Partner (Consulting)
        """)
    
    st.markdown("**Key Certifications:** PMP, MBA, CFA, CPA, SHRM, Digital Marketing, Six Sigma")

# ===== FINAL TIPS SECTION =====
st.markdown("---")
with st.expander("💡 **Quick Tips for Job Searching**"):
    st.markdown("""
    1. **Combine Technical + Business Skills** for management roles
    2. **Get Certified** in your chosen field for better opportunities
    3. **Build a Portfolio** with real projects and case studies
    4. **Network Actively** on LinkedIn and industry events
    5. **Stay Updated** with latest technologies and trends
    6. **Consider Remote Work** options for global opportunities
    7. **Focus on AI-Resistant Skills** for long-term career security
    
    **High-Demand Skills for 2026:**
    - AI/ML Engineering
    - Cybersecurity
    - Cloud Computing
    - Data Science
    - Digital Marketing
    - Product Management
    - Quantum Computing
    - Edge AI
    - AI Ethics & Governance
    - Sustainable Tech
    """)

# ===== SKILLS LIST EXPANDER =====
with st.expander("📋 Click to view all available skills"):
    st.markdown("""
    ### All Available Skills
    
    **Technical Skills:**
    - python, java, javascript, c++, sql, cloud, machine learning, ai, html, css
    - cybersecurity, security, penetration testing, ethical hacking
    - network security, cloud security, application security, incident response
    - threat intelligence, vulnerability assessment, risk assessment
    - security auditing, forensics, cryptography, compliance, grc, siem, firewall
    
    **Database Skills:**
    - database, oracle, mysql, postgresql, mongodb, nosql
    - data warehousing, etl
    
    **AI/ML Skills:**
    - deep learning, nlp, computer vision, tensorflow, pytorch
    - data mining, big data
    
    **Game Development Skills:**
    - game development, unity, unreal, 3d modeling, game design
    - virtual reality, augmented reality
    
    **Web Development Skills:**
    - react, angular, vue, node.js, docker, kubernetes
    - aws, azure, gcp, wordpress
    
    **Business & Soft Skills:**
    - excel, design, marketing, communication, leadership, strategy
    - sales, finance, accounting, negotiation, presentation, analytics
    - management, budgeting, recruiting, training, risk management
    - supply chain, entrepreneurship, consulting
    
    **Data & Analytics Skills:**
    - tableau, power bi, sap, agile, scrum
    
    **Design Skills:**
    - photoshop, illustrator, figma, sketch
    
    **💡 Tip:** Combine related skills for better matches (e.g., "python, sql, cloud")
    """)


# ===== FOOTER =====
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 20px;">
    <p style="color: white; opacity: 0.8;">
        © 2026 AI Job Recommender | Data based on UAE market averages | Salaries in AED<br>
        By <a href="https://www.linkedin.com/in/mohamed-ayoujil/" style="color: white; text-decoration: underline;">Mohamed Ayoujil</a>
    </p>
</div>
""", unsafe_allow_html=True)