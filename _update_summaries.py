# -*- coding: utf-8 -*-
import json, datetime, os

D = 'data/pending_summaries/'
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')

S = {
'UCB1MBbdhhBGxxyX9I_3eLUg__2HnoF4YTiFk.json': {
 'summary_3lines': "7.5周年ガチャを掛け合い形式で実況引き\n水着ガチャからすり抜け・爆死を連発\n最後は第3希望止まりでほぼ終了",
 'key_topics': ["7.5周年ガチャ","水着ガチャ","ガチャ実況","すり抜け","爆死"],
 'positive_points': [],
 'negative_points': ["ガチャがすり抜け続きで渋い引き","第3希望止まりで爆死気味"],
},
'UCB1MBbdhhBGxxyX9I_3eLUg__eqMb4U798LI.json': {
 'summary_3lines': "「七」のつく日の確定ガチャ告知動画\n夏のシーズナルイベント開催を予告\n字幕は音楽主体で内容はほぼ取得できず",
 'key_topics': ["確定ガチャ","七のつく日","シーズナルイベント","夏イベント"],
 'positive_points': [],
 'negative_points': [],
},
'UCBC_Fpd3wW-2kjYXVbQJ2hQ__lgZzTfufSv8.json': {
 'summary_3lines': "セフィロト戦で光(陽)PTと闇(陰)PTを比較\n陰PTは火力型で決着が早い\n防御型の陽PTでもイリスの火力が突出",
 'key_topics': ["セフィロト戦","陽単体vs陰単体","エクストラフォース","光PT/闇PT","イリス"],
 'positive_points': ["イリスがサポーターなのに火力トップで優秀","陰PTは火力が高く決着が早い","リラの火力が終盤しっかり伸びる","白バラがBP撒き・毒解除で活躍","ODのエクストラフォース陽が強力"],
 'negative_points': ["陽PT(防御型)はLP攻撃がきつく長期戦","白バラ採用でEPが後半枯渇しがち","ダリオは覚醒まで9ターンかかり火力が遅い"],
},
'UCIzvPxpqEhy_HxidniB_3ow__mdcDdJ4pI5g.json': {
 'summary_3lines': "GジェネエターナルのSSRガンダムF90IIを紹介\n武装のアニメーションを見せるショート動画\n台詞のみで解説はなし",
 'key_topics': ["Gジェネエターナル","ガンダムF90II","SSR","武装アニメ","ショート"],
 'positive_points': [],
 'negative_points': [],
},
'UCNZslKXryDOOEZz7C5aW1TQ__JBTDVzVAJ6M.json': {
 'summary_3lines': "環境変化を踏まえ魂アビリティを再ランキング\n1位は吸収系、敵弱体化・デバフ系が高評価\nダメブロや行動速度系の価値が上昇",
 'key_topics': ["魂アビリティ","ランキング","吸収系","能力弱体解除","ダメージブロック","無人島"],
 'positive_points': ["吸収4は敵を弱らせ自分を強化する究極のチート","能力弱体・全能力アップ解除が高難度で刺さる","ダメージブロック系は価値が上がった","ラウンド開始の行動速度上下系が行動調整に有用"],
 'negative_points': ["全体力アップ系は他アビ増加で優先度が低下","排水の意思は入手困難で汎用性は高くない"],
},
'UCNZslKXryDOOEZz7C5aW1TQ__pt57iTFfUho.json': {
 'summary_3lines': "7.5周年の5大ガチャを使用感込みで再評価\n1位は気発(SSS8ヒット)で環境破壊級\n副防具は3種解説、私はダメブロのサンダル",
 'key_topics': ["5大ガチャランキング","気発","お玉","副防具選択","無人島","7.5周年"],
 'positive_points': ["気発はSSS8ヒットで6億火力の化け物","お玉はチョコ継承で2ターン無敵が破格","サンダルのダメブロ→リレイズ生存戦法が強烈","イリスは属性ヒットリーダーで幻統でも活躍","麦わら帽子は5ターン以降の火力底上げが強力"],
 'negative_points': ["人間女は能力Eで火力が伸びにくい","フェルディナントは剣姫線の威力が低く罠","大当たりバックは序盤が弱く西洋アビスに刺さらない"],
},
'UCNZslKXryDOOEZz7C5aW1TQ__sbPsoxxwxp8.json': {
 'summary_3lines': "日曜恒例の最新キャラランキングを調整\n気発・お玉はトリプルSの特級戦力枠\n単体エクホ持ち増加でマイス枠は評価下げ",
 'key_topics': ["最新キャラランキング","気発","お玉","イリス","特級戦力","無人島"],
 'positive_points': ["気発は1回行動で6億の唯一無二の火力","お玉は挑発+ストック追撃で最強の盾","お玉のチョコ継承2ターン無敵は破格","イリスは双剣・属性ヒットリーダーでS評価"],
 'negative_points': ["ディーバ5は防御軽減75%が標準的でSS届かず","ウルピナは自己バフが薄く火力が伸びにくい","マイス枠(ラゼム/バルテルミ)は評価下げ"],
},
'UCTnmCbMtBLO1IJ6iwRPkySg__py-7_FQmS4Y.json': {
 'summary_3lines': "7.5周年セレクトチケットのおすすめ最終版\n交換期限7/9、7/7ガチャの技マシンに注意\n最新持ちなら技マシン優先、お玉ネメシス等",
 'key_topics': ["セレクトチケット","技マシン","7.5周年","お玉/ネメシス","交換期限","ケルビン枠"],
 'positive_points': ["お玉のチョコ継承は価値が跳ね上がった","ネメシスのジャッジメントシャドウは無人島必須","貝のアクアフォールは水着貝と相性抜群","イリスのヘブンズインペールは要編成で優秀","女神(赤ネサス)は今でも十分強い"],
 'negative_points': ["対応する最新スタイル未所持なら無理に交換不要","気発の発期ラメは価値が下がった","雷パは組む機会が少なく技マシンが使いにくい"],
},
'UCVWjF9UkqPAgr4myD6L91QA__cyEtLQkYl9w.json': {
 'summary_3lines': "終了間近の水着ガチャキャラを最終評価\nネメシス・人間女は星1、貝は星2評価\nイベント防具は瀕死付きサンダルを選択",
 'key_topics': ["水着キャラ最終評価","ネメシス","人間女","貝","イベント防具","無人島"],
 'positive_points': ["貝は3ターン目以降の火ダメ軽減90%超で高難度向き","ネメシスは過去継承で無人島適性あり(星2)","貝は攻防バフが強力で高難度適性が高い"],
 'negative_points': ["ネメシスはエクホ自前無しで火力が出にくい(星1)","人間女はOD1.25倍が低く優先度低め(星1)","貝は5ターンかかり序盤のパワー不足が気になる"],
},
'UCttGAXHA-hoLEVqsXoMVqXQ__RHD-_nR0Ss0.json': {
 'summary_3lines': "キャンベルマリンリゾートの限定SS副防具3種解説\n基本は火力底上げのハイビスカス麦わら帽子推奨\n第2候補は瀕死・無敵を作る日輪層のサンダル",
 'key_topics': ["限定SS副防具","麦わら帽子","日輪層のサンダル","朝顔のパレオ","キャンベルマリンリゾート"],
 'positive_points': ["麦わら帽子は5ターン以降ダメージ1.5倍で高難度に重宝","サンダルは1ターン無敵と能動的瀕死化で唯一性あり","パレオの消費BP-5は周回で便利"],
 'negative_points': ["麦わら帽子は1~4ターン戦・レイドでは意味がない","パレオは使い所が想像しにくく優先度低め","麦わら帽子は将来エクホクリ重複で無意味化の恐れ"],
},
}

for fn, fields in S.items():
    p = D + fn
    with open(p, encoding='utf-8') as f:
        d = json.load(f)
    d.update(fields)
    d['summarized_at'] = NOW
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print('updated', fn)
print('DONE', NOW)
