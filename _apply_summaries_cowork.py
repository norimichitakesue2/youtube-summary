import json, os
from datetime import datetime, timezone

D = 'data/pending_summaries/'
NOW = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

S = {
 'UCB1MBbdhhBGxxyX9I_3eLUg__H6XLRgO7sqY.json': {
  'summary_3lines': "2026年5月のスタイルを振り返るワースト＆MVP企画。\nサイバ・セイオー・コヨミが今も続く強スタイル筆頭。\n周年前は我慢、第1弾は配布席で確保が安心と結論。",
  'key_topics': ["5月振り返り","ワースト＆MVP","サイバ最評価","コヨミ短期環境","周年前確保"],
  'positive_points': ["サイバ：編成頻度が圧倒的で今も現役","セイオー：高難度で替えが効かない","コヨミ：短期決戦環境を作った永久デバフ","ビクトール：高火力ばらまきで廃れにくい","サライ：全てハイスペックの接待スタイル"],
  'negative_points': ["シレイ：超低スペックの周年大外れ枠","ミルザ：見た目より火力が低い","ヴァンパイアレディ：回避継承が生かせず","アルドラ：舞姫の劣化版で浮上せず","ドロレス：最初の1度だけ接待で以降ダメ"],
 },
 'UCBC_Fpd3wW-2kjYXVbQJ2hQ__NS5OEAYfVmo.json': {
  'summary_3lines': "あんずもんが2026年に取って良かったキャラTOP10を発表。\n1位サイバ、2位イズナ暦、3位西王アビスがトップ3。\nコッペパンやワグナスなど汎用性の高いキャラを高評価。",
  'key_topics': ["取って良かったTOP10","1位サイバ","2位暦","コッペパン評価","将来性重視"],
  'positive_points': ["サイバ：バフ量が圧倒的で入れる入れないで激変","イズナ暦：技が強く回復も便利で2位","コッペパン：瀕死編成でダメブロ＋回避が優秀","ワグナス：EF干渉が少なく長期的に使える","アセルスアビス：高火力期待値で将来性あり"],
  'negative_points': ["アセルスアビス：回復できないのが懸念","コッペパン：瀕死にする手間がある","ヴィンセント：バフ運用で使うのが難しい"],
 },
 'UCBC_Fpd3wW-2kjYXVbQJ2hQ__R62_Mnawdpk.json': {
  'summary_3lines': "トゥ・クアイ147回を攻略しつつ火力インフレに驚く回。\n玄武が10億、レッドが桁違いの火力を叩き出す。\n周年前から2桁億が見え、インフレ加速に警戒を促す。",
  'key_topics': ["トゥ・クアイ147","火力インフレ","レッド超火力","玄武10億","周年前"],
  'positive_points': ["レッド：魂レベル60台で桁違いの火力","暦・サイバ：火力バフで底上げが効く"],
  'negative_points': ["インフレの加速が止まらず火力バランスに戸惑い"],
 },
 'UCIzvPxpqEhy_HxidniB_3ow__1oczFH7vRZ8.json': {
  'summary_3lines': "GジェネETのジェミナス01武装アニメを見せるShort動画。\nアサルトブースター装備のEXシステム演出が中心。\n解説はなくセリフと演出のみの短尺コンテンツ。",
  'key_topics': ["GジェネET","ジェミナス01","武装アニメ","EXシステム","Shorts"],
  'positive_points': [],
  'negative_points': [],
 },
 'UCNZslKXryDOOEZz7C5aW1TQ__dqlnVAJgM9Q.json': {
  'summary_3lines': "つもつもが自身の使用回数で選ぶ2026年キャラランキング。\n1位サイバ、2位暦、3位ヒースパーが環境を支配。\nギュスターヴなど推しキャラも交えて振り返る。",
  'key_topics': ["使用率ランキング","1位サイバ","暦の相性","ヒースパー","推しギュスターヴ"],
  'positive_points': ["サイバ：ダントツ1位、編成を壊してでも入れる性能","暦：行動回数で防御軽減、サイバと相性最強","コッペパン／銀パ：銀属性が今年猛威を振るう","ビクトール：2回行動の超早モーション","ギュスターヴ：破壊力が高く使って楽しい推し"],
  'negative_points': ["セオ：ゴリ押しスタイルに合わず使用回数8位","アルティメットミド：EF倍率上昇で使う人が減った"],
 },
 'UCTnmCbMtBLO1IJ6iwRPkySg__3WNm4pyKICw.json': {
  'summary_3lines': "三蔵ゲームズが8周年イベント前夜に期待を語る回。\n配布ジュエル・制圧戦・復刻ガチャ・新ガチャを予想。\n第1弾は発火戦SS8体ダブルガチャと大胆予想。",
  'key_topics': ["8周年前夜祭","公式生放送","ジュエル配布予想","新ガチャ予想","予想答え合わせ"],
  'positive_points': ["7.5周年ガチャ：暦・サイバが半年環境を引っ張る良設計","周年の配布・制圧戦・新コンテンツに期待"],
  'negative_points': ["手持ちジュエルが9600と心許ない","セレチケがアニバでは配られない傾向"],
 },
 'UCTnmCbMtBLO1IJ6iwRPkySg__RiXfsAO60IQ.json': {
  'summary_3lines': "三蔵が8周年直前の確保優先度ランキングを発表。\n最優先はアセルスアビスとリアム、技継承で腐らない点を絶賛。\nアポロンやキャンディは旧世代・趣味枠で優先度低め。",
  'key_topics': ["確保優先度","最優先アセルス","リアム絶賛","モンド意外な高評価","周年直前"],
  'positive_points': ["アセルスアビス：EFばらまき＋回避付与＋短期トップ火力","リアム：毎ターン高ヒット、技本体で将来腐らない","モンド：重撃軽減とデバフ付与が強力","ウルピナアビス：ディフェンダー最上位で棍棒コンボ","レッド：妖属性の2ターンに1回の強力火力"],
  'negative_points': ["アポロン：旧世代で今から属性揃える価値は薄い","ファイアブリンガー：熱パの編成難易度が高い","キャンディ：趣味パで編成難度の割に弱い","人間男アビス：体験枠で必須感が薄い"],
 },
 'UCVWjF9UkqPAgr4myD6L91QA__tDCrHTWweHo.json': {
  'summary_3lines': "微課金視点で2026年に引いて良かったキャラの共通点を分析。\n唯一性と汎用性の高いキャラが長く活躍すると結論。\n8周年は火力だけでなく自分に必要か見極めて引くべきと助言。",
  'key_topics': ["確保して良かったキャラ","唯一性重視","汎用性","活躍限定的キャラ","8周年判断基準"],
  'positive_points': ["オタマ：2ターンダメブロが唯一性高く現役","コッペパン：瀕死＋自給力で幅広く活躍","サイバ・暦：汎用性が高く幅広いコンテンツで使える","ターミン：5属性サポートで選択肢が広い"],
  'negative_points': ["ヴァンパイアレディ：インキャラ増加で代用され出番減","ストライフ：アタッカーインフレに飲まれ引退","ジニー：現登場限定で汎用性が低い"],
 },
 'UCdH4Ijk0D4FFJFRYrUFNzDQ__anGO-wQutWI.json': {
  'summary_3lines': "レッドの能力値を早見表でまとめた解説動画。\n単発10億超え、49ヒットで約500億ダメージのぶっ壊れ火力。\n持っていて未使用なら育てる価値ありと推奨。",
  'key_topics': ["レッド能力値","単発10億","49ヒット","超火力アタッカー","育成推奨"],
  'positive_points': ["レッド：単発10億超・49ヒットで約500億ダメージ可能な超火力"],
  'negative_points': ["性能はシンプルなアタッカーのみでサポート要素はない"],
 },
 'UChLJCB4jXvr1Zi0WT-a4ReQ__J8JQwXT9ack.json': {
  'summary_3lines': "くんチャンネルが人間男ガチャを本人不在で引く実況動画。\nすり抜け連発で本命が出ず悲劇的なスタートに。\n天井近くまで回しアポロンや体験バルドなどを入手。",
  'key_topics': ["人間男ガチャ","本人不在実況","すり抜け連発","天井近く","ガチャ実況"],
  'positive_points': [],
  'negative_points': [],
 },
}

done=[]
for fn, add in S.items():
    p = D+fn
    with open(p, encoding='utf-8') as fp:
        d = json.load(fp)
    d['summary_3lines'] = add['summary_3lines']
    d['key_topics'] = add['key_topics']
    d['positive_points'] = add['positive_points']
    d['negative_points'] = add['negative_points']
    d['summarized_at'] = NOW
    with open(p, 'w', encoding='utf-8') as fp:
        json.dump(d, fp, ensure_ascii=False, indent=2)
    done.append(fn)

print('APPLIED', len(done), 'files at', NOW)
for f in done: print(' ', f)
