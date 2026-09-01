import json
import sys

from deployment_agent.config import AgentConfig
from deployment_agent.executor import DeploymentExecutor
from deployment_agent.server import serve
from deployment_agent.store import AgentStore

if __name__ == "__main__":
    config = AgentConfig.from_env()
    if sys.argv[1:] == ["preflight"]:
        executor = DeploymentExecutor(config, AgentStore(config.state_path))
        result = executor.preflight()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        raise SystemExit(0 if result["ok"] else 1)
    if sys.argv[1:] == ["bootstrap-current"]:
        executor = DeploymentExecutor(config, AgentStore(config.state_path))
        print(executor.bootstrap_current())
        raise SystemExit(0)
    if len(sys.argv) > 1:
        raise SystemExit("usage: python -m deployment_agent [preflight|bootstrap-current]")
    serve(config)
