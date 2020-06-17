CREATE SCHEMA IF NOT EXISTS raven 
  AUTHORIZATION raven_adm;

CREATE SCHEMA IF NOT EXISTS raven
  AUTHORIZATION raven_adm;

CREATE EXTENSION IF NOT EXISTS HSTORE ;

CREATE EXTENSION pgcrypto;

CREATE TABLESPACE TSDRAVEN01
  OWNER raven_adm
  LOCATION '/tablespace/data';

CREATE TABLESPACE TSIRAVEN01
  OWNER raven_adm
  LOCATION '/tablespace/index';


select pg_reload_conf();

CREATE TABLE IF NOT EXISTS raven.stock (
    id_stock BIGSERIAL NOT NULL,
    ticker VARCHAR NOT NULL,
    price_open DECIMAL(12,2) NOT NULL,
    price_close DECIMAL(12,2) NOT NULL,
    price_high DECIMAL(12,2) NOT NULL,
    price_low DECIMAL(12,2) NOT NULL,
    des_date VARCHAR NOT NULL,
    indicators JSONB,	
    dat_create TIMESTAMP NOT NULL,
    dat_update TIMESTAMP NULL,
    version INTEGER NOT NULL
) TABLESPACE TSDRAVEN01;

ALTER TABLE raven.stock ADD CONSTRAINT stock_pkey PRIMARY KEY (id_stock) USING INDEX TABLESPACE TSIRAVEN01;

CREATE INDEX stock_ticker_idx ON raven.stock USING btree (ticker) TABLESPACE TSIRAVEN01;

COMMENT ON TABLE raven.stock IS 'Dados da ação';


CREATE TABLE IF NOT EXISTS raven.stock_history (
    id_stock BIGSERIAL NOT NULL,
    ticker VARCHAR NOT NULL,
    price_open DECIMAL(12,2) NOT NULL,
    price_close DECIMAL(12,2) NOT NULL,
    price_high DECIMAL(12,2) NOT NULL,
    price_low DECIMAL(12,2) NOT NULL,
    des_date VARCHAR NOT NULL,
    indicators JSONB,	
    dat_create TIMESTAMP NOT NULL,
    dat_update TIMESTAMP NULL,
    version INTEGER NOT NULL
) TABLESPACE TSDRAVEN01;
