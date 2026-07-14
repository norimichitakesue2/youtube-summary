import json, datetime
D='data/pending_summaries/'
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
S={
"UCBC_Fpd3wW-2kjYXVbQJ2hQ__hrj0l69bMMU.json":{
 "summary_3lines":"性能度外視、投稿者が惚れ込んだ女性キャラTOP5。\n5位エレノア4位アールブ3位アーニャ2位オルレット。\n1位は最新イリス、絵欲しさに天井まで確保。",
 "key_topics":["女性キャラTOP5","性能度外視","イリス1位","キャラ絵の魅力","リクエスト企画"],
 "positive_points":["イリスは絵が欲しくて天井まで確保した最推し","オルレットは卓越した腹筋と足入れが魅力","アールブは上下半身のギャップと見た目が良い","エレノアはふくらはぎと膝裏のバランスが良い","アーニャは旅立ちの幕開けが素晴らしい"],
 "negative_points":[]},
"UCVWjF9UkqPAgr4myD6L91QA__Sc35oYfX6xQ.json":{
 "summary_3lines":"FFRKコラボの皇帝Romancing難度に挑戦するshorts。\n敵が体力全回復やエリクサーで長期戦化。\n押し切れず最後はやられて終了。",
 "key_topics":["FFRKコラボ","皇帝Romancing","高難度攻略","shorts"],
 "positive_points":[],
 "negative_points":["敵が体力を全回復してきて面倒","エリクサー使用で長期戦がだるい","このターンで倒せず押し切れなかった"]},
"UCVWjF9UkqPAgr4myD6L91QA__mDF9RLSr5TY.json":{
 "summary_3lines":"鬼八&イリスガチャ終了間近の最終評価ランキング。\n鬼八とお玉を特期戦力、DAとミーティアを星2に。\nウルピナ・イリスは星1、確保推奨は鬼八とお玉。",
 "key_topics":["鬼八&イリスガチャ","最終評価ランキング","鬼八特期戦力","お玉高難度","星3〜星1評価"],
 "positive_points":["鬼八は爆火力で周回コンテンツ引っ張りだこの特期戦力","お玉は唯一性満載で高難度・螺旋で活躍間違いなし","DAナンバー5は霊雷編成で攻防バランス良く現環境マッチ","ミーティアは置き物火力バフとBPサポートが優秀","鬼八とお玉は確保して損なしと評価"],
 "negative_points":["ウルピナは同型アタッカー多く唯一性が薄い星1","イリスは火力バフが単体かつ陽条件で場所を選ぶ星1","ミーティアはバフ量がイシスに劣り1ターンのみ","DAは編成難度が高く手持ち揃った人向け"]},
"UCdH4Ijk0D4FFJFRYrUFNzDQ__5aP56s_h9Cs.json":{
 "summary_3lines":"カモキングたちの井戸、100位台狙いの攻略動画。\nヒューズ無しの暦み・Sターミン等11手編成を紹介。\n結果は11手で172位クリア。",
 "key_topics":["カモキング井戸","100位台狙い","ヒューズ無し編成","11手クリア","ランキング"],
 "positive_points":["ヒューズ未所持でも100位台を狙える編成を用意"],
 "negative_points":["上位を狙うにはヒューズが必要になる"]},
"UCdH4Ijk0D4FFJFRYrUFNzDQ___ha_LEsmnoY.json":{
 "summary_3lines":"シュウザーたちの井戸トップクリア編成の解説。\n7手クリア編成と1位6手編成を比較紹介。\n範囲アタッカーが活躍した週。",
 "key_topics":["シュウザー井戸","7手クリア","TOP編成解説","グスタフ","アレツ"],
 "positive_points":["範囲アタッカーが活躍した井戸環境","魂強化が進んだアレツはグスタフ超えで6手可能"],
 "negative_points":["自分は魂が足りず6手クリアには届かなかった"]}
}
for fn,s in S.items():
    d=json.load(open(D+fn))
    d.update(s); d["summarized_at"]=now
    json.dump(d,open(D+fn,'w'),ensure_ascii=False,indent=2)
    print("updated",fn)
print("DONE_MINE", now)
