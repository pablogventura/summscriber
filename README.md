# Transcriber

Transcribe audio con [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (Whisper), con opciones de resumen (pysummarization, sumy, OpenAI) y respuesta corta con API OpenAI.

**Repositorio:** [github.com/pablogventura/transcriber](https://github.com/pablogventura/transcriber)

## Instalación

### Con pipx (recomendado: entorno aislado, comando global)

```bash
pipx install git+https://github.com/pablogventura/transcriber.git
```

Para actualizar:

```bash
pipx upgrade transcriber
```

### Con pip (desde el directorio del proyecto)

```bash
pip install .
```

O en modo editable (desarrollo):

```bash
pip install -e .
```

O desde el repositorio:

```bash
pip install git+https://github.com/pablogventura/transcriber.git
```

## Uso

Tras instalar, el comando `transcriber` queda disponible:

```bash
transcriber ARCHIVO [opciones]
```

Ejemplos:

```bash
transcriber grabacion.mp3
transcriber entrevista.ogg --resumen
transcriber audio.wav --resumen --respuesta --json
```

### Opciones principales

- **ARCHIVO**: archivo de audio a transcribir (obligatorio).
- `--resumen`: resumen (OpenAI si hay token; si no, el más corto entre pysummarization y sumy).
- `--resumen-pysummarization` / `--resumen-sumy` / `--resumen-openai`: resumen con un motor concreto.
- `--resumen-oraciones N`: número de oraciones del resumen (por defecto 3).
- `--respuesta`: genera una respuesta corta al mensaje con OpenAI.
- `--json`: salida en JSON.

Para resumen y respuesta con OpenAI se usa `config.ini` (sección `[openai]`) o las variables de entorno `OPENAI_API_KEY` y opcionalmente `OPENAI_BASE_URL`. Ver `config.ini.example`.

## Desarrollo

Sin instalar, desde la raíz del repo:

```bash
python -m transcriber ARCHIVO [opciones]
```
