.PHONY: doctor help setup test reset destroy ssh-cis-target ssh-web ssh-db ssh-comms

help: ## Show available commands
	@echo ""
	@echo "  STARFALL DEFENCE CORPS — Mission 2.2"
	@echo "  Compliance as Code"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'
	@echo ""

doctor: ## Check your machine is mission-ready (Docker, ports, tools)
	@bash $(ROOT_DIR)/scripts/doctor.sh

setup: ## Launch compliance range + fleet nodes (4 containers)
	@bash scripts/setup-lab.sh

test: ## Run ARIA verification
	@bash scripts/check-work.sh

reset: ## Destroy and rebuild all nodes
	@bash scripts/reset-lab.sh

destroy: ## Tear down everything
	@bash scripts/destroy-lab.sh

ssh-cis-target: ## SSH into cis-target (obstacle course, port 2251)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2251

ssh-web: ## SSH into sdc-web (fleet, Ubuntu, port 2221)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2221

ssh-db: ## SSH into sdc-db (fleet, Rocky Linux, port 2222)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2222

ssh-comms: ## SSH into sdc-comms (fleet, Ubuntu, port 2223)
	@ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
		-i .docker/ssh-keys/cadet_key cadet@localhost -p 2223
