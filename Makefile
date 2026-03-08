.PHONY: help setup banner

define BANNER
====================================================================
      🛡️         ___             _                           🛡️
                /   | ___  _____(_)________  ____ 
               / /| |/ _ \\/ ___/ / ___/ __ \\/ __ \\
              / ___ /  __(__  ) / /  / /_/ / / / /
             /_/  |_\\___/____/_/_/   \\____/_/ /_/ 

                  ___                                   
                 /   |  _________ ___  ____  _______  __
                / /| | / ___/ __ `__ \\/ __ \\/ ___/ / / /
               / ___ |/ /  / / / / / / /_/ / /  / /_/ / 
              /_/  |_/_/  /_/ /_/ /_/\\____/_/   \\__, /  
                                               /____/
====================================================================
endef
export BANNER

help: ## Exibe os comandos disponíveis
	@echo "$$BANNER"
	@awk 'BEGIN {FS = ":.*##"; printf "Uso: make \033[36m<target>\033[0m\n\nComandos:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

banner:
	@echo "$$BANNER"

setup: banner ## Configura o ambiente virtual root instalando dependências de todos os projetos (IntelliSense)
	@echo "🛠️  Configurando o ambiente virtual principal com Poetry (instalando aesiron)..."
	poetry install --no-root
	@echo ""
	@echo "📦 Instalando dependências dos sub-projetos para garantir o IntelliSense na raiz..."
	@poetry run pip install pip --upgrade
	@find . -mindepth 2 -name "requirements.txt" -not -path "*/\.*" | while read req; do \
		echo "⚙️  Instalando pacotes de: $$req"; \
		poetry run pip install -r "$$req"; \
	done
	@echo ""
	@echo "✅ Setup concluído! O seu editor deve utilizar a .venv gerada pelo Poetry para ter o IntelliSense completo."
