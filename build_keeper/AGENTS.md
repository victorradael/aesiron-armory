# AGENTS.md

## Objetivo
- Manter o app simples, previsivel e facil de evoluir.
- Priorizar legibilidade, baixo acoplamento e consistencia entre telas, regras e dados.

## Principios
- Faça mudancas pequenas, focadas e com impacto bem delimitado.
- Preserve o comportamento existente sempre que a tarefa nao exigir mudanca funcional.
- Prefira solucoes simples antes de introduzir novas camadas, abstrações ou dependencias.
- Mantenha nomes claros, consistentes e orientados ao dominio do app.

## Estrutura e organizacao
- Separe interface, regras de negocio e acesso a dados.
- Evite duplicacao; extraia helpers quando a mesma logica aparecer mais de uma vez.
- Nao misture tratamento visual com regra de negocio complexa.
- Centralize validacoes e transformacoes compartilhadas.

## Dados e regras
- Trate os dados com cuidado e preserve compatibilidade com o formato ja utilizado pelo app.
- Nunca remova ou altere campos persistidos sem necessidade explicita.
- Ao adicionar comportamento novo, considere estados vazios, dados incompletos e valores inesperados.
- Garanta que ordenacao, filtros e edicoes sejam deterministicas e faceis de entender.

## Interface
- Mantenha a experiencia objetiva, com textos claros e acoes previsiveis.
- Reaproveite padroes visuais e de interacao em vez de criar variacoes desnecessarias.
- Toda nova funcionalidade deve funcionar bem em desktop e mobile.
- Estados de sucesso, vazio, erro e carregamento devem ter feedback claro.

## Implementacao
- Prefira funcoes curtas e coesas.
- Evite comentarios desnecessarios; o codigo deve se explicar pelo nome das funcoes e variaveis.
- Nao introduza dependencias novas sem ganho claro de manutencao ou produtividade.
- Evite otimizações prematuras; melhore desempenho apenas quando houver necessidade real.

## Qualidade
- Valide manualmente os fluxos principais afetados pela mudanca.
- Considere casos limite antes de concluir a implementacao.
- Se uma regra mudar, ajuste a interface de forma coerente com o novo comportamento.
- Entregue sempre uma implementacao que outro agente consiga entender rapidamente.
