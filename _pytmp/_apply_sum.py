# -*- coding: utf-8 -*-
import json, os, datetime
D = os.path.expanduser('~/mnt/youtube-summary/data/pending_summaries/')
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

S = {
"UCB1MBbdhhBGxxyX9I_3eLUg__uTCoNjQ_A6I.json": {
 "summary_3lines": "ジュエルビースト井戸で満額80万ダメージを狙う挑戦\n5ターン目から本気、短期決戦ダンスタイル編成を解説\n熱雷は被ダメ強化、OD貫通とダメブロ活用が攻略の鍵",
 "key_topics": ["ジュエルビースト井戸","満額80万狙い","短期決戦編成","OD貫通","ダメブロ活用"],
 "positive_points": ["暦み/サルーインは短期決戦向きで有効","弱点が取れる斬属性が刺さる","防御が高いダメブロが便利","殴れるキャラを入れれば3ターン可能"],
 "negative_points": ["熱雷攻撃を受けると敵が被ダメ強化","カウンター連撃を止められると討伐ターンが伸びる","ジュエルビーストにスタンが効かない"]
},
"UCIzvPxpqEhy_HxidniB_3ow__RXxuIiLZ5jA.json": {
 "summary_3lines": "GジェネエターナルのSSRガンダムジェミナス02の武装アニメ紹介\nDXシステム起動など必殺演出を収録したShorts\nセリフ付きの武装モーションを短尺で披露",
 "key_topics": ["GジェネET","ガンダムジェミナス02","武装アニメ","SSR","Shorts"],
 "positive_points": [],
 "negative_points": []
},
"UCTnmCbMtBLO1IJ6iwRPkySg__4Fsu65nAQL0.json": {
 "summary_3lines": "アセルス編ガチャでレッド/メサルティム狙いの天井チャレンジ\n140連＋追加課金もピックアップが出ず天井突破の悲劇\n周年前にガチャのトラウマがさらに深まる悲報回",
 "key_topics": ["アセルス編ガチャ","天井突破","レッド/メサルティム狙い","追い課金ガチャ","周年前"],
 "positive_points": ["ムクちゃん(SS)が出た瞬間は激アツ","一発逆転があるのがロマサガRS"],
 "negative_points": ["140連でアセルスしか出ない","天井1.5万メダルでもコンプ不可","追加課金してもピックアップが出ず","爆死3より辛い物欲センサー","メサルティムを手放す危機に"]
},
"UCTnmCbMtBLO1IJ6iwRPkySg__jyl3em9xQTo.json": {
 "summary_3lines": "新追加の超進化防具(ロブスターメール/セオ3種)の性能レビュー\nセオのコテは毎ターンOD満タン永続で破格、絶対作るべき\nブーツ・兜は用途限定、ロブスターはボストン専用",
 "key_topics": ["超進化防具","セオのコテ","セオのブーツ/兜","ロブスターメール","OD満タン永続"],
 "positive_points": ["セオのコテは毎ターンOD満タン永続で破格","編成の幅が大きく広がる","全ステ100上昇も馬鹿にできない","被ダメ軽減15%が全てに付く"],
 "negative_points": ["セオのブーツの先攻耐性は1ターン目のみで惜しい","セオの兜の怪獣は自分だけでピンポイント","ロブスターメールはボストン専用で汎用性低い","セオの鎧は1個しか使えない"]
},
"UCdH4Ijk0D4FFJFRYrUFNzDQ__hrHEl9rijU0.json": {
 "summary_3lines": "ジュエルビースト井戸で50〜100位入りを狙う3編成を公開\nコヨミ・サイバ・アセルス・サルーイン軸の構成を紹介\nヴィクトール入り構成で38位あたりを記録",
 "key_topics": ["ジュエルビースト井戸","50-100位編成","3パターン編成","サイバ/アセルス軸"],
 "positive_points": ["サイバ・アセルス・サルーイン軸は安定","ヴィクトール構成で38位の好順位"],
 "negative_points": ["上位との順位差はなかなか大きい"]
},
"UCB1MBbdhhBGxxyX9I_3eLUg__QFhN5Q9-qbs.json": {
 "summary_3lines": "周年前の前夜祭前にガチャ厳選勢がガチャを引きまくる回\nアセルス狙いで天井覚悟、掛け合い形式で実況\n30連で早めの当たりを引き大物キャラを確保",
 "key_topics": ["周年前ガチャ","ガチャ厳選","アセルス狙い","天井覚悟","前夜祭前"],
 "positive_points": ["30連で早めに当たりを引けた","大物キャラが続々で引き時との声"],
 "negative_points": ["天井が見えるほど渋い","人魚キャラは使いづらい","ポルカをロストした疑惑"]
},
"UCBC_Fpd3wW-2kjYXVbQJ2hQ__vhO3w1hqga4.json": {
 "summary_3lines": "キャンディ性能チェックで性別不明VS女性の縛り対決\n性別不明編成はキャンディ・原流で6億超えの火力を記録\n女性縛りも健闘、コッペパン有無が勝敗の分かれ目",
 "key_topics": ["キャンディ性能","性別不明縛り","女性縛り対決","原流/コッペパン","エクストラフォース"],
 "positive_points": ["キャンディは意外と火力が乗る好印象","原流が圧倒的火力でぶっ壊し","コッペパンのバフ/防御が強力","代々は防御強化量が高い","性別不明は全体火力が高い"],
 "negative_points": ["キャンディは事前の期待は薄かった","女性縛りはコッペパン不在で火力出し切れず","ピンクパンチが手持ちになく惜しい"]
},
"UCIzvPxpqEhy_HxidniB_3ow__BNcdi3jjyGw.json": {
 "summary_3lines": "GジェネエターナルのSSRガンダムグリープの武装アニメ紹介\nEXシステム発動・オーバードライブの演出を収録\nセリフ付きの必殺モーションの短尺Shorts",
 "key_topics": ["GジェネET","ガンダムグリープ","武装アニメ","EXシステム","Shorts"],
 "positive_points": [],
 "negative_points": []
},
"UCTnmCbMtBLO1IJ6iwRPkySg__KJ-Ch86y_FY.json": {
 "summary_3lines": "11/17最新版、6ガチャ22スタイルの確保優先度ランキング\n最優先は聖王アビス・聖王・アセルス・フェルディナント\n優先度高の筆頭はリアム、長期戦最強候補と高評価",
 "key_topics": ["確保優先度ランキング","聖王アビス最優先","アセルス評価","リアム長期戦最強","周年前ガチャ"],
 "positive_points": ["聖王アビスは高難度で覇権級","アセルスは火力+EFばらまき+回避で優秀","リアムは長期戦で全キャラ最強候補","フェルディナントは瀕死サポで火力高い","ミカエルは証券持ちアタッカーで優秀"],
 "negative_points": ["聖王2位はアビス所持前提気味","復刻アビス聖王の商法がやらしい","ミカエルは後出しで優先度中に落ちうる","キャンディは編成ハードル高く特別強くない","メサルティムは隷パ向けで特別感薄い"]
},
"UCdH4Ijk0D4FFJFRYrUFNzDQ__no8Jqf3E79o.json": {
 "summary_3lines": "ジュエルビースト3ターンクリアの最重要ポイント8つを解説\n熱冷雷属性は避け斬属性多段＋火力サポートを採用\n2ターン目のOD調整とダメブロ・術師で安定攻略",
 "key_topics": ["ジュエルビースト3T攻略","属性選び","OD打順ギミック","ダメブロ配置","魂アビリティ"],
 "positive_points": ["斬属性多段＋火力サポート持ちが有効","ダメブロ先頭配置で被害を防げる","魂アビ全捨てバフで火力と耐久を両立"],
 "negative_points": ["熱冷雷属性は敵の火力が跳ね上がる","2ターン目に全員ODを打つと全滅する","単純なアタッカー性能だけでは活躍しづらい"]
},
"UChLJCB4jXvr1Zi0WT-a4ReQ__ccxtp7l0qjE.json": {
 "summary_3lines": "聖王編後編ガチャを3歳児と絵本を読みつつ実況する追いガチャ回\n序盤パウルス高発進も追加なく天井まで到達\nピックアップ4体がパウルス偏り(パウループ)で本命は空振り",
 "key_topics": ["聖王編後編ガチャ","西王/フェルディナント狙い","天井到達","パウループ","親子実況"],
 "positive_points": ["序盤20連でパウルス2体の高発進","天井でピックアップ4体を確保"],
 "negative_points": ["20連以降は追加スタイルなしの渋さ","ピックアップがパウルス偏りで本命出ず","西王・フェルディナントとは縁がなかった"]
},
"UCttGAXHA-hoLEVqsXoMVqXQ__CKeeCi_wvkI.json": {
 "summary_3lines": "未消化ミッション消化の生配信、戦士編成で高難度に挑戦\nクイーン/4魔貴族ミッションを戦士運ゲ編成で攻略\n8周年63連ガチャの交換候補を視聴者と議論",
 "key_topics": ["未消化ミッション消化","戦士編成攻略","アビスナーガ","8周年63連ガチャ","交換候補議論"],
 "positive_points": ["リアムは長期戦アタッカートップで評価","パワーエンチャント戦士が高難度に刺さる","セオのコテでレント運用が改善","ヒューズ/エリスは層の薄い枠で交換価値あり"],
 "negative_points": ["アビスナーガはギミックが面倒なクソボス扱い","戦士攻略は結局運ゲになりがち","バルマンテは弱く上位互換が欲しい","代々は硬いスタイル増加で価値低下"]
},
}

ok=0; miss=[]
for fn, fields in S.items():
    p = D+fn
    if not os.path.exists(p):
        miss.append(fn); continue
    d = json.load(open(p, encoding='utf-8'))
    d["summary_3lines"] = fields["summary_3lines"]
    d["key_topics"] = fields["key_topics"]
    d["positive_points"] = fields["positive_points"]
    d["negative_points"] = fields["negative_points"]
    d["summarized_at"] = now
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    ok+=1
print("updated", ok, "missing", miss)
