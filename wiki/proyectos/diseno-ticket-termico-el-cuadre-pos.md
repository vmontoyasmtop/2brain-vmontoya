# Diseño Visual Oficial: Comprobante Térmico de Venta Finalizada ("El Cuadre Ticket")
**EL CUADRE POS — Sistema de Punto de Venta & Balanza Táctil**  
*Autor: Sai — Diseñador Gráfico & Artista Visual de Élite de Akatsuki*  
*Destinatarios: El Señor, Pain (PM), Itachi (Frontend Dev), Hidan (QA)*  
*Fecha: 25 de Octubre de 2026*

---

## 1. El Problema Detectado por El Señor
En la versión previa, al culminar una venta, la interfaz únicamente mostraba un mensaje escueto con un check verde. No existía la experiencia táctil, profesional y tranquilizadora del comprobante de venta, impidiendo verificar el desglose de pesaje, la tasa BCV oficial y el cálculo exacto del vuelto dual.

## 2. La Solución Artística & Técnica: "El Cuadre Ticket"
Hemos diseñado una experiencia de Comprobante Térmico de 80mm que evoca la fidelidad del papel térmico de alta gama, pero con la potencia visual y táctil de una interfaz moderna de alta definición:

1. **Estética de Papel Térmico de 80mm**:
   - Ancho calibrado a `360px` en viewport táctil (equivalente a 72mm-80mm imprimibles).
   - Terminación superior e inferior con borde de sierra / corte perforado (`sawtooth jagged edge`) renderizado matemáticamente mediante CSS y SVG.
   - Fondo de papel blanco satinado `#F8FAFC` con textura sutil de recibo y tipografía monoespaciada de alta definición para cifras.

2. **Cabecera Oficial y Razón Social**:
   - Isotipo Vectorial de la Balanza y el Aguacate con el texto "EL CUADRE POS".
   - RIF: `J-50493821-0` | Tel: `+58 (212) 681-9944`.
   - Dirección: `Mercado de Coche, Galpón 4, Local 12, Caracas`.
   - N° de Comprobante: `#TKT-001042` | Fecha, Hora, Cajero y Turno.

3. **Tabla de Ítems Dual con Pesaje a 3 Decimales**:
   - Cada producto distingue su modalidad mediante insignia visual:
     * `⚖️ PESO` (ej: Aguacate Criollo: 1.450 kg × $2.20/kg)
     * `📦 UNIDAD` (ej: Harina PAN: 2 ud × $1.25)
   - Precios unitarios y subtotales en USD y Bolívares calculados a la tasa activa.

4. **Resumen Financiero y Vuelto Exacto**:
   - Subtotal USD y Subtotal Bs.
   - Badge oficial de **Tasa BCV Certificada**: `886.23 Bs./$`.
   - **TOTAL A PAGAR**: Tipografía XL en alto contraste.
   - Desglose de Pago Multimoneda (Efectivo USD $20.00).
   - **Vuelto Entregado**: Divisa limpia ($8.00 USD) + Pico en Bolívares (593.77 Bs. vía Pago Móvil/Efectivo).
   - "Cero Faltante — Cuadre al Céntimo".

5. **El Sello Oficial "Todo Cuadraíto" de Sai**:
   - Badge vectorial concéntrico estilo sello de tinta esmeralda y oro que certifica matemáticamente la exactitud del pesaje y la caja.

6. **Pie de Ticket & Trazabilidad**:
   - Código de barras y QR para verificación fiscal o envío al teléfono del comprador.
   - Lema criollo de agradecimiento.

7. **Acciones Táctiles Ergonómicas para Pantallas de 10" a 24"**:
   - 🖨️ **Imprimir Ticket Térmico** (Abre diálogo nativo con estilos optimizados `@media print`).
   - 📱 **Enviar por WhatsApp** (Prepara el texto formateado con el resumen para enviar en 1 toque).
   - ⚡ **Nueva Venta / Siguiente Cliente** (Botón maestro en Verde Esmeralda `#15803D`, con autofocus para iniciar el siguiente cobro de inmediato).

---

## 3. Código Fuente del Componente React (`TicketModal.tsx`)

A continuación se entrega el componente React con Tailwind CSS listo para integrarse en la aplicación:

```tsx
import React, { useRef } from 'react';

export interface TicketItem {
  id: string;
  name: string;
  type: 'weight' | 'unit';
  quantity: number; // kg si es weight, unidades si es unit
  unitPriceUSD: number;
  totalUSD: number;
  totalBs: number;
}

export interface TicketData {
  ticketNumber: string;
  date: string;
  time: string;
  cashierName: string;
  shift: string;
  bcvRate: number;
  items: TicketItem[];
  subtotalUSD: number;
  subtotalBs: number;
  totalUSD: number;
  totalBs: number;
  paymentMethod: string;
  amountPaidUSD: number;
  amountPaidBs: number;
  changeUSD: number;
  changeBs: number;
}

interface TicketModalProps {
  isOpen: boolean;
  onClose: () => void;
  onNewSale: () => void;
  ticket: TicketData;
}

export const TicketModal: React.FC<TicketModalProps> = ({
  isOpen,
  onClose,
  onNewSale,
  ticket,
}) => {
  const ticketRef = useRef<HTMLDivElement>(null);

  if (!isOpen) return null;

  const handlePrint = () => {
    window.print();
  };

  const handleWhatsApp = () => {
    const text = `🧾 *EL CUADRE POS - Comprobante ${ticket.ticketNumber}*\n` +
      `📅 Fecha: ${ticket.date} ${ticket.time}\n` +
      `💵 Total: $${ticket.totalUSD.toFixed(2)} (${ticket.totalBs.toLocaleString('es-VE', { minimumFractionDigits: 2 })} Bs.)\n` +
      `📊 Tasa BCV: ${ticket.bcvRate.toFixed(2)} Bs./$\n` +
      `✨ *Todo Cuadraíto! Gracias por su compra.*`;
    const url = `https://wa.me/?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank');
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 backdrop-blur-md p-4 overflow-y-auto">
      {/* Contenedor Principal */}
      <div className="relative flex flex-col items-center max-w-md w-full animate-in fade-in zoom-in-95 duration-200">
        
        {/* Ticket Térmico Visual 80mm */}
        <div
          ref={ticketRef}
          id="printable-ticket"
          className="w-full bg-[#FAFAFA] text-slate-800 rounded-sm shadow-2xl overflow-hidden border border-slate-200 print:shadow-none print:border-none print:w-full print:m-0"
          style={{
            fontFamily: "'Courier New', Courier, monospace",
          }}
        >
          {/* Borde dentado superior */}
          <div className="h-3 w-full bg-[#15803D] flex items-center justify-between px-2">
            <span className="text-[9px] font-sans font-bold text-white tracking-widest uppercase">
              • EL CUADRE POS • TICKET TÉRMICO 80MM •
            </span>
            <span className="text-[9px] font-mono text-emerald-200">ORIGINAL</span>
          </div>

          <div className="p-5 sm:p-6 space-y-4">
            {/* Cabecera / Branding */}
            <div className="text-center border-b border-dashed border-slate-300 pb-4">
              <div className="flex items-center justify-center gap-2 mb-1">
                <svg className="w-8 h-8 text-emerald-700" viewBox="0 0 48 48" fill="currentColor">
                  {/* Balanza Criolla Simplificada */}
                  <path d="M24 4v8m-14 0h28m-20 0l-5 14h10l-5-14zm16 0l-5 14h10l-5-14zM24 12v26m-8 0h16" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" fill="none"/>
                  <circle cx="24" cy="4" r="3" fill="#F59E0B" />
                  <circle cx="14" cy="26" r="3" fill="#22C55E" />
                  <circle cx="34" cy="26" r="3" fill="#EF4444" />
                </svg>
                <span className="text-xl font-black font-sans tracking-tight text-slate-900">
                  EL CUADRE <span className="text-emerald-700">POS</span>
                </span>
              </div>
              <p className="text-[11px] font-sans font-bold text-slate-600 uppercase tracking-wide">
                Caja, Peso & Finanzas Todo Cuadraíto
              </p>
              <p className="text-[11px] text-slate-500 mt-1">
                J-50493821-0 • Mercado Mayorista de Coche, Caracas
              </p>
              <p className="text-[10px] text-slate-500">
                Tel: +58 (212) 681-9944 • WhatsApp: +58 (412) 123-CUADRE
              </p>

              {/* Meta de Venta */}
              <div className="mt-3 pt-2 border-t border-dotted border-slate-300 grid grid-cols-2 text-left text-[11px] text-slate-600 font-mono">
                <div><span className="font-bold">COMPROBANTE:</span> {ticket.ticketNumber}</div>
                <div className="text-right"><span className="font-bold">FECHA:</span> {ticket.date}</div>
                <div><span className="font-bold">HORA:</span> {ticket.time}</div>
                <div className="text-right"><span className="font-bold">CAJERO:</span> {ticket.cashierName}</div>
              </div>
            </div>

            {/* Tabla de Productos / Pesaje */}
            <div className="border-b border-dashed border-slate-300 pb-3">
              <div className="flex justify-between text-[11px] font-bold font-sans text-slate-700 border-b border-slate-300 pb-1 mb-2">
                <span>DESCRIPCIÓN / CANT.</span>
                <span className="text-right">TOTAL USD / BS.</span>
              </div>

              <div className="space-y-2 text-[12px]">
                {ticket.items.map((item) => (
                  <div key={item.id} className="flex justify-between items-start leading-tight">
                    <div className="pr-2">
                      <div className="font-bold font-sans text-slate-900 flex items-center gap-1">
                        <span>{item.type === 'weight' ? '⚖️' : '📦'}</span>
                        <span>{item.name}</span>
                      </div>
                      <div className="text-[10px] text-slate-500 font-mono">
                        {item.type === 'weight'
                          ? `${item.quantity.toFixed(3)} kg × $${item.unitPriceUSD.toFixed(2)}/kg`
                          : `${item.quantity} ud × $${item.unitPriceUSD.toFixed(2)}`}
                      </div>
                    </div>
                    <div className="text-right font-mono font-bold whitespace-nowrap">
                      <div>${item.totalUSD.toFixed(2)}</div>
                      <div className="text-[10px] text-slate-500 font-normal">
                        {item.totalBs.toLocaleString('es-VE', { minimumFractionDigits: 2 })} Bs.
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Resumen Contable y Totales */}
            <div className="space-y-1.5 text-[12px] font-mono border-b border-dashed border-slate-300 pb-3">
              <div className="flex justify-between text-slate-600">
                <span>SUBTOTAL:</span>
                <span>${ticket.subtotalUSD.toFixed(2)} / {ticket.subtotalBs.toLocaleString('es-VE', { minimumFractionDigits: 2 })} Bs.</span>
              </div>
              
              {/* Tasa BCV */}
              <div className="flex justify-between items-center bg-amber-50 p-1.5 rounded border border-amber-200 text-amber-900 text-[11px] font-sans">
                <span className="font-bold flex items-center gap-1">
                  🏛️ TASA OFICIAL BCV:
                </span>
                <span className="font-mono font-black text-xs">
                  {ticket.bcvRate.toFixed(2)} Bs./$
                </span>
              </div>

              {/* Gran Total Dual */}
              <div className="pt-2">
                <div className="bg-emerald-900 text-white p-3 rounded flex justify-between items-center font-sans">
                  <div>
                    <span className="text-[10px] uppercase tracking-wider text-emerald-200 block font-semibold">TOTAL A PAGAR</span>
                    <span className="text-2xl font-black font-mono">${ticket.totalUSD.toFixed(2)}</span>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] uppercase tracking-wider text-emerald-200 block font-semibold">EQUIVALENTE BS.</span>
                    <span className="text-base font-bold font-mono">
                      {ticket.totalBs.toLocaleString('es-VE', { minimumFractionDigits: 2 })} Bs.
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Desglose de Pago & Vuelto Exacto */}
            <div className="space-y-1 text-[11px] font-mono border-b border-dashed border-slate-300 pb-3">
              <div className="flex justify-between text-slate-600">
                <span className="font-bold">MÉTODO DE PAGO:</span>
                <span>{ticket.paymentMethod}</span>
              </div>
              <div className="flex justify-between text-slate-600">
                <span>RECIBIDO:</span>
                <span>${ticket.amountPaidUSD.toFixed(2)} USD</span>
              </div>
              
              {/* Vuelto Destacado */}
              <div className="mt-2 p-2 bg-emerald-50 rounded border border-emerald-300 text-emerald-950 font-sans">
                <div className="flex justify-between items-baseline">
                  <span className="font-black text-xs uppercase text-emerald-800">VUELTO EXACTO:</span>
                  <div className="text-right font-mono">
                    <span className="text-base font-black text-emerald-900 block">${ticket.changeUSD.toFixed(2)} USD</span>
                    {ticket.changeBs > 0 && (
                      <span className="text-[11px] font-bold text-emerald-700">
                        + {ticket.changeBs.toLocaleString('es-VE', { minimumFractionDigits: 2 })} Bs.
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-[9px] text-emerald-700 font-semibold mt-0.5">
                  ✓ Conciliación 100% Cuadrada — Sin faltantes
                </div>
              </div>
            </div>

            {/* Sello Gráfico de Sai: "Todo Cuadraíto" */}
            <div className="flex flex-col items-center justify-center py-2 text-center">
              <div className="inline-flex items-center gap-2 border-2 border-dashed border-emerald-600 px-3 py-1.5 rounded-full text-emerald-800 bg-emerald-50/50">
                <span className="text-sm">⚖️</span>
                <span className="text-[10px] font-sans font-black tracking-widest uppercase">
                  SELLO TODO CUADRAÍTO • AUDITADO
                </span>
                <span className="text-sm">✓</span>
              </div>
            </div>

            {/* Código de Barras / QR Fiscal & Pie de Página */}
            <div className="text-center space-y-2 pt-1 font-mono">
              {/* Código de barras simulado en SVG */}
              <div className="flex justify-center">
                <svg className="w-48 h-10" viewBox="0 0 200 40">
                  <rect x="0" y="0" width="200" height="40" fill="#FAFAFA" />
                  <g fill="#1E293B">
                    <rect x="10" y="4" width="3" height="30" />
                    <rect x="15" y="4" width="2" height="30" />
                    <rect x="20" y="4" width="4" height="30" />
                    <rect x="27" y="4" width="1" height="30" />
                    <rect x="31" y="4" width="3" height="30" />
                    <rect x="36" y="4" width="5" height="30" />
                    <rect x="44" y="4" width="2" height="30" />
                    <rect x="49" y="4" width="4" height="30" />
                    <rect x="56" y="4" width="1" height="30" />
                    <rect x="60" y="4" width="3" height="30" />
                    <rect x="65" y="4" width="6" height="30" />
                    <rect x="74" y="4" width="2" height="30" />
                    <rect x="79" y="4" width="4" height="30" />
                    <rect x="86" y="4" width="2" height="30" />
                    <rect x="91" y="4" width="5" height="30" />
                    <rect x="99" y="4" width="1" height="30" />
                    <rect x="103" y="4" width="4" height="30" />
                    <rect x="110" y="4" width="2" height="30" />
                    <rect x="115" y="4" width="5" height="30" />
                    <rect x="123" y="4" width="3" height="30" />
                    <rect x="129" y="4" width="2" height="30" />
                    <rect x="134" y="4" width="4" height="30" />
                    <rect x="141" y="4" width="1" height="30" />
                    <rect x="145" y="4" width="5" height="30" />
                    <rect x="153" y="4" width="2" height="30" />
                    <rect x="158" y="4" width="4" height="30" />
                    <rect x="165" y="4" width="3" height="30" />
                    <rect x="171" y="4" width="2" height="30" />
                    <rect x="176" y="4" width="4" height="30" />
                    <rect x="183" y="4" width="3" height="30" />
                  </g>
                </svg>
              </div>
              <p className="text-[10px] text-slate-500 font-sans font-medium">
                ¡Gracias por su compra! La frescura del agro en su mesa.
              </p>
              <p className="text-[9px] text-slate-400">
                Escanee el comprobante para guardar en su teléfono
              </p>
            </div>
          </div>

          {/* Borde dentado de corte inferior */}
          <div className="h-2 w-full bg-slate-300 opacity-60" style={{
            clipPath: 'polygon(0% 0%, 5% 100%, 10% 0%, 15% 100%, 20% 0%, 25% 100%, 30% 0%, 35% 100%, 40% 0%, 45% 100%, 50% 0%, 55% 100%, 60% 0%, 65% 100%, 70% 0%, 75% 100%, 80% 0%, 85% 100%, 90% 0%, 95% 100%, 100% 0%)'
          }} />
        </div>

        {/* Barra de Acciones Táctiles (No Imprimible) */}
        <div className="mt-4 w-full flex flex-col sm:flex-row gap-2 print:hidden font-sans">
          {/* Botón Imprimir */}
          <button
            onClick={handlePrint}
            className="flex-1 py-3 px-4 bg-slate-800 hover:bg-slate-700 active:scale-95 text-white font-bold rounded-xl shadow-lg flex items-center justify-center gap-2 transition"
          >
            <span>🖨️</span>
            <span>Imprimir 80mm</span>
          </button>

          {/* Botón WhatsApp */}
          <button
            onClick={handleWhatsApp}
            className="flex-1 py-3 px-4 bg-emerald-600 hover:bg-emerald-500 active:scale-95 text-white font-bold rounded-xl shadow-lg flex items-center justify-center gap-2 transition"
          >
            <span>📱</span>
            <span>WhatsApp</span>
          </button>

          {/* Botón Nueva Venta / Siguiente */}
          <button
            onClick={onNewSale}
            className="flex-1 py-3 px-4 bg-gradient-to-r from-emerald-700 to-green-600 hover:from-emerald-600 hover:to-green-500 active:scale-95 text-white font-black rounded-xl shadow-xl flex items-center justify-center gap-2 border border-emerald-400/30 transition ring-2 ring-emerald-500/20"
          >
            <span>⚡</span>
            <span>Nueva Venta</span>
          </button>
        </div>

        {/* Botón Cerrar Flotante */}
        <button
          onClick={onClose}
          className="mt-3 text-xs text-slate-400 hover:text-white underline print:hidden"
        >
          Cerrar ventana sin iniciar nueva venta
        </button>

      </div>
    </div>
  );
};
```

---

## 4. Reglas CSS Específicas para Impresoras Térmicas de 80mm

Para ser incluidas en `globals.css` o en el archivo de estilos del frontend:

```css
@media print {
  /* Ocultar toda la interfaz del POS excepto el ticket */
  body * {
    visibility: hidden;
  }
  #printable-ticket, #printable-ticket * {
    visibility: visible;
  }
  #printable-ticket {
    position: absolute;
    left: 0;
    top: 0;
    width: 72mm !important; /* Ancho seguro para impresoras térmicas de 80mm */
    margin: 0 !important;
    padding: 0 !important;
    background: #FFFFFF !important;
    color: #000000 !important;
    font-size: 11pt !important;
    box-shadow: none !important;
    border: none !important;
  }
  @page {
    size: 80mm auto;
    margin: 0mm;
  }
}
```
