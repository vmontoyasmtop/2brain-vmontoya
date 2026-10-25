import React from 'react';

export interface CriolloIconProps extends React.SVGProps<SVGSVGElement> {
  size?: number | string;
  className?: string;
}

/**
 * 🍅 Icono Tomate Perita
 * Representa hortalizas, pesaje por gramaje en balanza criolla.
 */
export const IconTomate: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="21" rx="7" ry="2" fill="#1C2B3C" opacity="0.6" />
    <path
      d="M12 5.5C8 5.5 5 8.5 5 13C5 17.5 8 20.5 12 20.5C16 20.5 19 17.5 19 13C19 8.5 16 5.5 12 5.5Z"
      fill="#EF4444"
    />
    <path
      d="M8 9C7.2 10.5 7.2 13 8 15"
      stroke="#FCA5A5"
      strokeWidth="1.5"
      strokeLinecap="round"
    />
    <path d="M12 2.5V5.5" stroke="#10B981" strokeWidth="2" strokeLinecap="round" />
    <path
      d="M12 5.5L8.5 4.5M12 5.5L15.5 4.5M12 5.5L10 7M12 5.5L14 7"
      stroke="#4EDEA3"
      strokeWidth="1.8"
      strokeLinecap="round"
    />
  </svg>
);

/**
 * 🍌 Icono Plátano Maduro
 * Frutas y verduras con pesaje táctil directo.
 */
export const IconPlatano: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="21.5" rx="8" ry="1.5" fill="#1C2B3C" opacity="0.6" />
    <path
      d="M4 16C5.5 19 9.5 21 14.5 19.5C18.5 18 20.5 14 21 10C21.3 7 19.5 5 19 4.5C18.5 4 17 5 16.5 7C15.5 11 13 14.5 9 15.5C6.5 16 4.8 15.5 4 16Z"
      fill="#FFB95F"
      stroke="#EE9800"
      strokeWidth="1.2"
      strokeLinejoin="round"
    />
    <path
      d="M19 4.5L20.5 2.5C21 2 21.8 2.2 22 2.8C22.2 3.5 21.5 4.5 21 5L19 4.5Z"
      fill="#10B981"
    />
    <circle cx="4.2" cy="16" r="1" fill="#78350F" />
    <circle cx="10" cy="17" r="0.8" fill="#78350F" />
    <circle cx="13" cy="16.5" r="0.9" fill="#78350F" />
    <circle cx="16" cy="13.5" r="0.8" fill="#78350F" />
    <circle cx="18" cy="9.5" r="0.7" fill="#78350F" />
  </svg>
);

/**
 * 🥑 Icono Aguacate Criollo
 * Producto gourmet de mostrador vendido por peso o unidad.
 */
export const IconAguacate: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="21.5" rx="6.5" ry="1.5" fill="#1C2B3C" opacity="0.6" />
    <path
      d="M12 2C8.5 2 6 6 6 12C6 17 8.5 21 12 21C15.5 21 18 17 18 12C18 6 15.5 2 12 2Z"
      fill="#065F46"
      stroke="#10B981"
      strokeWidth="1.2"
    />
    <path
      d="M12 3.8C9.2 3.8 7.3 7 7.3 12C7.3 16.2 9.2 19.5 12 19.5C14.8 19.5 16.7 16.2 16.7 12C16.7 7 14.8 3.8 12 3.8Z"
      fill="#D9F99D"
    />
    <path
      d="M12 5.5C10 5.5 8.5 8 8.5 12.2C8.5 15.5 10 18.5 12 18.5C14 18.5 15.5 15.5 15.5 12.2C15.5 8 14 5.5 12 5.5Z"
      fill="#BEF264"
      opacity="0.5"
    />
    <ellipse
      cx="12"
      cy="14"
      rx="3.3"
      ry="3.8"
      fill="#92400E"
      stroke="#78350F"
      strokeWidth="1"
    />
    <ellipse cx="11.2" cy="12.8" rx="0.9" ry="1.2" fill="#FBBF24" opacity="0.6" />
  </svg>
);

/**
 * 🧀 Icono Queso Blanco Llanero
 * Charcutería por gramaje exacto con tara automática.
 */
export const IconQueso: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="21.5" rx="8.5" ry="1.8" fill="#1C2B3C" opacity="0.6" />
    <polygon
      points="4,11 12,6 20,10 12,14"
      fill="#FFFFFF"
      stroke="#94A3B8"
      strokeWidth="1.2"
      strokeLinejoin="round"
    />
    <polygon
      points="4,11 12,14 12,19.5 4,16.5"
      fill="#E2E8F0"
      stroke="#94A3B8"
      strokeWidth="1.2"
      strokeLinejoin="round"
    />
    <polygon
      points="12,14 20,10 20,15.5 12,19.5"
      fill="#CBD5E1"
      stroke="#94A3B8"
      strokeWidth="1.2"
      strokeLinejoin="round"
    />
    <circle cx="7.5" cy="13.8" r="0.9" fill="#94A3B8" />
    <circle cx="10" cy="16.5" r="0.7" fill="#94A3B8" />
    <circle cx="9" cy="10" r="0.8" fill="#CBD5E1" />
    <circle cx="14" cy="9.5" r="1.1" fill="#CBD5E1" />
    <circle cx="15.5" cy="14" r="0.8" fill="#94A3B8" />
    <circle cx="18" cy="12.5" r="0.7" fill="#94A3B8" />
    <circle cx="13.5" cy="17" r="0.9" fill="#64748B" />
  </svg>
);

/**
 * 🌽 Icono Harina P.A.N. / Paquete de Víveres
 * Producto básico empaquetado vendido por unidad con código de barras o táctil.
 */
export const IconHarina: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="21.5" rx="6.5" ry="1.5" fill="#1C2B3C" opacity="0.6" />
    <rect
      x="6"
      y="4"
      width="12"
      height="16.5"
      rx="2"
      fill="#FFB95F"
      stroke="#EE9800"
      strokeWidth="1.2"
    />
    <rect x="6" y="8" width="12" height="5.5" fill="#1D4ED8" />
    <ellipse cx="12" cy="10.7" rx="3.5" ry="2.2" fill="#FFFFFF" />
    <path
      d="M10 10.7H14"
      stroke="#1D4ED8"
      strokeWidth="1.4"
      strokeLinecap="round"
    />
    <path
      d="M6 5.5L12 3.5L18 5.5"
      stroke="#EE9800"
      strokeWidth="1.2"
      strokeLinecap="round"
    />
    <line x1="12" y1="3.5" x2="12" y2="5" stroke="#EE9800" strokeWidth="1.2" />
    <circle cx="12" cy="16.5" r="1.3" fill="#EE9800" />
    <path
      d="M10.2 17.5C11 16 13 16 13.8 17.5"
      stroke="#10B981"
      strokeWidth="1"
      strokeLinecap="round"
    />
  </svg>
);

/**
 * ⚖️ Icono Balanza Digital / Pesaje
 * Dispositivo de mostrador para lectura continua en vivo o manual.
 */
export const IconBalanza: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="21" rx="8" ry="1.5" fill="#1C2B3C" opacity="0.6" />
    <path
      d="M3 6.5H21L19.5 8.5H4.5L3 6.5Z"
      fill="#CBD5E1"
      stroke="#94A3B8"
      strokeWidth="1.2"
      strokeLinejoin="round"
    />
    <line x1="7" y1="8.5" x2="7" y2="10.5" stroke="#94A3B8" strokeWidth="1.5" />
    <line x1="17" y1="8.5" x2="17" y2="10.5" stroke="#94A3B8" strokeWidth="1.5" />
    <rect
      x="4"
      y="10.5"
      width="16"
      height="8.5"
      rx="2"
      fill="#122131"
      stroke="#1C2B3C"
      strokeWidth="1.2"
    />
    <rect
      x="6.5"
      y="12"
      width="11"
      height="4.5"
      rx="1"
      fill="#051424"
      stroke="#10B981"
      strokeWidth="0.8"
    />
    <path
      d="M8.5 13.5H9.5V15.5H8.5V13.5ZM11.5 13.5H12.5V15.5H11.5V13.5ZM14.5 13.5H15.5V15.5H14.5V13.5Z"
      fill="#4EDEA3"
    />
    <circle cx="10.5" cy="15.2" r="0.4" fill="#4EDEA3" />
    <rect x="5.5" y="19" width="3" height="1.5" rx="0.5" fill="#1C2B3C" />
    <rect x="15.5" y="19" width="3" height="1.5" rx="0.5" fill="#1C2B3C" />
  </svg>
);

/**
 * 💵 Icono Billete Dólar ($ Cash)
 * Cobro bimonetario en efectivo divisa con vuelto calculado.
 */
export const IconDolar: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="20.5" rx="9" ry="1.5" fill="#1C2B3C" opacity="0.6" />
    <rect
      x="2.5"
      y="6"
      width="19"
      height="11.5"
      rx="1.5"
      fill="#D1FAE5"
      stroke="#10B981"
      strokeWidth="1.2"
    />
    <rect
      x="4.5"
      y="7.5"
      width="15"
      height="8.5"
      rx="1"
      fill="none"
      stroke="#059669"
      strokeWidth="0.8"
      strokeDasharray="2 1"
    />
    <ellipse
      cx="12"
      cy="11.75"
      rx="3.8"
      ry="3.2"
      fill="#A7F3D0"
      stroke="#10B981"
      strokeWidth="0.8"
    />
    <path
      d="M12 9.5V14M13.2 10.3C13.2 9.8 12.6 9.5 12 9.5C11.3 9.5 10.8 9.9 10.8 10.5C10.8 11.4 13.2 11.2 13.2 12.5C13.2 13.2 12.6 13.7 11.8 13.7C11.1 13.7 10.6 13.3 10.6 12.8"
      stroke="#065F46"
      strokeWidth="1.3"
      strokeLinecap="round"
    />
    <circle cx="4.2" cy="8" r="0.8" fill="#10B981" />
    <circle cx="19.8" cy="8" r="0.8" fill="#10B981" />
    <circle cx="4.2" cy="15.5" r="0.8" fill="#10B981" />
    <circle cx="19.8" cy="15.5" r="0.8" fill="#10B981" />
  </svg>
);

/**
 * 📲 Icono Pago Móvil / QR Criollo
 * Método de pago interbancario instantáneo venezolano en bolívares.
 */
export const IconPagoMovil: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="22" rx="6" ry="1.2" fill="#1C2B3C" opacity="0.6" />
    <rect
      x="6"
      y="2.5"
      width="12"
      height="18.5"
      rx="2.5"
      fill="#122131"
      stroke="#1C2B3C"
      strokeWidth="1.2"
    />
    <rect x="7.5" y="5" width="9" height="12.5" rx="1" fill="#051424" />
    <line
      x1="10"
      y1="3.8"
      x2="14"
      y2="3.8"
      stroke="#94A3B8"
      strokeWidth="0.8"
      strokeLinecap="round"
    />
    <circle cx="12" cy="19.2" r="0.7" fill="#94A3B8" />
    <rect x="8.8" y="6.3" width="2.5" height="2.5" fill="#4EDEA3" />
    <rect x="12.7" y="6.3" width="2.5" height="2.5" fill="#4EDEA3" />
    <rect x="8.8" y="10.2" width="2.5" height="2.5" fill="#4EDEA3" />
    <rect x="12.7" y="10.2" width="1.1" height="1.1" fill="#FFB95F" />
    <rect x="14.1" y="11.6" width="1.1" height="1.1" fill="#FFB95F" />
    <path
      d="M10 15C11 14.3 13 14.3 14 15"
      stroke="#FFB95F"
      strokeWidth="1.2"
      strokeLinecap="round"
    />
    <path
      d="M8.5 16.5C10.5 15.5 13.5 15.5 15.5 16.5"
      stroke="#EE9800"
      strokeWidth="1.2"
      strokeLinecap="round"
    />
  </svg>
);

/**
 * 💳 Icono Punto de Venta / Tarjeta Débito
 * Terminal bancario físico con tarjeta chip insertada.
 */
export const IconTarjeta: React.FC<CriolloIconProps> = ({
  size = 24,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <ellipse cx="12" cy="22" rx="7.5" ry="1.2" fill="#1C2B3C" opacity="0.6" />
    <rect
      x="5.5"
      y="4"
      width="13"
      height="17"
      rx="2"
      fill="#122131"
      stroke="#1C2B3C"
      strokeWidth="1.2"
    />
    <rect
      x="7"
      y="5.8"
      width="10"
      height="5"
      rx="1"
      fill="#051424"
      stroke="#10B981"
      strokeWidth="0.8"
    />
    <path
      d="M10 8.3L11.5 9.8L14.5 6.8"
      stroke="#4EDEA3"
      strokeWidth="1.2"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <circle cx="8.5" cy="12.8" r="0.7" fill="#94A3B8" />
    <circle cx="12" cy="12.8" r="0.7" fill="#94A3B8" />
    <circle cx="15.5" cy="12.8" r="0.7" fill="#94A3B8" />
    <circle cx="8.5" cy="15" r="0.7" fill="#94A3B8" />
    <circle cx="12" cy="15" r="0.7" fill="#94A3B8" />
    <circle cx="15.5" cy="15" r="0.7" fill="#94A3B8" />
    <rect x="8" y="17" width="2" height="1" rx="0.5" fill="#EF4444" />
    <rect x="11" y="17" width="2" height="1" rx="0.5" fill="#FFB95F" />
    <rect x="14" y="17" width="2" height="1" rx="0.5" fill="#10B981" />
    <path
      d="M7.5 4V2C7.5 1.5 8 1 8.5 1H15.5C16 1 16.5 1.5 16.5 2V4"
      fill="#3B82F6"
      stroke="#1D4ED8"
      strokeWidth="1"
    />
    <rect x="10.5" y="1.8" width="3" height="1.8" rx="0.4" fill="#FFB95F" />
  </svg>
);

/**
 * 🎖️ Sello Oficial "TODO CUADRAÍTO"
 * Sello de garantía de cuadre perfecto, cero pérdidas y tranquilidad contable.
 */
export const SelloCuadraito: React.FC<CriolloIconProps> = ({
  size = 48,
  className = '',
  ...props
}) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 100 100"
    width={size}
    height={size}
    fill="none"
    className={`inline-block shrink-0 ${className}`}
    {...props}
  >
    <circle cx="50" cy="52" r="44" fill="#051424" opacity="0.5" />
    <circle
      cx="50"
      cy="50"
      r="44"
      fill="#122131"
      stroke="#10B981"
      strokeWidth="3"
      strokeDasharray="6 2"
    />
    <circle cx="50" cy="50" r="38" fill="#051424" stroke="#4EDEA3" strokeWidth="2" />
    <path id="curveTopComponent" d="M22 50 A28 28 0 0 1 78 50" fill="none" />
    <text
      fontFamily="'Inter', sans-serif"
      fontSize="7.5"
      fontWeight="900"
      fill="#FFB95F"
      letterSpacing="1.5"
    >
      <textPath href="#curveTopComponent" startOffset="50%" textAnchor="middle">
        TODO CUADRAÍTO
      </textPath>
    </text>
    <polygon
      points="50,68 51.5,72 55.5,72 52.3,74.5 53.5,78.5 50,76 46.5,78.5 47.7,74.5 44.5,72 48.5,72"
      fill="#FFB95F"
    />
    <circle cx="34" cy="74" r="1.5" fill="#4EDEA3" />
    <circle cx="66" cy="74" r="1.5" fill="#4EDEA3" />
    <path
      d="M36 50 L46 60 L66 38"
      stroke="#4EDEA3"
      strokeWidth="6"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
    <path
      d="M64 26 C40 22 28 35 28 50 C28 65 40 76 64 72"
      stroke="#10B981"
      strokeWidth="2"
      strokeLinecap="round"
      opacity="0.4"
    />
  </svg>
);

/**
 * 📦 Catálogo de Iconos Criollos para Acceso Dinámico
 */
export const CRIOLLO_ICONS = {
  tomate: IconTomate,
  platano: IconPlatano,
  aguacate: IconAguacate,
  queso: IconQueso,
  harina: IconHarina,
  balanza: IconBalanza,
  dolar: IconDolar,
  pagomovil: IconPagoMovil,
  tarjeta: IconTarjeta,
  sello: SelloCuadraito,
} as const;

export type CriolloIconName = keyof typeof CRIOLLO_ICONS;

export interface DynamicCriolloIconProps extends CriolloIconProps {
  name: CriolloIconName;
}

export const CriolloIcon: React.FC<DynamicCriolloIconProps> = ({
  name,
  ...props
}) => {
  const IconComponent = CRIOLLO_ICONS[name];
  if (!IconComponent) return null;
  return <IconComponent {...props} />;
};

export default CriolloIcon;
