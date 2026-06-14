# agents.py
import os
import importlib
from openai import AzureOpenAI
from dotenv import load_dotenv

import mock_data
importlib.reload(mock_data)

COMPANY_POLICIES = mock_data.COMPANY_POLICIES
TEAM_CONTEXTS = mock_data.TEAM_CONTEXTS

load_dotenv(override=True)

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-06-01",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o-mini")

def run_hr_pulse_agent(role: str, dynamic_policies: dict, language: str) -> str:
    policy = dynamic_policies.get(role, "")
    if not policy: return "Error: Policy missing."
    
    system_instruction = (
        "You are HR Pulse, a strict and highly accurate Enterprise Compliance Agent.\n"
        f"CRITICAL LANGUAGE DIRECTIVE: You must output your entire response strictly in the '{language}' language.\n"
        "Ground your response completely and exclusively within the provided corporate policy data."
    )
    user_content = f"Target Role: {role}\n\nCorporate Policy Context:\n{policy}"
    try:
        response = client.chat.completions.create(model=DEPLOYMENT_NAME, messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_content}], temperature=0.0)
        return response.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

def run_team_context_agent(role: str, dynamic_contexts: dict, language: str) -> str:
    context = dynamic_contexts.get(role, {})
    if not context: return "Error: Team context missing."
    
    system_instruction = (
        "You are Team Context, an elite AI Technical Lead and Agile Director Agent.\n"
        f"CRITICAL LANGUAGE DIRECTIVE: You must output your entire response strictly in the '{language}' language.\n"
        "Provide a clear, motivating structural breakdown detailing team identity, active project, and tactical roadmap."
    )
    user_content = f"Role: {role}\nTeam Identity: {context.get('team_name')}\nActive Project: {context.get('current_project')}\nRoadmap: {context.get('first_30_days_roadmap')}"
    try:
        response = client.chat.completions.create(model=DEPLOYMENT_NAME, messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_content}], temperature=0.0)
        return response.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

def run_review_gate_agent(role: str, user_submission: str, dynamic_policies: dict, language: str) -> str:
    policy = dynamic_policies.get(role, "")
    if not policy: return "Error: Policy missing."
    
    system_instruction = (
        "You are Review Gate, a critical Enterprise Risk Audit Agent.\n"
        f"CRITICAL LANGUAGE DIRECTIVE: You must output your entire response strictly in the '{language}' language.\n"
        "Identify security violations. Conclude your output with a line stating exactly: 'Confidence Score: [X]/100'."
    )
    user_content = f"Company Policy Requirements:\n{policy}\n\nSubmission:\n{user_submission}"
    try:
        response = client.chat.completions.create(model=DEPLOYMENT_NAME, messages=[{"role": "system", "content": system_instruction}, {"role": "user", "content": user_content}], temperature=0.0)
        return response.choices[0].message.content
    except Exception as e: return f"Error: {str(e)}"

def run_conversational_buddy_agent(role: str, user_question: str, policy: str, context_str: str, history: list, pending_tasks: list, language: str) -> str:
    tasks_string = ", ".join(pending_tasks)
    system_instruction = (
        f"You are OnboardBuddy, an advanced interactive conversational onboarding assistant for a newly joined '{role}'.\n"
        f"CRITICAL LANGUAGE DIRECTIVE: You must converse and answer strictly in the '{language}' language.\n"
        f"CURRENT PENDING CHECKLIST: [{tasks_string}].\n\n"
        "STATE UPDATE DIRECTIVE:\n"
        "If the user explicitly states they finished a task, append exactly at the end: [ACTION: COMMIT_TASK -> Task Name].\n\n"
        "DOUBT & ESCALATION DIRECTIVE:\n"
        "If the user expresses confusion, stress, or asks an escalation doubt, generate a professional corporate email draft at the bottom of your response addressed to their manager/HR head."
    )
    messages = [{"role": "system", "content": system_instruction}]
    for msg in history:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_question})
    try:
        response = client.chat.completions.create(model=DEPLOYMENT_NAME, messages=messages, temperature=0.3)
        return response.choices[0].message.content
    except Exception as e: return f"Buddy Error: {str(e)}"