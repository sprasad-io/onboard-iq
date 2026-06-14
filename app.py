# app.py
# Real-World Role-Based Access Control (RBAC) Architecture for OnboardIQ.

import streamlit as st
import os
import re
import mock_data
from agents import run_hr_pulse_agent, run_team_context_agent, run_review_gate_agent, run_conversational_buddy_agent

# Initialize premium wide layout with fast-rendering caches
st.set_page_config(page_title="OnboardIQ Enterprise Workspace", layout="wide")

# ==============================================================================
# 🗄️ STATEFUL ENTERPRISE DATABASE INITIALIZATION (YEAR 2026)
# ==============================================================================
if "company_policies" not in st.session_state: st.session_state.company_policies = mock_data.COMPANY_POLICIES.copy()
if "team_contexts" not in st.session_state: st.session_state.team_contexts = mock_data.TEAM_CONTEXTS.copy()
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "user_role" not in st.session_state: st.session_state.user_role = None  # 'employee', 'manager', 'admin'
if "current_user" not in st.session_state: st.session_state.current_user = ""

# Persistent Agent Output Storage Caches mapped to unique roles
if "vault_hr" not in st.session_state: st.session_state.vault_hr = {}
if "vault_team" not in st.session_state: st.session_state.vault_team = {}
if "vault_review" not in st.session_state: st.session_state.vault_review = {}

# Corporate Hierarchy Database Mapped for 2026 Lifecycles
if "employee_roster" not in st.session_state:
    st.session_state.employee_roster = {
        "Rahul": {"role": "software_engineer", "title": "Junior Cloud Developer", "manager": "Anand Kumar (Team Lead)", "join_date": "2026-06-01", "bgv": "✅ Passed", "progress": 0, "risk": "Passed", "course": "Azure Security Advanced 202", "tasks": {"Setup 2FA": False, "Clone Repo": False, "Submit First Code": False}},
        "Priya": {"role": "data_analyst", "title": "Senior Data Ingestion Analyst", "manager": "Anand Kumar (Team Lead)", "join_date": "2026-06-10", "bgv": "⏳ Processing", "progress": 0, "risk": "Passed", "course": "GDPR Compliance Mapping", "tasks": {"GDPR Check": False, "PowerBI Access": False, "Export Data Pipeline": False}}
    }

if not os.getenv("AZURE_OPENAI_KEY") or not os.getenv("AZURE_OPENAI_ENDPOINT"):
    st.error("🔒 Security Alert: Configuration parameters 'AZURE_OPENAI_KEY' or 'AZURE_OPENAI_ENDPOINT' are missing from .env.")
    st.stop()

# ==============================================================================
# ♿ SIDEBAR DESIGN & LANGUAGE ENGINE CONTROLS
# ==============================================================================
st.sidebar.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=65)
st.sidebar.markdown("### ♿ Accessibility Suite")
font_multiplier = st.sidebar.slider("Text Zoom", min_value=1.0, max_value=1.5, value=1.0, step=0.1)
high_contrast = st.sidebar.toggle("High Contrast Mode", value=False)

st.sidebar.markdown("### 🌐 Language Settings")
lang_mode = st.sidebar.selectbox("Workspace Language", options=["English", "Malayalam", "Tamil", "Telugu", "Kannada", "Hindi"])

# Wipe caching matrices instantly on language update to guarantee live translator synchronizations
if "current_lang" not in st.session_state: st.session_state.current_lang = lang_mode
if lang_mode != st.session_state.current_lang:
    st.session_state.current_lang = lang_mode
    st.session_state.chat_history = []
    st.session_state.vault_hr = {}
    st.session_state.vault_team = {}
    st.session_state.vault_review = {}
    st.rerun()

base_font_size = int(16 * font_multiplier)
heading_1_size = int(30 * font_multiplier)
heading_2_size = int(22 * font_multiplier)

# Premium Native macOS Interface CSS styling rules
if high_contrast:
    apple_css = f"""<style>
        html, body, [data-testid="stAppViewContainer"] {{ background-color: #000000 !important; color: #FFFFFF !important; font-size: {base_font_size}px !important; }}
        .apple-container {{ background-color: #000000 !important; border: 2px solid #FFFFFF !important; padding: 20px; border-radius: 8px; margin-bottom: 15px; }}
        .scroll-vault {{ max-height: 420px; overflow-y: auto; padding: 15px; background: #000000; border: 1px dashed #FFFFFF; }}
    </style>"""
else:
    apple_css = f"""<style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{ background-color: #060709 !important; font-family: 'Inter', sans-serif !important; color: #E2E8F0 !important; font-size: {base_font_size}px !important; }}
        .apple-container {{ background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(24px); border-radius: 14px; padding: 22px; border: 1px solid rgba(255, 255, 255, 0.05); margin-bottom: 18px; transition: all 0.3s ease; }}
        .scroll-vault {{ max-height: 420px; overflow-y: auto; padding: 15px; background: rgba(0, 0, 0, 0.4); border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.03); line-height: 1.6; }}
        .role-badge {{ background: rgba(0, 113, 227, 0.12) !important; color: #0084FF !important; border: 1px solid rgba(0, 113, 227, 0.25) !important; padding: 5px 14px; border-radius: 20px; display: inline-block; font-weight: 500; font-size: 13px; }}
        .stButton>button {{ background: #0071E3 !important; color: white !important; border-radius: 7px !important; border: none !important; padding: 6px 20px !important; font-weight: 500; }}
        .stButton>button:hover {{ background: #147CE5 !important; }}
    </style>"""

st.markdown(apple_css, unsafe_allow_html=True)

# ==============================================================================
# 🔐 HIERARCHICAL SECURITY GATEWAY (ZERO-FRICTION DROPDOWN AUTOMATION)
# ==============================================================================
if not st.session_state.authenticated:
    st.markdown("<h1 style='text-align: center; margin-top: 80px;'>🔒 OnboardIQ Security Gateway</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6E6E73; margin-bottom: 30px;'>Autonomous Multi-Agent Identity Verification Node</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<div class='apple-container'>", unsafe_allow_html=True)
        st.markdown("<h3>Select Access Profile Clearances</h3>", unsafe_allow_html=True)
        
        selected_login_tier = st.selectbox(
            "Corporate Role Selector Tier:",
            options=[
                "Select Identity...",
                "Employee: Rahul (Software Developer)",
                "Employee: Priya (Data Analyst)",
                "Manager: Anand Kumar (Team Lead)",
                "HR Systems Director (Admin Master)"
            ]
        )
        
        if st.button("Secure Login & Bypass Credentials", use_container_width=True):
            if "Rahul" in selected_login_tier:
                st.session_state.authenticated = True; st.session_state.user_role = "employee"; st.session_state.current_user = "Rahul"; st.rerun()
            elif "Priya" in selected_login_tier:
                st.session_state.authenticated = True; st.session_state.user_role = "employee"; st.session_state.current_user = "Priya"; st.rerun()
            elif "Anand" in selected_login_tier:
                st.session_state.authenticated = True; st.session_state.user_role = "manager"; st.session_state.current_user = "Anand Kumar"; st.rerun()
            elif "HR Systems" in selected_login_tier:
                st.session_state.authenticated = True; st.session_state.user_role = "admin"; st.session_state.current_user = "Admin Master"; st.rerun()
            else:
                st.error("Please select a valid identity node to execute verification loops.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Master Shell Structure Headers
col_header_title, col_header_act = st.columns([8, 2])
with col_header_title: st.markdown("<h1>🚀 OnboardIQ Workspace</h1>", unsafe_allow_html=True)
with col_header_act:
    if st.button("Sign Out of Session", use_container_width=True):
        st.session_state.authenticated = False; st.session_state.user_role = None; st.session_state.chat_history = []; st.rerun()


# ==============================================================================
# 👤 TIER 1: NEW HORE EMPLOYEE DASHBOARD INTERFACE (CHAT HUB FOCUS)
# ==============================================================================
if st.session_state.user_role == "employee":
    selected_name = st.session_state.current_user
    selected_role = st.session_state.employee_roster[selected_name]["role"]
    emp_title = st.session_state.employee_roster[selected_name]["title"]
    
    st.markdown(f"<span class='role-badge'>👤 Profile CLEARANCE: {selected_name} — {emp_title}</span>", unsafe_allow_html=True)
    
    emp_tabs = st.tabs(["💬 OnboardBuddy Chat Hub", "📋 Compliance Policy Brief", "💻 Engineering Roadmap Sync", "🔍 Code Security Gate"])
    
    # Tab 1: Chat Hub Focus
    with emp_tabs[0]:
        col_main_chat, col_side_summary = st.columns([2.3, 1])
        with col_side_summary:
            st.markdown("<div class='apple-container'>", unsafe_allow_html=True)
            st.markdown("<h4>📋 Milestone Synchronization</h4>", unsafe_allow_html=True)
            user_tasks = st.session_state.employee_roster[selected_name]["tasks"]
            for t_name, t_status in user_tasks.items():
                icon = "✅" if t_status else "⏳"
                st.markdown(f"{icon} {t_name}")
            p_val = st.session_state.employee_roster[selected_name]["progress"]
            st.progress(p_val / 100.0)
            st.markdown(f"**Velocity:** {p_val}% | **BGV Status:** {st.session_state.employee_roster[selected_name]['bgv']}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='apple-container' style='border-left: 4px solid #34D399;'>", unsafe_allow_html=True)
            st.markdown("<h4>🤖 AI Training Coordinator</h4>", unsafe_allow_html=True)
            st.info(f"📚 {st.session_state.employee_roster[selected_name]['course']}")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_main_chat:
            st.markdown("<div class='apple-container'>", unsafe_allow_html=True)
            st.markdown("<div class='scroll-vault'>", unsafe_allow_html=True)
            if not st.session_state.chat_history:
                greetings = {
                    "Malayalam": f"ഹലോ {selected_name}! ഓൺബോർഡിംഗ് വർക്ക്‌സ്‌പെയ്‌സിലേക്ക് സ്വാഗതം. ഇന്ന് 2026 ജൂൺ 15 ആണ്. നിങ്ങളുടെ ഓൺബോർഡിംഗ് സ്ട്രെസ്സ് ഫ്രീ ആക്കാൻ ഞാൻ ഇവിടെയുണ്ട്. 2FA സജ്ജീകരിക്കുകയോ റെപ്പോ ക്ലോൺ ചെയ്യുകയോ പോലുള്ള ജോലികൾ പൂർത്തിയാക്കുമ്പോൾ എന്നോട് പറയുക.",
                    "Tamil": f"வணக்கம் {selected_name}! உங்கள் ஆன்போர்டிங் பணிிடத்திற்கு வரவேற்கிறோம். 2FA அமைப்பது அல்லது ರೆಪೊ ಕ್ರಲೋನ್ ಮಾಡುವುದು ಮೈಲ್‌ಸ್ಟೋನ್ಸ್ ಮುಗಿಸಿದಾಗ ತಿಳಿಸಿ.",
                    "Telugu": f"నమస్కారం {selected_name}! మీ ఆన్‌బోర్డింగ్ వర్క్‌స్పేస్‌కు స్వాగతం. మీరు 2FA సెటప్ లేదా రెపో క్లోన్ వంటి పనులను పూర్తి చేసినప్పుడు నాకు చెప్పండి.",
                    "Kannada": f"ನಮಸ್ಕಾರ {selected_name}! ನಿಮ್ಮ ಆನ್‌ಬೋರ್ಡಿಂಗ್ ಕಾರ್ಯಕ್ಷೇತ್ರಕ್ಕೆ ಸುಸ್ವಾಗತ. ನೀವು 2FA ಸೆಟಪ್ ಅಥವಾ ರೆಪೊ ಕ್ಲೋನ್‌ನಂತಹ ಕಾರ್ಯಗಳನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದಾಗ ನನಗೆ ತಿಳಿಸಿ.",
                    "Hindi": f"नमस्ते {selected_name}! आपके ऑनboardिंग वर्कस्पेस में आपका स्वागत है। जब आप 2FA सेटअप या रेपो क्लोन जैसे काम पूरे कर लें, तो मुझे बताएं।",
                    "English": f"Hello {selected_name}! Welcome to your onboarding workspace. Today is June 15, 2026. Simply tell me when you complete milestones like setting up 2FA or cloning the repo, and I will autonomously update your dashboard."
                }
                st.session_state.chat_history.append({"role": "assistant", "content": greetings.get(lang_mode, greetings["English"])})
                
            for msg in st.session_state.chat_history:
                color = "#38BDF8" if msg["role"] == "user" else "#34D399"
                label = "👤 You" if msg["role"] == "user" else "🤖 OnboardBuddy"
                st.markdown(f"<p style='color: {color};'><strong>{label}:</strong> {msg['content']}</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            user_msg_input = st.chat_input("Talk with OnboardBuddy...")
            if user_msg_input:
                st.session_state.chat_history.append({"role": "user", "content": user_msg_input})
                pending_arr = [k for k, v in user_tasks.items() if not v]
                policy_text = st.session_state.company_policies.get(selected_role, "")
                ctx_obj = st.session_state.team_contexts.get(selected_role, {})
                context_str = f"Team: {ctx_obj.get('team_name')}\nProject: {ctx_obj.get('current_project')}\nRoadmap: {ctx_obj.get('first_30_days_roadmap')}"
                
                with st.spinner("Processing..."):
                    reply = run_conversational_buddy_agent(selected_role, user_msg_input, policy_text, context_str, st.session_state.chat_history[:-1], pending_arr, lang_mode)
                
                if "[ACTION: COMMIT_TASK ->" in reply:
                    match = re.search(r"\[ACTION: COMMIT_TASK -> (.*?)\]", reply)
                    if match:
                        matched_t_name = match.group(1).strip()
                        if matched_t_name in st.session_state.employee_roster[selected_name]["tasks"]:
                            st.session_state.employee_roster[selected_name]["tasks"][matched_t_name] = True
                            t_map = st.session_state.employee_roster[selected_name]["tasks"]
                            done = sum(1 for v in t_map.values() if v)
                            st.session_state.employee_roster[selected_name]["progress"] = int((done / len(t_map)) * 100)
                            badge = f"\n\n✨ **[System Log: Agent committed milestone in {lang_mode}]** ✨"
                            reply = re.sub(r"\[ACTION: COMMIT_TASK -> .*?\]", badge, reply)
                st.session_state.chat_history.append({"role": "assistant", "content": reply})
                st.rerun()

    # Tab 2: Compliance Brief
    with emp_tabs[1]:
        st.markdown("<h2>📋 Grounded Corporate Policy Directives</h2>", unsafe_allow_html=True)
        if st.button("Pull Compliance Framework Details", key="emp_hr_run"):
            with st.spinner("Executing Pulse Ingestion..."):
                st.session_state.vault_hr[selected_role] = run_hr_pulse_agent(selected_role, st.session_state.company_policies, lang_mode)
        cached_hr = st.session_state.vault_hr.get(selected_role, "")
        if cached_hr: st.markdown(f"<div class='apple-container'><div class='scroll-vault'>{cached_hr}</div></div>", unsafe_allow_html=True)

    # Tab 3: Roadmap Sync
    with emp_tabs[2]:
        st.markdown("<h2>💻 Live Git Telemetry Framework Build Mapping</h2>", unsafe_allow_html=True)
        if st.button("Synchronize Agile Sprint Milestones", key="emp_team_run"):
            with st.spinner("Executing Repository Ingestion..."):
                st.session_state.vault_team[selected_role] = run_team_context_agent(selected_role, st.session_state.team_contexts, lang_mode)
        cached_team = st.session_state.vault_team.get(selected_role, "")
        if cached_team: st.markdown(f"<div class='apple-container'><div class='scroll-vault' style='white-space: pre-wrap;'>{cached_team}</div></div>", unsafe_allow_html=True)

    # Tab 4: Security Ingestion sandbox
    with emp_tabs[3]:
        st.markdown("<h2>🔍 Code Security Gate Auditor Node Sandbox</h2>", unsafe_allow_html=True)
        mock_data_string = "Task Complete: Deployed cryptography hooks using plain text API passwords hardcoded open to repo headers."
        text_ingest_view = st.text_area("Audit Mock Payload Ingestion:", value=mock_data_string, height=80)
        if st.button("Trigger Automated Security Run", key="emp_review_run"):
            with st.spinner("Executing Risk Ingestion..."):
                res_rev = run_review_gate_agent(selected_role, text_ingest_view, st.session_state.company_policies, lang_mode)
                st.session_state.vault_review[selected_role] = res_rev
                if "Confidence Score" in res_rev: st.session_state.employee_roster[selected_name]["risk"] = "Risk Detected"
        cached_rev = st.session_state.vault_review.get(selected_role, "")
        if cached_rev: st.markdown(f"<div class='apple-container'><div class='scroll-vault'>{cached_rev}</div></div>", unsafe_allow_html=True)


# ==============================================================================
# 👑 TIER 2: LINE MANAGER / TEAM LEAD COMMAND VIEW (REVIEW ORIENTED)
# ==============================================================================
elif st.session_state.user_role == "manager":
    st.markdown("<span class='role-badge'>👑 Executive Clearances: Anand Kumar (Team Lead)</span>", unsafe_allow_html=True)
    
    mgr_tabs = st.tabs(["📊 Team Progress Telemetry", "🔍 Automated Code Security Auditor"])
    
    with mgr_tabs[0]:
        st.markdown("### Subordinate Resource Operational Metrics Grid")
        roster_grid = []
        for emp, details in st.session_state.employee_roster.items():
            if "Anand" in details["manager"]:
                roster_grid.append({
                    "Subordinate Resource": emp,
                    "Assigned Profile Track": details["role"].replace('_',' ').title(),
                    "Hiring Join Date": details["join_date"],
                    "Background Check (BGV)": details["bgv"],
                    "Milestone Progress Scores": f"{details['progress']}%",
                    "AI Review Gate Security Level": details["risk"]
                })
        st.table(roster_grid)

    with mgr_tabs[1]:
        st.markdown("### 🔍 Live Multi-Agent Review Sandbox Node")
        target_mgr_role = st.selectbox("Select Target Role Architecture Specification to Test:", options=list(st.session_state.company_policies.keys()), format_func=lambda x: x.replace('_', ' ').title())
        mock_str = "Task Complete: Exported internal client database metrics files public to unsecured dropbox configurations."
        user_text = st.text_area("Audit Payload Stream Node Ingestion:", value=mock_str, height=90)
        if st.button("Execute Core Security Risk Run Pipeline"):
            with st.spinner("Review Gate Agent parsing patterns..."):
                res = run_review_gate_agent(target_mgr_role, user_text, st.session_state.company_policies, lang_mode)
                st.markdown(f"<div class='apple-container'><h4>Agent Audit Analytics Report Matrix ({lang_mode}):</h4><div class='scroll-vault'>{res}</div></div>", unsafe_allow_html=True)


# ==============================================================================
# ⚙️ TIER 3: HR SYSTEMS MASTER ADMIN VIEW (CLEAN SYSTEM GROUNDING HUB)
# ==============================================================================
else:
    st.markdown("<span class='role-badge'>⚙️ HR Global Systems Director (Admin Master Profile Node)</span>", unsafe_allow_html=True)
    
    adm_tabs = st.tabs(["📊 Global Workforce Telemetry Center", "👥 Dynamic Lifecycle CRUD Simulator", "⚙️ Prompt Grounding Configuration Hub"])
    
    with adm_tabs[0]:
        st.markdown("### Cross-Divisional Resource Pipeline Overview")
        global_grid = []
        for emp, details in st.session_state.employee_roster.items():
            global_grid.append({
                "Employee Identifier": emp,
                "Operational Track Role": details["role"].replace('_',' ').title(),
                "Assigned Job Title": details["title"],
                "Reporting Line Manager": details["manager"],
                "Hiring Join Date": details["join_date"],
                "Background Clearance (BGV)": details["bgv"],
                "Task Completion Velocity": f"{details['progress']}%",
                "Automated Security Evaluation": details["risk"]
            })
        st.table(global_grid)

    with adm_tabs[1]:
        st.markdown("### Workforce Directory Lifecycle Configurations")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("<div class='apple-container'>", unsafe_allow_html=True)
            st.markdown("#### Onboard Incoming Profile (Join Event)")
            with st.form("add_form_adm"):
                new_n = st.text_input("First Name:")
                new_r = st.selectbox("Operational Track Parameters:", options=["software_engineer", "data_analyst"])
                new_t = st.text_input("Assigned Corporate Job Title:", value="Cloud Associate")
                submit_add = st.form_submit_button("Publish Event Tracking Node to AI Channels")
                if submit_add and new_n:
                    st.session_state.employee_roster[new_n] = {
                        "role": new_r, "title": new_t, "manager": "Anand Kumar (Team Lead)", "join_date": "2026-06-15", "bgv": "⏳ Processing", "progress": 0, "risk": "Passed",
                        "course": "Core Infrastructure Cryptography 101" if new_r == "software_engineer" else "Data Leakage Mitigations 101",
                        "tasks": {"Setup 2FA": False, "Clone Repo": False, "Submit First Code": False} if new_r == "software_engineer" else {"GDPR Check": False, "PowerBI Access": False, "Export Data Pipeline": False}
                    }
                    st.success(f"Workforce operational directories generated for '{new_n}'.")
            st.markdown("</div>", unsafe_allow_html=True)
        with col_c2:
            st.markdown("<div class='apple-container'>", unsafe_allow_html=True)
            st.markdown("#### Revoke Framework Clearances (Leave Event)")
            with st.form("del_form_adm"):
                target_del = st.selectbox("Select Account Node for Absolute Deactivation:", options=list(st.session_state.employee_roster.keys()))
                submit_del = st.form_submit_button("Trigger Immediate Access Revocation", type="primary")
                if submit_del:
                    del st.session_state.employee_roster[target_del]
                    st.success(f"Archived and severed corporate access pipelines for '{target_del}' live.")
            st.markdown("</div>", unsafe_allow_html=True)

    with adm_tabs[2]:
        st.markdown("### Prompt Core Spec Grounding Overwrites HUB")
        admin_target = st.selectbox("Select Target Core Grounding Specification Matrix to Re-write:", options=list(st.session_state.company_policies.keys()), format_func=lambda x: x.replace('_', ' ').title(), key="adm_hub_sel")
        modified_text_data = st.text_area("Edit Compliance Policy Guidelines Text Matrix Matrix Headers:", value=st.session_state.company_policies.get(admin_target, ""), height=140)
        if st.button("Publish Overwrites Matrix Asset Asset Configurations", type="primary"):
            st.session_state.company_policies[admin_target] = modified_text_data
            st.success(f"Grounding guidelines matrix for '{admin_target.replace('_',' ').title()}' successfully synchronized live into multi-agent caches.")

st.markdown("</main>", unsafe_allow_html=True)