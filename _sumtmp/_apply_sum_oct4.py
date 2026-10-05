# -*- coding: utf-8 -*-
import json
from datetime import datetime, timezone
D='data/pending_summaries/'
now=datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
fn="UCttGAXHA-hoLEVqsXoMVqXQ__5S5igBvzSwQ.json"
fields={"summary_3lines":"Romancing祭カタリナ編の3スタイルを考察。\nカタリナ/マリー/ファティーマの性能を解説＆ランク付け。\n総合評価はカタリナB・マリーB・ファティーマA-。","key_topics":["カタリナ編考察","カタリナ性能","マリー性能","ファティーマ性能","スタイルランク付け"],"positive_points":["カタリナは残例アタッカーとして倍率・ヒット数・事故が優秀","ファティーマはBP関連が優秀でレイド向きA-評価","マリーは熱20ヒットで8月幻闘場ボルカノ&ウンディネ特攻"],"negative_points":["カタリナの味方火ダメ軽減50%は心もとない","マリーは先制できないと火力もサポートも低下する","ファティーマはアタッカーは17ヒット止まりで力不足"]}
p=D+fn
with open(p,encoding='utf-8') as fp: d=json.load(fp)
for k in ('summary_3lines','key_topics','positive_points','negative_points'):
    d[k]=fields[k]
d['summarized_at']=now
with open(p,'w',encoding='utf-8') as fp: json.dump(d,fp,ensure_ascii=False,indent=2)
print('applied 14th:', fn, 'at', now)
