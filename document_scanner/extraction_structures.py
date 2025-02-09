def extraction_schema(schema_name="yrityksen_taloustiedot"):
    schema_name = schema_name.lower().strip()
    schemas = {
        "yrityksen_taloustiedot": {
            "type": "object",
            "properties": {
                "yrityksen_nimi": {"type": "string", "description": "Yrityksen nimi"},
                "tilikauden_alku": {"type": "string", "description": "Tilikauden alku"},
                "tilikauden_loppu": {
                    "type": "string",
                    "description": "Tilikauden loppu",
                },
                "liikevaihto": {"type": "number", "description": "Liikevaihto"},
                "kayttokate": {"type": "number", "description": "Käyttökate"},
                "liikevoitto": {"type": "number", "description": "Liikevoitto"},
                "nettotulos": {"type": "number", "description": "Nettotulos"},
                "oma_paoma": {"type": "number", "description": "Oma pääoma"},
                "vieras_paoma": {"type": "number", "description": "Vieras pääoma"},
                "vaihtuvat_vastaavat": {
                    "type": "number",
                    "description": "Vaihtuvat vastaavat",
                },
                "pysyvat_vastaavat": {
                    "type": "number",
                    "description": "Pysyvät vastaavat",
                },
                "kassavarat": {"type": "number", "description": "Kassavarat"},
            },
            "required": [
                "tilikauden_alku",
                "tilikauden_loppu",
                "liikevaihto",
                "kayttokate",
                "liikevoitto",
                "nettotulos",
                "oma_paoma",
                "vieras_paoma",
                "vaihtuvat_vastaavat",
                "pysyvat_vastaavat",
                "kassavarat",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    }

    schema = schemas.get(schema_name)
    if schema is None:
        raise ValueError(f"No schema defined for '{schema_name}'")
    return schema
