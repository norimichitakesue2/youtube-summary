# -*- coding: utf-8 -*-
import json, datetime, os
D = os.path.expanduser('~/mnt/youtube-summary/data/pending_summaries/')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

S = {
"UCB1MBbdhhBGxxyX9I_3eLUg__vz75pomfsWU.json": {
 "summary_3lines":"螺旋610階エルダードラゴンのギミック解明速報。\nアイツが単騎でも行ける2パターンの無双編成を紹介。\n〇〇縛りで超楽勝になる攻略を解説。",
 "key_topics":["螺旋610階","エルダードラゴン","ギミック解明","単騎攻略","縛り攻略"],
 "positive_points":["単騎でも610階を攻略できると高評価","縛り編成でも超楽勝とアピール"],
 "negative_points":[]
},
"UCIzvPxpqEhy_HxidniB_3ow__8FOdIa5dWn4.json": {
 "summary_3lines":"GジェネETでURチケットのガチャを実施。\n配信の切り抜き動画。\n引いた結果を実況している。",
 "key_topics":["GジェネET","URチケット","ガチャ","配信切り抜き"],
 "positive_points":[],
 "negative_points":[]
},
"UCNZslKXryDOOEZz7C5aW1TQ__Z8zMkh2NeOc.json": {
 "summary_3lines":"Gジェネのイベントシークレットをカウンター戦法で攻略。\n配布ユニット中心でフォースガードを活用。\n戦力強化すれば安定してクリア可能。",
 "key_topics":["Gジェネ","イベントシークレット","カウンター攻略","配布ユニット","フォースガード"],
 "positive_points":["カウンターぶっぱで安定攻略できると高評価","配布ユニットでも十分クリア可能","戦力を強化すれば簡単になる"],
 "negative_points":["スタミナ剤を10個ほど消費したと言及"]
},
"UCdH4Ijk0D4FFJFRYrUFNzDQ__ISx5unE9xbY.json": {
 "summary_3lines":"ロマサガRS『シグフレイたちの井戸』100位編成を紹介。\n3ターン63の立ち回りでジの火力を最大化。\nキャラが揃えば誰でもランクイン可能。",
 "key_topics":["ロマサガRS","シグフレイの井戸","100位編成","3ターン攻略","ジ火力編成"],
 "positive_points":["ジの火力で約9億ダメージが出ると高評価","キャラが揃えば誰でもランクイン可能"],
 "negative_points":["1ターン目に下の手下が交渉発動したらやり直しが必要と注意"]
},
"UCNZslKXryDOOEZz7C5aW1TQ__DLr5oC7URQs.json": {
 "summary_3lines":"Gジェネのエタロ31金色をガチャ産なしで攻略。\n開発機と配布サポートで組んだ編成を解説。\n装備強化を忘れてもクリアできる安定感。",
 "key_topics":["Gジェネ","エタロ31金色","ガチャ産なし","開発機編成","配布サポート"],
 "positive_points":["ガチャ産なしでも安定攻略できると高評価","アムロが偉すぎると性能を絶賛","装備を忘れてもクリアできる立ち回りの強さ"],
 "negative_points":["キュベレの取り巻き(お供)がうざいと不満","ガーサは兵装が高く倒しにくいと指摘"]
},
"UCNZslKXryDOOEZz7C5aW1TQ__t5HH7bVgb3g.json": {
 "summary_3lines":"ロマサガRS螺旋610階エルダードラゴンのギミックを解説。\n戦士軸の特攻編成と王道のミルザ編成を実況。\n突属性は1人だけ入れBP系ゲージを重視。",
 "key_topics":["ロマサガRS","螺旋610階","エルダードラゴン","ギミック解説","戦士軸編成","ミルザ編成"],
 "positive_points":["戦士軸の特攻編成が刺さって無双できると高評価","ミルザ(ネウ)編成は防御力が高く最強系と絶賛","ベントがサポートとして優秀"],
 "negative_points":["突属性を全員に入れると逆にやられると注意","ゼノンは行動回数が少なく3ターンは厳しいと指摘"]
},
"UCTnmCbMtBLO1IJ6iwRPkySg__6PWOLqUPGFs.json": {
 "summary_3lines":"ロマサガRSでギュスターブと戦士の確保を狙うガチャ実況。\n暦み編第9弾のダブルガチャを全力で回す。\n5万ジュエル課金し両キャラとも無事確保。",
 "key_topics":["ロマサガRS","ガチャ実況","ギュスターブ確保","戦士確保","暦み編第9弾"],
 "positive_points":["戦士はスペックが飛んでる(ぶっ壊れ)と性能を絶賛","ギュスターブを引けて大満足","ステップ7でWピックアップ確保の大勝利"],
 "negative_points":["お得ジュエル系がなく5万(4万円)課金を強いられたと不満","すり抜けが続き何も得られない展開に嘆く","ミカエルばかり出て当たりが遠いと愚痴"]
},
"UChLJCB4jXvr1Zi0WT-a4ReQ__MYf6uAaKh1s.json": {
 "summary_3lines":"ロマサガRSハロウィンガチャでロッキーを追い求める実況。\n53回引くもピックアップは0でロッキー出ず。\n天井には届かず残念な結果に。",
 "key_topics":["ロマサガRS","ハロウィンガチャ","追いガチャ","ロッキー狙い","すり抜け"],
 "positive_points":["バチバチは強いので期待と言及"],
 "negative_points":["53回引いてピックアップ0の渋い結果","ロッキーが出ず天井も間に合わないと落胆","すり抜けばかりで収穫なし"]
},
"UCttGAXHA-hoLEVqsXoMVqXQ__B9msULySSQQ.json": {
 "summary_3lines":"ロマサガRS螺旋回廊610階エルダードラゴンを攻略。\n実際の戦闘を実況。\nエルダードラゴン討伐の様子を紹介。",
 "key_topics":["ロマサガRS","螺旋610階","エルダードラゴン","攻略実況"],
 "positive_points":[],
 "negative_points":[]
},
}

for fn, fields in S.items():
    p = D+fn
    d = json.load(open(p, encoding='utf-8'))
    d['summary_3lines'] = fields['summary_3lines']
    d['key_topics'] = fields['key_topics']
    d['positive_points'] = fields['positive_points']
    d['negative_points'] = fields['negative_points']
    d['summarized_at'] = now
    json.dump(d, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print('OK', fn)
print('ALL DONE', now)
