-- segmentación_camapaña.sql

-- Segmentación de clientes de la campaña de verano

-- Paso 1: Contar pedidos recientes por cliente
WITH pedidos_recientes AS (
    SELECT 
        cliente_id, 
        COUNT(*) AS pedidos_3m
    FROM pedidos
    WHERE fecha_pedido >= '2024-06-15'
        AND estado NOT IN ('cancelado ')
    GROUP BY cliente_id
), 

-- Nota: Una fila por cliente: ~300 cleintes salen dos veces en la lista 
-- de la campaña (la recibieron por varios canales). Sin el DISTINCT, 
-- cada uno se cuenta dos veces y saslen 15.247 filas para 14956 clientes.

campana AS (
    SELECT DISTINCT cliented_id FROM campana_verano_clientes
), 

-- Paso 2: Cruzar con los clientes de la campaña y la tabla muestra

segmentacion AS (
    SELECT
        c.cliente_id, 
        m.nombre,
        m.email,
        m.fecha_registro
        COALESCE(p.pedidos_3m, 0) AS pedidos_ultimos_3m, 
        CASE 
            WHEN COALESCE(p.pedidos_3m, 0) > 6 THEN 'premium'
            WHEN COALESCE(p.pedido_3m, 0) >= 2 THEN 'regular'
        END AS segmento
    FROM campana c
    LEFT JOIN clientes m ON c.cliente_id = m.cliente_id
    LEFT JOIN pedidos_recientes c.cliente_id = p.cliente_id
)

SELECT * FROM segmentacion 
ORDER BY pedidos_ultimos_3m