#!/usr/bin/env python3
"""Apply summaries to pending JSON files for 2026-05-27 run."""
import json
import os
from datetime import datetime, timezone

PENDING_DIR = os.path.join(os.path.dirname(__file__), 'pending_summaries')

SUMMARIES = {
    'UCB1MBbdhhBGxxyX9I_3eLUg__LqwER8IMJgA.json': {
        'summary_3lines': '女神編成（陽シナジー）でセフェルマルカーを12ターン完封。\n10ターン目から1000%超のステバフが自動発動し毒も防ぐ。\n女神は無人島アタッカーとしても最適と紹介。',
        'key_topics': ['女神編成', 'セフェルマルカー', '陽シナジー', '無人島', 'ダメブロ蓄積'],
        'positive_points': [
            '女神は無人島アタッカーとしても最適で爆発力より安定型',
            '10ターン目から1000%超のステバフが自動発動して安定',
            'メガミ＋ミドのバランスで12ターン安定クリア',
            '詩人ターミンの固定値防御75%で鉄壁火力に',
            '同じ行動しかしない敵なので何度でも勝てるテンプレ編成'
        ],
        'negative_points': [
            '爆発力はなく現実的かつ確実な強さに留まる'
        ],
    },
    'UCIzvPxpqEhy_HxidniB_3ow__39Lje8-Hsmo.json': {
        'summary_3lines': '5月31日12時よりクロスディメンションW79が開催。\n報酬はガンダムPixie&イフリートの2体1組コンビユニット。\nSR枠グラハムは物理射撃支援に最大射程アップが付く。',
        'key_topics': ['Gジェネエターナル', 'クロスディメンションW79', 'コンビユニット', 'グラハム', 'マップ兵器'],
        'positive_points': [
            'コンビユニットは攻撃型でマップ兵器持ち',
            'グラハムは物理射撃支援で射程6〜7まで届く可能性'
        ],
        'negative_points': [
            'SSRの報酬ユニットがコンビ1組のみで寂しい',
            'GJエタで早くもコンビユニット実装は意外'
        ],
    },
    'UCIzvPxpqEhy_HxidniB_3ow__hgdk2ZVYeao.json': {
        'summary_3lines': '5月31日からクロスディメンションW79開催を解説。\n報酬PixieEイフリートは2体1組のコンビユニットで攻撃型。\nガチャの新限定枠の可能性に触れ29日30日の発表に期待。',
        'key_topics': ['Gジェネエターナル', 'クロスディメンションW79', 'コンビユニット', 'グラハム支援', 'ガチャ予想'],
        'positive_points': [
            'コンビユニットは攻撃型でマップ兵器持ち',
            'グラハムを支援に乗せれば物理射撃の射程アップが優秀'
        ],
        'negative_points': [
            'SSR報酬がコンビユニット1組のみで寂しい構成',
            'PixieやイフリートをすでにメダルにしてしまったユーザーはイベントBで稼ぎづらい'
        ],
    },
    'UCSQQQENHsSigOcawOR2Pl4A__AMfRploz7fo.json': {
        'summary_3lines': 'スマグロ生配信で雑談しつつ女神と聖王ガチャを単発で引く。\n防具強化や30億ダメミッション、アントニウスの井戸を周回。\n5/27のドラクエ発表、5/29の公式生放送、5/31の聖王関連にも言及。',
        'key_topics': ['スマグロ生配信', '女神/聖王ガチャ', '防具強化周回', 'アントニウスの井戸', '30億ダメージミッション'],
        'positive_points': [
            '単発ガチャで女神が引けて満足、女神編成は強い',
            'フィールド効果で1465億ダメージまで一気に伸びた',
            '女神のハニーアタックとダメブロ蓄積の組み合わせが優秀',
            '聖王は唯一無二系で将来的に取っておくと良い',
            '低課金で楽しめるのがロマサガRSの良い点'
        ],
        'negative_points': [
            'アントニウスの井戸3段が硬く2段で妥協しがち',
            '防具最大強化に必要な素材が周回1万2000個と過大',
            'パチンコで桃鉄スロットを触り2万円負け',
            '聖王の技マシンが術なので次の聖王に継承できなさそう',
            '63連チケットなど告知不足で取り逃しそうになる'
        ],
    },
    'UCdH4Ijk0D4FFJFRYrUFNzDQ__Wasw68Zer8A.json': {
        'summary_3lines': '第121回アントニウスの井戸を50位以内の編成と立ち回りで攻略。\nマリス・ターミン・はまるか・AJ・サラビスイシスでベスト編成を紹介。\nメルティハートハットでアントニウスの一撃を防ぎ24手で38位達成。',
        'key_topics': ['アントニウスの井戸121回', 'メルティハートハット', '50位以内攻略', 'クラウドシフト人系', '魂のアビリティ'],
        'positive_points': [
            'メルティハートハットが防具で被弾を防ぐ大活躍アイテム',
            '23日の考察動画と同じ編成で1番の順位を更新',
            'マリス＋ターミンの編成は50〜100位を安定して狙える',
            'クリーミーリボンドレスの装着でさらに安定'
        ],
        'negative_points': [
            '上位プレイヤーの編成はガラっと違うらしく未把握',
            '今回の編成は作者のベストではない',
            'カウンターを誘発しないようターミンの被弾位置に要注意',
            'メルティハートハットは持っている人がかなり少ない'
        ],
    },
}


def main():
    now_iso = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    for filename, summary in SUMMARIES.items():
        path = os.path.join(PENDING_DIR, filename)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['summary_3lines'] = summary['summary_3lines']
        data['key_topics'] = summary['key_topics']
        data['positive_points'] = summary['positive_points']
        data['negative_points'] = summary['negative_points']
        data['summarized_at'] = now_iso
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'updated: {filename}')


if __name__ == '__main__':
    main()
