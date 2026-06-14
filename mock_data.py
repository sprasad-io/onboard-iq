# mock_data.py
COMPANY_POLICIES = {
    "software_engineer": "CRITICAL SECURITY REQUIREMENTS:\n1. Multi-Factor Authentication (2FA) is mandatory for all Azure production deployments.\n2. Never commit secret keys, passwords, or configuration files (.env) to public GitHub repositories.\n3. All code modifications must undergo a peer review and maintain at least 80% unit test coverage before merging to the main branch.",
    "data_analyst": "DATA GOVERNANCE & PRIVACY REQUIREMENTS:\n1. Strict adherence to GDPR regulations is mandatory. Personally Identifiable Information (PII) must be anonymized.\n2. Corporate reporting and datasets must exclusively be published within protected, official Power BI production workspaces.\n3. Sharing database administrative credentials or raw unencrypted backups outside verified corporate channels is strictly prohibited."
}

TEAM_CONTEXTS = {
    "software_engineer": {
        "team_name": "Cloud Intelligence Core Infrastructure Team",
        "current_project": "Migrating mission-critical enterprise integration pipelines into secure autonomous multi-agent systems via Azure AI Foundry.",
        "upcoming_milestone": "Production deployment of the automated workspace orchestration framework by the end of the current development sprint.",
        "first_30_days_roadmap": "Week 1: Configure local secure terminal environment, clone codebase, and validate Azure AI SDK permissions.\nWeek 2: Shadow core infrastructure engineers and pick up active minor bug fixes in agent routing.\nWeek 3-4: Build out isolated automated regression tests for the secure review gate pipeline."
    },
    "data_analyst": {
        "team_name": "Enterprise Business Insights & Analytics Division",
        "current_project": "Architecting real-time transactional data analytics models and active predictive dashboards for executive operational monitoring.",
        "upcoming_milestone": "Presenting the Q2 asset utilization strategy models and operational financial forecasting directly to executive board members next Tuesday.",
        "first_30_days_roadmap": "Week 1: Submit formal access requests for the enterprise Snowflake warehouse and review corporate metadata schema sheets.\nWeek 2: Analyze historical ingestion pipeline performance gaps and trace data processing latencies.\nWeek 3-4: Deliver the first fully vetted custom executive summary dashboard and publish to the certified production workspace."
    }
}
