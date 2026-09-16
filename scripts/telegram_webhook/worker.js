/**
 * ALFRED 2brain — Cloudflare Worker Webhook 24/7 (Costo $0 USD)
 * Servidor Serverless en la nube para Telegram con soporte multimodal para texto y notas de voz.
 */

export default {
  async fetch(request, env, ctx) {
    // Si la petición es GET, responder estado operativo
    if (request.method !== 'POST') {
      return new Response('🎩 ALFRED 2brain Telegram Worker 24/7 está activo y operativo.', {
        status: 200,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' }
      });
    }

    try {
      const update = await request.json();
      if (!update.message) return new Response('OK', { status: 200 });

      const message = update.message;
      const chatId = message.chat.id;
      const text = (message.text || '').trim();
      const sender = message.from?.first_name || 'Señor';

      // 1. Obtener la última versión del Dashboard de Vida desde GitHub
      let dashboardCtx = "Dashboard de Vida del sistema 2brain.";
      try {
        const ghHeaders = { 'User-Agent': 'ALFRED-Worker-2brain' };
        if (env.GH_TOKEN) {
          ghHeaders['Authorization'] = `token ${env.GH_TOKEN}`;
        }
        const ghRes = await fetch('https://raw.githubusercontent.com/vmontoyasmtop/2brain-vmontoya/master/wiki/life-dashboard.md', { headers: ghHeaders });
        if (ghRes.ok) {
          const rawDash = await ghRes.text();
          dashboardCtx = rawDash.substring(0, 2000);
        }
      } catch (e) {
        console.error('Error al obtener dashboard desde GitHub:', e);
      }

      // Prompt de Sistema de ALFRED
      const systemPrompt = `Tu nombre es ALFRED. Eres el Mayordomo de Vida y Asistente Ejecutivo Personal del usuario en su sistema 2brain.
Te diriges al usuario con el trato de 'Señor', actuando con máxima cortesía, profesionalismo, elegancia y eficiencia.

Conocimiento del 2brain del usuario (Resumen Dashboard):
${dashboardCtx}

Responde de forma concisa, profesional y formal en español, como el fiel mayordomo ALFRED.`;

      // Comando /start o /help
      if (text.startsWith('/start') || text.startsWith('/help')) {
        const helpMsg = `🎩 *ALFRED — Mayordomo Ejecutivo 2brain (Nube 24/7)*\n\n` +
          `¡A sus órdenes, Señor ${sender}! Estoy activo las 24 horas del día desde la nube.\n\n` +
          `💬 *1. Mensajes de Texto y Notas de Voz*:\n` +
          `• Envíeme cualquier consulta por texto o nota de voz.\n` +
          `• Escucharé y responderé inmediatamente usando mi motor Gemini 3.6 Flash.\n\n` +
          `📌 *Estado*: Operativo 24/7 en Cloudflare Workers ($0 USD).`;
        
        await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ chat_id: chatId, text: helpMsg, parse_mode: 'Markdown' })
        });
        return new Response('OK', { status: 200 });
      }

      // 2. Procesamiento Multimodal (Texto o Notas de Voz)
      const hasVoice = Boolean(message.voice);
      const hasAudio = Boolean(message.audio);

      let parts = [];
      let captionText = text;

      if (hasVoice || hasAudio) {
        const audioItem = message.voice || message.audio;
        const fileId = audioItem.file_id;
        const mimeType = audioItem.mime_type || (hasVoice ? 'audio/ogg' : 'audio/mp3');
        captionText = (message.caption || '').trim();

        // Notificar que ALFRED está procesando voz...
        ctx.waitUntil(
          fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendChatAction`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ chat_id: chatId, action: 'record_voice' })
          })
        );

        // Descargar el archivo desde Telegram
        const fileRes = await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/getFile?file_id=${fileId}`);
        const fileData = await fileRes.json();
        if (fileData.ok && fileData.result?.file_path) {
          const dlUrl = `https://api.telegram.org/file/bot${env.TELEGRAM_BOT_TOKEN}/${fileData.result.file_path}`;
          const audioRes = await fetch(dlUrl);
          const audioBuf = await audioRes.arrayBuffer();

          // Convertir buffer a base64
          let binary = '';
          const bytes = new Uint8Array(audioBuf);
          for (let i = 0; i < bytes.byteLength; i++) {
            binary += String.fromCharCode(bytes[i]);
          }
          const base64Audio = btoa(binary);

          parts.push({
            inline_data: {
              mime_type: mimeType,
              data: base64Audio
            }
          });
        }
      }

      const promptMsg = captionText || (hasVoice || hasAudio 
        ? "Escucha con atención la nota de voz enviada por el Señor y responde a su solicitud o consulta con total elegancia y eficiencia." 
        : text);

      parts.push({ text: promptMsg });

      // 3. Consulta a Gemini 3.6 Flash con retornos de resiliencia
      const candidateModels = ["gemini-3.6-flash", "gemini-3.5-flash", "gemini-2.5-flash"];
      let replyText = "A su servicio, Señor.";
      let success = false;

      for (const modelName of candidateModels) {
        const geminiUrl = `https://generativelanguage.googleapis.com/v1beta/models/${modelName}:generateContent?key=${env.GEMINI_API_KEY}`;
        const geminiPayload = {
          system_instruction: { parts: [{ text: systemPrompt }] },
          contents: [{ role: 'user', parts: parts }]
        };

        try {
          const geminiRes = await fetch(geminiUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(geminiPayload)
          });

          if (geminiRes.ok) {
            const geminiData = await geminiRes.json();
            const textPart = geminiData.candidates?.[0]?.content?.parts?.[0]?.text;
            if (textPart) {
              replyText = textPart;
              success = true;
              break;
            }
          }
        } catch (err) {
          console.error(`Error con modelo ${modelName}:`, err);
        }
      }

      if (!success && !replyText) {
        replyText = "Disculpe la molestia, Señor. Ocurrió una saturación temporal en el servidor de IA.";
      }

      // 4. Enviar respuesta a Telegram
      await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: chatId,
          text: replyText
        })
      });

      return new Response('OK', { status: 200 });
    } catch (err) {
      console.error('Error general en Webhook Worker:', err);
      return new Response('OK', { status: 200 });
    }
  }
};
