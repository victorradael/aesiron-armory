# Variáveis locais do App build_keeper
COMPOSE := docker compose
APP_NAME := build_keeper

.PHONY: run dev down logs

run: ## Sobe o app em background
	$(COMPOSE) up -d

dev: ## Sobe o app em modo interativo
	$(COMPOSE) up

down: ## Para o app
	$(COMPOSE) down

logs: ## Mostra os logs do app
	$(COMPOSE) logs -f
