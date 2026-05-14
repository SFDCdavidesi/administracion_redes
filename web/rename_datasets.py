#!/usr/bin/env python3
"""
Script para renombrar archivos JSON en base a su contenido
y generar un index.json dinámico.
"""

import json
import os
from pathlib import Path
from collections import Counter
import re

DATASETS_DIR = Path(__file__).parent / "datasets"

def extract_topic_keywords(question_text: str, num_keywords: int = 3) -> list:
    """Extrae palabras clave del texto de una pregunta."""
    # Convertir a minúsculas y dividir
    words = re.findall(r'\b\w+\b', question_text.lower())
    
    # Palabras a ignorar (stopwords en español)
    stopwords = {
        'qué', 'cuál', 'cuáles', 'cómo', 'por', 'para', 'con', 'sin', 'de', 'del',
        'la', 'el', 'un', 'una', 'los', 'las', 'unos', 'unas', 'es', 'son', 'está',
        'están', 'fue', 'fueron', 'sea', 'sean', 'siendo', 'en', 'o', 'y', 'a',
        'ante', 'bajo', 'cabe', 'circa', 'contra', 'durante', 'desde', 'entre',
        'hacia', 'hasta', 'sobre', 'tras', 'versus', 'vía', 'q', 'se', 'ha', 'han'
    }
    
    filtered_words = [w for w in words if w not in stopwords and len(w) > 2]
    return filtered_words[:num_keywords]

def analyze_json_file(filepath: Path) -> dict:
    """Analiza un archivo JSON y extrae metadatos."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Determinar estructura
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict) and 'items' in data:
            items = data.get('items', [])
        else:
            items = []
        
        # Extraer metadatos
        num_questions = len(items)
        
        # Extraer palabras clave de todos los temas
        all_keywords = []
        for item in items[:10]:  # Usar primeras 10 preguntas
            if isinstance(item, dict):
                question = item.get('question', '') or item.get('qtext', '') or item.get('text', '')
                keywords = extract_topic_keywords(str(question))
                all_keywords.extend(keywords)
        
        # Obtener palabras más frecuentes
        if all_keywords:
            keyword_counter = Counter(all_keywords)
            top_keywords = [word for word, _ in keyword_counter.most_common(3)]
        else:
            top_keywords = []
        
        # Intentar obtener topic del metadato sourcePdf
        topic_from_pdf = ""
        if isinstance(data, dict) and 'sourcePdf' in data:
            pdf_path = data['sourcePdf']
            # Extraer nombre del PDF sin extensión
            pdf_name = Path(pdf_path).stem
            topic_from_pdf = pdf_name
        
        return {
            'num_questions': num_questions,
            'keywords': top_keywords,
            'pdf_topic': topic_from_pdf,
            'valid': num_questions > 0
        }
    except Exception as e:
        print(f"Error analizando {filepath}: {e}")
        return {'valid': False}

def generate_filename(analysis: dict, original_filename: str) -> str:
    """Genera un nombre significativo basado en el análisis."""
    # Prioridad: tema del PDF > palabras clave > nombre original
    
    if analysis.get('pdf_topic'):
        return f"{analysis['pdf_topic']}.json"
    
    if analysis.get('keywords'):
        keywords_str = '_'.join(analysis['keywords'][:2]).title()
        return f"{keywords_str}.json"
    
    return original_filename

def rename_datasets():
    """Renombra archivos y genera index.json."""
    if not DATASETS_DIR.exists():
        print(f"Directorio {DATASETS_DIR} no existe")
        return
    
    json_files = list(DATASETS_DIR.glob('*.json'))
    json_files = [f for f in json_files if f.name != 'index.json']
    
    if not json_files:
        print("No hay archivos JSON para procesar")
        return
    
    print(f"Procesando {len(json_files)} archivos JSON...")
    
    mapping = {}  # old_name -> new_name
    
    for json_file in json_files:
        print(f"\nAnalizando: {json_file.name}")
        analysis = analyze_json_file(json_file)
        
        if not analysis['valid']:
            print(f"  ❌ Archivo inválido o vacío")
            continue
        
        new_filename = generate_filename(analysis, json_file.name)
        
        # Evitar sobrescrituras: si el nuevo nombre ya existe, añadir sufijo
        new_path = DATASETS_DIR / new_filename
        counter = 1
        while new_path.exists() and new_path.name != json_file.name:
            base, ext = new_filename.rsplit('.', 1)
            new_filename = f"{base}_{counter}.{ext}"
            new_path = DATASETS_DIR / new_filename
            counter += 1
        
        # Renombrar solo si es diferente
        if json_file.name != new_filename:
            json_file.rename(new_path)
            mapping[json_file.name] = new_filename
            print(f"  ✅ Renombrado a: {new_filename}")
            print(f"     Preguntas: {analysis['num_questions']}")
            print(f"     Temas: {', '.join(analysis['keywords'])}")
        else:
            mapping[json_file.name] = new_filename
            print(f"  ℹ️  Nombre actual: {json_file.name}")
            print(f"     Preguntas: {analysis['num_questions']}")
    
    # Generar index.json dinámico
    print("\n" + "="*50)
    print("Generando index.json dinámico...")
    
    current_files = sorted([
        f.name for f in DATASETS_DIR.glob('*.json')
        if f.name != 'index.json'
    ])
    
    index_content = {
        'files': current_files,
        'generatedAt': str(Path(__file__).stat().st_mtime),
        'description': 'Listado dinámico de cuestionarios de redes'
    }
    
    index_path = DATASETS_DIR / 'index.json'
    with open(index_path, 'w', encoding='utf-8') as f:
        json.dump(index_content, f, indent=2, ensure_ascii=False)
    
    print(f"✅ index.json actualizado con {len(current_files)} archivos")
    
    # Mostrar resumen
    if mapping:
        print("\nResumen de cambios:")
        for old, new in mapping.items():
            if old != new:
                print(f"  {old} → {new}")
    else:
        print("\nNo hubo cambios de nombre")

if __name__ == '__main__':
    rename_datasets()
