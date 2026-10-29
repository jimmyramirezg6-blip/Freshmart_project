-- Tasa de conversión global de la campaña
SELECT
    COUNT(*) AS total_alcanzados,
    SUM(CASE WHEN compro THEN 1 ELSE 0) AS compraron, 
    ROUND(
        100.0 * SUM(CASE WHEN compro THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS tasa_conversion_pct
FROM campana_verano_clientes


-- Tasa de conversión por canal
SELECT 
    CASE 
        WHEN LOWER(canal_contacto) LIKE 'push%' THEN 'push'
        ELSE LOWER(canal_contacto)
    END AS canal, 
    COUNT(*) AS alcanzados, 
    SUM(CASE WHEN compro THEN 1 ELSE 0 END) AS compraron,
    ROUND(
        100.0 * SUM(CASE WHEN compro THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS tasa_conversion_pct
FROM campana
GROUP BY 
    CASE 
        WHEN LOWER(canla_contacto) LIKE 'push%' THEN 'push'
        ELSE LOWER(canal_contacto)
    END
ORDER BY tasa_conversion_pct DESC;