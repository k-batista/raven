#!/usr/bin/env python

import json
import uuid

from argparse import ArgumentParser
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer

data = {
    "IDT_MESSAGE": 0,
    "COD_SAFEPAY_USER":123972722,
    "COD_CUSTOMER": 'CUSTOMER:D50D19764D644E8DB9D018940B1C88CD',
    "DES_YEAR_MONTH": '2020-12',
    "DES_CONFERENCE": "NEW",
    "NUM_MAX_INSTALLMENTS":40,
    "NUM_MIN_RATE": 1,
    "DES_WALLET": "Varejo",
    "VLR_TPV_M1": 1000.01,
    "VLR_TPV_M2": 1000,
    "VLR_TPV_M3": 1000.02,
    "VLR_TPV_M4": 1000,
    "VLR_TPV_M5": 1000,
    "VLR_TPV_M6": 1000,
    "VLR_TPV_M7": 1000,
    "VLR_TPV_M8": 1000,
    "VLR_TPV_M9": 1000,
    "VLR_TPV_M10": 1000,
    "VLR_TPV_M11": 1000,
    "VLR_TPV_M12": 1000,
    "VLR_TPV_PROJ_0": 500.1,
    "VLR_TPV_PROJ_1": 500.1,
    "VLR_TPV_PROJ_2": 500.1,
    "VLR_TPV_PROJ_3": 500.1,
    "VLR_TPV_PROJ_4": 500.1,
    "VLR_TPV_PROJ_5": 500.1,
    "NUM_SCORE": 0,
    "DES_PUBLIC": 'F',
    "NAM_PROFILE": 'A',
    "VLR_LIMIT": 2000.90,
    "DAT_CREATION": '2020-12-23T10:10:10.111Z',
    "DAT_EXPIRATION": '2020-12-23T10:10:10.111Z',
}


schema_avro = """{
  "type": "record",
  "name": "LoanLimitTest",
  "namespace": "br.com.uol..loan.avro",
  "fields": [
    {
      "name": "IDT_MESSAGE",
      "type": "long",
      "doc": "[PK] Identificador da mensagem no tópico."
    },
    {
      "name": "COD_SAFEPAY_USER",
      "type": "long",
      "doc": "[NSA] Identificador do cliente no "
    },
    {
      "name": "COD_CUSTOMER",
      "type": {
        "type": "string",
        "avro.java.string": "String"
      },
      "doc": "[NSA] Identificador do cliente na plataforma de cadastro (Customer)"
    },
    {
      "name": "DES_YEAR_MONTH",
      "type": {
        "type": "string",
        "avro.java.string": "String"
      },
      "doc": "[NSA] Data com mês e ano da oferta (ex. 2020-01)"
    },
    {
      "name": "DES_CONFERENCE",
      "type": {
        "type": "string",
        "avro.java.string": "String"
      },
      "doc": "[NSA] Novos, manutenção ou retirada de ofertas (ex. NEW, MAINTENANCE ou REMOVE)"
    },
    {
      "name": "NUM_MAX_INSTALLMENTS",
      "type": "int",
      "doc": "[NSA] Número máximo de parcelas"
    },
    {
      "name": "NUM_MIN_RATE",
      "type": "double",
      "doc": "[NSA] Taxa mínima de juros"
    },
    {
      "name": "DES_WALLET",
      "type": {
        "type": "string",
        "avro.java.string": "String"
      },
      "doc": "[NSA] Tipo de cliente (ex. Longtail, GV, Varejo)"
    },
    {
      "name": "VLR_TPV_M1",
      "type": "double",
      "doc": "[STF] Valor do TPV de um mês atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M2",
      "type": "double",
      "doc": "[STF] Valor do TPV de dois meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M3",
      "type": "double",
      "doc": "[STF] Valor do TPV de três meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M4",
      "type": "double",
      "doc": "[STF] Valor do TPV de quatro meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M5",
      "type": "double",
      "doc": "[STF] Valor do TPV de cinco meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M6",
      "type": "double",
      "doc": "[STF] Valor do TPV de seis meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M7",
      "type": "double",
      "doc": "[STF] Valor do TPV de sete meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M8",
      "type": "double",
      "doc": "[STF] Valor do TPV de oito meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M9",
      "type": "double",
      "doc": "[STF] Valor do TPV de nove meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M10",
      "type": "double",
      "doc": "[STF] Valor do TPV de dez meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M11",
      "type": "double",
      "doc": "[STF] Valor do TPV de onze meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_M12",
      "type": "double",
      "doc": "[STF] Valor do TPV de doze meses atrás",
      "default": 0
    },
    {
      "name": "VLR_TPV_PROJ_0",
      "type": "double",
      "doc": "[NSA] Valor do TPV projetado 0",
      "default": 0
    },
    {
      "name": "VLR_TPV_PROJ_1",
      "type": "double",
      "doc": "[NSA] Valor do TPV projetado 1",
      "default": 0
    },
    {
      "name": "VLR_TPV_PROJ_2",
      "type": "double",
      "doc": "[NSA] Valor do TPV projetado 2",
      "default": 0
    },
    {
      "name": "VLR_TPV_PROJ_3",
      "type": "double",
      "doc": "[NSA] Valor do TPV projetado 3",
      "default": 0
    },
    {
      "name": "VLR_TPV_PROJ_4",
      "type": "double",
      "doc": "[NSA] Valor do TPV projetado 4",
      "default": 0
    },
    {
      "name": "VLR_TPV_PROJ_5",
      "type": "double",
      "doc": "[NSA] Valor do TPV projetado 5",
      "default": 0
    },
    {
      "name": "NUM_SCORE",
      "type": "long",
      "doc": "[STF] Score de crédito"
    },
    {
      "name": "DES_PUBLIC",
      "type": {
        "type": "string",
        "avro.java.string": "String"
      },
      "doc": "[NSA] Pessoa Fisica ou Pessoa Juridica"
    },
    {
      "name": "NAM_PROFILE",
      "type": {
        "type": "string",
        "avro.java.string": "String"
      },
      "doc": "[NSA] Perfil de crédito (ex. A, B)"
    },
    {
      "name": "VLR_LIMIT",
      "type": "double",
      "doc": "[STO] Limite de crédito calculado",
      "default": 0
    },
    {
      "name": "DAT_CREATION",
      "type": {
        "type": "string",
        "avro.java.string": "String"
      },
      "doc": "[NSA] Data da oferta (Data string em formato ISO-8601)"
    },
    {
      "name": "DAT_EXPIRATION",
      "type": {
        "type": "string",
        "avro.java.string": "String"
      },
      "doc": "[NSA] Data de expiração da oferta (Data string em formato ISO-8601)"
    }
  ]
}
"""

def load_avro_schema_from_file():
    key_schema_string = """
    {"type": "string"}
    """

    key_schema = avro.loads(key_schema_string)
    value_schema = avro.loads(schema_avro)

    return key_schema, value_schema

def send_record():
    key_schema, value_schema = load_avro_schema_from_file()

    producer_config = {
        "bootstrap.servers": 'kafka.qa-aws.intranet..uol:9092',
        "schema.registry.url": 'http://schema-registry.qa-aws.intranet..uol:8081'
    }

    producer = AvroProducer(producer_config, default_key_schema=key_schema, default_value_schema=value_schema)

    key = str(uuid.uuid4())
    # value = json.loads(data)

    try:
        producer.produce(topic='fct.dsr.financialservices.loan.Limites', key=key, value=data)
    except Exception as e:
        print(f"Exception while producing record value - {data}: {e}")
    else:
        print(f"Successfully producing record value")

    producer.flush()


if __name__ == "__main__":
    send_record()