# ⛏️ Build Keeper Electron

Esta é a versão desktop do Build Keeper, construída com **Electron**, **React** e **Tailwind CSS v4**, conectada a um servidor **Node.js** rodando em container.

## 🚀 Como Executar

Siga os passos abaixo para iniciar o ambiente de desenvolvimento:

### Passo 1: Iniciar o Backend (Docker)
O backend gerencia toda a persistência e lógica de negócio.
```bash
docker compose up -d
```
> O servidor estará disponível em `http://localhost:3000`.

### Passo 2: Iniciar o Frontend (Electron)
Em um novo terminal, entre na pasta `frontend` e inicie o processo de desenvolvimento.
```bash
cd frontend
npm install
npm run dev
```

## 🛠️ Tecnologias Utilizadas
- **Frontend:** Electron + React 19 + Vite.
- **Estilização:** Tailwind CSS v4 + Material Design 3.
- **Backend:** Node.js (Fastify) + Docker.
- **Qualidade:** Biome (Lint/Format) + Vitest (Testes Unitários).

## 📁 Estrutura do Projeto
- `backend/`: API Node.js e lógica de negócio.
- `frontend/`: Aplicação desktop Electron/React.
- `data/`: Arquivos JSON de persistência (mapeados via volume Docker).
- `specs/`: Documentação técnica e roteiro de construção.
