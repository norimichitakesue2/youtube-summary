import json, datetime
D='data/pending_summaries/'
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
fn="UCB1MBbdhhBGxxyX9I_3eLUg__Krxz6Ms0GZQ.json"
s={
 "summary_3lines":"最新の陰陽属性Tierと分布図でガチャ厳選を解説。\n上位は陰の万能スタイル、ビンセント裁判ターミンが最強格。\n属性を固める有用性は低下、手持ち少ないほど非推奨。",
 "key_topics":["陰陽属性Tier","属性分布図","ガチャ厳選","陰属性最強","上位層の指標"],
 "positive_points":["陰属性はウィーク無視でも強いスタイルが揃い最強格","ビンセントは弱点無しでも最大火力を出せる最上位アタッカー","ターミンは攻守デバフとBP回避を備え万能で入れ得","バルテルミーは全体連打可能で汎用性から浮上の可能性","女神はダメブロ蓄積と全体ODで無人島問わず活躍"],
 "negative_points":["属性を固める有用性は低く手持ち少ないほど非推奨","暦みは1ターンしか強くほぼ規制前提の割り切り性能","メイレンやアーニャは個人火力が低くバトル参加条件が厳しい","上位層を超えないスタイルはノールックでスルー可"]
}
d=json.load(open(D+fn))
d.update(s); d["summarized_at"]=now
json.dump(d,open(D+fn,'w'),ensure_ascii=False,indent=2)
print("updated",fn,now)
