import json, os, datetime

D = 'data/pending_summaries/'
NOW = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

S = {
"UCB1MBbdhhBGxxyX9I_3eLUg__CB17Q9CiKVM": {
  "summary_3lines": "Memoria『幼子の祈り』の③話から最終⑬話を収録\nストーリーパートを一気にプレイ\n字幕情報が乏しく内容の詳細は不明",
  "key_topics": ["Memoria", "幼子の祈り", "ストーリー周回"],
  "positive_points": [],
  "negative_points": [],
},
"UCB1MBbdhhBGxxyX9I_3eLUg__L0j_FrAtPdY": {
  "summary_3lines": "63連ガチャに挑戦した記録動画\n途中から大逆転、まさかのキャラが登場\n結果に手のひら返しで盛り上がる",
  "key_topics": ["63連ガチャ", "大逆転", "ガチャ結果"],
  "positive_points": ["まさかのキャラが当たり大逆転の引き"],
  "negative_points": [],
},
"UCB1MBbdhhBGxxyX9I_3eLUg__rybrEeMcChg": {
  "summary_3lines": "7.5周年ラスト5弾含む全8ガチャ24体を厳選ランキング\n暦み・ヴィンセント・ボルカノなど高難度向けを高評価\nスルー確定組も多く投稿者は暦みまで様子見の構え",
  "key_topics": ["24体ランキング", "厳選", "暦み", "ヴィンセント", "継承優先度"],
  "positive_points": ["暦みは高難度のクリアターン短縮が非常に有用", "ヴィンセントは汎用性と突出した強さ", "ボルカノは熱アタッカーと組ませると強力", "岩ずもは火力ベース作りに必須級"],
  "negative_points": ["メロトセロイは特徴なしで性能過去最低", "ボルレットはデバフしかできない", "ダリアス・ミニオンは出力が弱い", "ハーディは必然性がなく殴った方が早い"],
},
"UCBC_Fpd3wW-2kjYXVbQJ2hQ__89aV7MSyVUQ": {
  "summary_3lines": "信長の野望出陣プレイ259日目の進捗報告\n武将育成や拠点取りで意味値・制圧率を着実に向上\n城Lv上げと毛利元就対策に課題が残る",
  "key_topics": ["信長の野望出陣", "259日目", "武将育成", "拠点取り", "意味値"],
  "positive_points": ["弓の武将は希少価値が高くありがたい", "眠っていた武将を育成し意味値がアップ", "プレイヤーレベル92まで順調に上昇"],
  "negative_points": ["城Lv上げが困難で対策を知りたい", "毛利元就が勢力戦で大暴れし難敵", "中国地方の拠点がなかなか取れない"],
},
"UCTnmCbMtBLO1IJ6iwRPkySg__Y0Q-QykK5HI": {
  "summary_3lines": "7.5周年8ガチャを性能のみでランキング中間発表\n8位バルテルミー編、7位メロトセロイ編と新ガチャが下位\nリアム・ダリオは単体性能が高く上位候補",
  "key_topics": ["7.5周年", "ガチャランキング", "中間発表", "リアム", "ダリオ"],
  "positive_points": ["リアムは当たりで継承込み短期決戦が強力", "ダリオはカタログスペックが高い", "メリッサは使い所次第で良性能"],
  "negative_points": ["バルテルミー編は直近ガチャで見劣りし8位", "メロトセロイ編はコスプレ寄りで性能控えめ", "アーニャ・ダリアスは優先度が低い"],
},
"UCTnmCbMtBLO1IJ6iwRPkySg__ZabH-OccZ-U": {
  "summary_3lines": "4年ぶりのロマンシングブライドWガチャに挑戦\nメロトセロイ編で神引き連発、メリッサまでコンプ\n絶好調の流れでバルテルミー編にも続行",
  "key_topics": ["ロマンシングブライド", "Wガチャ", "メロトセロイ", "神引き", "ガチャ実況"],
  "positive_points": ["メロトセロイのイラストが最高で乗り換えたいほど", "序盤からムクチャ等の神引きで勝ち確", "花嫁ガチャのシーズナル演出が良い"],
  "negative_points": ["バーニーは昔ほどSSが出る信頼度がない"],
},
"UCTnmCbMtBLO1IJ6iwRPkySg__jyuYSHvqqQM": {
  "summary_3lines": "情説イベント・セオアビスの期間限定報酬を解説\nロマンシング1回クリアで報酬一括、無理なら周回でOK\n投稿者はこの救済設計を大絶賛",
  "key_topics": ["セオアビス", "聖王[厄]", "期間限定報酬", "記憶再戦", "ロマンシング"],
  "positive_points": ["ジュエル500・ソウルピース100など報酬が豪華", "ロマンシング以外は記憶再戦で楽に集められる", "クリア＋周回どちらでも取れる救済設計を大賛成"],
  "negative_points": ["報酬期間が約1週間と短い", "ロマンシングは難易度が高く忙しい層には厳しい"],
},
"UCdH4Ijk0D4FFJFRYrUFNzDQ__8g-s5I2OXgA": {
  "summary_3lines": "聖王[厄]の記憶周回を32秒で回す編成を紹介\nロマンシングをクリアできない人向けの周回用\n字幕情報が乏しく詳細解説は不明",
  "key_topics": ["聖王[厄]", "記憶周回", "32秒編成", "周回"],
  "positive_points": ["32秒で周回でき報酬集めが効率的"],
  "negative_points": [],
},
"UChLJCB4jXvr1Zi0WT-a4ReQ__xs9EnAaQ87Q": {
  "summary_3lines": "クロエ編ガチャでエスパーギャルを狙う追いガチャ実況\nヴィンセント3体やクロエ・アルベルトを引き当てる\n物欲センサーで本命は出ず天井到達",
  "key_topics": ["追いガチャ", "クロエ編", "エスパーギャル", "ヴィンセント", "天井"],
  "positive_points": ["クロエのイラストがとてもきれい", "ヴィンセントを3体引けた好調な引き"],
  "negative_points": ["物欲センサーで本命エスパーギャルが出ず", "ペット枠の連続すり抜けで天井到達"],
},
"UCttGAXHA-hoLEVqsXoMVqXQ__TNsnNSxkSnU": {
  "summary_3lines": "バルテルミー編ガチャのバルテルミー等を性能考察\n術算の火炎ODは1.75倍と強力だが運用条件が多い\nマイス/ラゼム所持なら無理に引かなくてよくB+評価",
  "key_topics": ["バルテルミー", "グスタフ", "性能考察", "オーバードライブ", "継承"],
  "positive_points": ["術算誓の火炎ODで最終ダメ1.75倍は強力", "味方への75%軽減が優秀", "メリッサと相性が良く夫婦コンビが噛み合う"],
  "negative_points": ["先制・BP消費22など運用ハードルが高い", "消費BP+5の重いデメリットがある", "ODゲージ上昇を自前で持たない", "マイス/ラゼム所持なら無理に取る必要なし"],
},
"UCttGAXHA-hoLEVqsXoMVqXQ__pcbgii6nDKQ": {
  "summary_3lines": "メロトセロイ編ガチャの3スタイルを性能考察\nメロトセロイ単体はC評価だが継承込みでA-に化ける\nメリッサはOD・BP・軽減の3要素が高水準で優秀",
  "key_topics": ["メロトセロイ", "メリッサ", "性能考察", "継承", "オーバードライブ"],
  "positive_points": ["メリッサはOD満タン5ターンとBP回復が優秀", "メロトセロイはクリスマス継承込みで大幅強化", "メロトセロイのOD連携付与は他と被らず利点"],
  "negative_points": ["メロトセロイ単体は最低のC評価", "アタッカーもサポーターも見劣りする", "メロトセロイの火ダメ軽減23%は低い"],
},
"UCv41cxF-vvrbJTjX3u4r2QQ__626Qz7Wk3Aw": {
  "summary_3lines": "討伐聖王[厄]のギミック解説と低難度向け編成紹介\nロマンシングは難しいが記憶再戦の周回で報酬は取れる\nチャレンジ3以下9種の編成を提示し無理クリア不要と説く",
  "key_topics": ["聖王[厄]", "討伐", "記憶再戦", "低難度編成", "期間限定報酬"],
  "positive_points": ["チャレンジ3以下は記憶再戦可で1日かからず集まる", "無理にロマンシングをクリアしなくても報酬を取れる"],
  "negative_points": ["ロマンシングは偶数ターンのバフ増で難しい", "熱来編成NGなどギミックが複雑", "イを過ぎると攻撃が激しく耐えきれない"],
},
}

cnt = 0
for vid, fields in S.items():
    p = D + vid + '.json'
    if not os.path.exists(p):
        print('MISSING', p); continue
    d = json.load(open(p, encoding='utf-8'))
    d.update(fields)
    d['summarized_at'] = NOW
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    cnt += 1
print('updated', cnt, 'files at', NOW)
