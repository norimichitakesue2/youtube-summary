import json, os, datetime, sys, importlib.util
D='data/pending_summaries/'
now=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
def apply(fn, s3, topics, pos, neg):
    p=D+fn
    d=json.load(open(p, encoding='utf-8'))
    d['summary_3lines']=s3
    d['key_topics']=topics
    d['positive_points']=pos
    d['negative_points']=neg
    d['summarized_at']=now
    json.dump(d, open(p,'w',encoding='utf-8'), ensure_ascii=False, indent=2)
    print('applied', fn)

spec=importlib.util.spec_from_file_location('batch', sys.argv[1])
batch=importlib.util.module_from_spec(spec); spec.loader.exec_module(batch)
for args in batch.DATA:
    apply(*args)
