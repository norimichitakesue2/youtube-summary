# -*- coding: utf-8 -*-
import json, datetime
D = 'data/pending_summaries/'
now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
S = {
'UCB1MBbdhhBGxxyX9I_3eLUg__SR2PBxfAZDo.json': {
 "summary_3lines": "8周年前夜祭のダブルガチャ内容を予想\nヒント皆無のため過去作から消去法で考察\nアビススタイルでセルマ・ラベールを本命予想",
 "key_topics": ["8周年前夜祭ガチャ","ダブルガチャ予想","アビススタイル","セルマ・ラベール","クラウドレルム軍団"],
 "positive_points": ["周年キャラは強力な闇属性傾向で焼き直しが当てやすい"],
 "negative_points": ["過去のシグルナス2年連続やシングルガチャは迷走気味","ラスボスと脇役のガチャ編成は地味"]},
'UCB1MBbdhhBGxxyX9I_3eLUg__mtATAD6Y8WE.json': {
 "summary_3lines": "視聴メダル配布スタイル3体を数値解析\nオグニアナは技弱くヒット数不足だがデバフが実用的\n少年はAJ劣化版で出番薄いがわざ継承に期待",
 "key_topics": ["視聴メダルスタイル","オグニアナ","ブルー","少年","わざ継承"],
 "positive_points": ["オグニアナのデバフ数値はそこそこ良く実用性が高い","少年のわざ継承は未来に可能性を残した"],
 "negative_points": ["オグニアナは技が弱くヒット数が少ない","ブルーは配布で限定より弱い","少年はAJ超劣化版で激戦区で出番なさそう"]},
'UCBC_Fpd3wW-2kjYXVbQJ2hQ__W94aQ_AqR4s.json': {
 "summary_3lines": "信長の野望出陣プレイ412日目の進捗報告\n新キャラ松永久秀など3体入手、最大名101万到達\n全国制圧率7.1%、沖縄制圧と天下5万を目指す",
 "key_topics": ["信長の野望出陣","412日目進捗","松永久秀","全国制圧率","天下・共闘"],
 "positive_points": ["松永久秀は先方範囲縮小が強く900部将では当たり","松永武式は手持ちが少なく入手が助かる"],
 "negative_points": ["列伝イベントが750位でいつもより低く編成見直しが必要","長宗化け・元地下がおらず編成が薄い"]},
'UCIzvPxpqEhy_HxidniB_3ow__3_j7YuGurNs.json': {
 "summary_3lines": "明日実装のハイドラガンダムの性能を確認\n向上ユニットの攻撃型でEX武装は射程が短め\nMPで火力上昇、アビリティは発動させやすい",
 "key_topics": ["ハイドラガンダム","向上ユニット","攻撃型","EX武装","バルダファルギル"],
 "positive_points": ["MP上昇スキルでアビリティや武装ダメージを発動させやすい"],
 "negative_points": ["EX武装の射程1〜4が短め","向上ユニットで目を引く性能はなさそう"]},
'UCIzvPxpqEhy_HxidniB_3ow__FcIO4nlvSuc.json': {
 "summary_3lines": "明日実装のガンダムグリープの性能を確認\n向上ユニットの耐久型でビーム被ダメを30%軽減\nアディンは支援防御2回でき防御範囲も広い",
 "key_topics": ["ガンダムグリープ","向上ユニット","耐久型","支援防御2回","アディンバーネット"],
 "positive_points": ["支援防御2回でき防御範囲が広い","ビーム被ダメ30%軽減で向上にしては固く悪くない"],
 "negative_points": ["EX武装の射程1〜4が短め","マップ兵器にデバフが付いていない"]},
'UCIzvPxpqEhy_HxidniB_3ow__r-hsxNql38Y.json': {
 "summary_3lines": "明日実装のハイドラ・グリープ・黒色サポーターを確認\nハイドラは攻撃型、グリープは耐久型で支援防御2回が優秀\n向上だけのガチャのため投稿者はスルー予定",
 "key_topics": ["ハイドラガンダム","ガンダムグリープ","黒色サポーター","向上ユニット","ガチャスルー"],
 "positive_points": ["グリープは支援防御2回・防御範囲広く向上にしては悪くない","黒色サポーター追加で部隊編成の幅が広がる"],
 "negative_points": ["ハイドラは向上で目を引く性能なし","向上だけのガチャで無理に追う必要はない"]},
'UCIzvPxpqEhy_HxidniB_3ow__uHbk-o3YT0o.json': {
 "summary_3lines": "SSRガンダムアスクレプオス(PXモード)の武装アニメ紹介\nゲーム内セリフ中心の短い演出動画\n性能解説はなし",
 "key_topics": ["ガンダムアスクレプオス","PXモード","武装アニメ","Shorts"],
 "positive_points": [],
 "negative_points": []},
'UCTnmCbMtBLO1IJ6iwRPkySg__ATjZZybiiXs.json': {
 "summary_3lines": "ガチャ中のリアムのフォトンリボルブ火力を実演検証\n追撃20ヒット×3で化け物火力、5〜7億ダメージ連発\n長期戦なら最強だが使う場面が来るか懸念",
 "key_topics": ["リアム","フォトンリボルブ","追撃ヒット数","長期戦","継承"],
 "positive_points": ["リアムの火力は長期戦でダントツ、他を寄せ付けない","フォトンリボルブの追撃ヒット数が化け物級","連車の1番隊長はサポート性能も優秀で継承推奨"],
 "negative_points": ["待機完成型で長期戦が来ないと活躍の場がない","最優先では引かなくてよい(周年待ち)"]},
'UCTnmCbMtBLO1IJ6iwRPkySg__DP4d0tAyBHQ.json': {
 "summary_3lines": "11/20の小夜曲編後編ガチャ内容を徹底予想\nアビス化キャラ+関係者2人のシングル構成と予想\n未登場のサガフロ2からリッチアビスを本命予想",
 "key_topics": ["8周年前ガチャ予想","小夜曲編後編","アビス化","リッチアビス","ディアナ・ウィル"],
 "positive_points": [],
 "negative_points": []},
'UCVWjF9UkqPAgr4myD6L91QA__w4VKjV6aH3Y.json': {
 "summary_3lines": "最新聖王を実際に使い強み弱点を評価\nほぼ1人で全バフ対応の万能サポーターで引き推奨\nビューネイ・ミカエルは基本スルー、周年前の見極め大事",
 "key_topics": ["聖王","ガチャ評価","補助特化","ビューネイ・ミカエル","復刻聖王アビス"],
 "positive_points": ["聖王はほぼ1人で全バフ対応の安定した万能サポーター","聖王ガチャは他もフェルディナント等つぶ揃いで豪華","聖王アビスに継承すれば高水準で使える"],
 "negative_points": ["聖王は単体だと自身の火力が出せない","全員攻撃参加ギミックには対応できない","ビューネイ・ミカエルガチャは動機が弱く基本スルー"]},
'UCdH4Ijk0D4FFJFRYrUFNzDQ__Lt6uYedrKyk.json': {
 "summary_3lines": "アーニャアビスの能力値を早見表でまとめ\n陰属性の火力サポートと自身のアタッカー性能を両立\n立ち上がり遅いが中長期戦・高難度で活躍する優秀スタイル",
 "key_topics": ["アーニャアビス","能力値早見表","陰属性","火力サポーター","高難度"],
 "positive_points": ["味方全体軽減75%とデバフ解除で守りも良い","火力サポートと自身アタッカーを両立するバランス型","取って損しない優秀スタイル"],
 "negative_points": ["攻撃強化の立ち上がりが遅くサンターン目以降","一瞬の火力はそこまで高くない"]},
}
for fn, add in S.items():
    p = D+fn
    d = json.load(open(p, encoding='utf-8'))
    d.update(add); d["summarized_at"] = now
    with open(p, 'w', encoding='utf-8') as fp:
        json.dump(d, fp, ensure_ascii=False, indent=2)
    print("OK", fn)
print("done", now)
