/**
 * Vercel Serverless Function para listar archivos JSON dinámicamente
 * 
 * Ubicación: /api/datasets.js
 * Acceso: GET /api/datasets
 * 
 * Lee el directorio web/datasets/ en tiempo real sin necesidad de index.json
 */

import { readdir } from 'fs/promises';
import { resolve } from 'path';

export default async function handler(req, res) {
  // Solo permitir GET
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Ruta del directorio datasets relativa a la raíz del proyecto
    const datasetsPath = resolve(process.cwd(), 'web', 'datasets');
    
    // Leer archivos del directorio
    const files = await readdir(datasetsPath);
    
    // Filtrar solo archivos .json (excluyendo index.json)
    const jsonFiles = files
      .filter(file => file.endsWith('.json') && file !== 'index.json')
      .sort();
    
    // Responder con CORS headers
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Content-Type', 'application/json');
    
    return res.status(200).json({
      files: jsonFiles,
      count: jsonFiles.length,
      generatedAt: new Date().toISOString()
    });
    
  } catch (error) {
    console.error('Error reading datasets:', error);
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Content-Type', 'application/json');
    
    return res.status(500).json({
      error: 'Failed to read datasets',
      message: error.message
    });
  }
}
