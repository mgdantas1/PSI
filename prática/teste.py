dicio = {
    1: {
        'titulo': 't1',
        'descricao': 't1',
        'status': 1,
        'status': '2025-06-12'
    },
    2: {
        'titulo': 't1',
        'descricao': 't1',
        'status': 1,
        'status': '2025-06-12'
    }
}

for valor in dicio.values():
    for v in valor.values():
        print(v)
