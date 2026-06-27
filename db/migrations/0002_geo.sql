-- PR2: normalización geográfica.
-- Agrega la zona canónica (señal decisiva de match para need/infra/service) y
-- lat/lon de enriquecimiento (links de mapa, desempate por distancia).

ALTER TABLE afirmacion
    ADD COLUMN IF NOT EXISTS geo_codigo    TEXT,             -- zona canónica (gazetteer)
    ADD COLUMN IF NOT EXISTS geo_zona      TEXT,
    ADD COLUMN IF NOT EXISTS geo_estado    TEXT,
    ADD COLUMN IF NOT EXISTS geo_municipio TEXT,
    ADD COLUMN IF NOT EXISTS lat           DOUBLE PRECISION, -- enriquecimiento, NO es la llave de match
    ADD COLUMN IF NOT EXISTS lon           DOUBLE PRECISION;

CREATE INDEX IF NOT EXISTS idx_afirmacion_geo_codigo ON afirmacion (geo_codigo);
