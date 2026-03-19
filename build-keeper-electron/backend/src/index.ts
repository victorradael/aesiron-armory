import fastify from 'fastify';
import cors from '@fastify/cors';
import { v4 as uuidv4 } from 'uuid';
import * as fs from 'node:fs/promises';
import path from 'node:path';
import { 
  prepareSetForDisplay, 
  getUniqueName, 
  cloneSet, 
  updateEquipmentAcquisition,
  bulkUpdateSets,
  createSet 
} from './core/equipment-manager';
import { ConfigManager } from './core/config-manager';
import { EQUIPMENT_CATALOG } from './core/catalog';
import type { EquipmentSet } from './types';

// Logger ativado para debug visual no terminal
const server = fastify({ logger: true });

server.register(cors, { origin: '*' });

const DATA_FILE = path.join(__dirname, '..', 'data', 'equipment_sets.json');

// Função de inicialização de dados (chamada em background ou após o listen)
async function setupData() {
  const dir = path.dirname(DATA_FILE);
  await fs.mkdir(dir, { recursive: true });
  try {
    await fs.access(DATA_FILE);
  } catch {
    await fs.writeFile(DATA_FILE, JSON.stringify([], null, 2));
  }
}

// --- ROTAS (EXEMPLO) ---
server.get('/ping', async () => ({ pong: true }));

server.get('/sets', async () => {
  const data = await fs.readFile(DATA_FILE, 'utf-8').catch(() => '[]');
  const sets = JSON.parse(data);
  return sets.map(prepareSetForDisplay);
});

server.get('/catalog', async () => EQUIPMENT_CATALOG);

server.post('/sets', async (request) => {
  const newSetData = request.body as Partial<EquipmentSet>;
  const data = await fs.readFile(DATA_FILE, 'utf-8').catch(() => '[]');
  const sets = JSON.parse(data) as EquipmentSet[];
  
  const setWithId = createSet(newSetData, sets.map(s => s.name));
  sets.push(setWithId);
  
  await fs.writeFile(DATA_FILE, JSON.stringify(sets, null, 2));
  return prepareSetForDisplay(setWithId);
});

server.get('/config', async () => ConfigManager.loadConfig());

server.patch('/sets/:id/items/:key', async (request, reply) => {
  const { id, key } = request.params as { id: string, key: string };
  const { acquired } = request.body as { acquired: boolean };
  
  const data = await fs.readFile(DATA_FILE, 'utf-8').catch(() => '[]');
  const sets = JSON.parse(data) as EquipmentSet[];
  
  const setIndex = sets.findIndex(s => s.id === id);
  const targetSet = sets[setIndex];
  
  if (!targetSet) return reply.status(404).send({ error: 'Não encontrado' });
  
  const updatedSet = updateEquipmentAcquisition(targetSet, key, acquired);
  sets[setIndex] = updatedSet;
  
  await fs.writeFile(DATA_FILE, JSON.stringify(sets, null, 2));
  return prepareSetForDisplay(updatedSet);
});

// Inicialização DIRETA e RÁPIDA
server.listen({ port: 3000, host: '0.0.0.0' }, (err, address) => {
  if (err) {
    console.error('❌ Erro Fatal ao abrir porta:', err);
    process.exit(1);
  }
  console.log(`🚀 SERVIDOR ESCUTANDO EM: ${address}`);
  
  // Inicializa dados APÓS o servidor estar escutando
  setupData().then(() => {
    console.log('📦 Arquivos de dados validados com sucesso.');
  });
});
