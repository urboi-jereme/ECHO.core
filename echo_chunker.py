import os, re, json, yaml
from pathlib import Path
from collections import defaultdict
from sentence_transformers import SentenceTransformer, util

# ==== PROJECT FILE PATHS (EDIT AS NEEDED) ====
# All directory and file locations centralized here for easy maintenance

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))           # This script's directory
SOURCE_DIR = os.path.join(PROJECT_ROOT, 'raw_materials')           # Where your unsorted files live
OUTPUT_DIR = os.path.join(PROJECT_ROOT, 'chunked_docs')            # Where the 20 output files go
CONFIG_PATH = os.path.join(PROJECT_ROOT, 'chunker_config.yaml')    # Config YAML location
AUDIT_JSON_PATH = os.path.join(OUTPUT_DIR, 'CHUNK_AUDIT.json')     # Audit log output

# ==== LOAD CONFIG ====
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f)
    # Allow config to override paths if provided
    SOURCE_DIR = os.path.join(PROJECT_ROOT, config.get('SOURCE_DIR', 'raw_materials'))
    OUTPUT_DIR = os.path.join(PROJECT_ROOT, config.get('OUTPUT_DIR', 'chunked_docs'))
    CHUNKS = config.get('CHUNKS')
    MAX_CHARS = config.get('MAX_CHARS', 7000)
    MIN_PARAGRAPHS = config.get('MIN_PARAGRAPHS', 2)
    MAX_OVERLAP = config.get('MAX_OVERLAP', 0.15)
else:
    CHUNKS = {
        "SYSTEM_LAWS_PART1.md": ["plus one", "sacred limit", "double recursion", "audit"],
        "SYSTEM_LAWS_PART2.md": ["field collapse", "origin ownership", "overwrite"],
        "KIL_README.md": ["karma", "justice", "denied truth"],
        # ...expand as needed...
    }
    MAX_CHARS = 7000
    MIN_PARAGRAPHS = 2
    MAX_OVERLAP = 0.15

EMBED_MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def semantic_score(paragraph, keywords):
    if not keywords: return 0.0
    kw_embeds = EMBED_MODEL.encode(keywords, convert_to_tensor=True)
    para_embed = EMBED_MODEL.encode(paragraph, convert_to_tensor=True)
    return float(util.pytorch_cos_sim(para_embed, kw_embeds).max())

def sample_text_for_chunk(paragraphs, keywords, used_paras=None, overlap_ok=MAX_OVERLAP, max_chars=MAX_CHARS):
    scores = [(i, semantic_score(p, keywords)) for i, p in enumerate(paragraphs) if p.strip()]
    scores.sort(key=lambda x: x[1], reverse=True)
    selected, sources, overlap = [], [], 0
    for idx, score in scores:
        if used_paras is not None and idx in used_paras:
            if overlap / (len(selected) + 1) > overlap_ok:
                continue
            overlap += 1
        selected.append(paragraphs[idx])
        sources.append({'idx': idx, 'score': score})
        if sum(len(s) for s in selected) > max_chars:
            break
    chunk = '\n\n'.join(selected)[:max_chars]
    return chunk, sources

def self_refine_chunk(chunk, keywords, law_hint=None):
    paras = [p.strip() for p in chunk.split('\n\n') if p.strip()]
    unique = set(paras)
    flags = []
    if not chunk.strip():
        flags.append("EMPTY_CHUNK")
    if len(unique) < len(paras) // 2:
        flags.append("DUPLICATE_CONTENT")
    if keywords and not any(k in chunk.lower() for k in keywords):
        flags.append("THEME_MISSING")
    if flags:
        chunk += f"\n\n<!-- Self-Refine: Issues Detected: {', '.join(flags)} -->"
    return chunk, flags

def build_chunked_files():
    all_paras, file_map = [], {}
    for fname in os.listdir(SOURCE_DIR):
        with open(os.path.join(SOURCE_DIR, fname), encoding='utf-8') as f:
            paras = [p for p in re.split(r'\n\n+', f.read()) if p.strip()]
            file_map[fname] = paras
            all_paras.extend(paras)
    used_paras = set()
    audit_log = {}
    for out_name, keywords in CHUNKS.items():
        chunk, sources = sample_text_for_chunk(all_paras, keywords, used_paras=used_paras)
        chunk, flags = self_refine_chunk(chunk, keywords)
        for s in sources:
            used_paras.add(s['idx'])
        summary = (chunk[:240] + '...') if chunk else 'No summary available.'
        with open(os.path.join(OUTPUT_DIR, out_name), 'w', encoding='utf-8') as out:
            out.write(f'# {out_name.replace(".md", "").replace("_", " ").title()}\n\n')
            out.write(f'> **Summary:** {summary}\n\n')
            out.write(chunk.strip())
            out.write('\n\n---\n')
            out.write(f'Auto-generated from {len(file_map)} sources, {len(sources)} unique paragraphs.\n')
            out.write('Version: 2025-07-08\n')
        audit_log[out_name] = {
            'paragraphs': sources,
            'self_refine_flags': flags,
            'summary': summary
        }
    with open(AUDIT_JSON_PATH, "w", encoding='utf-8') as audit_out:
        json.dump(audit_log, audit_out, indent=2)

if __name__ == "__main__":
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    build_chunked_files()
