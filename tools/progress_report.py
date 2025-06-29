import os
from collections import Counter
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import yaml

from memory import load_memory, load_pressure, load_alignments

MEMORY_PATH = os.path.join('memory', 'ECHO_MEMORY.yaml')
PRESSURE_PATH = os.path.join('memory', 'MOTIF_PRESSURE.yaml')
ALIGN_PATH = os.path.join('memory', 'RECURSIVE_ALIGNMENTS.yaml')


def summarize_motifs(entries):
    tags = []
    for e in entries:
        if 'tags' in e:
            tags.extend(e['tags'])
        elif 'motif' in e:
            tags.append(e['motif'])
    return Counter(tags)


def generate_chart(df, path):
    if df.empty:
        return
    df.plot(kind='bar', x='motif', y='pressure', legend=False)
    plt.ylabel('Pressure')
    plt.tight_layout()
    plt.savefig(path)
    plt.close()


def build_report():
    memory_data = load_memory(MEMORY_PATH)
    pressure_data = load_pressure(PRESSURE_PATH)
    align_data = load_alignments(ALIGN_PATH)

    entries = memory_data.get('echo_memory', [])
    pressure = pressure_data.get('motif_pressure', {})
    counts = summarize_motifs(entries)

    df = pd.DataFrame(
        [
            {'motif': m, 'mentions': counts.get(m, 0), 'pressure': pressure.get(m, 0)}
            for m in set(list(counts.keys()) + list(pressure.keys()))
        ]
    )
    df.sort_values('pressure', ascending=False, inplace=True)

    low_engagement = df[df['pressure'] <= 1]['motif'].tolist()

    chart_path = os.path.join('journal', 'progress.png')
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    generate_chart(df.head(10), chart_path)

    report = {
        'generated': datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC'),
        'total_entries': len(entries),
        'top_motifs': df.head(5).to_dict(orient='records'),
        'low_engagement': low_engagement,
        'alignment_count': len(align_data.get('recursive_alignments', [])),
        'chart_path': chart_path,
    }
    return report


def main():
    report = build_report()
    print('📝 Progress Report')
    print('Generated:', report['generated'])
    print('Total memory entries:', report['total_entries'])
    print('Total alignments:', report['alignment_count'])
    print('\nTop motifs:')
    for m in report['top_motifs']:
        print(f"- {m['motif']} (pressure={m['pressure']}, mentions={m['mentions']})")
    if report['low_engagement']:
        print('\nLow engagement motifs:', ', '.join(report['low_engagement']))
    print('\nChart saved to', report['chart_path'])


if __name__ == '__main__':
    main()
