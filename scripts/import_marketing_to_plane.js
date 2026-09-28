/**
 * Script Maestro de Importación para Plane (projects.mastergroupve.com)
 * ====================================================================
 * Soporta la importación del proyecto Marketing (43 tareas) y opcionalmente
 * de todos los proyectos del lote de exportación (Eventos, Creadores In House, ARGUS).
 */

const fs = require('fs');
const path = require('path');

const TOKEN = process.env.PLANE_API_KEY || 'plane_api_88d0adde65f14ab78a403bc61fe01449';
const BASE_URL = 'https://projects.mastergroupve.com';
const WORKSPACE_SLUG = 'marketing';

const CSV_MARKETING = 'C:/Users/vmontoyaMG/Downloads/mkt-mastergroupve-a364fdad-78bb-45da-a511-996cddde338c-4e141f62.csv';
const CSV_EVENTOS = 'C:/Users/vmontoyaMG/Downloads/mkt-mastergroupve-a364fdad-78bb-45da-a511-996cddde338c-11c36639.csv';
const CSV_CREADORES = 'C:/Users/vmontoyaMG/Downloads/mkt-mastergroupve-a364fdad-78bb-45da-a511-996cddde338c-3f556f94.csv';
const CSV_ARGUS = 'C:/Users/vmontoyaMG/Downloads/mkt-mastergroupve-a364fdad-78bb-45da-a511-996cddde338c-d69d95cd.csv';

const ALL_PROJECT_FILES = [
  { name: 'Marketing', identifier: 'MARKE', file: CSV_MARKETING },
  { name: 'Eventos', identifier: 'EVENT', file: CSV_EVENTOS },
  { name: 'Creadores (In House)', identifier: 'CREAI', file: CSV_CREADORES },
  { name: 'ARGUS', identifier: 'ARGUS', file: CSV_ARGUS }
];

const headers = {
  'x-api-key': TOKEN,
  'Content-Type': 'application/json'
};

function parseCSV(text) {
  const p = [];
  let row = [''];
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    const next = text[i+1];
    if (c === '"') {
      if (inQuotes && next === '"') {
        row[row.length - 1] += '"';
        i++;
      } else {
        inQuotes = !inQuotes;
      }
    } else if (c === ',' && !inQuotes) {
      row.push('');
    } else if ((c === '\r' || c === '\n') && !inQuotes) {
      if (c === '\r' && next === '\n') i++;
      p.push(row);
      row = [''];
    } else {
      row[row.length - 1] += c;
    }
  }
  if (row.length > 1 || row[0] !== '') p.push(row);
  return p;
}

function textToHtml(text) {
  if (!text) return '<p></p>';
  const escaped = text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
  return escaped.split(/\r?\n/).map(line => `<p>${line || '<br/>'}</p>`).join('');
}

async function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function fetchWithRetry(url, options = {}, retries = 5) {
  for (let attempt = 0; attempt < retries; attempt++) {
    const res = await fetch(url, options);
    if (res.status === 429) {
      const waitSec = parseInt(res.headers.get('retry-after') || '3', 10);
      console.log(`⏳ Rate limit alcanzado. Esperando ${waitSec + 1}s (intento ${attempt + 1}/${retries})...`);
      await sleep((waitSec + 1) * 1000);
      continue;
    }
    return res;
  }
  return await fetch(url, options);
}

async function importProject(projectInfo, isDryRun, cleanDemo = false) {
  console.log(`\n=======================================================`);
  console.log(`📂 PROYECTO: ${projectInfo.name} (${projectInfo.identifier})`);
  console.log(`=======================================================`);

  if (!fs.existsSync(projectInfo.file)) {
    console.log(`⚠️ Archivo ${projectInfo.file} no encontrado.`);
    return;
  }

  const raw = fs.readFileSync(projectInfo.file, 'utf8');
  if (raw.trim().length === 0) {
    console.log(`⚠️ Archivo ${projectInfo.file} está vacío (0 bytes).`);
    return;
  }

  const rows = parseCSV(raw);
  const data = rows.slice(1).filter(r => r.length > 4 && r[4] && r[4].trim());
  console.log(`📦 Tareas a importar: ${data.length}`);

  // 1. Obtener o crear proyecto en Plane
  const projRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/`, { headers });
  const projData = await projRes.json();
  const existingProjects = projData.results || [];
  let targetProject = existingProjects.find(p => p.name.toLowerCase() === projectInfo.name.toLowerCase() || p.identifier.toLowerCase() === projectInfo.identifier.toLowerCase());

  if (!targetProject) {
    if (isDryRun) {
      console.log(`[SIMULACIÓN] Crearía proyecto "${projectInfo.name}" (${projectInfo.identifier})`);
      targetProject = { id: 'sim-proj-' + projectInfo.identifier, name: projectInfo.name };
    } else {
      console.log(`Creando proyecto "${projectInfo.name}" (${projectInfo.identifier})...`);
      const createProjRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ name: projectInfo.name, identifier: projectInfo.identifier })
      });
      targetProject = await createProjRes.json();
      console.log(`✓ Proyecto creado (ID: ${targetProject.id})`);
    }
  } else {
    console.log(`✓ Proyecto encontrado: "${targetProject.name}" (ID: ${targetProject.id})`);
  }

  const projectId = targetProject.id;

  // 2. Obtener estados del proyecto
  let stateMap = {
    'backlog': null,
    'todo': null,
    'to do': null,
    'in progress': null,
    'done': null,
    'cancelled': null
  };
  let defaultStateId = null;

  if (!isDryRun || !projectId.startsWith('sim-')) {
    const statesRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/states/`, { headers });
    const statesData = await statesRes.json();
    (statesData.results || []).forEach(s => {
      const name = s.name.toLowerCase().trim();
      const group = s.group?.toLowerCase().trim();
      if (name.includes('backlog') || group === 'backlog') stateMap['backlog'] = s.id;
      if (name === 'todo' || name === 'to do' || group === 'unstarted') {
        stateMap['todo'] = s.id;
        stateMap['to do'] = s.id;
      }
      if (name.includes('progress') || group === 'started') stateMap['in progress'] = s.id;
      if (name.includes('done') || group === 'completed') stateMap['done'] = s.id;
      if (name.includes('cancel') || group === 'cancelled') stateMap['cancelled'] = s.id;
      if (!defaultStateId) defaultStateId = s.id;
    });
    defaultStateId = stateMap['backlog'] || defaultStateId;
  }

  // 3. Obtener etiquetas existentes
  const labelMap = new Map();
  if (!isDryRun || !projectId.startsWith('sim-')) {
    const labelsRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/labels/`, { headers });
    const labelsData = await labelsRes.json();
    (labelsData.results || []).forEach(l => labelMap.set(l.name.toLowerCase().trim(), l.id));
  }

  // Crear etiquetas faltantes
  const uniqueLabels = new Set();
  data.forEach(r => {
    const lbls = r[18];
    if (lbls) lbls.split('|').forEach(l => { if (l.trim()) uniqueLabels.add(l.trim()); });
  });

  const colors = ['#0079bf', '#eb5a46', '#61bd4f', '#f2d600', '#ff9f1a', '#c377e0'];
  let colorIdx = 0;
  for (const lbl of uniqueLabels) {
    const lower = lbl.toLowerCase();
    if (!labelMap.has(lower)) {
      if (!isDryRun && !projectId.startsWith('sim-')) {
        const createRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/labels/`, {
          method: 'POST',
          headers,
          body: JSON.stringify({ name: lbl, color: colors[colorIdx % colors.length] })
        });
        const created = await createRes.json();
        if (created.id) labelMap.set(lower, created.id);
        colorIdx++;
      } else {
        console.log(`  [SIMULACIÓN] Crearía etiqueta: "${lbl}"`);
      }
    }
  }

  // 4. Limpiar tareas demo si se solicita
  const existingByName = new Map();
  if (!isDryRun || !projectId.startsWith('sim-')) {
    const issuesRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/issues/?limit=200`, { headers });
    const issuesData = await issuesRes.json();
    const list = issuesData.results || [];
    for (const item of list) {
      if (cleanDemo && (item.name.includes('Welcome to Plane') || item.name.includes('Customize your settings') || item.name.includes('Use Cycles') || item.name.includes('Create Projects') || item.name.includes('Invite your team') || item.name.includes('Create and assign') || item.name.includes('Visualize your work'))) {
        console.log(`  🗑️ Eliminando tarea demo: "${item.name}"`);
        await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/issues/${item.id}/`, {
          method: 'DELETE',
          headers
        });
      } else {
        existingByName.set(item.name.trim().toLowerCase(), item);
      }
    }
  }

  // 5. Inserción jerárquica
  const csvIdentifierToPlaneId = new Map();
  const parents = data.filter(r => !r[2] || !r[2].trim());
  const children = data.filter(r => r[2] && r[2].trim());

  async function insertRow(r, isSubtask) {
    const originalId = r[3];
    const parentId = r[2];
    const name = r[4].trim();
    const stateName = (r[5] || '').toLowerCase().trim();
    const priority = (r[6] || 'none').toLowerCase().trim();
    const description = r[8];
    const startDate = r[11] || null;
    const dueDate = r[12] || null;
    const rawLabels = r[18];
    const rawLinks = r[23];

    if (existingByName.has(name.toLowerCase())) {
      const existing = existingByName.get(name.toLowerCase());
      csvIdentifierToPlaneId.set(originalId, existing.id);
      console.log(`  ⏭️ Ya existe: "${name}"`);
      return;
    }

    const stateId = stateMap[stateName] || defaultStateId;
    const taskLabels = [];
    if (rawLabels) {
      rawLabels.split('|').forEach(l => {
        const id = labelMap.get(l.trim().toLowerCase());
        if (id) taskLabels.push(id);
      });
    }

    let planeParentId = null;
    if (isSubtask && parentId) {
      planeParentId = csvIdentifierToPlaneId.get(parentId.trim()) || null;
    }

    const payload = {
      name,
      description_html: textToHtml(description),
      state: stateId,
      priority: ['urgent', 'high', 'medium', 'low', 'none'].includes(priority) ? priority : 'none',
      labels: taskLabels,
      parent: planeParentId,
      start_date: startDate || null,
      target_date: dueDate || null
    };

    if (isDryRun) {
      console.log(`  [SIMULACIÓN] Crear "${name}" (Estado: ${stateName || 'Backlog'})`);
      csvIdentifierToPlaneId.set(originalId, 'sim-' + originalId);
      return;
    }

    try {
      const createRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/issues/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload)
      });
      const created = await createRes.json();
      if (created.id) {
        csvIdentifierToPlaneId.set(originalId, created.id);
        console.log(`  ✅ Creado: [${created.sequence_id || 'OK'}] "${name}"`);

        if (rawLinks && rawLinks.trim()) {
          const linksList = rawLinks.split('|');
          for (const item of linksList) {
            const [url, title] = item.split(';');
            if (url && url.startsWith('http')) {
              await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/issues/${created.id}/links/`, {
                method: 'POST',
                headers,
                body: JSON.stringify({ url: url.trim(), title: (title || 'Enlace adjunto').trim() })
              });
            }
          }
        }
      } else {
        console.error(`  ❌ Error en "${name}":`, created);
      }
      await sleep(150);
    } catch (e) {
      console.error(`  ❌ Excepción en "${name}":`, e.message);
    }
  }

  console.log(`\nInsertando ${parents.length} tareas principales...`);
  for (let i = 0; i < parents.length; i++) {
    process.stdout.write(`[${i + 1}/${parents.length}] `);
    await insertRow(parents[i], false);
  }

  if (children.length > 0) {
    console.log(`\nInsertando ${children.length} sub-tareas...`);
    for (let i = 0; i < children.length; i++) {
      process.stdout.write(`[${i + 1}/${children.length}] `);
      await insertRow(children[i], true);
    }
  }
}

async function main() {
  const isDryRun = process.argv.includes('--dry-run');
  const importAll = process.argv.includes('--all');
  const cleanDemo = process.argv.includes('--clean-demo');

  console.log(`Iniciando Importador de Plane... (Modo: ${isDryRun ? 'SIMULACIÓN' : 'REAL'})`);

  if (importAll) {
    for (const proj of ALL_PROJECT_FILES) {
      await importProject(proj, isDryRun, cleanDemo);
    }
  } else {
    // Solo el proyecto Marketing por defecto
    await importProject(ALL_PROJECT_FILES[0], isDryRun, cleanDemo);
  }

  console.log('\n✨ Completado con éxito.');
}

main().catch(err => {
  console.error('Error fatal:', err);
  process.exit(1);
});
