/**
 * Script de Importación Integral de Marketing a Plane
 * ====================================================
 * Instancia: https://projects.mastergroupve.com
 * Workspace: marketing
 * Archivo fuente: mkt-mastergroupve-a364fdad-78bb-45da-a511-996cddde338c-3d0b87dd.csv (70 tareas)
 * 
 * Soporta los 5 proyectos del espacio de trabajo:
 *  - Marketing (MKT / MARKE)
 *  - Eventos (EVENTOS)
 *  - Creadores (In House) (CREAINH)
 *  - ARGUS (ARGUS)
 *  - Pantalla Móvil (PANTALLAMV)
 */

const fs = require('fs');

const TOKEN = process.env.PLANE_API_KEY || 'plane_api_88d0adde65f14ab78a403bc61fe01449';
const BASE_URL = 'https://projects.mastergroupve.com';
const WORKSPACE_SLUG = 'marketing';
const DEFAULT_CSV = 'C:/Users/vmontoyaMG/Downloads/mkt-mastergroupve-a364fdad-78bb-45da-a511-996cddde338c-3d0b87dd.csv';

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

async function main() {
  const isDryRun = process.argv.includes('--dry-run');
  const targetCsv = process.argv[2] && !process.argv[2].startsWith('--') ? process.argv[2] : DEFAULT_CSV;

  console.log(`=======================================================`);
  console.log(`  IMPORTADOR DE MARKETING A PLANE (projects.mastergroupve.com)`);
  console.log(`=======================================================`);
  console.log(`Modo: ${isDryRun ? '🔍 SIMULACIÓN (DRY-RUN)' : '🚀 EJECUCIÓN REAL'}`);
  console.log(`Archivo: ${targetCsv}`);

  if (!fs.existsSync(targetCsv)) {
    console.error(`❌ Archivo no encontrado: ${targetCsv}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(targetCsv, 'utf8');
  const rows = parseCSV(raw);
  const data = rows.slice(1).filter(r => r.length > 4 && r[4] && r[4].trim());
  console.log(`📦 Total de tareas en archivo: ${data.length}\n`);

  // 1. Obtener miembros del workspace para mapear asignados
  const membersRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/members/`, { headers });
  const membersData = await membersRes.json();
  const membersList = Array.isArray(membersData) ? membersData : (membersData.results || []);
  const memberByEmail = new Map();
  membersList.forEach(m => {
    const email = m.email || m.member?.email;
    const id = m.id || m.member?.id;
    if (email && id) memberByEmail.set(email.toLowerCase(), id);
  });
  console.log(`👤 Miembros detectados: ${memberByEmail.size} (${Array.from(memberByEmail.keys()).join(', ')})`);

  // 2. Agrupar tareas por proyecto
  const projectGroups = new Map();
  data.forEach(r => {
    const projName = r[0] ? r[0].trim() : 'Marketing';
    const projIden = r[1] ? r[1].trim() : 'MKT';
    const key = projName;
    if (!projectGroups.has(key)) {
      projectGroups.set(key, { name: projName, identifier: projIden, rows: [] });
    }
    projectGroups.get(key).rows.push(r);
  });

  console.log(`📂 Proyectos detectados en el CSV: ${projectGroups.size}`);
  for (const [name, g] of projectGroups.entries()) {
    console.log(`   - ${name} [${g.identifier}]: ${g.rows.length} tareas`);
  }

  // 3. Procesar cada proyecto
  let totalCreated = 0;
  let totalSkipped = 0;

  for (const [projName, group] of projectGroups.entries()) {
    console.log(`\n=======================================================`);
    console.log(`Procesando Proyecto: ${projName} (${group.identifier})`);
    console.log(`=======================================================`);

    // Consultar proyectos en Plane
    const projRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/`, { headers });
    const projData = await projRes.json();
    const existingProjects = projData.results || [];

    let targetProject = existingProjects.find(p => 
      p.name.toLowerCase() === projName.toLowerCase() || 
      p.identifier.toLowerCase() === group.identifier.toLowerCase() ||
      (projName.toLowerCase() === 'marketing' && p.identifier.toLowerCase() === 'marke')
    );

    if (!targetProject) {
      if (isDryRun) {
        console.log(`[SIMULACIÓN] Crearía proyecto "${projName}" con prefijo "${group.identifier}"`);
        targetProject = { id: 'sim-' + group.identifier, name: projName };
      } else {
        console.log(`Creando proyecto "${projName}" [${group.identifier}] en Plane...`);
        const createRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/`, {
          method: 'POST',
          headers,
          body: JSON.stringify({ name: projName, identifier: group.identifier })
        });
        targetProject = await createRes.json();
        console.log(`✓ Proyecto creado (ID: ${targetProject.id})`);
      }
    } else {
      console.log(`✓ Proyecto existente: "${targetProject.name}" (ID: ${targetProject.id})`);
    }

    const projectId = targetProject.id;

    // Obtener estados del proyecto
    let stateMap = { backlog: null, todo: null, 'to do': null, 'in progress': null, done: null, cancelled: null };
    let defaultStateId = null;

    if (!isDryRun || !projectId.startsWith('sim-')) {
      const statesRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/states/`, { headers });
      const statesData = await statesRes.json();
      (statesData.results || []).forEach(s => {
        const sName = s.name.toLowerCase().trim();
        const sGroup = s.group?.toLowerCase().trim();
        if (sName.includes('backlog') || sGroup === 'backlog') stateMap['backlog'] = s.id;
        if (sName === 'todo' || sName === 'to do' || sGroup === 'unstarted') {
          stateMap['todo'] = s.id;
          stateMap['to do'] = s.id;
        }
        if (sName.includes('progress') || sGroup === 'started') stateMap['in progress'] = s.id;
        if (sName.includes('done') || sGroup === 'completed') stateMap['done'] = s.id;
        if (sName.includes('cancel') || sGroup === 'cancelled') stateMap['cancelled'] = s.id;
        if (!defaultStateId) defaultStateId = s.id;
      });
      defaultStateId = stateMap['backlog'] || defaultStateId;
    }

    // Obtener y sincronizar etiquetas
    const labelMap = new Map();
    if (!isDryRun || !projectId.startsWith('sim-')) {
      const labelsRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/labels/`, { headers });
      const labelsData = await labelsRes.json();
      (labelsData.results || []).forEach(l => labelMap.set(l.name.toLowerCase().trim(), l.id));
    }

    const projectLabels = new Set();
    group.rows.forEach(r => {
      const lbls = r[18];
      if (lbls) lbls.split('|').forEach(l => { if (l.trim()) projectLabels.add(l.trim()); });
    });

    const colors = ['#0079bf', '#eb5a46', '#61bd4f', '#f2d600', '#ff9f1a', '#c377e0', '#00c2e0'];
    let cIdx = 0;
    for (const lbl of projectLabels) {
      const lower = lbl.toLowerCase();
      if (!labelMap.has(lower)) {
        if (!isDryRun && !projectId.startsWith('sim-')) {
          const createLabelRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/labels/`, {
            method: 'POST',
            headers,
            body: JSON.stringify({ name: lbl, color: colors[cIdx % colors.length] })
          });
          const createdLabel = await createLabelRes.json();
          if (createdLabel.id) labelMap.set(lower, createdLabel.id);
          cIdx++;
        }
      }
    }

    // Limpiar tarjetas demo de prueba (solo si tienen nombres estándar de onboarding de Plane)
    const existingByName = new Map();
    if (!isDryRun || !projectId.startsWith('sim-')) {
      const issuesRes = await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/issues/?limit=200`, { headers });
      const issuesData = await issuesRes.json();
      const list = issuesData.results || [];
      for (const item of list) {
        if (item.name.includes('Welcome to Plane') || item.name.includes('Customize your settings') || 
            item.name.includes('Use Cycles to') || item.name.includes('Create Projects') || 
            item.name.includes('Invite your team') || item.name.includes('Create and assign Work Items') || 
            item.name.includes('Visualize your work')) {
          console.log(`  🗑️ Eliminando demo item: "${item.name}"`);
          await fetchWithRetry(`${BASE_URL}/api/v1/workspaces/${WORKSPACE_SLUG}/projects/${projectId}/issues/${item.id}/`, {
            method: 'DELETE',
            headers
          });
        } else {
          existingByName.set(item.name.trim().toLowerCase(), item);
        }
      }
    }

    // Separar padres e hijos
    const csvIdToPlaneId = new Map();
    const parents = group.rows.filter(r => !r[2] || !r[2].trim());
    const children = group.rows.filter(r => r[2] && r[2].trim());

    async function insertIssue(r, isSubtask) {
      const originalId = r[3];
      const parentId = r[2];
      const name = r[4].trim();
      const stateName = (r[5] || '').toLowerCase().trim();
      const priority = (r[6] || 'none').toLowerCase().trim();
      const assigneeEmail = r[7];
      const description = r[8];
      const startDate = r[11] || null;
      const dueDate = r[12] || null;
      const rawLabels = r[18];
      const rawLinks = r[23];

      if (existingByName.has(name.toLowerCase())) {
        const ex = existingByName.get(name.toLowerCase());
        csvIdToPlaneId.set(originalId, ex.id);
        totalSkipped++;
        console.log(`  ⏭️ Ya existe: "${name}"`);
        return;
      }

      const stateId = stateMap[stateName] || defaultStateId;
      const taskLabels = [];
      if (rawLabels) {
        rawLabels.split('|').forEach(l => {
          const lid = labelMap.get(l.trim().toLowerCase());
          if (lid) taskLabels.push(lid);
        });
      }

      const assignees = [];
      if (assigneeEmail) {
        assigneeEmail.split(/[|,]/).forEach(em => {
          const clean = em.trim().toLowerCase();
          if (memberByEmail.has(clean)) assignees.push(memberByEmail.get(clean));
        });
      }

      let planeParentId = null;
      if (isSubtask && parentId) {
        planeParentId = csvIdToPlaneId.get(parentId.trim()) || null;
      }

      const payload = {
        name,
        description_html: textToHtml(description),
        state: stateId,
        priority: ['urgent', 'high', 'medium', 'low', 'none'].includes(priority) ? priority : 'none',
        labels: taskLabels,
        assignees: assignees,
        parent: planeParentId,
        start_date: startDate || null,
        target_date: dueDate || null
      };

      if (isDryRun) {
        console.log(`  [SIMULACIÓN] Crear "${name}" (Estado: ${stateName || 'Backlog'})`);
        csvIdToPlaneId.set(originalId, 'sim-' + originalId);
        totalCreated++;
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
          csvIdToPlaneId.set(originalId, created.id);
          totalCreated++;
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

    console.log(`Insertando ${parents.length} tareas principales...`);
    for (let i = 0; i < parents.length; i++) {
      process.stdout.write(`[${i + 1}/${parents.length}] `);
      await insertIssue(parents[i], false);
    }

    if (children.length > 0) {
      console.log(`Insertando ${children.length} sub-tareas...`);
      for (let i = 0; i < children.length; i++) {
        process.stdout.write(`[${i + 1}/${children.length}] `);
        await insertIssue(children[i], true);
      }
    }
  }

  console.log(`\n=======================================================`);
  console.log(`✨ RESUMEN FINAL`);
  console.log(`=======================================================`);
  console.log(`Tareas Creadas / Importadas : ${totalCreated}`);
  console.log(`Tareas Omitidas (ya existían): ${totalSkipped}`);
  console.log(`Proceso completado exitosamente.`);
}

main().catch(err => {
  console.error('Error fatal:', err);
  process.exit(1);
});
