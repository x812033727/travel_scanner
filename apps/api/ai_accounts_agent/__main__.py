from ai_accounts_agent.config import AgentConfig
from ai_accounts_agent.server import serve

if __name__ == "__main__":
    serve(AgentConfig.from_env())
