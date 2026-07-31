# Contributing

Keep the schema, checker, examples, and field documentation consistent. Explain what decision a new field supports, and add a synthetic example and checker test.

```bash
python3 tools/check-record.py examples/*.json
python3 -m unittest discover -s tests -v
```

Do not add private evidence, customer names, internal links, credentials, or real incident data to examples.
