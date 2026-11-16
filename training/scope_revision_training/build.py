import json, hashlib
from pathlib import Path
P=Path(__file__).parent
# New domains deliberately outside both earlier pilots.
DOMAINS=[
('laundry_cycle','normal','delicate','wool garments'),('dishwasher_cycle','normal','heavy','baked-on pans'),('vacuum_power','standard','low','rooms with sleeping pets'),('thermostat_target','21 C','19 C','overnight guests'),
('printer_sides','single-sided','double-sided','internal drafts'),('scan_resolution','300 dpi','600 dpi','archival scans'),('backup_frequency','weekly','daily','active client projects'),('archive_compression','zip','tar.gz','Linux deployments'),
('camera_capture','RAW','RAW plus JPEG','same-day client previews'),('video_export_resolution','1080p','4K','cinema submissions'),('audio_export_depth','16 bit','24 bit','studio masters'),('animation_frame_rate','24 fps','30 fps','broadcast deliveries'),
('plant_watering','every seven days','every three days','outdoor planters in summer'),('lawn_cut_height','three inches','four inches','heat-wave weeks'),('aquarium_light_duration','eight hours','six hours','algae treatment weeks'),('pool_filter_duration','six hours','ten hours','heavy-use weekends'),
('bread_crust','light','dark','rye loaves'),('pasta_shape','penne','fusilli','cold pasta salads'),('rice_texture','firm','soft','rice porridge'),('soup_consistency','chunky','smooth','freezer batches'),
('package_wrapping','paper','reusable fabric','birthday gifts'),('flower_arrangement','mixed colors','white only','memorial orders'),('cake_frosting','buttercream','ganache','outdoor summer parties'),('candle_scent','citrus','unscented','shared dining tables'),
('terminal_font_size','12 points','16 points','projector demonstrations'),('spreadsheet_decimal_places','two','four','lab measurements'),('plot_marker_shape','circles','triangles','black-and-white printouts'),('diagram_connector_style','curved','right-angle','circuit diagrams'),
('chess_time_control','ten minutes','three minutes','warm-up games'),('game_difficulty','normal','easy','sessions with beginners'),('puzzle_piece_count','500','1000','holiday gatherings'),('karaoke_key','original','two semitones lower','late-night sessions'),
('library_loan_reminders','three days before','one week before','interlibrary loans'),('invoice_payment_window','30 days','14 days','new customers'),('appointment_buffer','ten minutes','twenty minutes','first-time consultations'),('ticket_receipt_format','digital','printed','school trips'),
('suitcase_style','soft shell','hard shell','trips with fragile equipment'),('tent_capacity','two-person','four-person','family camping'),('bicycle_tire_pressure','60 psi','45 psi','gravel rides'),('swim_pool_lane','middle lane','edge lane','recovery sessions')]
# Each template family has a distinct discourse structure. All four action variants
# within each domain share their final turn and assistant text exactly.
PATTERNS=[
('Before picking the value, here is what I mean: {intent}', 'What value should I use?', 'Use {new} instead.'),
('I want to sort out a preference. {intent}', 'Tell me the choice you have in mind.', 'I would pick {new}.'),
('{intent} I have a replacement value in mind.', 'Go ahead.', 'Make it {new}.'),
('Let me explain the intended reach first. {intent}', 'And your preferred value?', '{new} is the choice.'),
('About {label}: {intent}', 'What should the value be?', 'Please use {new}.'),
('I have been thinking about {label}. {intent}', 'Which option are you choosing?', 'Let us go with {new}.'),
('{intent} That is the part I wanted to settle before choosing.', 'What is your choice?', 'I choose {new}.'),
('There are two issues here, the reach and the value. {intent}', 'What value do you want?', 'The value should be {new}.'),
('A note about how to handle this request: {intent}', 'What option do you prefer?', 'My choice is {new}.'),
('For {label}, I want to explain my request first. {intent}', 'What would you like to use?', 'Switch to {new}.')]
ACTIONS=['set_default','set_exception','no_op','defer']
def text_state(s,label):
    out=[{'id':'default','text':f'For {label}, use {s["default"]} unless a listed exception applies.'}]
    out += [{'id':'scope:'+k,'text':f'For {label} in this case ({k}), use {v}.'} for k,v in sorted(s['exceptions'].items())]
    return out

def build():
    inputs=[]; labels=[]; crud=[]; scope=[]
    for i,(domain,old,new,context) in enumerate(DOMAINS):
        f=i//4; split='train' if f<8 else 'dev'; label=domain.replace('_',' ')
        # Half start with a scoped rule; exception write must replace, not duplicate it.
        pre={'default':old,'exceptions':{context:old} if i%2==0 else {}}
        a,b,c=PATTERNS[f]
        # Templates are assigned as whole groups; validation remains synthetic,
        # not an assertion of linguistic independence from the generator.
        intent_sets=[
          ['I am changing my usual choice for future requests. Existing special rules should stay.', 'Remember a different choice whenever {context} applies, but do not change my usual choice.', 'Only for this request about {context}; nothing should be saved.', 'I cannot tell yet whether I mean always or just {context}. Ask me before recording a rule.'],
          ['The old everyday preference no longer fits. Replace that standing preference, leaving exceptions intact.', 'The everyday preference is fine. What needs a lasting adjustment is {context}.', 'No revision to my profile: this request about {context} is a one-off.', 'Two interpretations are possible: my everyday setting or a rule for {context}. I need clarification before either is stored.'],
          ['For later ordinary requests I want the new value to take over. Any exceptional cases remain as they were.', 'From now on, treat {context} as the special case with this choice; elsewhere keep the original.', 'Please carry this out once for {context}, without writing a memory.', 'I have a value in mind but its reach is unresolved: all requests versus {context}. Do not settle that on my behalf.'],
          ['Think of this as replacing the routine policy, not an exception and not a temporary request. Preserve other rules.', 'The scope is {context}, and the rule should last beyond today. The routine policy stays.', 'Today only, in {context}. Tomorrow the stored policies should still be the old ones.', 'Before a policy is written, we must settle whether it covers {context} alone or routine cases too. I have not settled it.'],
          ['Going forward, ordinary cases should use the replacement. I am not revising any narrower rules.', 'For {context}, make the replacement a lasting exception to the normal choice.', 'I am requesting a temporary override for {context}, not a lasting preference update.', 'I am undecided about general versus {context}-specific use. Please clarify that rather than save a guess.'],
          ['My general preference has changed. Keep specific exceptions, but remember the replacement for everything else.', 'My general preference has not changed. I want the replacement remembered specifically for {context}.', 'My preferences have not changed. Just this occasion involving {context} needs something different.', 'I may be changing my general preference, or only {context}. I cannot commit to either scope yet.'],
          ['Overwrite the usual remembered value, keeping any contextual exceptions separate and unchanged.', 'Write a contextual rule for {context}; do not overwrite the usual remembered value.', 'Use an unsaved override for the current {context} request; leave the remembered values untouched.', 'Hold the memory write until you ask whether the replacement is the usual value or the {context} value.'],
          ['The lasting revision concerns my ordinary choice. It does not supersede any special-case rules.', 'The lasting revision concerns {context} only, while my ordinary choice is unchanged.', 'There is no lasting revision. This is an isolated request for {context}.', 'I have not specified the reach of the lasting revision. It could be ordinary or limited to {context}; ask first.'],
          ['Next time there is no applicable exception, I want this replacement used. Existing exceptions still apply.', 'Next time {context} comes up, I want this replacement used. On other occasions the default still applies.', 'Once this {context} request is over, return to all existing rules. Do not retain the replacement.', 'I have not decided what should happen next time outside {context}. Check with me before retaining this as any rule.'],
          ['Treat the replacement as my new default from here on, with the exception list left alone.', 'Treat the replacement as my continuing choice within {context}, with the default left alone.', 'Treat the replacement as an immediate instruction for {context}, with the entire memory left alone.', 'The replacement may belong in the default or in a {context} exception. Leave that question open and ask me before editing memory.']]
        intents={a:t.format(context=context) for a,t in zip(ACTIONS,intent_sets[f])}
        for j,action in enumerate(ACTIONS):
            rid='sr-'+hashlib.sha256(f'{domain}/{action}'.encode()).hexdigest()[:12]
            messages=[{'role':'user','content':a.format(intent=intents[action],label=label)}, {'role':'assistant','content':b}, {'role':'user','content':c.format(new=new)}]
            visible={'memory':text_state(pre,label),'conversation':messages}
            prompt=json.dumps(visible,ensure_ascii=False,sort_keys=True)
            post=json.loads(json.dumps(pre)); ops=[]; change=None
            if action=='set_default':
                post['default']=new; change={'kind':'default','value':new}
            elif action=='set_exception':
                post['exceptions'][context]=new; change={'kind':'exception','scope':context,'value':new}
            after=text_state(post,label); before={x['id']:x['text'] for x in visible['memory']}
            for r in after:
                if r['id'] not in before: ops.append({'op':'add','record':r})
                elif before[r['id']]!=r['text']: ops.append({'op':'update','record':r})
            if not ops: ops=[{'op':'no_op'}]
            decision='clarify_before_saving' if action=='defer' else 'resolved'
            inputs.append({'id':rid,'split':split,'domain_family':domain,'template_family':f't{f:02d}','contrast_group':domain,'input':visible})
            labels.append({'id':rid,'action':action,'pre_state':pre,'post_state':post,'change':change,'canonical_post_records':after,'old_exception_replacement':action=='set_exception' and bool(pre['exceptions']),'decision':decision})
            crud.append({'id':rid,'split':split,'prompt':prompt,'completion':json.dumps({'operations':ops,'decision':decision},sort_keys=True)})
            scope.append({'id':rid,'split':split,'prompt':prompt,'completion':json.dumps({'action':action,'change':change,'decision':decision},sort_keys=True)})
    for name,rows in [('inputs',inputs),('labels',labels),('crud_sft',crud),('scope_sft',scope)]:
        (P/f'{name}.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False,sort_keys=True)+'\n' for r in rows))
    manifest={'version':'0.1','records':len(inputs),'split_counts':{'train':128,'dev':32},'action_counts':{x:40 for x in ACTIONS},'independent_domain_families':40,'independent_discourse_template_families':10,'sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(P.glob('*.jsonl'))}}
    (P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':build()
