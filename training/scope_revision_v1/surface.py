"""Grounded, context-dependent dialogue realization for the offline v1.1 build.

No label is exposed to an assistant turn. The user's local request supplies
scope and duration; subsequent replies discuss the practical reason for raising
that request. In the matched controls only that earlier request is changed.
Aliases are authored alongside the original catalog, not inferred at runtime.
"""
from functools import lru_cache
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent

@lru_cache(None)
def _aliases(split):
    path = HERE / 'banks' / split / 'aliases.json'
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}


def _entry(scenario, split):
    data = _aliases(split)
    if isinstance(data, list):
        data = {row['attribute']: row for row in data}
    return data.get(scenario['attribute'], {})


def catalog_aliases(scenario, split):
    entry = _entry(scenario, split)
    scopes = entry.get('scopes', scenario['scopes'])
    values = entry.get('options', scenario['options'])
    def many(value):
        return value if isinstance(value, list) else [value]
    scope_aliases = [[v for v in many(alias) if v != canonical]
                     for canonical, alias in zip(scenario['scopes'], scopes)]
    value_aliases = {canonical: [v for v in many(alias) if v != canonical]
                     for canonical, alias in zip(scenario['options'], values)}
    return {'attr_short': entry.get('attr_short', scenario['attribute']),
            'scope_alias': many(scopes[0])[0], 'neighbor_alias': many(scopes[1])[0],
            'scope_aliases': scope_aliases, 'value_aliases': value_aliases}


def prepare_args(scenario, args, split):
    args = dict(args)
    entry = _entry(scenario, split)
    aliases = catalog_aliases(scenario, split)
    args['attr_short'] = entry.get('attr_short', scenario['attribute'])
    args['_scope_forms'] = {canon: [canon] + vals for canon, vals in
                            zip(scenario['scopes'], aliases['scope_aliases'])}
    args['_value_forms'] = {canon: [canon] + aliases['value_aliases'].get(canon, [])
                            for canon in scenario['options']}
    args['_topics'] = entry.get('topics', [args['attr_short']])
    args['_reasons'] = entry.get('reasons', [
        'I want to give the practical details of ' + args['attr_short'] + ' some thought.'])
    args['_scenario'] = scenario
    return args


def pick(rng, pool, **kwargs):
    return rng.choice(pool).format_map(kwargs)


# These are practical questions, not inferred decisions or memory read-backs.
# All can follow any of the six semantic classes, including someone else's
# reported choice or an unresolved target. The topic arguments are specific to
# the attribute being discussed, rather than unrelated diversity padding.
REASON_PROMPTS = {'train': ['What makes {topic} a concern?',
           'Is {topic} what got you thinking about it?',
           'What matters most to you about {topic}?',
           "I'd like to hear a little more about {topic}.",
           'How much of this comes down to {topic}?',
           'What have you noticed about {topic}?',
           'Does {topic} affect how you feel about it?',
           'Tell me a bit about {topic}.',
           'I can see why you brought up {topic}.',
           'What has been bothering you about {topic}?',
           'Is there anything about {topic} I should know?',
           'How does {topic} come into it?',
           'What stands out to you about {topic}?',
           "I'm listening if there's more to say about {topic}.",
           "Is {topic} something you've been running into a lot?",
           'Would it help to talk through {topic}?',
           'That brings us back to {topic}.',
           "What's been on your mind about {topic}?"],
 'dev': ["What's the issue with {topic}, if there is one?",
         'How did you come to notice {topic}?',
         'Does this have much to do with {topic}?',
         'It sounds worth discussing {topic}.',
         'Can you tell me what happened with {topic}?',
         'Do you have a concern about {topic}?',
         "I'd be interested to hear why {topic} matters here.",
         'Say a little more about {topic}, if you like.',
         'Does the way you feel about {topic} explain part of this?',
         'Have you run into trouble with {topic}?',
         'How important is {topic} in practice?',
         'What made {topic} stand out this time?',
         "Let's talk about {topic} for a moment.",
         'Is {topic} mostly a practical concern?',
         "What's the experience been like with {topic}?",
         "I hadn't heard much from you about {topic}.",
         'Do you see {topic} as a big part of it?',
         'Would you mind saying a bit more about {topic}?'],
 'test': ["What's your biggest concern around {topic}?",
          'Is this partly about {topic}?',
          'How did {topic} get on your mind?',
          'I can see how {topic} could make a difference.',
          'Could you say why {topic} matters to you?',
          'Is there a connection with {topic}?',
          'What did you find difficult about {topic}?',
          "I'm curious about {topic}, too.",
          'Have you been noticing anything new about {topic}?',
          'How has {topic} worked out in practice?',
          'What would make {topic} easier to deal with?',
          'Did something in particular draw your attention to {topic}?',
          'I see why this could come up while thinking about {topic}.',
          "What's your impression of {topic} so far?",
          'Is {topic} part of what you want to work out?',
          'Tell me what struck you about {topic}.',
          "There's room to talk more about {topic} if you want.",
          'What do you tend to notice first about {topic}?']}

OPENERS = {'train': ["I've been thinking about {short}. I keep noticing {topic}.",
           'Can we talk about {short}? Something brought it to mind again.',
           'I had a thought about {short} after dealing with {topic}.',
           "{topic_cap} got me thinking. It's about {short}.",
           'I meant to bring up {short} earlier.',
           "Something small: I've been looking again at {short}."],
 'dev': ['Do you have a minute to talk about {short}?',
         "I've been going back and forth on {short}.",
         'I keep coming back to {short} when I think about {topic}.',
         'I was mulling over {short} the other day.',
         'Before I get on with things, can I bring up {short}?',
         'One thing I wanted to mention is {short}.'],
 'test': ['I have something on my mind about {short}.',
          'I remembered something about {short} while thinking about {topic}.',
          'There was one thing about {short} I wanted to talk through.',
          'I thought about {short} again this morning.',
          '{topic_cap} has been on my mind. Can we get back to {short}?',
          "I've got a minute now to explain what I mean about {short}."]}

INVITATIONS = {'train': ["What's on your mind about it?",
           'I can stay with {topic} if that helps.',
           'What would you like to talk through?',
           "Go on; I'm listening.",
           'What made you look at {topic} again?',
           'Was there something you wanted to try?',
           'Say what you were thinking, in your own words.',
           'What part would you like to start with?'],
 'dev': ["Is there a part you'd like to talk about first?",
         'Sure, we can take a moment for {topic}.',
         'What have you been thinking?',
         "I'm here. Tell me anything that seems relevant.",
         'Was there a specific thing about {topic} you wanted to bring up?',
         "Go ahead and say what you're considering.",
         'How would you put it?',
         'What did you want to mention?'],
 'test': ['Of course. We can talk about {topic}.',
          'What would you like to work through first?',
          "I'm listening. What's on your mind?",
          'How have you been thinking about it?',
          'Was something about {topic} especially important?',
          'What did you want me to know?',
          "Feel free to start with whatever's most useful.",
          'Did you want to say what you had in mind?']}

# Directive stems are intentionally reusable for an existing scoped record, a
# new scoped record, and a general record. The preceding state distinguishes
# addition from revision, not a label-specific conversational catchphrase.
DIRECTIVES = {
 'train': [
    'For {where}, I want {new}. {duration}',
    'When it comes to {where}, please use {new}. {duration}',
    'My preference for {where} is {new}. {duration}',
    'I would like {new} when we are dealing with {where}. {duration}',
    'Let us go with {new} for {where}. {duration}',
    'About {where}: {new} is what I would choose. {duration}',
    'The choice I want for {where} is {new}. {duration}',
    'Please make it {new} for {where}. {duration}',
    'What suits me for {where} is {new}. {duration}',
    'If the situation is {where}, use {new}. {duration}',
    'I have settled on {new} for {where}. {duration}',
    'For anything that falls under {where}, I would pick {new}. {duration}',
    'Here is my choice concerning {where}: {new}. {duration}',
    'Remember {new} as my preference for {where}. {duration}',
    'Save {new} as what I want for {where}. {duration}',
    'I want the arrangement for {where} to be {new}. {duration}',
 ],
 'dev': [
    'In the case of {where}, {new} would be my choice. {duration}',
    'The arrangement I am asking for is {new}, for {where}. {duration}',
    'I am choosing {new} in relation to {where}. {duration}',
    'Apply {new} when it is a matter of {where}. {duration}',
    'With {where} in mind, put me down for {new}. {duration}',
    'Concerning {where}, my answer is {new}. {duration}',
    'What I am requesting for {where} is {new}. {duration}',
    'I would select {new} in situations described as {where}. {duration}',
    'My instruction concerning {where} is to use {new}. {duration}',
    'Set the choice for {where} to {new}. {duration}',
    'For {where}, the option that I want is {new}. {duration}',
    'I am asking you to remember {new} for {where}. {duration}',
    'Could you save {new} as my selection for {where}? {duration}',
    'I have reached a decision about {where}: {new}. {duration}',
    'Let {new} be the choice used for {where}. {duration}',
    'Please take {new} as my preference in connection with {where}. {duration}',
 ],
 'test': [
    'Here is where I have landed: {new}, for {where}. {duration}',
    '{new_cap} is the one I want when we are talking about {where}. {duration}',
    'The answer for {where}, as far as I am concerned, is {new}. {duration}',
    'Put {new} against {where} for me. {duration}',
    'Regarding {where}, I am going for {new}. {duration}',
    'Use this choice for {where}: {new}. {duration}',
    'When {where} comes up, my choice is {new}. {duration}',
    'It is {new} that I want for {where}. {duration}',
    'I would put {new} first for {where}. {duration}',
    'Keep {new} in mind as the choice I am making for {where}. {duration}',
    'I am settling the question of {where} with {new}. {duration}',
    'Let the arrangement be {new} when the situation is {where}. {duration}',
    'For {where}, please remember that I choose {new}. {duration}',
    'My request is to save {new} for {where}. {duration}',
    'Given {where}, make the choice {new}. {duration}',
    'The option I am selecting where {where} is concerned is {new}. {duration}',
 ]}

PERSISTENT = {
 'train': [
    'I want that each time from now on.',
    'That is for the next time and the times after it.',
    'Treat it as a continuing preference, not a one-off.',
    'I mean always in that situation, rather than a trial.',
    'There is no planned end to that choice.',
    'Carry that forward whenever those occasions come up.',
    'This is how I want it going forward, without an expiry date.',
    'Keep doing it on later occasions as well.',
    'That is the lasting arrangement I am asking for.',
    'Use it again whenever the same circumstances arise.',
    'It is not temporary; I want to stick with it.',
    'I am making this my standing choice for those occasions.',
 ],
 'dev': [
    'This applies on successive occasions, indefinitely.',
    'I intend this to continue as the normal choice here rather than end after one occasion.',
    'Please carry this preference into future occasions too.',
    'I am asking for an ongoing arrangement without a fixed finish.',
    'This should not be treated as a temporary experiment.',
    'I want this to hold whenever the situation recurs.',
    'The special choice here is meant to remain in place for the longer term.',
    'It is a standing preference for each occasion of this sort, not merely for today.',
    'Future occasions of that sort should use it as well.',
    'There is no expiration intended for this arrangement.',
    'This is always my choice in that situation, not a one-off.',
    'Consider this a lasting request rather than a trial run.',
 ],
 'test': [
    'That goes for the occasions ahead, with no finishing point.',
    'I want to keep coming back to that choice, not try it once.',
    'Leave that as the choice whenever this comes round again.',
    'This is for the long run rather than a temporary spell.',
    'It is meant to last beyond the occasion in front of us.',
    'I am not putting an end date on this preference.',
    'Next time, and after that, I still want this choice.',
    'Keep it in place for recurring occasions of this sort.',
    'I mean an enduring arrangement rather than a one-off.',
    'That is what I always want under those circumstances.',
    'This should carry on; it is not just a test.',
    'Make that the standing arrangement from this point ahead.',
 ]}

OPEN_DURATION = {
 'train': [
    'This is temporary, but use it each time for now; I have no end date.',
    'Keep it for the coming occasions as a stopgap. I do not know when that will finish.',
    'I need it repeatedly for a while, not permanently. The stopping point is still unknown.',
    'For now this applies whenever the situation comes up. It is temporary and I will tell you when to stop.',
    'Treat it as a temporary arrangement over multiple occasions, with the end still open.',
    'I cannot give an end date for this short-term choice; keep using it until I say otherwise.',
    'This is not a one-off or a lasting choice. It continues for the time being, with no finish set.',
    'Until I work out when to stop, use it on those occasions as a provisional arrangement.',
    'I need a temporary run of this choice, not just today; there is no known final day.',
    'Please carry it over to later occasions for the time being. It is a stopgap with no fixed end.',
 ],
 'dev': [
    'The request is provisional and recurring, with no end date available yet.',
    'This is for a temporary stretch of occasions, although I cannot specify its duration.',
    'Use it repeatedly for now, not permanently; I have not established when it ends.',
    'I intend a stopgap over successive occasions, ending when I give further notice.',
    'It should remain in force temporarily until I can say when to stop.',
    'The next few occasions need it, and perhaps more; this is temporary with the finish undecided.',
    'There is no fixed last occasion for this provisional arrangement.',
    'It is neither a one-off nor permanent: use it for now, with the ending left open.',
    'Keep applying it during this temporary period. I do not yet know its final day.',
    'I cannot promise a date when this temporary need will end, so continue in the meantime.',
 ],
 'test': [
    'Only as a stopgap, but on each occasion for now. I cannot name the last day.',
    'This is temporary and recurring; the finishing date is something I still do not know.',
    'Let it run across the coming occasions until I can end this temporary arrangement.',
    'I need it for a while rather than once, and rather than forever. No end is fixed.',
    'For the time being, keep using it. The need is temporary, but its duration is unknown.',
    'There is a temporary need for it whenever this arises; I will let you know when it passes.',
    'Not permanently, and not just this time: it continues provisionally with no closing date.',
    'I have no calendar date for stopping this temporary run of the choice.',
    'This is the temporary arrangement until further notice, including later occasions.',
    'Use it as a recurring stopgap while I work things out; I cannot say when that ends.',
 ]}

WINDOW_DURATION = {
 'train': [
    'Use it from {start} through {end}, including both days, and return to my ordinary choice afterward.',
    'This applies starting {start} and ending after {end}; outside those dates I want my normal choice.',
    'Only the stretch from {start} to {end}, both endpoints included, needs this temporary arrangement.',
    'It is temporary: the first day is {start} and the last is {end}, then use my usual choice again.',
    'The run begins on {start} and includes all of {end}; it does not apply beyond those days.',
    'For the inclusive period {start} to {end}, use this rather than my ordinary choice.',
    'The covered dates are {start} through {end}, including both; nothing outside that interval.',
    'Those occasions between {start} and {end}, including both dates, need it; not the ones outside.',
    'The first included day is {start}, the final included day is {end}; afterward my ordinary choice applies.',
    'Keep this temporary choice for {start} through {end} only, with both dates included.',
 ],
 'dev': [
    'Apply it during {start} through {end}, inclusive; my ordinary preference applies outside that interval.',
    'The arrangement is limited to the dates {start} through {end}, counting both; all other dates use my usual choice.',
    'Its validity begins on {start} and ends when {end} finishes, with the ordinary choice returning afterward.',
    'This is a temporary period beginning {start}, including {end}, but not continuing past it.',
    'Every relevant occasion from {start} to {end}, both days included, should use it and no others.',
    'Use this until the end of {end}, having begun on {start}; outside that span, use my normal preference.',
    'The bounded run covers {start} through {end}, including each endpoint.',
    'It starts with {start} and finishes with {end}; after that, follow my ordinary arrangement again.',
    'Only the inclusive span {start} to {end} is covered by this temporary request.',
    'Take {start} as the first covered date and {end} as the final one, then return to the usual choice.',
 ],
 'test': [
    'The dates are {start} through {end}, with both counted; after that I am back to the ordinary choice.',
    'The interval includes {start} and the whole of {end}, but nothing beyond those dates.',
    'This temporary spell runs from the start of {start} to the end of {end}.',
    'Only occasions in {start} to {end}, with both ends included, get this arrangement.',
    'The request covers {start} and continues through {end}; then my normal preference takes over.',
    'I want it for the full period {start} through {end}, not before or afterward.',
    'Its first day is {start}; {end} is included as the last, and then it is over.',
    'Keep this for the inclusive dates {start} to {end}; outside them use the ordinary choice.',
    'The first included date is {start}; it runs until {end} has finished, then I want the usual arrangement back.',
    'It is a dated exception, beginning {start} and ending with {end}, both included.',
 ]}

ORDINARY = {
 'train': ['ordinary occasions', 'everyday occasions', 'my usual run of occasions',
           'the ordinary case', 'occasions without a separate instruction',
           'the general case rather than a special situation', 'routine occasions',
           'situations where no separate choice applies', 'the everyday case',
           'my default arrangement outside any special cases',
           'the normal run of things', 'my ordinary use'],
 'dev': ['normal occasions without their own arrangement', 'the standard case',
         'ordinary situations in general', 'my overall preference outside separate arrangements',
         'routine cases with no dedicated instruction', 'the usual case in general',
         'my general default rather than an exception',  'an everyday occasion',
         'my everyday use', "requests that don't need a separate choice", 'a regular occurrence with nothing else specified', 'the typical day', 'the normal case altogether', 'regular occasions generally',
         'the baseline case', 'what I normally want'],
 'test': ['the everyday situation', 'the general choice rather than a special case',
          'ordinary occasions overall', 'cases that have no separate preference',
          'normal use in general', 'my usual default outside exceptions',
          'the broad run of ordinary occasions', 'the usual situation',
          'everyday use with no dedicated arrangement', 'routine circumstances',
          'regular occasions without a special choice', 'the general everyday case']}

RETIRES = {
 'train': [
    'Let {scope} follow whatever I generally choose; I do not want a separate arrangement there anymore.',
    'For {scope}, go back to my ordinary preference and keep following it if it changes.',
    'What I normally choose should apply to {scope} too; drop the separate instruction.',
    'I no longer need a special choice for {scope}. Let the ordinary choice handle those occasions now and later.',
    'Please remove the distinct arrangement for {scope}, so those occasions inherit my general preference.',
    'The exception we made for {scope} can end. From here on, use whatever my everyday choice is.',
    'Stop treating {scope} differently. That should use the normal arrangement, including any later changes to it.',
    'I am withdrawing the instruction that singled out {scope}; put those occasions back under my general choice.',
    'The usual choice is enough for {scope}. There should no longer be a separate rule for those occasions.',
    'Forget the special arrangement for {scope}, not my general preference; that is what should apply there again.',
    'Merge {scope} back into the ordinary case. Future changes to my general choice should apply there as well.',
    'No dedicated choice for {scope} anymore, please. Whatever I normally want should carry through there too.',
    'End the separate setup for {scope} and let it take its choice from the general arrangement.',
    'I would rather have {scope} use the default than keep its own arrangement. Remove that separate arrangement.',
    'Treat {scope} just like ordinary occasions from now on, with no special preference of its own.',
    'The distinction for {scope} is no longer wanted. Use the general choice there, even when that changes later.',
 ],
 'dev': [
    'The separate provision for {scope} should be withdrawn, leaving those occasions under my general preference.',
    'I want to discontinue that individual arrangement for {scope}, not replace it with another separate choice.',
    'Put {scope} back under the everyday arrangement; that instruction can end.',
    'The choice for {scope} should track my ordinary preference from now on. Please remove its separate arrangement.',
    'There should be no distinction for {scope} anymore. Apply the general preference whenever those occasions arise.',
    'Let the exception for {scope} lapse now, and have those occasions follow my normal choice thereafter.',
    'I am ending the special treatment of {scope}. Give it the choice I normally make.',
    'For {scope}, the general arrangement is sufficient; remove the distinct choice attached to it.',
    'Cancel the instruction that gives {scope} its own preference and use the general one in its place.',
    'I want {scope} included in the ordinary case, both now and on subsequent occasions.',
    'Return {scope} to the overall default rather than retaining a choice particular to it.',
    'Please let {scope} go the same way as other occasions, even if I change my choice later.',
    'The particular choice associated with {scope} has served its purpose; have the baseline govern future occasions there.',
    'Remove the distinction we made for {scope}, so later changes in my general preference also reach it.',
    'My request is to stop maintaining a separate preference for {scope}. The ordinary one should apply.',
    'Give {scope} the same choice as other occasions, even if I change my mind later.',
 ],
 'test': [
    'That separate choice for {scope} has run its course. Put it back under whatever I generally want.',
    'I am done with having a special arrangement for {scope}; the everyday preference should cover it again.',
    'No more separate treatment for {scope}. Let it follow the general choice now and when that changes.',
    'Take away the choice dedicated to {scope}, leaving the usual arrangement to apply there.',
    'The special case for {scope} can go. I want those occasions to use the ordinary choice from here ahead.',
    'Bring {scope} back into line with my overall preference, rather than keeping a separate one for it.',
    'I want {scope} covered by my general arrangement again, not by an instruction of its own.',
    'The distinction we used for {scope} is over; whatever my usual choice becomes should apply there too.',
    'Drop the exception attached to {scope}. Those occasions should take their preference from the ordinary case.',
    'For {scope}, let the default take over permanently instead of preserving its own separate preference.',
    'Undo the separate arrangement we gave {scope}; my everyday preference is what should govern it again.',
    'There is nothing to keep apart for {scope} anymore. I want it to follow whatever I choose for other occasions.',
    'I do not want a dedicated preference for {scope} now. Fold it into the ordinary arrangement.',
    'The normal choice should cover {scope}, including future changes. I don’t need a different choice for that anymore.',
    'I would like {scope} to stop being an exception and simply follow my general preference.',
    'Let the separate rule for {scope} finish here; use the usual choice for those occasions after this.',
 ]}

UNCERTAIN = {
 'train': [
    '{new_cap} appeals to me, but I have not settled whether I mean {scope} or {neighbor}.',
    'I am thinking of {new}. The unresolved bit is the situation: {scope}, or perhaps {neighbor}.',
    'There is a possible request for {new} here. I cannot yet say whether it concerns {scope} or {neighbor}.',
    'I want to discuss {new}, but the target is still up in the air between {scope} and {neighbor}.',
    'I was thinking of {new}, but it could be for {scope} or {neighbor}. I’m still deciding.',
    'I keep considering {new} for either {scope} or {neighbor}, without having chosen between those situations.',
    'Something involving {new} needs sorting out, but I have not worked out which of {scope} and {neighbor} I mean.',
    'I am not ready to pin this to a situation: it might be {scope}, or it might be {neighbor}. The choice is {new}.',
    'Maybe {new} for {scope}, maybe for {neighbor}. I need help because the intended situation is not settled.',
    'I have a candidate, {new}, and two possible situations, {scope} and {neighbor}; I have not narrowed that down.',
    'The part I cannot answer yet is whether {new} would be for {scope} rather than {neighbor}.',
    'I cannot make a complete request yet. I am considering {new}, with {scope} and {neighbor} both possible targets.',
    'There is still a question about where {new} belongs: {scope} or {neighbor}. I have no answer to that yet.',
    'Before this can be acted on, I need to choose between {scope} and {neighbor} as the target for {new}.',
    'I would like to sort out {new}; I am wavering about applying it to {scope} versus {neighbor}.',
    'I have not settled the situation for {new}. It could be {scope} or, instead, {neighbor}.',
 ],
 'dev': [
    'I am considering {new}, but cannot identify whether the intended situation is {scope} or {neighbor}.',
    'I have {new} in mind. I haven’t decided between {scope} and {neighbor}.',
    'There is an unresolved distinction between {scope} and {neighbor} in what I mean by choosing {new}.',
    'I can name {new} as a possibility, but not yet which situation: {scope} or {neighbor}.',
    'Please do not infer a target for {new}. I am still choosing between {scope} and {neighbor}.',
    'I have not finished deciding where to apply {new}, since both {scope} and {neighbor} are candidates.',
    'My thought about {new} is incomplete: I cannot yet distinguish whether I mean {scope} or {neighbor}.',
    'It is the situation, not the option {new}, that I have left open: {scope} versus {neighbor}.',
    'I need to settle whether {new} concerns {scope} or {neighbor}, and have not done so.',
    'There is no definite target for this thought about {new}. I am weighing {scope} against {neighbor}.',
    'The potential request is {new}, but I remain uncertain which situation it concerns, {scope} or {neighbor}.',
    'I am not in a position to specify whether {new} belongs with {scope} or with {neighbor}.',
    'For {new}, two possible contexts remain on the table: {scope} and {neighbor}. Neither is selected yet.',
    'I have reached the option {new} without resolving its context, which could be {scope} or {neighbor}.',
    'It would be premature to place {new} under either {scope} or {neighbor}; I have not chosen the target.',
    'I am leaving the situation unsettled between {scope} and {neighbor} while we discuss {new}.',
 ],
 'test': [
    'The option is {new}; where it belongs is the bit I have not worked out, {scope} or {neighbor}.',
    'I have got as far as {new}, but not as far as choosing between {scope} and {neighbor}.',
    'It could be {new} for {scope}, or for {neighbor}. I cannot tell you which I intend yet.',
    'I am stuck on the situation for {new}: {scope} and {neighbor} are both still in the running.',
    'Do not put {new} anywhere yet. I have not answered whether it is for {scope} or {neighbor}.',
    'I like the sound of {new}. I’m still weighing {scope} against {neighbor}.',
    'I cannot pin down whether this idea of {new} goes with {scope} or {neighbor}.',
    'The choice sounds like {new}; the situation is still a question between {scope} and {neighbor}.',
    'I have not sorted out the intended setting for {new}. {scope_cap} and {neighbor} are the possibilities.',
    'There is a missing piece before I can ask for {new}: whether I mean {scope} rather than {neighbor}.',
    'I am torn about where {new} should apply, with {scope} on one side and {neighbor} on the other.',
    'The plan involving {new} is not complete. I still need to settle whether it is about {scope} or {neighbor}.',
    'I could be talking about {scope} or {neighbor} when I mention {new}; that part is genuinely undecided.',
    'It is {new} I am considering, without a decision on which situation, {scope} or {neighbor}.',
    'There are two possible homes for {new}, {scope} and {neighbor}, and I have not picked one.',
    'I cannot yet attach {new} to a particular situation: it is between {scope} and {neighbor}.',
 ]}

ONE_OFF = {
 'train': [
    'For this single occasion involving {scope}, I want {new}; later occasions keep the preferences we already had.',
    'Let me use {new} for {scope} just this once, with no change to my standing choices.',
    'This request for {new} is a one-off for the current instance of {scope}, not something to carry forward.',
    'Today I want {new} in the case of {scope}. Once this occasion is over, keep my earlier preferences.',
    'On the particular occasion of {scope} in front of us, use {new}, without changing the ongoing arrangement.',
    'I need a single try of {new} for {scope}; it says nothing new about my later choices.',
    'Only this instance of {scope} needs {new}. My continuing preferences remain as they were.',
    'I would like {new} for the current {scope} request, and not as a new preference for future requests.',
 ],
 'dev': [
    'For the {scope} request we are working on just now, use {new}; leave my earlier preferences in place.',
    'I am requesting {new} on one occasion of {scope}, with no lasting change to my preferences.',
    'This is a one-off use of {new} for {scope}, not an instruction for later occasions.',
    'The current request concerning {scope} needs {new}, but my ongoing choices should not be altered.',
    'Try {new} for this particular {scope} occasion alone, retaining all standing preferences.',
    'I would like one use of {new} for {scope}, without carrying it into future requests.',
    'Use {new} only for the {scope} occasion at hand; keep the earlier arrangement for subsequent ones.',
    'The choice of {new} is confined to this occasion of {scope}, not to my future preference.',
 ],
 'test': [
    'Just for the {scope} occasion in front of me, make it {new}. Nothing about my ongoing choices is changing.',
    'I want one go with {new} for {scope}, then the preferences we already had still apply.',
    'This instance of {scope} gets {new}, but it is a one-off, not the beginning of a different arrangement.',
    'Let this single {scope} request use {new}; do not carry it over to later occasions.',
    'I am asking for {new} this time with {scope}, leaving my established preferences alone.',
    'One occasion of {scope}, one use of {new}. The ongoing arrangement stays as it was.',
    'Only the request at hand for {scope} calls for {new}, with no new preference after it.',
    'For the immediate occasion involving {scope}, I would like {new}, not a standing change.',
 ]}

# Reported or imagined directives retain meaningful overlap with real requests.
# Explicit framing keeps them from authorizing a personal preference update.
FRAMES = {
 'train': {
  'other': [
   'A friend said, "{directive}" I am quoting their preference, not changing mine.',
   'Someone else described their choice like this: "{directive}" That is their request, not one from me.',
   'The line in the story was, "{directive}" It belongs to the character, not to my own preferences.',
   'Here is the remark I was passing along: "{directive}" I am reporting it, not adopting it.',
   'My colleague put their preference this way: "{directive}" My own arrangements are unchanged.',
  ],
  'hypothetical': [
   'Suppose I said, "{directive}" I am only exploring an imaginary choice, not asking for it.',
   'As a thought experiment, imagine this request: "{directive}" Please do not apply it to my real choices.',
   'I am playing with a hypothetical: "{directive}" Nothing about my actual preferences is changing.',
   'In an imagined version of this, I might say, "{directive}" That is not a request for my actual setup.',
   'What if the request were, "{directive}"? This is an example to discuss, not a choice I am making.',
  ],
  'rejected': [
   'I considered saying, "{directive}" But I have decided against it; keep my existing preferences.',
   'The suggestion was, "{directive}" I am rejecting that suggestion, not taking it up.',
   'I had drafted, "{directive}" I do not want to go ahead with it. My earlier choices still stand.',
   'Someone proposed, "{directive}" That does not appeal to me; leave my arrangements alone.',
   'I thought about asking, "{directive}" On reflection, no. I want the preferences I already had.',
  ],
  'reaffirm': [
   'My everyday choice is still {new}; I looked again and do not want to change any of my arrangements.',
   'I still want {new} as my ordinary preference. Nothing new to apply; the existing choices all stand.',
   'After reconsidering {new}, I am staying with it in the ordinary case and keeping my separate choices too.',
   'I checked my usual preference, {new}, and I am still happy with the choices we already have.',
   'No change from me: {new} remains my general choice, and I am not altering any special arrangements.',
  ]},
 'dev': {
  'other': [
   'A visitor expressed their preference as, "{directive}" I am relaying it, not requesting a change for myself.',
   'The statement was made by someone else: "{directive}" My own preferences are not affected.',
   'I read the following in a fictional conversation: "{directive}" It is the speaker\'s choice, not mine.',
   'My acquaintance requested, "{directive}" This is a report of their request rather than an instruction from me.',
   'Someone described what they wanted: "{directive}" I have not adopted their preference.',
  ],
  'hypothetical': [
   'Consider this imaginary instruction: "{directive}" It is not intended to change my real preferences.',
   'For a thought exercise, the request could be, "{directive}" I am not making that request myself.',
   'Hypothetically, I could ask, "{directive}" Please treat it as discussion rather than an actual choice.',
   'Imagine a case in which I said, "{directive}" That case is invented; my preferences remain unchanged.',
   'The purely speculative request is, "{directive}" I do not want it implemented.',
  ],
  'rejected': [
   'I considered the instruction, "{directive}" I have ruled it out and retain my previous preferences.',
   'The proposal was, "{directive}" My answer to that proposal is no; the arrangements stand as they are.',
   'I had entertained the request, "{directive}" I am not proceeding with it.',
   'One suggestion read, "{directive}" I have decided to reject it rather than change my choices.',
   'The option put to me was, "{directive}" I prefer not to take it up; leave the existing choices in place.',
  ],
  'reaffirm': [
   'I have reviewed my general choice of {new} and am confirming it, without changing any other arrangement.',
   'My preferences in general still suit me, including {new} ordinarily; I am not asking for revisions.',
   'I still prefer {new} in the standard case, and all established special arrangements remain as they were.',
   'My review ended where it began: {new} for ordinary occasions, with no changes to the existing preferences.',
   'There is no new request here. I continue to want {new} generally and the separate choices already established.',
  ]},
 'test': {
  'other': [
   'This was somebody else talking: "{directive}" I am recounting their words, not asking you to change my choices.',
   'The person beside me said, "{directive}" That belongs to their preferences, not to mine.',
   'A character in the book asks, "{directive}" I am talking about the book, not adopting the request.',
   'The remark I heard was, "{directive}" It is a secondhand account, not a new preference of my own.',
   'An acquaintance was saying, "{directive}" I am leaving my own arrangements as they are.',
  ],
  'hypothetical': [
   'What if someone said, "{directive}"? I mean an imaginary situation, not an actual request from me.',
   'Picture me asking, "{directive}" This is make-believe; none of my real choices should change.',
   'The imagined version would be, "{directive}" I am not putting that into practice.',
   'Here is a hypothetical to think about: "{directive}" It is not permission to change my preferences.',
   'I could invent a request like, "{directive}" But I am only discussing the idea, not choosing it.',
  ],
  'rejected': [
   'I nearly asked, "{directive}" I have thought better of it. Keep the preferences we already had.',
   'The suggestion went, "{directive}" I am turning it down, not changing my arrangements.',
   'I had been tempted to say, "{directive}" That is not what I want now; leave things as they stand.',
   'One possibility was, "{directive}" I have crossed that off and am sticking with the existing preferences.',
   'I was considering, "{directive}" My decision is against it. Nothing new should be saved from that suggestion.',
  ],
  'reaffirm': [
   'I came back to the same general preference, {new}. The choices I already have still stand.',
   'It is still {new} for the everyday case. I am not changing that or any separate arrangements.',
   'Looking again has left me with {new}, just as before, and no changes to the other choices.',
   'My usual choice of {new} holds up. Everything about my established preferences stays as it was.',
   'Nothing different to request: {new} remains what I want ordinarily, alongside the special choices already there.',
  ]}}

FOLLOWUPS = {'train': [('Is there more to the part about {topic}?',
            'Maybe, but I don’t have more to add right now.'),
           ('Do you want to go into {topic} any further?', 'No, that’s enough detail for now.'),
           ('What else should I keep in mind about {topic}?',
            'I think that covers what I wanted to bring up.'),
           ('We can leave the details of {topic} there for now.',
            'Works for me. I don’t have anything else to add.'),
           ('Was there anything else worth saying about {topic}?',
            'That’s most of what I wanted to talk through.')],
 'dev': [('Is there another side of {topic} you want to get into?',
          'Nothing else springs to mind at the moment.'),
         ('Should we spend any longer on {topic}?', 'I think I’ve said what I meant to say about it.'),
         ('Anything I missed about {topic}?', 'No, I’m happy leaving the conversation there for now.'),
         ('We don’t have to get into all of {topic} in one go.',
          'That’s fine. I didn’t have any other details in mind.'),
         ('Does that cover the part about {topic} you meant to raise?',
          'Yes, at least the part I wanted to get across today.')],
 'test': [('Do you have another thought on {topic}?', 'Not one I can put into words right now.'),
          ('We can leave {topic} there if you like.', 'Let’s do that. That’s all I meant to bring up.'),
          ('Is there anything about {topic} we haven’t touched on?',
           'Nothing I wanted to get into this time.'),
          ('How much more do you want to say about {topic}?', 'Not much more than that, really.'),
          ('Would you prefer to talk more about {topic} another time?',
           'Sure, there’s no need to get into it further right now.')]}


USER_LEADS = {'train': ["I've been thinking about {attr}. ",
           'A thought about {attr}: ',
           'One thing about {attr}. ',
           'Can I mention something about {attr}?'],
 'dev': ['I wanted to talk about {attr}. ',
         "On {attr}, here's what I mean. ",
         "There's something I'd like to bring up about {attr}. ",
         "I've given {attr} some thought."],
 'test': ['Can we get back to {attr}? ',
          "Here's what I meant about {attr}. ",
          'I thought again about {attr}. ',
          'I had a point to make about {attr}.']}

CONTRAST_TURNS = {'train': {'persistent': ["For {scope}, I'm choosing what I want to go with each time it comes up.",
                          "I'd like to settle on something for {scope} that I can keep using."],
           'one_off': ['For {scope}, I just need to choose something for the one we have coming up.',
                       "I'd like to decide what to use on this occasion of {scope}, not commit beyond "
                       'it.',
                       "Let's work out my pick for {scope} today and keep it to the request in front "
                       'of us.',
                       "I need to make today's call about {scope}; I'm not making plans for the next "
                       'one.',
                       'What I pick for {scope} here is just for this particular occasion.',
                       "I'm thinking of {scope} now, not about how I want to do it in the future.",
                       "Could we settle this single choice for {scope}? I won't use it to make up my "
                       'mind for later.',
                       "I've got one occurrence of {scope} to deal with, so that's the one I'm "
                       'choosing for.'],
           'invite': ['Is there a frontrunner for you?',
                      'What would work for you?',
                      'Which one would you go with?'],
           'choose': ["I think I'd pick {new}.", "The one I'd go with is {new}.", 'I want {new}.'],
           'follow': ['Anything else you want to weigh up with {topic}?',
                      "That's enough to talk through for now, if you like."],
           'close': ["No, I've made up my mind.", "I'm comfortable with what I've picked."]},
 'dev': {'persistent': ["I'm looking to settle what I'll use whenever it is a matter of {scope}.",
                        "For {scope}, I'd like to make a choice that still applies on later "
                        'occasions.'],
         'one_off': ["I need a choice for {scope} right now, not for any occasions "
                     'after it.',
                     "For {scope}, I'm deciding what to do this time alone.",
                     "This question is about one upcoming occasion for {scope}; I'm not choosing a "
                     'pattern.',
                     'For {scope}, I would like a pick for today and nothing after today.',
                     "Let's settle the one occasion of {scope} we have here, without committing past "
                     'it.',
                     "I'm just trying to sort out what's coming up for {scope}. How I do it later isn't part "
                     'of this decision.',
                     "I'd like to decide on {scope} for the immediate request, not make a rule for "
                     'myself.',
                     'I only mean the request at hand for {scope}; later occasions are a different '
                     'conversation.',
                     "Picking something right now for {scope} doesn't mean I'm setting up a lasting "
                     'change.',
                     'I have one occasion of {scope} to deal with; that is all I want to choose for.'],
         'invite': ['What are you leaning towards?',
                    'Which option do you feel happy with?',
                    "What do you think you'd pick?"],
         'choose': ["I'd like to go with {new}.",
                    'I feel best about {new}.',
                    'My pick would be {new}.'],
         'follow': ['Is there more you wanted to think through around {topic}?',
                    'We can leave {topic} here for the moment.'],
         'close': ["I think that's as far as I need to go today.", "No, I've settled on it."]},
 'test': {'persistent': ["I want to choose what I'll keep doing for {scope}, not just on the next "
                         'occasion.',
                         'Whatever I decide for {scope} now is what I want to carry forward.'],
          'one_off': ['For {scope}, let me choose something for this one time, and leave the next time '
                      'out of it.',
                      "I need to settle the current choice for {scope}, not what I'll want beyond this "
                      'occasion.',
                      "For the next instance of {scope}, I need to pick something. That's the only one "
                      "I'm thinking about.",
                      "I'm choosing for the {scope} occasion I've got in front of me, not making a "
                      'longer plan.',
                      'We can work out this single occurrence of {scope} without choosing for another '
                      'one.',
                      "For {scope}, what I pick here applies once and then I'm back to what I've been "
                      'doing.',
                      "I want a choice for the present business with {scope}; don't carry the decision "
                      'forward.',
                      "There's one request about {scope} I'm trying to handle, and the choice stops "
                      'there.',
                      'Today is the one occasion for {scope} this choice should affect.',
                      "I'm not picking a lasting arrangement for {scope}; I need something for this "
                      'instance.'],
          'invite': ['What feels right to you?',
                     'Which sounds most like what you want?',
                     "What's the choice you'd make?"],
          'choose': ["I'd choose {new}, I think.", "For me it'd be {new}.", "Let's go with {new}."],
          'follow': ['Are you happy to stop there about {topic}?',
                     'That gives us enough to go on for now.'],
          'close': ["Yes, I don't have anything to add.", "That'll do. I'm happy with my choice."]}}

def _capitalize(text):
    return text[:1].upper() + text[1:]


def _semantic(args, rng, split, action, branch):
    scope = args['scope_surface']
    neighbor = args['neighbor_surface']
    new = args['new_surface']
    fmt = dict(scope=scope, scope_cap=_capitalize(scope), neighbor=neighbor,
               new=new, new_cap=_capitalize(new), start=args['start'], end=args['end'])
    kind = 'persistent' if action in ('general', 'contrast') else args.get('kind', 'persistent')
    if kind == 'window':
        duration = pick(rng, WINDOW_DURATION[split], **fmt)
    elif kind == 'open':
        duration = pick(rng, OPEN_DURATION[split], **fmt)
    else:
        duration = rng.choice(PERSISTENT[split])
    where = rng.choice(ORDINARY[split]) if action == 'general' else scope
    directive = pick(rng, DIRECTIVES[split], where=where, duration=duration, **fmt)
    if action in ('add', 'revise', 'resolve', 'general'):
        # Restrict general requests to ordinary occasions without repealing any
        # situation-specific choices. No declaration of a nonexistent rule.
        if rng.random() < .24:
            preservation = {
                'train': ['I am not changing any other preferences.',
                          'Leave any other choices as they are.',
                          'This does not replace any other arrangements.'],
                'dev': ['Any other preferences should stay in place.',
                        'No changes are intended for the other choices.',
                        'Other arrangements are not part of this request.'],
                'test': ['That does not change the rest of my preferences.',
                         'Anything outside this request keeps the choices it already had.',
                         'Leave the other arrangements alone.']}
            directive += ' ' + rng.choice(preservation[split])
        return directive
    if action == 'retire':
        return pick(rng, RETIRES[split], **fmt)
    if action == 'clarify':
        return pick(rng, UNCERTAIN[split], **fmt)
    if action == 'contrast':
        return directive if branch == 'persistent' else pick(rng, ONE_OFF[split], **fmt)
    if action in ('stable', 'trial'):
        subtype = args.get('_stable_subtype', 'oneoff')
        if subtype == 'oneoff':
            return pick(rng, ONE_OFF[split], **fmt)
        # Non-own, imagined and rejected remarks may concern any kind of
        # preference operation, including dropping an existing distinction.
        # This is semantic counterevidence, not unrelated keyword padding.
        if subtype in ('other', 'hypothetical', 'rejected'):
            frame_kind = rng.randrange(5)
            if frame_kind == 0:
                directive = pick(rng, RETIRES[split], **fmt)
            elif frame_kind == 1:
                directive = pick(rng, UNCERTAIN[split], **fmt)
            elif frame_kind == 2:
                directive = pick(rng, DIRECTIVES[split], where=rng.choice(ORDINARY[split]),
                                 duration=rng.choice(PERSISTENT[split]), **fmt)
        return pick(rng, FRAMES[split][subtype], directive=directive, **fmt)
    raise ValueError('unknown dialogue action: ' + str(action))


def _address_user(text):
    # Author-authored shorthand is in the user's voice. An assistant talking
    # about that same attribute must address the user, not claim it as its own.
    changes = {"I've": "you've", "I'm": "you're", 'I': 'you', 'my': 'your', 'me': 'you'}
    return re.sub(r"\b(?:I've|I'm|I|my|me)\b", lambda match: changes[match.group()], text)


def render(row, args, rng, split, action, branch=None):
    """Return alternating messages and their 1-based decisive user index.

    rng must be episode-local and branch-independent. We reserve every choice
    before rendering a matched branch so suffixes remain byte-identical.
    """
    args = dict(args)
    subtype = str(args.get('stable_key', row.get('template_id', 'oneoff')))
    args['_stable_subtype'] = next((v for v in ('other','hypothetical','rejected','reaffirm')
                                    if v in subtype), 'oneoff')
    value_forms = args.get('_value_forms', {})
    scope_forms = args.get('_scope_forms', {})
    # Full canonical attribute names occur deliberately, but not by default.
    # Every other turn uses a genuinely descriptive phrase authored per scene.
    short = args.get('attr_short', args['attribute'])
    mention = args['attribute'] if rng.random() < .18 else short
    args['scope_surface'] = rng.choice(scope_forms.get(args['scope'], [args['scope']]))
    args['neighbor_surface'] = rng.choice(scope_forms.get(args['neighbor'], [args['neighbor']]))
    args['new_surface'] = rng.choice(value_forms.get(args['new'], [args['new']]))
    topics = args.get('_topics', [short])
    topic = rng.choice(topics)
    other_topic = rng.choice(topics)
    reason_pool = args.get('_reasons', ['The practical side of ' + short + ' matters to me.'])
    reason = _capitalize(reason_pool[0] if rng.random() < .78 else rng.choice(reason_pool))
    if reason[-1:] not in '.!?':
        reason += '.'
    fields = dict(short=short, topic=topic, topic_cap=_capitalize(topic), attr=mention)
    other_fields = dict(short=short, topic=other_topic, topic_cap=_capitalize(other_topic), attr=mention)
    opening = pick(rng, OPENERS[split], **fields)
    assistant_fields = dict(fields, short=_address_user(short))
    invitation = pick(rng, INVITATIONS[split], **assistant_fields)
    question = pick(rng, REASON_PROMPTS[split], **assistant_fields)
    follow_a, follow_u = rng.choice(FOLLOWUPS[split])
    follow_a = follow_a.format_map(dict(other_fields, short=_address_user(short)))
    follow_u = follow_u.format_map(other_fields)
    # Layout variety is decided independently of the class. The matched pair
    # uses the same genuine reason-follow-up sequence with four exact messages.
    layout = rng.choices((0, 1, 2, 3, 4, 5), weights=(27, 29, 14, 8, 15, 7))[0]
    if action == 'contrast':
        layout = 2
    # Reserve a semantic RNG so branch-specific strings cannot alter any later
    # sampling. The outer generator's subsequent events are also unaffected.
    import random
    semantic_rng = random.Random(rng.getrandbits(64))
    semantic = _semantic(args, semantic_rng, split, action, branch)
    # Attribute grounding belongs in the user's request, not in an unrelated
    # extra turn or an assistant announcement of the target memory record.
    lead = pick(rng, USER_LEADS[split], **fields)
    request = lead + ' ' + semantic
    if action == 'contrast':
        # Only the persistence instruction differs. The value is separately
        # chosen on turn five, in the identical suffix of both versions.
        turns = CONTRAST_TURNS[split]
        local = dict(topic=topic, scope=args['scope_surface'], new=args['new_surface'])
        branch_rng = random.Random(rng.getrandbits(64))
        texts = [lead + ' ' + pick(branch_rng, turns[branch], **local), question, reason,
                 pick(rng, turns['invite'], **local), pick(rng, turns['choose'], **local),
                 pick(rng, turns['follow'], **local), pick(rng, turns['close'], **local)]
        evidence = 5
    elif layout == 0:
        texts, evidence = [request, question, reason], 1
    elif layout == 1:
        texts, evidence = [opening, invitation, request, question, reason], 3
    elif layout == 2:
        texts, evidence = [request, question, reason, follow_a, follow_u], 1
    elif layout == 3:
        texts, evidence = [opening, invitation, request, question, reason, follow_a, follow_u], 3
    elif layout == 4:
        texts, evidence = [opening, invitation, request], 3
    else:
        texts, evidence = [opening, question, reason, invitation, request], 5
    return ([{'role': 'user' if i % 2 == 0 else 'assistant', 'content': _capitalize(text)}
             for i, text in enumerate(texts)], evidence)
