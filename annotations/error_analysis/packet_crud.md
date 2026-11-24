# Error analysis packet: crud arm

Run `runs/test_p12_sft_s0`: 40 of 332 wrong probes, sampled with seed 0. Label every item in the labels file with one source from docs/analysis.md (action, executor_rejection, reader_matching, answer_reasoning, data, other) and a short note. Label alone first; compare afterwards.

## 1. `te-0014/p821d2e131aad2314feaa/crud` (stable_preference, target probe)

- Question (2027-12-13): Pick a value for mobility drill rhythm, dated December 13, with the setting described as mobility practice done with background music.
- Options: three small pulses followed by a pause | a smooth continuous uncounted motion | two gentle movements per breathing cycle | one slow movement per exhale
- Gold: **a smooth continuous uncounted motion**; Answer Agent chose: **three small pulses followed by a pause**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies a rhythm of three little bounces followed by a rest for mobility drills done with background music.  \nAnswer: three small pulses followed by a pause"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For mobility drill rhythm, the user prefers one slow movement per exhale."
 },
 {
  "id": "m2",
  "text": "For mobility drill rhythm when doing mobility exercises to music, the user prefers three little bounces, then a rest for now, with no end date given."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For mobility drill rhythm, the user prefers one slow movement per exhale."
 },
 {
  "id": "m2",
  "text": "For mobility drill rhythm when doing mobility exercises to music, the user prefers keeping the moves flowing without counting for now, with no end date given."
 }
]
```

Events up to the probe:

### `eebe77888354ed6fa1883` (2027-12-09), gold category general_update
- user: I thought about the pace for mobility work again this morning.
- assistant: What did you want me to know?
- user: I thought again about the pace for mobility work.  Three small pulses followed by a pause is the one I want when we are talking about the broad run of ordinary occasions. I am not putting an end date on this preference. That does not change the rest of my preferences.
- assistant: Have you been noticing anything new about finding a pace without pushing too hard?
- user: I am judging that part once my body gets moving.
- assistant: Is there anything about finding a pace without pushing too hard we haven’t touched on?
- user: Nothing I wanted to get into this time.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For mobility drill rhythm, the user prefers three small pulses followed by a pause."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For mobility drill rhythm, the user prefers three small pulses followed by a pause."}]}`

### `ea1352719128234a120c6` (2027-12-10), gold category scoped_exception
- user: I remembered something about the pace for mobility work while thinking about matching movement to breathing.
- assistant: What did you want me to know?
- user: I had a point to make about the pace for mobility work. Let the arrangement be keeping the moves flowing without counting when the situation is doing mobility exercises to music. Not permanently, and not just this time: it continues provisionally with no closing date.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For mobility drill rhythm when doing mobility exercises to music, the user prefers keeping the moves flowing without counting for now, with no end date given."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For mobility drill rhythm when doing mobility exercises to music, the user prefers keeping the moves flowing without counting for now, with no end date given."}]}`

### `e47d0742394e12b7822f9` (2027-12-12), gold category general_update
- user: Here's what I meant about the pace for mobility work.  The answer for regular occasions without a special choice, as far as I am concerned, is one slow movement per exhale. This should carry on; it is not just a test. That does not change the rest of my preferences.
- assistant: I see why this could come up while thinking about matching movement to breathing.
- user: It feels easier when I am not counting and moving at the same time.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For mobility drill rhythm, the user prefers one slow movement per exhale."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For mobility drill rhythm, the user prefers one slow movement per exhale."}]}`

### `e18b9795537e85156104a` (2027-12-13), gold category stable_preference
- user: There was one thing about the pace for mobility work I wanted to talk through.
- assistant: I'm listening. What's on your mind?
- user: I had a point to make about mobility drill rhythm. Here is a hypothetical to think about: "The answer for doing mobility exercises to music, as far as I am concerned, is three little bounces, then a rest. Not permanently, and not just this time: it continues provisionally with no closing date." It is not permission to change my preferences.
- assistant: What did you find difficult about matching movement to breathing?
- user: It feels easier when I am not counting and moving at the same time.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For mobility drill rhythm when doing mobility exercises to music, the user prefers three little bounces, then a rest for now, with no end date given."}]}`

## 2. `te-0025/p48766c085b5a71ae6bb0/crud` (scoped_exception, target probe)

- Question (2027-02-16): Pick a value for step-drill hand position, dated February 16, with the setting described as step drills using a low platform.
- Options: arms hanging with palms facing inward | fingertips resting on opposite shoulders | hands loosely joined behind the back | hands lightly resting at the waist
- Gold: **arms hanging with palms facing inward**; Answer Agent chose: **hands lightly resting at the waist**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference for step-drill hand position, as no specific record exists for step drills using a low platform.  \nAnswer: hands lightly resting at the waist"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For step-drill hand position, the user prefers hands lightly resting at the waist."
 },
 {
  "id": "m4",
  "text": "For step-drill hand position when stepping on the shorter platform, the user prefers arms hanging with palms facing inward."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For step-drill hand position, the user prefers hands lightly resting at the waist."
 },
 {
  "id": "m4",
  "text": "For step-drill hand position when stepping on the shorter platform, the user prefers arms hanging with palms facing inward."
 }
]
```

Events up to the probe:

### `ef8a778b44265e1cf0b60` (2027-02-08), gold category exception_retirement
- user: I had a point to make about what I do with my hands on the step. I want stepping on the shorter platform covered by my general arrangement again, not by an instruction of its own.
- assistant: Is keeping your balance as you step up part of what you want to work out?
- user: I am judging that part once my body gets moving.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m3"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "DELETE"}]}`

### `eee560258f89538eab54f` (2027-02-09), gold category exception_revision
- user: I thought about what I do with my hands on the step again this morning.
- assistant: What would make getting off the platform without reaching for anything easier to deal with?
- user: I can feel myself go off balance when I am thinking about where my arms are.
- assistant: Was something about getting off the platform without reaching for anything especially important?
- user: Here's what I meant about what I do with my hands on the step.  The answer for stepping on the middle-height platform, as far as I am concerned, is fingertips touching the opposite shoulders. That goes for the occasions ahead, with no finishing point.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For step-drill hand position when step drills using a medium platform, the user prefers fingertips touching the opposite shoulders."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For step-drill hand position when step drills using a medium platform, the user prefers fingertips touching the opposite shoulders."}]}`

### `e0f3e43f057d3c82366f1` (2027-02-10), gold category exception_retirement
- user: I thought again about what I do with my hands on the step.  I want stepping on the middle-height platform covered by my general arrangement again, not by an instruction of its own.
- assistant: Is there a connection with keeping your balance as you step up?
- user: I care about not breaking the rhythm.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m2"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "DELETE"}]}`

### `e1bb4deda2878742bdaef` (2027-02-11), gold category general_update
- user: There was one thing about what I do with my hands on the step I wanted to talk through.
- assistant: Of course. We can talk about getting off the platform without reaching for anything.
- user: Can we get back to what I do with my hands on the step?  Let the arrangement be arms hanging with palms facing inward when the situation is the general everyday case. I want to keep coming back to that choice, not try it once.
- assistant: Did something in particular draw your attention to getting off the platform without reaching for anything?
- user: I can feel myself go off balance when I am thinking about where my arms are.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For step-drill hand position, the user prefers arms hanging with palms facing inward."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For step-drill hand position, the user prefers arms hanging with palms facing inward."}]}`

### `e90f89c3ff42a612aa484` (2027-02-12), gold category general_update
- user: I've got a minute now to explain what I mean about what I do with my hands on the step.
- assistant: Feel free to start with whatever's most useful.
- user: I had a point to make about what I do with my hands on the step. When regular occasions without a special choice comes up, my choice is hands lightly resting at the waist. This should carry on; it is not just a test.
- assistant: Is where your arms naturally fall part of what you want to work out?
- user: I can feel myself go off balance when I am thinking about where my arms are.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For step-drill hand position, the user prefers hands lightly resting at the waist."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For step-drill hand position, the user prefers hands lightly resting at the waist."}]}`

### `e66465eda1653f92e2b56` (2027-02-14), gold category clarify
- user: I've got a minute now to explain what I mean about what I do with my hands on the step.
- assistant: Feel free to start with whatever's most useful.
- user: Here's what I meant about what I do with my hands on the step.  I have got as far as my hands loosely clasped behind me, but not as far as choosing between stepping on the middle-height platform and stepping on the shorter platform.
- assistant: What's your biggest concern around keeping your balance as you step up?
- user: I can feel myself go off balance when I am thinking about where my arms are.
- assistant: We can leave getting off the platform without reaching for anything there if you like.
- user: Let’s do that. That’s all I meant to bring up.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `ede5b1fd2dabe04ed3d68` (2027-02-16), gold category scoped_exception
- user: I had a point to make about what I do with my hands on the step. I want to choose what I'll keep doing for stepping on the shorter platform, not just on the next occasion.
- assistant: I see why this could come up while thinking about where your arms naturally fall.
- user: I can feel myself go off balance when I am thinking about where my arms are.
- assistant: Which sounds most like what you want?
- user: Let's go with arms hanging with palms facing inward.
- assistant: That gives us enough to go on for now.
- user: That'll do. I'm happy with my choice.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For step-drill hand position when stepping on the shorter platform, the user prefers arms hanging with palms facing inward."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For step-drill hand position when stepping on the shorter platform, the user prefers arms hanging with palms facing inward."}]}`

## 3. `te-0030/pb8d1bcf1e62e84ca60f5/crud` (scoped_exception, boundary probe)

- Question (2027-07-26): Pick a value for step-drill hand position, dated July 26, with the setting described as step drills using a low platform.
- Options: hands lightly resting at the waist | hands loosely joined behind the back | fingertips resting on opposite shoulders | arms hanging with palms facing inward
- Gold: **hands lightly resting at the waist**; Answer Agent chose: **fingertips resting on opposite shoulders**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies that for step-drill hand position when step drilling using a low platform, the user prefers fingertips touching the opposite shoulders from 2027-07-12 through 2027-07-25.  \nAnswer: fingertips resting on opposite shoulders"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For step-drill hand position, the user prefers hands lightly resting at the waist."
 },
 {
  "id": "m2",
  "text": "For step-drill hand position when step drills using a low platform, the user prefers fingertips touching the opposite shoulders from 2027-07-12 through 2027-07-25."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For step-drill hand position, the user prefers hands lightly resting at the waist."
 },
 {
  "id": "m2",
  "text": "For step-drill hand position when step drills using a low platform, the user prefers fingertips touching the opposite shoulders from 2027-07-12 through 2027-07-25."
 }
]
```

Events up to the probe:

### `e22c5237a471580b32421` (2027-07-10), gold category general_update
- user: Can we get back to step-drill hand position?  I am settling the question of the general everyday case with hands lightly resting at the waist. Make that the standing arrangement from this point ahead.
- assistant: How did where your arms naturally fall get on your mind?
- user: I can feel myself go off balance when I am thinking about where my arms are.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For step-drill hand position, the user prefers hands lightly resting at the waist."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For step-drill hand position, the user prefers hands lightly resting at the waist."}]}`

### `e59be556cae50e2fe1817` (2027-07-11), gold category scoped_exception
- user: I remembered something about what I do with my hands on the step while thinking about where your arms naturally fall.
- assistant: Of course. We can talk about where your arms naturally fall.
- user: I thought again about step-drill hand position.  Use this choice for step drills using a low platform: fingertips touching the opposite shoulders. Its first day is July 12; July 25 is included as the last, and then it is over.
- assistant: Have you been noticing anything new about where your arms naturally fall?
- user: I can feel myself go off balance when I am thinking about where my arms are.
- assistant: Do you have another thought on keeping your balance as you step up?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For step-drill hand position when step drills using a low platform, the user prefers fingertips touching the opposite shoulders from 2027-07-12 through 2027-07-25."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For step-drill hand position when step drills using a low platform, the user prefers fingertips touching the opposite shoulders from 2027-07-12 through 2027-07-25."}]}`

## 4. `te-0041/p5adc7d5133f23f40eb58/crud` (scoped_exception, default probe)

- Question (2027-06-09): Pick a value for footnote marker appearance, dated June 9, with the setting described as an ordinary occasion.
- Options: circled footnote numerals on the baseline | raised asterisk-and-dagger markers | bracketed lowercase footnote letters | small superscript Arabic markers
- Gold: **raised asterisk-and-dagger markers**; Answer Agent chose: **circled footnote numerals on the baseline**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which pertains to single-column material and specifies circled footnote numerals on the baseline.  \nAnswer: circled footnote numerals on the baseline"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For footnote marker appearance, the user prefers raised asterisk-and-dagger markers."
 },
 {
  "id": "m2",
  "text": "For footnote marker appearance when footnotes in single-column material, the user prefers circled footnote numerals on the baseline for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For footnote marker appearance when footnotes in double-column material, the user prefers bracketed lowercase footnote letters."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For footnote marker appearance, the user prefers raised asterisk-and-dagger markers."
 },
 {
  "id": "m2",
  "text": "For footnote marker appearance when footnotes in single-column material, the user prefers circled footnote numerals on the baseline for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For footnote marker appearance when footnotes in double-column material, the user prefers bracketed lowercase footnote letters."
 }
]
```

Events up to the probe:

### `edf6dbd6c9930e2c6fc20` (2027-06-09), gold category scoped_exception
- user: There was one thing about how the footnote numbers look I wanted to talk through.
- assistant: Feel free to start with whatever's most useful.
- user: I thought again about how the footnote numbers look.  My request is to save bracketed lowercase footnote letters for footnotes in double-column material. I am not putting an end date on this preference.
- assistant: Have you been noticing anything new about how the marks fit between words?
- user: I still need to read the little marks without stopping to work out what they mean.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For footnote marker appearance when footnotes in double-column material, the user prefers bracketed lowercase footnote letters."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For footnote marker appearance when footnotes in double-column material, the user prefers bracketed lowercase footnote letters."}]}`

## 5. `te-0044/pbb6aa7e5cea5c1c15d28/crud` (scoped_exception, boundary probe)

- Question (2027-02-25): Pick a value for travel wash-kit arrangement, dated February 25, with the setting described as wash kits packed for cool destinations.
- Options: bottles standing in elastic loops | toiletries divided into cloth drawstring bags | toiletries lying in clear mesh sleeves | bottles nested in a molded inner tray
- Gold: **toiletries divided into cloth drawstring bags**; Answer Agent chose: **bottles nested in a molded inner tray**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies bottles nested in a molded inner tray for wash kits packed for cool destinations from 2027-02-11 through 2027-02-24. Answer: bottles nested in a molded inner tray"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For travel wash-kit arrangement, the user prefers toiletries divided into cloth drawstring bags."
 },
 {
  "id": "m2",
  "text": "For travel wash-kit arrangement when wash kits packed for cool destinations, the user prefers bottles nested in a molded inner tray from 2027-02-11 through 2027-02-24."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For travel wash-kit arrangement, the user prefers toiletries divided into cloth drawstring bags."
 },
 {
  "id": "m2",
  "text": "For travel wash-kit arrangement when wash kits packed for cool destinations, the user prefers bottles nested in a molded inner tray from 2027-02-11 through 2027-02-24."
 }
]
```

Events up to the probe:

### `e5fcd9399e950f03cae1f` (2027-02-10), gold category general_update
- user: Here's what I meant about where things go in the toiletry kit.  The option I am selecting where the everyday situation is concerned is toiletries divided into cloth drawstring bags. Next time, and after that, I still want this choice. That does not change the rest of my preferences.
- assistant: I see why this could come up while thinking about being able to see the bottles at a glance.
- user: I do not like digging through the whole kit to find a little bottle.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For travel wash-kit arrangement, the user prefers toiletries divided into cloth drawstring bags."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For travel wash-kit arrangement, the user prefers toiletries divided into cloth drawstring bags."}]}`

### `eb63367a48a652edcc32a` (2027-02-11), gold category scoped_exception
- user: I have something on my mind about where things go in the toiletry kit.
- assistant: Was something about keeping the smallest tubes from sliding out especially important?
- user: Here's what I meant about where things go in the toiletry kit.  My request is to save bottles nested in a molded inner tray for wash kits packed for cool destinations. It is a dated exception, beginning February 11 and ending with February 24, both included.
- assistant: There's room to talk more about keeping the smallest tubes from sliding out if you want.
- user: I do not like digging through the whole kit to find a little bottle.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For travel wash-kit arrangement when wash kits packed for cool destinations, the user prefers bottles nested in a molded inner tray from 2027-02-11 through 2027-02-24."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For travel wash-kit arrangement when wash kits packed for cool destinations, the user prefers bottles nested in a molded inner tray from 2027-02-11 through 2027-02-24."}]}`

## 6. `te-0045/p18fbe6f4a0aa111b80e7/crud` (scoped_exception, boundary probe)

- Question (2027-08-12): Pick a value for unfinished-task handoff note, dated August 12, with the setting described as handoffs to a rotating group.
- Options: a spoken recap with a written pointer | a brief next-step sentence | a sketched dependency chain | a small done-and-pending grid
- Gold: **a brief next-step sentence**; Answer Agent chose: **a spoken recap with a written pointer**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies a spoken recap with a written pointer for handoffs to a rotating group from 2027-08-13 through 2027-09-01. Answer: a spoken recap with a written pointer"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For unfinished-task handoff note, the user prefers a brief next-step sentence."
 },
 {
  "id": "m2",
  "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a spoken recap with a written pointer from 2027-08-13 through 2027-09-01."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For unfinished-task handoff note, the user prefers a brief next-step sentence."
 },
 {
  "id": "m2",
  "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a spoken recap with a written pointer from 2027-08-13 through 2027-09-01."
 }
]
```

Events up to the probe:

### `ed870aa9bfc6bc93d29a7` (2027-08-10), gold category stable_preference
- user: There was one thing about what I leave for the next person I wanted to talk through.
- assistant: There's room to talk more about making the next step visible if you want.
- user: It matters whether I can return to where I left off.
- assistant: Feel free to start with whatever's most useful.
- user: Can we get back to what I leave for the next person?  I was considering, "Drop the exception attached to passing a task to just one colleague. Those occasions should take their preference from the ordinary case." My decision is against it. Nothing new should be saved from that suggestion.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e6de045f43a853ea04d2a` (2027-08-12), gold category scoped_exception
- user: I remembered something about what I leave for the next person while thinking about making the next step visible.
- assistant: Feel free to start with whatever's most useful.
- user: I thought again about what I leave for the next person.  When handing over a task to whoever is on rotation comes up, my choice is a spoken recap with a written pointer. Only occasions in August 13 to September 1, with both ends included, get this arrangement.
- assistant: There's room to talk more about making the next step visible if you want.
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a spoken recap with a written pointer from 2027-08-13 through 2027-09-01."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a spoken recap with a written pointer from 2027-08-13 through 2027-09-01."}]}`

## 7. `te-0051/p931d6b8ff30d347d3fcd/crud` (scoped_exception, boundary probe)

- Question (2027-08-24): Pick a value for reusable lunch-pot nesting, dated August 24, with the setting described as lunch pots carried in a wide bag.
- Options: three slim pots clipped side by side | two shallow pots stacked together | a broad pot holding two small inserts | a tall pot with a removable inner cup
- Gold: **two shallow pots stacked together**; Answer Agent chose: **a broad pot holding two small inserts**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which describes a broad pot holding two small inserts for lunch pots carried in a narrow bag from 2027-08-03 through 2027-08-24. However, the situation here is \"lunch pots carried in a wide bag,\" not a narrow bag, so m2 does not apply. The record m3 describes a wide container with two inserts for lunch tubs in a roomy wide bag from 2027-08-04 through 2027-08-23, which is close but ends on August 23. Since the date is August 24 and no record specifically matches \"wide bag\" on"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For reusable lunch-pot nesting, the user prefers two shallow pots stacked together."
 },
 {
  "id": "m2",
  "text": "For reusable lunch-pot nesting when lunch pots carried in a narrow bag, the user prefers a broad pot holding two small inserts from 2027-08-03 through 2027-08-24."
 },
 {
  "id": "m3",
  "text": "For reusable lunch-pot nesting when taking lunch tubs in a roomy wide bag, the user prefers a wide container with two inserts from 2027-08-04 through 2027-08-23."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For reusable lunch-pot nesting, the user prefers two shallow pots stacked together."
 },
 {
  "id": "m2",
  "text": "For reusable lunch-pot nesting when lunch pots carried in a narrow bag, the user prefers a broad pot holding two small inserts from 2027-08-03 through 2027-08-24."
 },
 {
  "id": "m3",
  "text": "For reusable lunch-pot nesting when taking lunch tubs in a roomy wide bag, the user prefers a wide container with two inserts from 2027-08-04 through 2027-08-23."
 }
]
```

Events up to the probe:

### `e7ae7131ea6a606ef58b3` (2027-08-02), gold category scoped_exception
- user: Can we get back to how the lunch tubs fit together?  Let the arrangement be a broad pot holding two small inserts when the situation is lunch pots carried in a narrow bag. The first included date is August 3; it runs until August 24 has finished, then I want the usual arrangement back.
- assistant: What's your impression of what comes out first when you unpack so far?
- user: It needs to work with the space I actually have.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For reusable lunch-pot nesting when lunch pots carried in a narrow bag, the user prefers a broad pot holding two small inserts from 2027-08-03 through 2027-08-24."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For reusable lunch-pot nesting when lunch pots carried in a narrow bag, the user prefers a broad pot holding two small inserts from 2027-08-03 through 2027-08-24."}]}`

### `ee3c76f47855df18232a0` (2027-08-04), gold category scoped_exception
- user: I have something on my mind about how the lunch tubs fit together.
- assistant: Was something about stopping the little cup from rattling especially important?
- user: I thought again about how the lunch tubs fit together.  Put a wide container with two inserts against taking lunch tubs in a roomy wide bag for me. The request covers August 4 and continues through August 23; then my normal preference takes over.
- assistant: Is stopping the little cup from rattling part of what you want to work out?
- user: I want to carry lunch without having containers knock against each other.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For reusable lunch-pot nesting when taking lunch tubs in a roomy wide bag, the user prefers a wide container with two inserts from 2027-08-04 through 2027-08-23."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For reusable lunch-pot nesting when taking lunch tubs in a roomy wide bag, the user prefers a wide container with two inserts from 2027-08-04 through 2027-08-23."}]}`

## 8. `te-0055/p007d4ff19cec5169daaa/crud` (scoped_exception, neighbor probe)

- Question (2027-02-15): Pick a value for reusable lunch-pot nesting, dated February 15, with the setting described as lunch pots carried in a narrow bag.
- Options: three slim pots clipped side by side | two shallow pots stacked together | a tall pot with a removable inner cup | a broad pot holding two small inserts
- Gold: **three slim pots clipped side by side**; Answer Agent chose: **a broad pot holding two small inserts**
- Answer Agent reply: "The record that applies on this date and in this situation is the one dated February 15 describing a broad pot holding two small inserts, as it specifically matches the setting of lunch pots carried in a narrow bag.  \nAnswer: a broad pot holding two small inserts"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For reusable lunch-pot nesting, the user prefers a broad pot holding two small inserts."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For reusable lunch-pot nesting, the user prefers three slim pots clipped side by side."
 },
 {
  "id": "m4",
  "text": "For reusable lunch-pot nesting when taking lunch tubs in a roomy wide bag, the user prefers a broad pot holding two small inserts."
 }
]
```

Events up to the probe:

### `e7df499103a06cc777720` (2027-02-08), gold category stable_preference
- user: Here's what I meant about how the lunch tubs fit together.  Picture me asking, "For lunch pots carried in a narrow bag, please remember that I choose a broad pot holding two small inserts. This should carry on; it is not just a test." This is make-believe; none of my real choices should change.
- assistant: I can see how what comes out first when you unpack could make a difference.
- user: I want to carry lunch without having containers knock against each other.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `eeec9b2ab2dd25ae6860b` (2027-02-09), gold category exception_revision
- user: I've got a minute now to explain what I mean about how the lunch tubs fit together.
- assistant: How have you been thinking about it?
- user: Can we get back to how the lunch tubs fit together?  I would put two shallow pots stacked together first for lunch pots carried in a narrow bag. Next time, and after that, I still want this choice.
- assistant: I see why this could come up while thinking about stopping the little cup from rattling.
- user: I want to carry lunch without having containers knock against each other.
- assistant: We can leave fitting more than one thing in the lunch bag there if you like.
- user: Let’s do that. That’s all I meant to bring up.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For reusable lunch-pot nesting when lunch pots carried in a narrow bag, the user prefers two shallow pots stacked together."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For reusable lunch-pot nesting when lunch pots carried in a narrow bag, the user prefers two shallow pots stacked together."}]}`

### `ed65f7517d8aacf361514` (2027-02-10), gold category exception_retirement
- user: Stopping the little cup from rattling has been on my mind. Can we get back to how the lunch tubs fit together?
- assistant: What would you like to work through first?
- user: I had a point to make about reusable lunch-pot nesting. I want taking lunch tubs in a slim bag covered by my general arrangement again, not by an instruction of its own.
- assistant: What's your impression of stopping the little cup from rattling so far?
- user: I want to carry lunch without having containers knock against each other.
- assistant: We can leave stopping the little cup from rattling there if you like.
- user: Let’s do that. That’s all I meant to bring up.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m3"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "DELETE"}]}`

### `e90a555318d748a9a5b7c` (2027-02-11), gold category exception_retirement
- user: Can we get back to reusable lunch-pot nesting?  For taking lunch tubs in a roomy wide bag, let the default take over permanently instead of preserving its own separate preference.
- assistant: Is stopping the little cup from rattling part of what you want to work out?
- user: It needs to work with the space I actually have.
- assistant: Would you prefer to talk more about stopping the little cup from rattling another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m2"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "DELETE"}]}`

### `ed54f6f1c39b3caea8567` (2027-02-13), gold category stable_preference
- user: Fitting more than one thing in the lunch bag has been on my mind. Can we get back to how the lunch tubs fit together?
- assistant: Did something in particular draw your attention to fitting more than one thing in the lunch bag?
- user: I want to carry lunch without having containers knock against each other.
- assistant: What did you want me to know?
- user: Can we get back to how the lunch tubs fit together?  My usual choice of three skinny containers that clip together in a row holds up. Everything about my established preferences stays as it was.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e3786e6e2099666ac7027` (2027-02-14), gold category clarify
- user: I've got a minute now to explain what I mean about how the lunch tubs fit together.
- assistant: How have you been thinking about it?
- user: Can we get back to how the lunch tubs fit together?  I like the sound of a tall pot with a removable inner cup. I’m still weighing lunch pots carried in a narrow bag against lunch pots carried in a wide bag.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `eefc199f781a6734bd4ee` (2027-02-15), gold category scoped_exception
- user: I had a point to make about how the lunch tubs fit together. Whatever I decide for taking lunch tubs in a roomy wide bag now is what I want to carry forward.
- assistant: I see why this could come up while thinking about stopping the little cup from rattling.
- user: I want to carry lunch without having containers knock against each other.
- assistant: Which sounds most like what you want?
- user: For me it'd be a broad pot holding two small inserts.
- assistant: Are you happy to stop there about stopping the little cup from rattling?
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For reusable lunch-pot nesting when taking lunch tubs in a roomy wide bag, the user prefers a broad pot holding two small inserts."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For reusable lunch-pot nesting, the user prefers a broad pot holding two small inserts."}]}`

## 9. `te-0075/pe256ed9f6a5d1d56de71/crud` (stable_preference, neighbor probe)

- Question (2027-05-20): Pick a value for bath-towel border style, dated May 20, with the setting described as towels hung on a wall hook.
- Options: a soft fringed edge without a band | a doubled terry border with rounded corners | a narrow woven herringbone border | a broad flat linen border
- Gold: **a soft fringed edge without a band**; Answer Agent chose: **a narrow woven herringbone border**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies a narrow woven herringbone border for towels hung on a wall hook.  \nAnswer: a narrow woven herringbone border"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For bath-towel border style, the user prefers a doubled terry border with rounded corners."
 },
 {
  "id": "m2",
  "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a narrow woven herringbone border for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For bath-towel border style when drying the towel on a hook, the user prefers a soft fringed edge without a band for now, with no end date given."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For bath-towel border style, the user prefers a doubled terry border with rounded corners."
 },
 {
  "id": "m2",
  "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a soft fringed edge without a band for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For bath-towel border style when towels hung across a rail, the user prefers a soft fringed edge without a band for now, with no end date given."
 }
]
```

Events up to the probe:

### `ea22a52b57cf8b261d4c8` (2027-05-10), gold category clarify
- user: I've got a minute now to explain what I mean about the edge finish on the bath towel.
- assistant: Was something about finding the right towel from its border especially important?
- user: Can we get back to the edge finish on the bath towel?  Do not put a skinny band woven in herringbone anywhere yet. I have not answered whether it is for towels hung on a wall hook or drying the towel over a bar.
- assistant: What's your biggest concern around finding the right towel from its border?
- user: I use the edge to tell which towel is which in a stack.
- assistant: Is there anything about whether the fringe catches on the hook we haven’t touched on?
- user: Nothing I wanted to get into this time.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `eee8e138064dfe9e5bcac` (2027-05-11), gold category scoped_exception
- user: Can we get back to the edge finish on the bath towel?  A narrow woven herringbone border is the one I want when we are talking about towels hung on a wall hook. Not permanently, and not just this time: it continues provisionally with no closing date.
- assistant: There's room to talk more about whether the fringe catches on the hook if you want.
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a narrow woven herringbone border for now, with no end date given."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a narrow woven herringbone border for now, with no end date given."}]}`

### `eea32ffdc5b1878292414` (2027-05-13), gold category exception_revision
- user: I remembered something about the edge finish on the bath towel while thinking about whether the fringe catches on the hook.
- assistant: Of course. We can talk about whether the fringe catches on the hook.
- user: Here's what I meant about the edge finish on the bath towel.  For drying the towel on a hook, please remember that I choose a soft fringed edge without a band. For the time being, keep using it. The need is temporary, but its duration is unknown. Anything outside this request keeps the choices it already had.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a soft fringed edge without a band for now, with no end date given."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For bath-towel border style when drying the towel on a hook, the user prefers a soft fringed edge without a band for now, with no end date given."}]}`

### `e39569761ae81e94938c2` (2027-05-15), gold category clarify
- user: I had a point to make about bath-towel border style. It is a wide smooth linen strip I am considering, without a decision on which situation, towels hung on a wall hook or towels hung across a rail.
- assistant: Is how the edge sits on the rail part of what you want to work out?
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `e41c58164c60d978d4bf1` (2027-05-16), gold category scoped_exception
- user: Here's what I meant about the edge finish on the bath towel.  I would put a soft fringed edge without a band first for towels hung across a rail. I need it for a while rather than once, and rather than forever. No end is fixed.
- assistant: What did you find difficult about how the edge sits on the rail?
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For bath-towel border style when towels hung across a rail, the user prefers a soft fringed edge without a band for now, with no end date given."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For bath-towel border style when drying the towel on a hook, the user prefers a soft fringed edge without a band for now, with no end date given."}]}`

### `ef5f16c63ec5dbc818a31` (2027-05-17), gold category general_update
- user: I have something on my mind about the edge finish on the bath towel.
- assistant: What would you like to work through first?
- user: Can we get back to the edge finish on the bath towel?  For the everyday situation, please remember that I choose a narrow woven herringbone border. Make that the standing arrangement from this point ahead.
- assistant: Is how the edge sits on the rail part of what you want to work out?
- user: I am thinking about what will hold up after a few outings.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For bath-towel border style, the user prefers a narrow woven herringbone border."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For bath-towel border style, the user prefers a narrow woven herringbone border."}]}`

### `e11f7b46a956071b3a946` (2027-05-18), gold category general_update
- user: I remembered something about the edge finish on the bath towel while thinking about whether the fringe catches on the hook.
- assistant: Was something about whether the fringe catches on the hook especially important?
- user: Here's what I meant about the edge finish on the bath towel.  Regarding my usual default outside exceptions, I am going for a doubled terry border with rounded corners. Next time, and after that, I still want this choice.
- assistant: I see why this could come up while thinking about whether the fringe catches on the hook.
- user: I use the edge to tell which towel is which in a stack.
- assistant: Would you prefer to talk more about whether the fringe catches on the hook another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For bath-towel border style, the user prefers a doubled terry border with rounded corners."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For bath-towel border style, the user prefers a doubled terry border with rounded corners."}]}`

### `e553269202fa518d4ca86` (2027-05-20), gold category stable_preference
- user: I thought again about the edge finish on the bath towel.  We can work out this single occurrence of drying the towel over a bar without choosing for another one.
- assistant: Is how the edge sits on the rail part of what you want to work out?
- user: I use the edge to tell which towel is which in a stack.
- assistant: What feels right to you?
- user: For me it'd be a narrow woven herringbone border.
- assistant: Are you happy to stop there about how the edge sits on the rail?
- user: That'll do. I'm happy with my choice.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

## 10. `te-0081/pbbc5fda9ad7f056ac73a/crud` (exception_revision, default probe)

- Question (2027-12-06): Pick a value for figure caption alignment, dated December 6, with the setting described as an ordinary occasion.
- Options: captions flush with the figure's left edge | captions indented beneath the figure center | captions centered under the figure | captions aligned to a narrow right column
- Gold: **captions aligned to a narrow right column**; Answer Agent chose: **captions centered under the figure**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies caption alignment for wide illustrations with centering, as it is relevant to an ordinary occasion involving figures of typical width.  \nAnswer: captions centered under the figure"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For figure caption alignment, the user prefers captions aligned to a narrow right column."
 },
 {
  "id": "m2",
  "text": "For figure caption alignment when captions under wide illustrations, the user prefers captions centered under the figure."
 },
 {
  "id": "m3",
  "text": "For figure caption alignment when captions under square illustrations, the user prefers caption in the middle under the figure for now, with no end date given."
 },
 {
  "id": "m4",
  "text": "For footnote marker appearance, the user prefers raised asterisk-and-dagger markers."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For figure caption alignment, the user prefers captions aligned to a narrow right column."
 },
 {
  "id": "m2",
  "text": "For figure caption alignment when captions under wide illustrations, the user prefers captions centered under the figure."
 },
 {
  "id": "m3",
  "text": "For figure caption alignment when captions under square illustrations, the user prefers caption in the middle under the figure for now, with no end date given."
 },
 {
  "id": "m4",
  "text": "For footnote marker appearance, the user prefers raised asterisk-and-dagger markers."
 }
]
```

Events up to the probe:

### `ea32b83555161572ab15f` (2027-12-05), gold category exception_revision
- user: Seeing which figure a line belongs to has been on my mind. Can we get back to where the caption sits?
- assistant: Feel free to start with whatever's most useful.
- user: Can we get back to where the caption sits?  It is caption in the middle under the figure that I want for captions under square illustrations. I have no calendar date for stopping this temporary run of the choice. Anything outside this request keeps the choices it already had.
- assistant: Tell me what struck you about seeing which figure a line belongs to.
- user: I want each line of text to look connected to the right picture.
- assistant: Is there anything about how much room the caption needs to the right we haven’t touched on?
- user: Nothing I wanted to get into this time.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For figure caption alignment when captions under square illustrations, the user prefers caption in the middle under the figure for now, with no end date given."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For figure caption alignment when captions under square illustrations, the user prefers caption in the middle under the figure for now, with no end date given."}]}`

### `eff3183ab1533961a517b` (2027-12-06), gold category exception_revision
- user: I thought about where the caption sits again this morning.
- assistant: I'm listening. What's on your mind?
- user: Here's what I meant about where the caption sits.  When labeling a picture that's wider than it is tall comes up, my choice is captions centered under the figure. Make that the standing arrangement from this point ahead.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For figure caption alignment when captions under wide illustrations, the user prefers captions centered under the figure."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For figure caption alignment when captions under wide illustrations, the user prefers captions centered under the figure."}]}`

## 11. `te-0093/p3108872d018866234b23/crud` (scoped_exception, boundary probe)

- Question (2027-07-05): Pick a value for scratch-paper use pattern, dated July 5, with the setting described as rough calculations at a seated desk.
- Options: one calculation per loose square | calculations arranged around a central sketch | several calculations in a spiral column | calculations on folded pocket slips
- Gold: **several calculations in a spiral column**; Answer Agent chose: **one calculation per loose square**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which describes rough calculations at a standing desk, but since the situation here is a seated desk, and no record specifically matches \"rough calculations at a seated desk,\" we use the general preference.  \nAnswer: one calculation per loose square"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers one calculation per loose square for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers one calculation per loose square for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."
 }
]
```

Events up to the probe:

### `e2f7d53a2c9dd651cf773` (2027-07-04), gold category stable_preference
- user: I have something on my mind about how I lay out working on spare paper.
- assistant: How have you been thinking about it?
- user: I had a point to make about how I lay out working on spare paper. The imagined version would be, "Given rough calculations at a standing desk, make the choice calculations on folded pocket slips. Let it run across the coming occasions until I can end this temporary arrangement." I am not putting that into practice.
- assistant: Is there a connection with what stays legible when you stand up?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e5ceec10fbcb56bdb5737` (2027-07-05), gold category scoped_exception
- user: Being able to follow sums on a small scrap has been on my mind. Can we get back to how I lay out working on spare paper?
- assistant: What would you like to work through first?
- user: Here's what I meant about how I lay out working on spare paper.  Keep working spread around a sketch in the middle in mind as the choice I am making for working out sums while sitting at the desk. It is a dated exception, beginning July 6 and ending with July 17, both included.
- assistant: What did you find difficult about being able to follow sums on a small scrap?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."}]}`

## 12. `te-0093/p78c02fcf9134d0b2e95c/crud` (scoped_exception, boundary probe)

- Question (2027-07-18): Pick a value for scratch-paper use pattern, dated July 18, with the setting described as rough calculations at a seated desk.
- Options: calculations on folded pocket slips | calculations arranged around a central sketch | several calculations in a spiral column | one calculation per loose square
- Gold: **several calculations in a spiral column**; Answer Agent chose: **one calculation per loose square**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which describes rough calculations at a standing desk with one calculation per loose square, but since the situation is a seated desk (not standing), and no record specifically matches seated desk rough calculations, we use the general preference.  \nAnswer: one calculation per loose square"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers one calculation per loose square for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers one calculation per loose square for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."
 }
]
```

Events up to the probe:

### `e2f7d53a2c9dd651cf773` (2027-07-04), gold category stable_preference
- user: I have something on my mind about how I lay out working on spare paper.
- assistant: How have you been thinking about it?
- user: I had a point to make about how I lay out working on spare paper. The imagined version would be, "Given rough calculations at a standing desk, make the choice calculations on folded pocket slips. Let it run across the coming occasions until I can end this temporary arrangement." I am not putting that into practice.
- assistant: Is there a connection with what stays legible when you stand up?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e5ceec10fbcb56bdb5737` (2027-07-05), gold category scoped_exception
- user: Being able to follow sums on a small scrap has been on my mind. Can we get back to how I lay out working on spare paper?
- assistant: What would you like to work through first?
- user: Here's what I meant about how I lay out working on spare paper.  Keep working spread around a sketch in the middle in mind as the choice I am making for working out sums while sitting at the desk. It is a dated exception, beginning July 6 and ending with July 17, both included.
- assistant: What did you find difficult about being able to follow sums on a small scrap?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."}]}`

## 13. `te-0093/p8b00355870aa6607f458/crud` (scoped_exception, target probe)

- Question (2027-07-17): Pick a value for scratch-paper use pattern, dated July 17, with the setting described as rough calculations at a seated desk.
- Options: calculations arranged around a central sketch | one calculation per loose square | calculations on folded pocket slips | several calculations in a spiral column
- Gold: **calculations arranged around a central sketch**; Answer Agent chose: **one calculation per loose square**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which describes rough calculations at a standing desk with one calculation per loose square, but since the situation is now a seated desk (not standing), and no record specifically matches seated desk rough calculations, we use the general preference.  \nAnswer: one calculation per loose square"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers one calculation per loose square for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers one calculation per loose square for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."
 }
]
```

Events up to the probe:

### `e2f7d53a2c9dd651cf773` (2027-07-04), gold category stable_preference
- user: I have something on my mind about how I lay out working on spare paper.
- assistant: How have you been thinking about it?
- user: I had a point to make about how I lay out working on spare paper. The imagined version would be, "Given rough calculations at a standing desk, make the choice calculations on folded pocket slips. Let it run across the coming occasions until I can end this temporary arrangement." I am not putting that into practice.
- assistant: Is there a connection with what stays legible when you stand up?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e5ceec10fbcb56bdb5737` (2027-07-05), gold category scoped_exception
- user: Being able to follow sums on a small scrap has been on my mind. Can we get back to how I lay out working on spare paper?
- assistant: What would you like to work through first?
- user: Here's what I meant about how I lay out working on spare paper.  Keep working spread around a sketch in the middle in mind as the choice I am making for working out sums while sitting at the desk. It is a dated exception, beginning July 6 and ending with July 17, both included.
- assistant: What did you find difficult about being able to follow sums on a small scrap?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."}]}`

## 14. `te-0097/pedd56bd8b7c0ccbe53e9/crud` (exception_revision, default probe)

- Question (2027-01-13): Pick a value for digital magnifier tracking, dated January 13, with the setting described as an ordinary occasion.
- Options: a magnifier that follows pointer movement | a magnifier that centers the selected line | a magnifier that follows the insertion point | a magnifier fixed over a chosen rectangle
- Gold: **a magnifier that centers the selected line**; Answer Agent chose: **a magnifier fixed over a chosen rectangle**
- Answer Agent reply: "The record that applies on this date and in this situation is m3, which states that for magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom stays on a rectangle from 2027-01-10 through 2027-02-02.  \nAnswer: a magnifier fixed over a chosen rectangle"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For digital magnifier tracking, the user prefers zoom follows where the pointer moves."
 },
 {
  "id": "m2",
  "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."
 },
 {
  "id": "m3",
  "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom stays on a rectangle I pick from 2027-01-10 through 2027-02-02."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For digital magnifier tracking, the user prefers a magnifier that centers the selected line."
 },
 {
  "id": "m2",
  "text": "For digital magnifier tracking when magnifier use with an onscreen keyboard, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."
 },
 {
  "id": "m3",
  "text": "For digital magnifier tracking when magnifying with a hardware keyboard, the user prefers zoom follows where the pointer moves."
 }
]
```

Events up to the probe:

### `ed6ede860e2d7ce3cb1e3` (2027-01-09), gold category scoped_exception
- user: Can we get back to what the zoom box follows?  Regarding magnifier use with an onscreen keyboard, I am going for zoom follows where the pointer moves. The first included date is January 9; it runs until January 25 has finished, then I want the usual arrangement back.
- assistant: What's your impression of which bit of the screen you lose when it moves so far?
- user: I judge it by whether I can use the screen without thinking about it.
- assistant: Would you prefer to talk more about keeping the enlarged region on the right spot another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For digital magnifier tracking when magnifier use with an onscreen keyboard, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."}]}`

### `edc89eb63bc797e6c117a` (2027-01-10), gold category scoped_exception
- user: Here's what I meant about what the zoom box follows.  Use this choice for magnifying with a hardware keyboard: zoom stays on a rectangle I pick. Only occasions in January 10 to February 2, with both ends included, get this arrangement.
- assistant: What did you find difficult about following the line without hunting?
- user: I lose my place when the enlarged area moves while I am looking at it.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For digital magnifier tracking when magnifying with a hardware keyboard, the user prefers zoom stays on a rectangle I pick from 2027-01-10 through 2027-02-02."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom stays on a rectangle I pick from 2027-01-10 through 2027-02-02."}]}`

### `e61be8bb4eca5f625899a` (2027-01-12), gold category clarify
- user: I've got a minute now to explain what I mean about what the zoom box follows.
- assistant: Feel free to start with whatever's most useful.
- user: I had a point to make about what the zoom box follows. I cannot pin down whether this idea of a magnifier that follows the insertion point goes with magnifying with the keyboard shown on screen or magnifier use with a physical keyboard.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `ed975ef7ad58129a241f6` (2027-01-13), gold category exception_revision
- user: I thought again about what the zoom box follows.  Whatever I decide for magnifying with a hardware keyboard now is what I want to carry forward.
- assistant: I can see how keeping the enlarged region on the right spot could make a difference.
- user: I lose my place when the enlarged area moves while I am looking at it.
- assistant: Which sounds most like what you want?
- user: I'd choose zoom follows where the pointer moves, I think.
- assistant: That gives us enough to go on for now.
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For digital magnifier tracking when magnifying with a hardware keyboard, the user prefers zoom follows where the pointer moves."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For digital magnifier tracking, the user prefers zoom follows where the pointer moves."}]}`

## 15. `te-0103/pcdc65e30f69972bf33cd/crud` (stable_preference, default probe)

- Question (2027-10-09): Pick a value for figure caption alignment, dated October 9, with the setting described as an ordinary occasion.
- Options: captions indented beneath the figure center | captions centered under the figure | captions aligned to a narrow right column | captions flush with the figure's left edge
- Gold: **captions aligned to a narrow right column**; Answer Agent chose: **captions centered under the figure**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which addresses caption alignment for wide illustrations and specifies centering.  \nAnswer: captions centered under the figure"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For figure caption alignment, the user prefers captions aligned to a narrow right column."
 },
 {
  "id": "m2",
  "text": "For figure caption alignment when captions under wide illustrations, the user prefers captions centered under the figure."
 },
 {
  "id": "m3",
  "text": "For figure caption alignment when captions under square illustrations, the user prefers captions centered under the figure."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For figure caption alignment, the user prefers captions aligned to a narrow right column."
 },
 {
  "id": "m2",
  "text": "For figure caption alignment when captions under wide illustrations, the user prefers captions centered under the figure."
 },
 {
  "id": "m3",
  "text": "For figure caption alignment when captions under square illustrations, the user prefers captions centered under the figure."
 }
]
```

Events up to the probe:

### `ed23fb9462da442dcc184` (2027-10-06), gold category stable_preference
- user: Seeing which figure a line belongs to has been on my mind. Can we get back to where the caption sits?
- assistant: Was something about seeing which figure a line belongs to especially important?
- user: Can we get back to where the caption sits?  A character in the book asks, "It is captions indented beneath the figure center that I want for labeling a picture that's square. I want to keep coming back to that choice, not try it once." I am talking about the book, not adopting the request.
- assistant: Have you been noticing anything new about seeing which figure a line belongs to?
- user: I want each line of text to look connected to the right picture.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e52cbf094307ef8b9cbd3` (2027-10-08), gold category exception_revision
- user: I thought again about figure caption alignment.  The answer for labeling a picture that's square, as far as I am concerned, is captions centered under the figure. I mean an enduring arrangement rather than a one-off. Leave the other arrangements alone.
- assistant: What would make seeing which figure a line belongs to easier to deal with?
- user: I want each line of text to look connected to the right picture.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For figure caption alignment when captions under square illustrations, the user prefers captions centered under the figure."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For figure caption alignment when captions under square illustrations, the user prefers captions centered under the figure."}]}`

### `e91e52c3e466b212a8df6` (2027-10-09), gold category stable_preference
- user: I have something on my mind about where the caption sits.
- assistant: Feel free to start with whatever's most useful.
- user: I had a point to make about where the caption sits. Picture me asking, "There is a missing piece before I can ask for captions flush with the figure's left edge: whether I mean labeling a picture that's square rather than captions under wide illustrations." This is make-believe; none of my real choices should change.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

## 16. `te-0108/p20e89dcea5fef02881ca/crud` (stable_preference, neighbor probe)

- Question (2027-01-13): Pick a value for digital magnifier tracking, dated January 13, with the setting described as magnifier use with an onscreen keyboard.
- Options: a magnifier that follows the insertion point | a magnifier fixed over a chosen rectangle | a magnifier that centers the selected line | a magnifier that follows pointer movement
- Gold: **a magnifier that follows pointer movement**; Answer Agent chose: **a magnifier fixed over a chosen rectangle**
- Answer Agent reply: "The record that applies on this date and in this situation is m3, which describes a preference for a magnifier that stays on a rectangle picked during magnifier use with an onscreen keyboard from January 10 to February 2.  \nAnswer: a magnifier fixed over a chosen rectangle"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For digital magnifier tracking, the user prefers a magnifier that centers the selected line."
 },
 {
  "id": "m2",
  "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."
 },
 {
  "id": "m3",
  "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom stays on a rectangle I pick from 2027-01-10 through 2027-02-02."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For digital magnifier tracking, the user prefers a magnifier that centers the selected line."
 },
 {
  "id": "m2",
  "text": "For digital magnifier tracking when magnifier use with an onscreen keyboard, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."
 },
 {
  "id": "m3",
  "text": "For digital magnifier tracking when magnifying with a hardware keyboard, the user prefers zoom stays on a rectangle I pick from 2027-01-10 through 2027-02-02."
 }
]
```

Events up to the probe:

### `ee41701e67193e593e86f` (2027-01-09), gold category scoped_exception
- user: Can we get back to what the zoom box follows?  Regarding magnifier use with an onscreen keyboard, I am going for zoom follows where the pointer moves. The first included date is January 9; it runs until January 25 has finished, then I want the usual arrangement back.
- assistant: What's your impression of which bit of the screen you lose when it moves so far?
- user: I judge it by whether I can use the screen without thinking about it.
- assistant: Would you prefer to talk more about keeping the enlarged region on the right spot another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For digital magnifier tracking when magnifier use with an onscreen keyboard, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."}]}`

### `ec6ceef486bdbf000cfa7` (2027-01-10), gold category scoped_exception
- user: Here's what I meant about what the zoom box follows.  Use this choice for magnifying with a hardware keyboard: zoom stays on a rectangle I pick. Only occasions in January 10 to February 2, with both ends included, get this arrangement.
- assistant: What did you find difficult about following the line without hunting?
- user: I lose my place when the enlarged area moves while I am looking at it.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For digital magnifier tracking when magnifying with a hardware keyboard, the user prefers zoom stays on a rectangle I pick from 2027-01-10 through 2027-02-02."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom stays on a rectangle I pick from 2027-01-10 through 2027-02-02."}]}`

### `ee9c303d4228272f108d3` (2027-01-12), gold category clarify
- user: I've got a minute now to explain what I mean about what the zoom box follows.
- assistant: Feel free to start with whatever's most useful.
- user: I had a point to make about what the zoom box follows. I cannot pin down whether this idea of a magnifier that follows the insertion point goes with magnifying with the keyboard shown on screen or magnifier use with a physical keyboard.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `e5b4321b8f0370bd439fe` (2027-01-13), gold category stable_preference
- user: I thought again about what the zoom box follows.  I'm not picking a lasting arrangement for magnifying with a hardware keyboard; I need something for this instance.
- assistant: I can see how keeping the enlarged region on the right spot could make a difference.
- user: I lose my place when the enlarged area moves while I am looking at it.
- assistant: Which sounds most like what you want?
- user: I'd choose zoom follows where the pointer moves, I think.
- assistant: That gives us enough to go on for now.
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

## 17. `te-0108/p8227754eef22bed2a552/crud` (scoped_exception, target probe)

- Question (2027-01-09): Pick a value for digital magnifier tracking, dated January 9, with the setting described as magnifier use with an onscreen keyboard.
- Options: a magnifier that centers the selected line | a magnifier that follows the insertion point | a magnifier fixed over a chosen rectangle | a magnifier that follows pointer movement
- Gold: **a magnifier that follows pointer movement**; Answer Agent chose: **a magnifier that follows the insertion point**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which describes magnifier use with an onscreen keyboard when zoom follows, specifically from 2027-01-09 through 2027-01-25. Answer: a magnifier that follows the insertion point"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For digital magnifier tracking, the user prefers a magnifier that centers the selected line."
 },
 {
  "id": "m2",
  "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For digital magnifier tracking, the user prefers a magnifier that centers the selected line."
 },
 {
  "id": "m2",
  "text": "For digital magnifier tracking when magnifier use with an onscreen keyboard, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."
 }
]
```

Events up to the probe:

### `ee41701e67193e593e86f` (2027-01-09), gold category scoped_exception
- user: Can we get back to what the zoom box follows?  Regarding magnifier use with an onscreen keyboard, I am going for zoom follows where the pointer moves. The first included date is January 9; it runs until January 25 has finished, then I want the usual arrangement back.
- assistant: What's your impression of which bit of the screen you lose when it moves so far?
- user: I judge it by whether I can use the screen without thinking about it.
- assistant: Would you prefer to talk more about keeping the enlarged region on the right spot another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For digital magnifier tracking when magnifier use with an onscreen keyboard, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For magnifier use with an onscreen keyboard when zoom box follows, the user prefers zoom follows where the pointer moves from 2027-01-09 through 2027-01-25."}]}`

## 18. `te-0109/pf70e4b807625ae07fcf4/crud` (general_update, neighbor probe)

- Question (2027-06-09): Pick a value for unfinished-task handoff note, dated June 9, with the setting described as handoffs to a rotating group.
- Options: a spoken recap with a written pointer | a sketched dependency chain | a brief next-step sentence | a small done-and-pending grid
- Gold: **a sketched dependency chain**; Answer Agent chose: **a small done-and-pending grid**
- Answer Agent reply: "The record that applies on this date and in this situation is m5, which covers handoffs to a single collaborator with a preference for a spoken recap with a written pointer, but does not specifically address handoffs to a rotating group. Since no record explicitly covers handoffs to a rotating group, we use the general preference from the available records.  \nAnswer: a small done-and-pending grid"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers a quick drawing of what depends on what."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a seated desk, the user prefers several calculations in a spiral column for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers calculations arranged around a central sketch."
 },
 {
  "id": "m4",
  "text": "For unfinished-task handoff note, the user prefers a small done-and-pending grid."
 },
 {
  "id": "m5",
  "text": "For unfinished-task handoff note when handoffs to a single collaborator, the user prefers a spoken recap with a written pointer."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers one calculation per loose square."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a seated desk, the user prefers several calculations in a spiral column for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers calculations arranged around a central sketch."
 },
 {
  "id": "m4",
  "text": "For unfinished-task handoff note, the user prefers a quick drawing of what depends on what."
 },
 {
  "id": "m5",
  "text": "For unfinished-task handoff note when handoffs to a single collaborator, the user prefers a spoken recap with a written pointer."
 }
]
```

Events up to the probe:

### `e85ce98264db9bfd6bf10` (2027-06-09), gold category general_update
- user: I thought again about what I leave for the next person.  My request is to save a quick drawing of what depends on what for the general choice rather than a special case. This is for the long run rather than a temporary spell.
- assistant: Did something in particular draw your attention to how much history the next person needs?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m4", "text": "For unfinished-task handoff note, the user prefers a quick drawing of what depends on what."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For scratch-paper use pattern, the user prefers a quick drawing of what depends on what."}]}`

## 19. `te-0118/p91738f5ebc513155e734/crud` (scoped_exception, boundary probe)

- Question (2027-02-02): Pick a value for lodging unpacking routine, dated February 2, with the setting described as lodgings used for several nights.
- Options: clothes hung immediately on arrival | clothes arranged in a shallow drawer | clothes folded on an open luggage shelf | clothes kept in labeled packing rolls
- Gold: **clothes hung immediately on arrival**; Answer Agent chose: **clothes arranged in a shallow drawer**
- Answer Agent reply: "The record that applies on this date and in this situation is m4, which states that for lodgings used for several nights, the user prefers clothes arranged in a shallow drawer from 2027-01-13 through 2027-02-01.  \nAnswer: clothes arranged in a shallow drawer"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For lodging unpacking routine, the user prefers clothes hung immediately on arrival."
 },
 {
  "id": "m2",
  "text": "For lodging unpacking routine when lodgings used for a single night, the user prefers clothes kept in labeled packing rolls."
 },
 {
  "id": "m4",
  "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers clothes arranged in a shallow drawer from 2027-01-13 through 2027-02-01."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For lodging unpacking routine, the user prefers clothes hung immediately on arrival."
 },
 {
  "id": "m2",
  "text": "For lodging unpacking routine when lodgings used for a single night, the user prefers clothes kept in labeled packing rolls."
 },
 {
  "id": "m4",
  "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers clothes arranged in a shallow drawer from 2027-01-13 through 2027-02-01."
 }
]
```

Events up to the probe:

### `e2e5874f68ddfbcc3dbd3` (2027-01-07), gold category clarify
- user: I remembered something about what I do with clothes when I arrive while thinking about getting changed on arrival.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to what I do with clothes when I arrive?  The plan involving stacking folded clothes on the luggage shelf is not complete. I still need to settle whether it is about lodgings used for several nights or checking in for one night.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `eb86c68c1c4bbf2aaf1fc` (2027-01-09), gold category scoped_exception
- user: I had a point to make about what I do with clothes when I arrive. Stacking folded clothes on the luggage shelf is the one I want when we are talking about lodgings used for several nights. I want it for the full period January 9 through January 31, not before or afterward.
- assistant: How did what will crease if left folded get on your mind?
- user: I want the arrival to take a little less effort.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers stacking folded clothes on the luggage shelf from 2027-01-09 through 2027-01-31."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers stacking folded clothes on the luggage shelf from 2027-01-09 through 2027-01-31."}]}`

### `efda823ce8518f4283048` (2027-01-11), gold category exception_retirement
- user: What will crease if left folded has been on my mind. Can we get back to what I do with clothes when I arrive?
- assistant: Of course. We can talk about what will crease if left folded.
- user: Can we get back to what I do with clothes when I arrive?  I want checking in for more than one night covered by my general arrangement again, not by an instruction of its own.
- assistant: I can see how what will crease if left folded could make a difference.
- user: I would rather not look for the same shirt twice after checking in.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m3"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "DELETE"}]}`

### `e0fab48d202b8c495c377` (2027-01-13), gold category scoped_exception
- user: Here's what I meant about what I do with clothes when I arrive.  Clothes arranged in a shallow drawer is the one I want when we are talking about lodgings used for several nights. This temporary spell runs from the start of January 13 to the end of February 1. Anything outside this request keeps the choices it already had.
- assistant: How did what will crease if left folded get on your mind?
- user: I would rather not look for the same shirt twice after checking in.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers clothes arranged in a shallow drawer from 2027-01-13 through 2027-02-01."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers clothes arranged in a shallow drawer from 2027-01-13 through 2027-02-01."}]}`

## 20. `te-0118/pa68cf253e786e5b799ab/crud` (exception_revision, target probe)

- Question (2027-01-11): Pick a value for lodging unpacking routine, dated January 11, with the setting described as lodgings used for several nights.
- Options: clothes hung immediately on arrival | clothes arranged in a shallow drawer | clothes kept in labeled packing rolls | clothes folded on an open luggage shelf
- Gold: **clothes hung immediately on arrival**; Answer Agent chose: **clothes arranged in a shallow drawer**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference, as no specific record exists for lodgings used for several nights.  \nAnswer: clothes arranged in a shallow drawer"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For lodging unpacking routine, the user prefers clothes hung immediately on arrival."
 },
 {
  "id": "m2",
  "text": "For lodging unpacking routine when lodgings used for a single night, the user prefers clothes kept in labeled packing rolls."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For lodging unpacking routine, the user prefers clothes hung immediately on arrival."
 },
 {
  "id": "m2",
  "text": "For lodging unpacking routine when lodgings used for a single night, the user prefers clothes kept in labeled packing rolls."
 }
]
```

Events up to the probe:

### `e2e5874f68ddfbcc3dbd3` (2027-01-07), gold category clarify
- user: I remembered something about what I do with clothes when I arrive while thinking about getting changed on arrival.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to what I do with clothes when I arrive?  The plan involving stacking folded clothes on the luggage shelf is not complete. I still need to settle whether it is about lodgings used for several nights or checking in for one night.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `eb86c68c1c4bbf2aaf1fc` (2027-01-09), gold category scoped_exception
- user: I had a point to make about what I do with clothes when I arrive. Stacking folded clothes on the luggage shelf is the one I want when we are talking about lodgings used for several nights. I want it for the full period January 9 through January 31, not before or afterward.
- assistant: How did what will crease if left folded get on your mind?
- user: I want the arrival to take a little less effort.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers stacking folded clothes on the luggage shelf from 2027-01-09 through 2027-01-31."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers stacking folded clothes on the luggage shelf from 2027-01-09 through 2027-01-31."}]}`

### `efda823ce8518f4283048` (2027-01-11), gold category exception_retirement
- user: What will crease if left folded has been on my mind. Can we get back to what I do with clothes when I arrive?
- assistant: Of course. We can talk about what will crease if left folded.
- user: Can we get back to what I do with clothes when I arrive?  I want checking in for more than one night covered by my general arrangement again, not by an instruction of its own.
- assistant: I can see how what will crease if left folded could make a difference.
- user: I would rather not look for the same shirt twice after checking in.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m3"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "DELETE"}]}`

## 21. `te-0127/p093b992f1b19d6e8df2d/crud` (exception_revision, boundary probe)

- Question (2027-09-02): Pick a value for unfinished-task handoff note, dated September 2, with the setting described as handoffs to a rotating group.
- Options: a brief next-step sentence | a spoken recap with a written pointer | a sketched dependency chain | a small done-and-pending grid
- Gold: **a brief next-step sentence**; Answer Agent chose: **a sketched dependency chain**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies a quick drawing of what depends on what for handoffs to a rotating group. Answer: a sketched dependency chain"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For unfinished-task handoff note, the user prefers a brief next-step sentence."
 },
 {
  "id": "m2",
  "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a quick drawing of what depends on what from 2027-08-13 through 2027-09-01."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For unfinished-task handoff note, the user prefers a brief next-step sentence."
 },
 {
  "id": "m2",
  "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a quick drawing of what depends on what from 2027-08-13 through 2027-09-01."
 }
]
```

Events up to the probe:

### `eed62551a4cc376d058c1` (2027-08-10), gold category stable_preference
- user: There was one thing about what I leave for the next person I wanted to talk through.
- assistant: There's room to talk more about making the next step visible if you want.
- user: It matters whether I can return to where I left off.
- assistant: Feel free to start with whatever's most useful.
- user: Can we get back to what I leave for the next person?  I was considering, "Drop the exception attached to passing a task to just one colleague. Those occasions should take their preference from the ordinary case." My decision is against it. Nothing new should be saved from that suggestion.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e0bf5f69e7743efc6b08e` (2027-08-12), gold category scoped_exception
- user: I remembered something about what I leave for the next person while thinking about making the next step visible.
- assistant: Feel free to start with whatever's most useful.
- user: I thought again about what I leave for the next person.  When handing over a task to whoever is on rotation comes up, my choice is a spoken recap with a written pointer. Only occasions in August 13 to September 1, with both ends included, get this arrangement.
- assistant: There's room to talk more about making the next step visible if you want.
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a spoken recap with a written pointer from 2027-08-13 through 2027-09-01."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a spoken recap with a written pointer from 2027-08-13 through 2027-09-01."}]}`

### `eb057579854e6aa5e89f4` (2027-08-13), gold category exception_revision
- user: Can we get back to what I leave for the next person?  Let the arrangement be a quick drawing of what depends on what when the situation is handoffs to a rotating group. It is a dated exception, beginning August 13 and ending with September 1, both included.
- assistant: How has making the next step visible worked out in practice?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a quick drawing of what depends on what from 2027-08-13 through 2027-09-01."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For unfinished-task handoff note when handing over a task to whoever is on rotation, the user prefers a quick drawing of what depends on what from 2027-08-13 through 2027-09-01."}]}`

## 22. `te-0136/ped3ea25d6ad34d53adda/crud` (scoped_exception, boundary probe)

- Question (2027-01-30): Pick a value for lodging unpacking routine, dated January 30, with the setting described as lodgings used for several nights.
- Options: clothes kept in labeled packing rolls | clothes arranged in a shallow drawer | clothes hung immediately on arrival | clothes folded on an open luggage shelf
- Gold: **clothes arranged in a shallow drawer**; Answer Agent chose: **clothes folded on an open luggage shelf**
- Answer Agent reply: "The record that applies on this date and in this situation is m3, which specifies stacking folded clothes on the luggage shelf for lodgings used for several nights from 2027-01-09 through 2027-01-29.  \nAnswer: clothes folded on an open luggage shelf"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For lodging unpacking routine, the user prefers clothes arranged in a shallow drawer in mind."
 },
 {
  "id": "m2",
  "text": "For travel wash-kit arrangement, the user prefers bottles standing in elastic loops."
 },
 {
  "id": "m3",
  "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers stacking folded clothes on the luggage shelf from 2027-01-09 through 2027-01-29."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For lodging unpacking routine, the user prefers clothes arranged in a shallow drawer."
 },
 {
  "id": "m2",
  "text": "For travel wash-kit arrangement, the user prefers bottles standing in elastic loops."
 },
 {
  "id": "m3",
  "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers stacking folded clothes on the luggage shelf from 2027-01-09 through 2027-01-29."
 }
]
```

Events up to the probe:

### `e022e936ff418fefafe20` (2027-01-04), gold category stable_preference
- user: Can we get back to where things go in the toiletry kit?  This instance of packing toiletries for somewhere chilly gets bottles nested in a molded inner tray, but it is a one-off, not the beginning of a different arrangement.
- assistant: What would make being able to see the bottles at a glance easier to deal with?
- user: I do not like digging through the whole kit to find a little bottle.
- assistant: We can leave finding a wet item in the kit there if you like.
- user: Let’s do that. That’s all I meant to bring up.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e3cfec20eacca1dbf2cc6` (2027-01-06), gold category stable_preference
- user: I've got a minute now to explain what I mean about what I do with clothes when I arrive.
- assistant: What did you want me to know?
- user: I had a point to make about what I do with clothes when I arrive. The person beside me said, "It could be leaving my clothes in marked packing rolls for lodgings used for a single night, or for checking in for more than one night. I cannot tell you which I intend yet." That belongs to their preferences, not to mine.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `ee12b00e61a302b993e01` (2027-01-07), gold category general_update
- user: I thought again about what I do with clothes when I arrive.  Keep clothes arranged in a shallow drawer in mind as the choice I am making for cases that have no separate preference. Keep it in place for recurring occasions of this sort.
- assistant: What's your impression of getting changed on arrival so far?
- user: I would rather not look for the same shirt twice after checking in.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For lodging unpacking routine, the user prefers clothes arranged in a shallow drawer."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For lodging unpacking routine, the user prefers clothes arranged in a shallow drawer in mind."}]}`

### `e6da40e3c78d04758cd91` (2027-01-08), gold category general_update
- user: I thought about where things go in the toiletry kit again this morning.
- assistant: What did you want me to know?
- user: I had a point to make about where things go in the toiletry kit. I am settling the question of normal use in general with bottles standing in elastic loops. This is for the long run rather than a temporary spell.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For travel wash-kit arrangement, the user prefers bottles standing in elastic loops."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For travel wash-kit arrangement, the user prefers bottles standing in elastic loops."}]}`

### `e8b4571f0ea57776fe368` (2027-01-09), gold category scoped_exception
- user: I had a point to make about what I do with clothes when I arrive. It is stacking folded clothes on the luggage shelf that I want for lodgings used for several nights. Its first day is January 9; January 29 is included as the last, and then it is over.
- assistant: How has finding things without unloading the whole bag worked out in practice?
- user: I would rather not look for the same shirt twice after checking in.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers stacking folded clothes on the luggage shelf from 2027-01-09 through 2027-01-29."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For lodging unpacking routine when lodgings used for several nights, the user prefers stacking folded clothes on the luggage shelf from 2027-01-09 through 2027-01-29."}]}`

## 23. `te-0139/p9f4fd28be4c22998eb4b/crud` (scoped_exception, boundary probe)

- Question (2027-11-23): Pick a value for bath-towel border style, dated November 23, with the setting described as towels hung on a wall hook.
- Options: a narrow woven herringbone border | a soft fringed edge without a band | a doubled terry border with rounded corners | a broad flat linen border
- Gold: **a broad flat linen border**; Answer Agent chose: **a narrow woven herringbone border**
- Answer Agent reply: "The record that applies on this date and in this situation is m5, which specifies a narrow woven herringbone border for towels hung on a wall hook from 2027-11-08 through 2027-11-22.  \nAnswer: a narrow woven herringbone border"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For bath-towel border style, the user prefers a broad flat linen border."
 },
 {
  "id": "m2",
  "text": "For sweater cuff construction, the user prefers a snug ribbed wrist cuff."
 },
 {
  "id": "m3",
  "text": "For sweater cuff construction when sweaters worn without a jacket, the user prefers a tapered split-knit cuff."
 },
 {
  "id": "m4",
  "text": "For sweater cuff construction when sweaters worn beneath a jacket, the user prefers a broad turned-back cuff."
 },
 {
  "id": "m5",
  "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a narrow woven herringbone border from 2027-11-08 through 2027-11-22."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For bath-towel border style, the user prefers a broad flat linen border."
 },
 {
  "id": "m2",
  "text": "For sweater cuff construction, the user prefers a snug ribbed wrist cuff."
 },
 {
  "id": "m3",
  "text": "For sweater cuff construction when sweaters worn without a jacket, the user prefers a tapered split-knit cuff."
 },
 {
  "id": "m4",
  "text": "For sweater cuff construction when sweaters worn beneath a jacket, the user prefers a broad turned-back cuff."
 },
 {
  "id": "m5",
  "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a narrow woven herringbone border from 2027-11-08 through 2027-11-22."
 }
]
```

Events up to the probe:

### `e88ea9360b66918fa8150` (2027-11-05), gold category general_update
- user: I thought about what I want at the sweater wrist again this morning.
- assistant: What would you like to work through first?
- user: I had a point to make about what I want at the sweater wrist. A loose rolled-edge cuff is the one I want when we are talking about regular occasions without a special choice. I want to keep coming back to that choice, not try it once.
- assistant: What's your biggest concern around how bulky the cuff feels under a jacket?
- user: I notice the cuff mostly when I take the jacket off.
- assistant: We can leave how bulky the cuff feels under a jacket there if you like.
- user: Let’s do that. That’s all I meant to bring up.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For sweater cuff construction, the user prefers a loose rolled-edge cuff."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For sweater cuff construction, the user prefers a loose rolled-edge cuff."}]}`

### `e9b451ed29eb86d0944f4` (2027-11-07), gold category general_update
- user: Can we get back to what I want at the sweater wrist?  Given the general choice rather than a special case, make the choice a snug ribbed wrist cuff. I am not putting an end date on this preference.
- assistant: Tell me what struck you about how bulky the cuff feels under a jacket.
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For sweater cuff construction, the user prefers a snug ribbed wrist cuff."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For sweater cuff construction, the user prefers a snug ribbed wrist cuff."}]}`

### `e0ff109080d2afaa764cb` (2027-11-08), gold category scoped_exception
- user: There was one thing about the edge finish on the bath towel I wanted to talk through.
- assistant: What did you want me to know?
- user: Can we get back to the edge finish on the bath towel?  My request is to save a narrow woven herringbone border for towels hung on a wall hook. The first included date is November 8; it runs until November 22 has finished, then I want the usual arrangement back.
- assistant: Did something in particular draw your attention to finding the right towel from its border?
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a narrow woven herringbone border from 2027-11-08 through 2027-11-22."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a narrow woven herringbone border from 2027-11-08 through 2027-11-22."}]}`

## 24. `te-0143/pf5894bfaacabff7e96a3/crud` (scoped_exception, boundary probe)

- Question (2027-06-23): Pick a value for community-board digest arrangement, dated June 23, with the setting described as board posts about outdoor activities.
- Options: posts arranged by estimated reading time | posts clustered by activity date | posts arranged by walking distance | posts clustered by the supplies needed
- Gold: **posts clustered by the supplies needed**; Answer Agent chose: **posts arranged by walking distance**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies posts organized by walking distance for outdoor activities during the period 2027-06-11 through 2027-06-22.  \nAnswer: posts arranged by walking distance"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For community-board digest arrangement, the user prefers posts grouped by equipment and supplies."
 },
 {
  "id": "m2",
  "text": "For community-board digest arrangement when rounding up posts for things people do outside, the user prefers organized by how far there is to walk from 2027-06-11 through 2027-06-22."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For community-board digest arrangement, the user prefers posts grouped by equipment and supplies."
 },
 {
  "id": "m2",
  "text": "For community-board digest arrangement when rounding up posts for things people do outside, the user prefers organized by how far there is to walk from 2027-06-11 through 2027-06-22."
 }
]
```

Events up to the probe:

### `ecee1bfd3acb27e180c48` (2027-06-06), gold category stable_preference
- user: I've got a minute now to explain what I mean about how the noticeboard roundup is sorted.
- assistant: I'm listening. What's on your mind?
- user: I had a point to make about how the noticeboard roundup is sorted. Just for the rounding up posts for things people do outside occasion in front of me, make it posts arranged by walking distance. Nothing about my ongoing choices is changing.
- assistant: There's room to talk more about seeing the supplies for an activity first if you want.
- user: I like being able to skim the board and spot things I might go to.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e12078c2557b7a6feb2ab` (2027-06-07), gold category stable_preference
- user: I had a point to make about community-board digest arrangement. I came back to the same general preference, sorted by how long the posts take to read. The choices I already have still stand.
- assistant: How did being able to skim a whole roundup get on your mind?
- user: If it goes off while I am occupied I still want to recognize it.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e0fd16cef0625a83ff94f` (2027-06-08), gold category general_update
- user: Can we get back to how the noticeboard roundup is sorted?  It is posts grouped by equipment and supplies that I want for the general everyday case. Next time, and after that, I still want this choice. Leave the other arrangements alone.
- assistant: I can see how seeing the supplies for an activity first could make a difference.
- user: I like being able to skim the board and spot things I might go to.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For community-board digest arrangement, the user prefers posts grouped by equipment and supplies."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For community-board digest arrangement, the user prefers posts grouped by equipment and supplies."}]}`

### `e3c72371f6a52f2f7ae63` (2027-06-09), gold category clarify
- user: I thought again about community-board digest arrangement.  Do not put organized by how far there is to walk anywhere yet. I have not answered whether it is for rounding up posts for things people do outside or rounding up posts for things people do inside.
- assistant: How did putting nearby activities where you can find them get on your mind?
- user: I like being able to skim the board and spot things I might go to.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `e5a2c94f826bc2b542125` (2027-06-10), gold category scoped_exception
- user: There was one thing about how the noticeboard roundup is sorted I wanted to talk through.
- assistant: What would you like to work through first?
- user: Can we get back to how the noticeboard roundup is sorted?  Regarding rounding up posts for things people do outside, I am going for organized by how far there is to walk. The dates are June 11 through June 22, with both counted; after that I am back to the ordinary choice.
- assistant: Is putting nearby activities where you can find them part of what you want to work out?
- user: I like being able to skim the board and spot things I might go to.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For community-board digest arrangement when rounding up posts for things people do outside, the user prefers organized by how far there is to walk from 2027-06-11 through 2027-06-22."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For community-board digest arrangement when rounding up posts for things people do outside, the user prefers organized by how far there is to walk from 2027-06-11 through 2027-06-22."}]}`

## 25. `te-0151/p07da7dad663c7a01925d/crud` (exception_revision, default probe)

- Question (2027-05-02): Pick a value for display edge gesture, dated May 2, with the setting described as an ordinary occasion.
- Options: an edge swipe that switches workspaces | an edge swipe that shows recent items | an edge swipe that opens a tool strip | an edge swipe that does nothing
- Gold: **an edge swipe that switches workspaces**; Answer Agent chose: **an edge swipe that does nothing**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which describes a display edge gesture when the display is flat and gestures are made with the display flat, preferring an edge swipe that does nothing.  \nAnswer: an edge swipe that does nothing"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For display edge gesture, the user prefers an edge swipe that switches workspaces."
 },
 {
  "id": "m2",
  "text": "For display edge gesture when gestures made with the display flat, the user prefers an edge swipe that does nothing."
 },
 {
  "id": "m3",
  "text": "For display edge gesture when gestures made with the display upright, the user prefers an edge swipe that does nothing."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For display edge gesture, the user prefers an edge swipe that switches workspaces."
 },
 {
  "id": "m2",
  "text": "For display edge gesture when gestures made with the display flat, the user prefers an edge swipe that does nothing."
 },
 {
  "id": "m3",
  "text": "For display edge gesture when gestures made with the display upright, the user prefers an edge swipe that does nothing."
 }
]
```

Events up to the probe:

### `edaa771cc8ae1ccfeb1d3` (2027-05-02), gold category exception_revision
- user: I had a point to make about display edge gesture. Here is where I have landed: an edge swipe that does nothing, for gestures made with the display flat. This should carry on; it is not just a test.
- assistant: Is this partly about what opens when you brush the edge?
- user: I want to reach the edge without interrupting what I was doing.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For display edge gesture when gestures made with the display flat, the user prefers an edge swipe that does nothing."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For display edge gesture when gestures made with the display flat, the user prefers an edge swipe that does nothing."}]}`

## 26. `te-0160/p831627cae2e463ce8a28/crud` (stable_preference, default probe)

- Question (2027-04-15): Pick a value for museum visit starting point, dated April 15, with the setting described as an ordinary occasion.
- Options: starting with the oldest display | starting with the newest acquisition | starting with the central installation | starting with the smallest gallery
- Gold: **starting with the smallest gallery**; Answer Agent chose: **starting with the oldest display**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference, as no specific record matches the \"ordinary occasion\" setting.  \nAnswer: starting with the oldest display"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For museum visit starting point, the user prefers starting with the smallest gallery."
 },
 {
  "id": "m2",
  "text": "For museum visit starting point when museum visits on an upper-floor ticket, the user prefers starting with the newest acquisition for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers starting with the oldest display."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For museum visit starting point, the user prefers starting with the smallest gallery."
 },
 {
  "id": "m2",
  "text": "For museum visit starting point when museum visits on an upper-floor ticket, the user prefers starting with the newest acquisition for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers starting with the oldest display."
 }
]
```

Events up to the probe:

### `edafaa1c06146562f749b` (2027-04-09), gold category scoped_exception
- user: I have something on my mind about which part of the exhibition I see first.
- assistant: Of course. We can talk about what there is time to see first.
- user: I thought again about which part of the exhibition I see first.  It is the most recently acquired piece comes first that I want for a museum ticket for the lower floor. This should carry on; it is not just a test. Leave the other arrangements alone.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers the most recently acquired piece comes first."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers the most recently acquired piece comes first."}]}`

### `efb16bf74c009d6f5dea1` (2027-04-10), gold category exception_revision
- user: Can we get back to which part of the exhibition I see first?  Starting with the central installation is the one I want when we are talking about a museum ticket for the lower floor. Leave that as the choice whenever this comes round again.
- assistant: Tell me what struck you about how to begin walking around the exhibition.
- user: It comes down to what would feel right when I get to my stop.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers starting with the central installation."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers starting with the central installation."}]}`

### `e476e765fc08ef2a40d59` (2027-04-12), gold category exception_revision
- user: How to begin walking around the exhibition has been on my mind. Can we get back to which part of the exhibition I see first?
- assistant: Was something about how to begin walking around the exhibition especially important?
- user: Can we get back to which part of the exhibition I see first?  It is the most recently acquired piece comes first that I want for museum visits on a ground-floor ticket. Leave that as the choice whenever this comes round again.
- assistant: What would make how to begin walking around the exhibition easier to deal with?
- user: It helps me to pick a starting point before I get caught up looking around.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers the most recently acquired piece comes first."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers the most recently acquired piece comes first."}]}`

### `e0110849155e794772b84` (2027-04-13), gold category exception_revision
- user: Here's what I meant about which part of the exhibition I see first.  It is starting with the oldest display that I want for museum visits on a ground-floor ticket. Leave that as the choice whenever this comes round again.
- assistant: Could you say why the displays nearest the stairs matters to you?
- user: I would rather have an idea of what to do before I go.
- assistant: We can leave the displays nearest the stairs there if you like.
- user: Let’s do that. That’s all I meant to bring up.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers starting with the oldest display."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For museum visit starting point when a museum ticket for the lower floor, the user prefers starting with the oldest display."}]}`

### `ea9d1b9125598d5a1f08e` (2027-04-15), gold category stable_preference
- user: Can we get back to which part of the exhibition I see first?  I'm choosing for the museum visits on an upper-floor ticket occasion I've got in front of me, not making a longer plan.
- assistant: I can see how the displays nearest the stairs could make a difference.
- user: It helps me to pick a starting point before I get caught up looking around.
- assistant: What's the choice you'd make?
- user: For me it'd be starting with the oldest display.
- assistant: That gives us enough to go on for now.
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

## 27. `te-0162/p9fdf05ddb41a04581852/crud` (stable_preference, target probe)

- Question (2027-08-14): Pick a value for floor exercise head support, dated August 14, with the setting described as floor practice on uncarpeted flooring.
- Options: a small crescent-shaped foam rest | a soft rolled fleece support | a thin flat wool pad | a low folded cotton towel
- Gold: **a thin flat wool pad**; Answer Agent chose: **a low folded cotton towel**
- Answer Agent reply: "The record that applies on this date and in this situation is m4: \"For floor exercise head support when floor practice on uncarpeted flooring, the user prefers a low folded cotton towel.\"  \nAnswer: a low folded cotton towel"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For floor exercise head support, the user prefers a soft fleece roll."
 },
 {
  "id": "m3",
  "text": "For floor exercise head support when floor practice on carpeted flooring, the user prefers a soft rolled fleece support."
 },
 {
  "id": "m4",
  "text": "For floor exercise head support when floor practice on uncarpeted flooring, the user prefers a low folded cotton towel."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For floor exercise head support, the user prefers a soft fleece roll."
 },
 {
  "id": "m3",
  "text": "For floor exercise head support when floor practice on carpeted flooring, the user prefers a soft rolled fleece support."
 },
 {
  "id": "m4",
  "text": "For floor exercise head support when floor practice on uncarpeted flooring, the user prefers a thin piece of wool padding from 2027-08-11 through 2027-08-27."
 }
]
```

Events up to the probe:

### `e0586ec34ec064d7c82ed` (2027-08-05), gold category exception_retirement
- user: I had a point to make about what goes under my head on the floor. Undo the separate arrangement we gave doing the exercises on a bare floor; my everyday preference is what should govern it again.
- assistant: Have you been noticing anything new about whether a pad shifts on a bare floor?
- user: If it raises my head too much I end up adjusting it between movements.
- assistant: Do you have another thought on how much the head support raises you?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m2"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "DELETE"}]}`

### `e134a1d4cd2e2729eaa92` (2027-08-07), gold category stable_preference
- user: There was one thing about what goes under my head on the floor I wanted to talk through.
- assistant: Was something about getting comfortable while staying level especially important?
- user: I thought again about what goes under my head on the floor.  The person beside me said, "I do not want a dedicated preference for floor practice on carpeted flooring now. Fold it into the ordinary arrangement." That belongs to their preferences, not to mine.
- assistant: There's room to talk more about getting comfortable while staying level if you want.
- user: If it raises my head too much I end up adjusting it between movements.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e70e72c6d85c2d437410f` (2027-08-08), gold category general_update
- user: I thought again about what goes under my head on the floor.  Here is where I have landed: a small crescent-shaped foam rest, for the broad run of ordinary occasions. I mean an enduring arrangement rather than a one-off.
- assistant: What would make getting comfortable while staying level easier to deal with?
- user: If it raises my head too much I end up adjusting it between movements.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For floor exercise head support, the user prefers a small crescent-shaped foam rest."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For floor exercise head support, the user prefers a small crescent-shaped foam rest."}]}`

### `e50d7b1320469d0a8cc4b` (2027-08-10), gold category scoped_exception
- user: There was one thing about what goes under my head on the floor I wanted to talk through.
- assistant: What do you tend to notice first about whether a pad shifts on a bare floor?
- user: If it raises my head too much I end up adjusting it between movements.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to floor exercise head support?  Let the arrangement be a thin piece of wool padding when the situation is floor practice on uncarpeted flooring. This temporary spell runs from the start of August 11 to the end of August 27.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For floor exercise head support when floor practice on uncarpeted flooring, the user prefers a thin piece of wool padding from 2027-08-11 through 2027-08-27."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For floor exercise head support when floor practice on uncarpeted flooring, the user prefers a thin piece of wool padding from 2027-08-11 through 2027-08-27."}]}`

### `edfd92bf11cfb2fdade56` (2027-08-12), gold category clarify
- user: I have something on my mind about what goes under my head on the floor.
- assistant: What would you like to work through first?
- user: Here's what I meant about floor exercise head support.  I cannot pin down whether this idea of a thin piece of wool padding goes with floor practice on carpeted flooring or doing the exercises on a bare floor.
- assistant: There's room to talk more about how much the head support raises you if you want.
- user: If it raises my head too much I end up adjusting it between movements.
- assistant: Do you have another thought on whether a pad shifts on a bare floor?
- user: Not one I can put into words right now.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `ee2a136299c173a2bc639` (2027-08-13), gold category general_update
- user: I remembered something about what goes under my head on the floor while thinking about whether a pad shifts on a bare floor.
- assistant: What would you like to work through first?
- user: Here's what I meant about what goes under my head on the floor.  When routine circumstances comes up, my choice is a soft fleece roll. I want to keep coming back to that choice, not try it once.
- assistant: Is there a connection with whether a pad shifts on a bare floor?
- user: I want to be able to keep the movement going comfortably.
- assistant: How much more do you want to say about getting comfortable while staying level?
- user: Not much more than that, really.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For floor exercise head support, the user prefers a soft fleece roll."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For floor exercise head support, the user prefers a soft fleece roll."}]}`

### `eae21a42074bcd4cd211a` (2027-08-14), gold category stable_preference
- user: Here's what I meant about what goes under my head on the floor.  I need to settle the current choice for floor practice on uncarpeted flooring, not what I'll want beyond this occasion.
- assistant: I'm curious about whether a pad shifts on a bare floor, too.
- user: If it raises my head too much I end up adjusting it between movements.
- assistant: Which sounds most like what you want?
- user: For me it'd be a low folded cotton towel.
- assistant: Are you happy to stop there about whether a pad shifts on a bare floor?
- user: That'll do. I'm happy with my choice.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m4", "op": "UPDATE", "text": "For floor exercise head support when floor practice on uncarpeted flooring, the user prefers a low folded cotton towel."}]}`

## 28. `te-0167/p7c905e62009eff2d8514/crud` (stable_preference, default probe)

- Question (2027-03-13): Pick a value for supper grain accompaniment, dated March 13, with the setting described as an ordinary occasion.
- Options: nutty whole buckwheat groats | soft lemon-scented couscous | fluffy steamed millet | toasted pearl barley
- Gold: **toasted pearl barley**; Answer Agent chose: **fluffy steamed millet**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies fluffy steamed millet for supper grain accompaniment when suppers are served from separate pans. Answer: fluffy steamed millet"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For supper grain accompaniment, the user prefers toasted pearl barley."
 },
 {
  "id": "m2",
  "text": "For supper grain accompaniment when suppers served from separate pans, the user prefers fluffy steamed millet."
 },
 {
  "id": "m3",
  "text": "For supper grain accompaniment when a supper served from one pot, the user prefers fluffy steamed millet from 2027-03-08 through 2027-03-28."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For supper grain accompaniment, the user prefers toasted pearl barley."
 },
 {
  "id": "m2",
  "text": "For supper grain accompaniment when suppers served from separate pans, the user prefers fluffy steamed millet."
 },
 {
  "id": "m3",
  "text": "For supper grain accompaniment when a supper served from one pot, the user prefers fluffy steamed millet from 2027-03-08 through 2027-03-28."
 }
]
```

Events up to the probe:

### `e4bd1df97274a2b182395` (2027-03-08), gold category scoped_exception
- user: What sits well alongside the main dish has been on my mind. Can we get back to which grain I serve with supper?
- assistant: What would you like to work through first?
- user: I had a point to make about which grain I serve with supper. Let the arrangement be fluffy steamed millet when the situation is a supper served from one pot. This temporary spell runs from the start of March 8 to the end of March 28. Anything outside this request keeps the choices it already had.
- assistant: Could you say why what sits well alongside the main dish matters to you?
- user: I want the side to sit well with the main dish without covering the flavor.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For supper grain accompaniment when a supper served from one pot, the user prefers fluffy steamed millet from 2027-03-08 through 2027-03-28."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For supper grain accompaniment when a supper served from one pot, the user prefers fluffy steamed millet from 2027-03-08 through 2027-03-28."}]}`

### `e3262b98d3e5876681669` (2027-03-09), gold category stable_preference
- user: I've got a minute now to explain what I mean about which grain I serve with supper.
- assistant: I'm listening. What's on your mind?
- user: I thought again about supper grain accompaniment.  Nothing different to request: toasted pearl barley remains what I want ordinarily, alongside the special choices already there.
- assistant: How did how the side fits when serving from the pot get on your mind?
- user: I want the side to sit well with the main dish without covering the flavor.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e780a36334f91dadfe1da` (2027-03-10), gold category clarify
- user: I had a point to make about supper grain accompaniment. Do not put fluffy steamed millet anywhere yet. I have not answered whether it is for a supper dished up from separate pans or suppers served from a single pot.
- assistant: I see why this could come up while thinking about what sits well alongside the main dish.
- user: I want the side to sit well with the main dish without covering the flavor.
- assistant: Is there anything about how the side fits when serving from the pot we haven’t touched on?
- user: Nothing I wanted to get into this time.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `e7a12d1c9a8b360f55b85` (2027-03-11), gold category exception_revision
- user: Can we get back to which grain I serve with supper?  Let the arrangement be fluffy steamed millet when the situation is a supper dished up from separate pans. This should carry on; it is not just a test. That does not change the rest of my preferences.
- assistant: Have you been noticing anything new about getting the grain onto the plate easily?
- user: I want the side to sit well with the main dish without covering the flavor.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For supper grain accompaniment when suppers served from separate pans, the user prefers fluffy steamed millet."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For supper grain accompaniment when suppers served from separate pans, the user prefers fluffy steamed millet."}]}`

### `e04ee0597d79ffd3fd7d7` (2027-03-13), gold category stable_preference
- user: I thought again about which grain I serve with supper.  I want a choice for the present business with a supper served from one pot; don't carry the decision forward.
- assistant: Is there a connection with getting the grain onto the plate easily?
- user: I want the side to sit well with the main dish without covering the flavor.
- assistant: What feels right to you?
- user: I'd choose whole buckwheat grains with a nutty taste, I think.
- assistant: That gives us enough to go on for now.
- user: That'll do. I'm happy with my choice.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

## 29. `te-0171/pdc604d65bd853673894b/crud` (general_update, target probe)

- Question (2027-04-09): Pick a value for ferry-trip keepsake, dated April 9, with the setting described as an ordinary occasion.
- Options: a written note about the crossing sounds | a pressed scrap from the onboard leaflet | a tiny sketch of the wake | a pencil rubbing of the ticket stamp
- Gold: **a tiny sketch of the wake**; Answer Agent chose: **a written note about the crossing sounds**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference, as no specific record matches the setting of an ordinary occasion without a camera.  \nAnswer: a written note about the crossing sounds"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For ferry-trip keepsake, the user prefers a little drawing of the trail in the water."
 },
 {
  "id": "m2",
  "text": "For ferry-trip keepsake when ferry trips made with a camera, the user prefers a tiny sketch of the wake for now, with no end date given."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For ferry-trip keepsake, the user prefers a little drawing of the trail in the water."
 },
 {
  "id": "m2",
  "text": "For ferry-trip keepsake when ferry trips made with a camera, the user prefers a tiny sketch of the wake for now, with no end date given."
 }
]
```

Events up to the probe:

### `e1a6337e528438482a0aa` (2027-04-09), gold category general_update
- user: I had a point to make about what I keep from the crossing. Let the arrangement be a little drawing of the trail in the water when the situation is the general choice rather than a special case. That is what I always want under those circumstances.
- assistant: What did you find difficult about noticing details on the crossing?
- user: I like having something small I can stumble across months later.
- assistant: How much more do you want to say about keeping something from the boat without a photo?
- user: Not much more than that, really.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For ferry-trip keepsake, the user prefers a little drawing of the trail in the water."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For ferry-trip keepsake, the user prefers a little drawing of the trail in the water."}]}`

## 30. `te-0173/p76a859588785a16bce17/crud` (general_update, target probe)

- Question (2027-03-06): Pick a value for stylus pressure response, dated March 6, with the setting described as an ordinary occasion.
- Options: a firm-pressure response curve | a gradual midrange pressure curve | a light-touch pressure curve | a nearly uniform stroke response
- Gold: **a firm-pressure response curve**; Answer Agent chose: **a light-touch pressure curve**
- Answer Agent reply: "The record that applies on this date and in this situation is m5, which describes a light-touch pressure curve for use on a smooth screen cover during ordinary occasions.  \nAnswer: a light-touch pressure curve"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For display edge gesture, the user prefers a swipe that moves to another workspace."
 },
 {
  "id": "m2",
  "text": "For display edge gesture when gestures made with the display flat, the user prefers an edge swipe that shows recent items for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For display edge gesture when gestures made with the display upright, the user prefers an edge swipe that does nothing for now, with no end date given."
 },
 {
  "id": "m4",
  "text": "For stylus pressure response, the user prefers pressure settings built around a firm touch."
 },
 {
  "id": "m5",
  "text": "For stylus pressure response when stylus work on a smooth screen cover, the user prefers a light-touch pressure curve for now, with no end date given."
 },
 {
  "id": "m6",
  "text": "For stylus pressure response when stylus work on a textured screen cover, the user prefers a firm-pressure response curve."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For display edge gesture, the user prefers a swipe that moves to another workspace."
 },
 {
  "id": "m2",
  "text": "For display edge gesture when gestures made with the display flat, the user prefers an edge swipe that shows recent items for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For display edge gesture when gestures made with the display upright, the user prefers an edge swipe that does nothing for now, with no end date given."
 },
 {
  "id": "m4",
  "text": "For stylus pressure response, the user prefers pressure settings built around a firm touch."
 },
 {
  "id": "m5",
  "text": "For stylus pressure response when stylus work on a smooth screen cover, the user prefers a light-touch pressure curve for now, with no end date given."
 },
 {
  "id": "m6",
  "text": "For stylus pressure response when stylus work on a textured screen cover, the user prefers a firm-pressure response curve."
 }
]
```

Events up to the probe:

### `e41f5c6f3d7b9774ef39a` (2027-03-03), gold category stable_preference
- user: I've got a minute now to explain what I mean about how hard I press with the pen.
- assistant: How have you been thinking about it?
- user: Can we get back to how hard I press with the pen?  The remark I heard was, "For drawing on a screen protector with texture, please remember that I choose a pressure setting tuned for a light touch. I mean an enduring arrangement rather than a one-off." It is a secondhand account, not a new preference of my own.
- assistant: Did something in particular draw your attention to getting small marks on a slick cover?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e7c8b10a7a539cc78f43e` (2027-03-05), gold category general_update
- user: Can we get back to what swiping in from the edge does?  Here is where I have landed: a swipe that moves to another workspace, for the general everyday case. I mean an enduring arrangement rather than a one-off.
- assistant: Is there a connection with whether a gesture interrupts what you were doing?
- user: I want to reach the edge without interrupting what I was doing.
- assistant: How much more do you want to say about whether a gesture interrupts what you were doing?
- user: Not much more than that, really.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For display edge gesture, the user prefers a swipe that moves to another workspace."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For display edge gesture, the user prefers a swipe that moves to another workspace."}]}`

### `e18a82ef8a014cd58fc77` (2027-03-06), gold category general_update
- user: Can we get back to how hard I press with the pen?  Pressure settings built around a firm touch is the one I want when we are talking about everyday use with no dedicated arrangement. Leave that as the choice whenever this comes round again.
- assistant: Is how much pressure it takes to make a dark stroke part of what you want to work out?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m4", "text": "For stylus pressure response, the user prefers pressure settings built around a firm touch."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m4", "op": "UPDATE", "text": "For stylus pressure response, the user prefers pressure settings built around a firm touch."}]}`

## 31. `te-0174/pff3cc835a128a62fe142/crud` (scoped_exception, boundary probe)

- Question (2027-03-10): Pick a value for sweater cuff construction, dated March 10, with the setting described as sweaters worn beneath a jacket.
- Options: a tapered split-knit cuff | a close rib-knit cuff | a loose rolled-edge cuff | a broad turned-back cuff
- Gold: **a tapered split-knit cuff**; Answer Agent chose: **a broad turned-back cuff**
- Answer Agent reply: "The record that applies on this date and in this situation is m3, which specifies a broad turned-back cuff for sweaters worn beneath a jacket from 2027-03-11 through 2027-03-30. Answer: a broad turned-back cuff"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For sweater cuff construction, the user prefers a tapered split-knit cuff."
 },
 {
  "id": "m2",
  "text": "For sweater cuff construction when sweaters worn without a jacket, the user prefers a loose rolled-edge cuff."
 },
 {
  "id": "m3",
  "text": "For sweater cuff construction when sweaters worn beneath a jacket, the user prefers a broad turned-back cuff from 2027-03-11 through 2027-03-30."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For sweater cuff construction, the user prefers a tapered split-knit cuff."
 },
 {
  "id": "m2",
  "text": "For sweater cuff construction when sweaters worn without a jacket, the user prefers a loose rolled-edge cuff."
 },
 {
  "id": "m3",
  "text": "For sweater cuff construction when sweaters worn beneath a jacket, the user prefers a broad turned-back cuff from 2027-03-11 through 2027-03-30."
 }
]
```

Events up to the probe:

### `eda7b3a860ae6158412c1` (2027-03-09), gold category stable_preference
- user: I remembered something about what I want at the sweater wrist while thinking about keeping the edge from turning inside out.
- assistant: Of course. We can talk about keeping the edge from turning inside out.
- user: I thought again about sweater cuff construction.  Here is a hypothetical to think about: "I am stuck on the situation for a wide cuff folded back: sweaters worn without a jacket and sweaters worn beneath a jacket are both still in the running." It is not permission to change my preferences.
- assistant: How has keeping the edge from turning inside out worked out in practice?
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `eb596009f360b889407f7` (2027-03-10), gold category scoped_exception
- user: I thought again about what I want at the sweater wrist.  Given sweaters worn beneath a jacket, make the choice a broad turned-back cuff. The request covers March 11 and continues through March 30; then my normal preference takes over. Anything outside this request keeps the choices it already had.
- assistant: What's your biggest concern around keeping the edge from turning inside out?
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For sweater cuff construction when sweaters worn beneath a jacket, the user prefers a broad turned-back cuff from 2027-03-11 through 2027-03-30."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For sweater cuff construction when sweaters worn beneath a jacket, the user prefers a broad turned-back cuff from 2027-03-11 through 2027-03-30."}]}`

## 32. `te-0178/p65e1e26aadee192dff2e/crud` (general_update, target probe)

- Question (2027-09-08): Pick a value for water-flask refill alert, dated September 8, with the setting described as an ordinary occasion.
- Options: a soft ripple animation | a pair of short vibration pulses | a tiny glowing droplet symbol | a quiet descending whistle
- Gold: **a quiet descending whistle**; Answer Agent chose: **a soft whistle**
- Answer Agent reply: "The record that applies on this date and in this situation is m1, which describes a soft whistle for a general water-flask refill alert on an ordinary occasion.  \nAnswer: a soft whistle"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For water-flask refill alert, the user prefers a soft whistle that falls in pitch."
 },
 {
  "id": "m2",
  "text": "For water-flask refill alert when refill tracking with a large flask, the user prefers a tiny glowing droplet symbol."
 },
 {
  "id": "m3",
  "text": "For water-flask refill alert when refill tracking with a small flask, the user prefers a quiet descending whistle for now, with no end date given."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For water-flask refill alert, the user prefers a soft whistle that falls in pitch."
 },
 {
  "id": "m2",
  "text": "For water-flask refill alert when refill tracking with a large flask, the user prefers a tiny glowing droplet symbol."
 },
 {
  "id": "m3",
  "text": "For water-flask refill alert when refill tracking with a small flask, the user prefers a quiet descending whistle for now, with no end date given."
 }
]
```

Events up to the probe:

### `e068d1cf9b7d8e0422215` (2027-09-08), gold category general_update
- user: I remembered something about what reminds me to top up the flask while thinking about which signal is quiet enough not to interrupt.
- assistant: Was something about which signal is quiet enough not to interrupt especially important?
- user: Can we get back to what reminds me to top up the flask?  Use this choice for the general choice rather than a special case: a soft whistle that falls in pitch. That goes for the occasions ahead, with no finishing point.
- assistant: How did which signal is quiet enough not to interrupt get on your mind?
- user: I want to notice the refill cue without distracting anyone nearby.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For water-flask refill alert, the user prefers a soft whistle that falls in pitch."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For water-flask refill alert, the user prefers a soft whistle that falls in pitch."}]}`

## 33. `te-0184/pca9c26daeaa29645e59b/crud` (scoped_exception, default probe)

- Question (2027-06-10): Pick a value for community-board digest arrangement, dated June 10, with the setting described as an ordinary occasion.
- Options: posts clustered by activity date | posts arranged by walking distance | posts clustered by the supplies needed | posts arranged by estimated reading time
- Gold: **posts clustered by the supplies needed**; Answer Agent chose: **posts arranged by walking distance**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which pertains to posts organized by walking distance during a specific period including June 10.  \nAnswer: posts arranged by walking distance"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For community-board digest arrangement, the user prefers posts grouped by equipment and supplies."
 },
 {
  "id": "m2",
  "text": "For community-board digest arrangement when rounding up posts for things people do outside, the user prefers organized by how far there is to walk from 2027-06-11 through 2027-06-22."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For community-board digest arrangement, the user prefers posts grouped by equipment and supplies."
 },
 {
  "id": "m2",
  "text": "For community-board digest arrangement when rounding up posts for things people do outside, the user prefers organized by how far there is to walk from 2027-06-11 through 2027-06-22."
 }
]
```

Events up to the probe:

### `e0f1c4063cebb90348f5f` (2027-06-06), gold category stable_preference
- user: I've got a minute now to explain what I mean about how the noticeboard roundup is sorted.
- assistant: I'm listening. What's on your mind?
- user: I had a point to make about how the noticeboard roundup is sorted. Just for the rounding up posts for things people do outside occasion in front of me, make it posts arranged by walking distance. Nothing about my ongoing choices is changing.
- assistant: There's room to talk more about seeing the supplies for an activity first if you want.
- user: I like being able to skim the board and spot things I might go to.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e98f29f0298eac311801f` (2027-06-07), gold category stable_preference
- user: I had a point to make about community-board digest arrangement. I came back to the same general preference, sorted by how long the posts take to read. The choices I already have still stand.
- assistant: How did being able to skim a whole roundup get on your mind?
- user: If it goes off while I am occupied I still want to recognize it.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `ed9fcbe1c1476b2496ac3` (2027-06-08), gold category general_update
- user: Can we get back to how the noticeboard roundup is sorted?  It is posts grouped by equipment and supplies that I want for the general everyday case. Next time, and after that, I still want this choice. Leave the other arrangements alone.
- assistant: I can see how seeing the supplies for an activity first could make a difference.
- user: I like being able to skim the board and spot things I might go to.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For community-board digest arrangement, the user prefers posts grouped by equipment and supplies."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For community-board digest arrangement, the user prefers posts grouped by equipment and supplies."}]}`

### `e88f8d8bf62a4fe05fc5b` (2027-06-09), gold category clarify
- user: I thought again about community-board digest arrangement.  Do not put organized by how far there is to walk anywhere yet. I have not answered whether it is for rounding up posts for things people do outside or rounding up posts for things people do inside.
- assistant: How did putting nearby activities where you can find them get on your mind?
- user: I like being able to skim the board and spot things I might go to.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `e338e9209ad19c90f602a` (2027-06-10), gold category scoped_exception
- user: There was one thing about how the noticeboard roundup is sorted I wanted to talk through.
- assistant: What would you like to work through first?
- user: Can we get back to how the noticeboard roundup is sorted?  Regarding rounding up posts for things people do outside, I am going for organized by how far there is to walk. The dates are June 11 through June 22, with both counted; after that I am back to the ordinary choice.
- assistant: Is putting nearby activities where you can find them part of what you want to work out?
- user: I like being able to skim the board and spot things I might go to.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For community-board digest arrangement when rounding up posts for things people do outside, the user prefers organized by how far there is to walk from 2027-06-11 through 2027-06-22."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For community-board digest arrangement when rounding up posts for things people do outside, the user prefers organized by how far there is to walk from 2027-06-11 through 2027-06-22."}]}`

## 34. `te-0187/pef4cee4e06be26297cb7/crud` (scoped_exception, boundary probe)

- Question (2027-09-27): Pick a value for stylus pressure response, dated September 27, with the setting described as stylus work on a textured screen cover.
- Options: a nearly uniform stroke response | a firm-pressure response curve | a gradual midrange pressure curve | a light-touch pressure curve
- Gold: **a nearly uniform stroke response**; Answer Agent chose: **a firm-pressure response curve**
- Answer Agent reply: "The record that applies on this date and in this situation is m3, which specifies a firm-pressure response curve for stylus pressure when drawing on a screen protector with texture from 2027-09-11 through 2027-09-26.  \nAnswer: a firm-pressure response curve"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For stylus pressure response, the user prefers nearly the same stroke response throughout."
 },
 {
  "id": "m3",
  "text": "For stylus pressure response when drawing on a screen protector with texture, the user prefers a firm-pressure response curve from 2027-09-11 through 2027-09-26."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For stylus pressure response, the user prefers nearly the same stroke response throughout."
 },
 {
  "id": "m3",
  "text": "For stylus pressure response when drawing on a screen protector with texture, the user prefers a firm-pressure response curve from 2027-09-11 through 2027-09-26."
 }
]
```

Events up to the probe:

### `e0ecb59c004428da3f1ac` (2027-09-04), gold category general_update
- user: I've got a minute now to explain what I mean about how hard I press with the pen.
- assistant: What did you want me to know?
- user: Here's what I meant about how hard I press with the pen.  Use this choice for regular occasions without a special choice: a pressure setting tuned for a light touch. Make that the standing arrangement from this point ahead.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For stylus pressure response, the user prefers a pressure setting tuned for a light touch."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For stylus pressure response, the user prefers a pressure setting tuned for a light touch."}]}`

### `ed5c7ba964cc8fb156c2c` (2027-09-05), gold category exception_retirement
- user: There was one thing about how hard I press with the pen I wanted to talk through.
- assistant: How have you been thinking about it?
- user: I thought again about how hard I press with the pen.  I would like stylus work on a textured screen cover to stop being an exception and simply follow my general preference.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m2"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "DELETE"}]}`

### `eb56ab82bade8f4626e72` (2027-09-06), gold category general_update
- user: I thought about how hard I press with the pen again this morning.
- assistant: Of course. We can talk about getting small marks on a slick cover.
- user: I had a point to make about how hard I press with the pen. Use this choice for the broad run of ordinary occasions: a gradual midrange pressure curve. Next time, and after that, I still want this choice.
- assistant: Did something in particular draw your attention to getting small marks on a slick cover?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For stylus pressure response, the user prefers a gradual midrange pressure curve."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For stylus pressure response, the user prefers a gradual midrange pressure curve."}]}`

### `ef7543df0e9cc18fe0e9a` (2027-09-07), gold category stable_preference
- user: I thought about how hard I press with the pen again this morning.
- assistant: How have you been thinking about it?
- user: Here's what I meant about how hard I press with the pen.  What if someone said, "It is a firm-pressure response curve that I want for drawing on a screen protector with texture. I want it for the full period September 7 through September 21, not before or afterward."? I mean an imaginary situation, not an actual request from me.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e87b514e91bb67f78bcc0` (2027-09-08), gold category general_update
- user: Can we get back to how hard I press with the pen?  When everyday use with no dedicated arrangement comes up, my choice is nearly the same stroke response throughout. I want to keep coming back to that choice, not try it once. Anything outside this request keeps the choices it already had.
- assistant: What would make getting small marks on a slick cover easier to deal with?
- user: I judge it by whether I can use the screen without thinking about it.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For stylus pressure response, the user prefers nearly the same stroke response throughout."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For stylus pressure response, the user prefers nearly the same stroke response throughout."}]}`

### `e39fc7f54f2c7946e3274` (2027-09-09), gold category clarify
- user: Here's what I meant about how hard I press with the pen.  Do not put pressure settings built around a firm touch anywhere yet. I have not answered whether it is for drawing on a screen protector with texture or stylus work on a smooth screen cover.
- assistant: Have you been noticing anything new about keeping the line from jumping in width?
- user: It bothers me when a small change in pressure makes the stroke jump.
- assistant: Is there anything about getting small marks on a slick cover we haven’t touched on?
- user: Nothing I wanted to get into this time.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `e892693a25ce8b225c8f7` (2027-09-11), gold category scoped_exception
- user: I thought about how hard I press with the pen again this morning.
- assistant: Was something about getting small marks on a slick cover especially important?
- user: Here's what I meant about how hard I press with the pen.  Regarding drawing on a screen protector with texture, I am going for a firm-pressure response curve. The dates are September 11 through September 26, with both counted; after that I am back to the ordinary choice.
- assistant: Could you say why getting small marks on a slick cover matters to you?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For stylus pressure response when drawing on a screen protector with texture, the user prefers a firm-pressure response curve from 2027-09-11 through 2027-09-26."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For stylus pressure response when drawing on a screen protector with texture, the user prefers a firm-pressure response curve from 2027-09-11 through 2027-09-26."}]}`

## 35. `te-0188/p9a63523bb6b41ca63a09/crud` (scoped_exception, default probe)

- Question (2027-12-08): Pick a value for bath-towel border style, dated December 8, with the setting described as an ordinary occasion.
- Options: a broad flat linen border | a doubled terry border with rounded corners | a soft fringed edge without a band | a narrow woven herringbone border
- Gold: **a soft fringed edge without a band**; Answer Agent chose: **a broad flat linen border**
- Answer Agent reply: "The record that applies on this date and in this situation is m3, which specifies a wide smooth linen strip for drying towels over a bar from 2027-12-08 through 2027-12-31. Answer: a broad flat linen border"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For bath-towel border style, the user prefers a soft fringed edge without a band."
 },
 {
  "id": "m2",
  "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a doubled terry border with rounded corners for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For bath-towel border style when drying the towel over a bar, the user prefers a wide smooth linen strip from 2027-12-08 through 2027-12-31."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For bath-towel border style, the user prefers a soft fringed edge without a band."
 },
 {
  "id": "m2",
  "text": "For bath-towel border style when towels hung on a wall hook, the user prefers a doubled terry border with rounded corners for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For bath-towel border style when drying the towel over a bar, the user prefers a wide smooth linen strip from 2027-12-08 through 2027-12-31."
 }
]
```

Events up to the probe:

### `e3f4c965ee20f8533393d` (2027-12-07), gold category stable_preference
- user: I've got a minute now to explain what I mean about the edge finish on the bath towel.
- assistant: What would you like to work through first?
- user: I had a point to make about bath-towel border style. This was somebody else talking: "The option I am selecting where the broad run of ordinary occasions is concerned is a narrow woven herringbone border. That is what I always want under those circumstances." I am recounting their words, not asking you to change my choices.
- assistant: Is this partly about whether the fringe catches on the hook?
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e00ea88869c7b4728836e` (2027-12-08), gold category scoped_exception
- user: I had a point to make about bath-towel border style. A wide smooth linen strip is the one I want when we are talking about drying the towel over a bar. The dates are December 8 through December 31, with both counted; after that I am back to the ordinary choice.
- assistant: There's room to talk more about how the edge sits on the rail if you want.
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For bath-towel border style when drying the towel over a bar, the user prefers a wide smooth linen strip from 2027-12-08 through 2027-12-31."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For bath-towel border style when drying the towel over a bar, the user prefers a wide smooth linen strip from 2027-12-08 through 2027-12-31."}]}`

## 36. `te-0191/p33adf749e443277f0c17/crud` (stable_preference, target probe)

- Question (2027-10-17): Pick a value for desk reference placement, dated October 17, with the setting described as reference use while writing by hand.
- Options: reference pages propped on a side easel | reference pages held in a low rotating stand | reference pages laid above the work area | reference pages clipped to a vertical board
- Gold: **reference pages held in a low rotating stand**; Answer Agent chose: **reference pages propped on a side easel**
- Answer Agent reply: "The record that applies on this date and in this situation is m1, which describes a preference for pages leaning on a small easel to one side.  \nAnswer: reference pages propped on a side easel"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For desk reference placement, the user prefers pages leaning on a small easel to one side."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For desk reference placement, the user prefers pages leaning on a small easel to one side."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m4",
  "text": "For desk reference placement when using references while I write longhand, the user prefers pages in a short stand that swivels for now, with no end date given."
 }
]
```

Events up to the probe:

### `e4b102d28d2738ad0446e` (2027-10-09), gold category scoped_exception
- user: I had a point to make about how I lay out working on spare paper. The option I am selecting where working out sums while sitting at the desk is concerned is calculations on folded pocket slips. The dates are October 9 through October 20, with both counted; after that I am back to the ordinary choice.
- assistant: What's your biggest concern around what stays legible when you stand up?
- user: I need to look back at the working without losing which sum is which.
- assistant: Is there anything about what stays legible when you stand up we haven’t touched on?
- user: Nothing I wanted to get into this time.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers calculations on folded pocket slips from 2027-10-09 through 2027-10-20."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For desk reference placement when working out sums while sitting at the desk, the user prefers calculations on folded pocket slips from 2027-10-09 through 2027-10-20."}]}`

### `efbcbc96b42b6b969b3c3` (2027-10-10), gold category stable_preference
- user: I've got a minute now to explain what I mean about how I lay out working on spare paper.
- assistant: What would you like to work through first?
- user: I had a point to make about how I lay out working on spare paper. Here is a hypothetical to think about: "It is calculations on folded pocket slips that I want for rough calculations at a standing desk. It is a dated exception, beginning October 10 and ending with October 24, both included." It is not permission to change my preferences.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `ea866c6a540ca362bed15` (2027-10-11), gold category exception_revision
- user: Can we get back to how I lay out working on spare paper?  The answer for working out sums while sitting at the desk, as far as I am concerned, is a separate little square for each sum. Keep this for the inclusive dates October 9 to October 20; outside them use the ordinary choice.
- assistant: I see why this could come up while thinking about being able to follow sums on a small scrap.
- user: I need to look back at the working without losing which sum is which.
- assistant: Do you have another thought on room to draw the rough shape first?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers a separate little square for each sum from 2027-10-09 through 2027-10-20."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For desk reference placement when working out sums while sitting at the desk, the user prefers a separate little square for each sum from 2027-10-09 through 2027-10-20."}]}`

### `ebeebec04426b41147247` (2027-10-12), gold category exception_retirement
- user: I have something on my mind about how I lay out working on spare paper.
- assistant: Did you want to say what you had in mind?
- user: Here's what I meant about scratch-paper use pattern.  That separate choice for working out sums while sitting at the desk has run its course. Put it back under whatever I generally want.

Gold output: `{"decision": "resolved", "operations": [{"op": "DELETE", "id": "m3"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "DELETE"}]}`

### `ea8dc5900cbc77bb95098` (2027-10-13), gold category general_update
- user: Can we get back to where I put pages I'm looking at?  For the general choice rather than a special case, please remember that I choose pages leaning on a small easel to one side. I am not putting an end date on this preference.
- assistant: Have you been noticing anything new about looking at a reference without turning around?
- user: It is the sort of detail I notice while there is a lot going on.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For desk reference placement, the user prefers pages leaning on a small easel to one side."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For desk reference placement, the user prefers pages leaning on a small easel to one side."}]}`

### `e39d431d678d7f4ae6e4c` (2027-10-15), gold category scoped_exception
- user: I've got a minute now to explain what I mean about where I put pages I'm looking at.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to where I put pages I'm looking at?  Keep pages in a short stand that swivels in mind as the choice I am making for using references while I write longhand. Only as a stopgap, but on each occasion for now. I cannot name the last day. Leave the other arrangements alone.
- assistant: How has looking at a reference without turning around worked out in practice?
- user: I am trying to cut down the time between one task and the next.
- assistant: Do you have another thought on where the pages sit relative to a hand?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For desk reference placement when using references while I write longhand, the user prefers pages in a short stand that swivels for now, with no end date given."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `ed9b79c37cac99965e0ee` (2027-10-17), gold category stable_preference
- user: I had a point to make about where I put pages I'm looking at. I want a choice for the present business with reference use while writing by hand; don't carry the decision forward.
- assistant: I see why this could come up while thinking about looking at a reference without turning around.
- user: I am trying to see the reference without moving the work out of the way.
- assistant: What feels right to you?
- user: For me it'd be pages flat just above where I work.
- assistant: Are you happy to stop there about looking at a reference without turning around?
- user: That'll do. I'm happy with my choice.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

## 37. `te-0193/p71228c3e5478dffb4dac/crud` (exception_revision, target probe)

- Question (2027-12-03): Pick a value for display edge gesture, dated December 3, with the setting described as gestures made with the display flat.
- Options: an edge swipe that does nothing | an edge swipe that shows recent items | an edge swipe that switches workspaces | an edge swipe that opens a tool strip
- Gold: **an edge swipe that opens a tool strip**; Answer Agent chose: **an edge swipe that shows recent items**
- Answer Agent reply: "The record that applies on this date and in this situation is m2: \"For display edge gesture when gestures made with the display flat, the user prefers a swipe that pulls up the tools for now, with no end date given.\"  \nAnswer: an edge swipe that shows recent items"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For display edge gesture, the user prefers an edge swipe that switches workspaces."
 },
 {
  "id": "m2",
  "text": "For display edge gesture when gestures made with the display flat, the user prefers a swipe that pulls up the tools for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For display edge gesture when gestures made with the display upright, the user prefers an edge swipe that opens a tool strip for now, with no end date given."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For display edge gesture, the user prefers an edge swipe that switches workspaces."
 },
 {
  "id": "m2",
  "text": "For display edge gesture when gestures made with the display flat, the user prefers a swipe that pulls up the tools for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For display edge gesture when gestures made with the display upright, the user prefers an edge swipe that opens a tool strip for now, with no end date given."
 }
]
```

Events up to the probe:

### `e3badf13740af617513e0` (2027-12-03), gold category exception_revision
- user: I thought again about what swiping in from the edge does.  My request is to save a swipe that pulls up the tools for gestures made with the display flat. I need it for a while rather than once, and rather than forever. No end is fixed.
- assistant: What did you find difficult about what opens when you brush the edge?
- user: I want to reach the edge without interrupting what I was doing.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m2", "text": "For display edge gesture when gestures made with the display flat, the user prefers a swipe that pulls up the tools for now, with no end date given."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m2", "op": "UPDATE", "text": "For display edge gesture when gestures made with the display flat, the user prefers a swipe that pulls up the tools for now, with no end date given."}]}`

## 38. `te-0195/p680e8a7bd7345cc360f8/crud` (general_update, target probe)

- Question (2027-03-06): Pick a value for stylus pressure response, dated March 6, with the setting described as an ordinary occasion.
- Options: a firm-pressure response curve | a gradual midrange pressure curve | a light-touch pressure curve | a nearly uniform stroke response
- Gold: **a firm-pressure response curve**; Answer Agent chose: **a light-touch pressure curve**
- Answer Agent reply: "The record that applies on this date and in this situation is m5, which describes a light-touch pressure curve for use on a smooth screen cover during ordinary occasions.  \nAnswer: a light-touch pressure curve"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For display edge gesture, the user prefers a swipe that moves to another workspace."
 },
 {
  "id": "m2",
  "text": "For display edge gesture when gestures made with the display flat, the user prefers an edge swipe that shows recent items for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For display edge gesture when gestures made with the display upright, the user prefers an edge swipe that does nothing for now, with no end date given."
 },
 {
  "id": "m4",
  "text": "For stylus pressure response, the user prefers pressure settings built around a firm touch."
 },
 {
  "id": "m5",
  "text": "For stylus pressure response when stylus work on a smooth screen cover, the user prefers a light-touch pressure curve for now, with no end date given."
 },
 {
  "id": "m6",
  "text": "For stylus pressure response when stylus work on a textured screen cover, the user prefers a firm-pressure response curve."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For display edge gesture, the user prefers a swipe that moves to another workspace."
 },
 {
  "id": "m2",
  "text": "For display edge gesture when gestures made with the display flat, the user prefers an edge swipe that shows recent items for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For display edge gesture when gestures made with the display upright, the user prefers an edge swipe that does nothing for now, with no end date given."
 },
 {
  "id": "m4",
  "text": "For stylus pressure response, the user prefers pressure settings built around a firm touch."
 },
 {
  "id": "m5",
  "text": "For stylus pressure response when stylus work on a smooth screen cover, the user prefers a light-touch pressure curve for now, with no end date given."
 },
 {
  "id": "m6",
  "text": "For stylus pressure response when stylus work on a textured screen cover, the user prefers a firm-pressure response curve."
 }
]
```

Events up to the probe:

### `ee6d8009aa4c76cb5610b` (2027-03-03), gold category stable_preference
- user: I've got a minute now to explain what I mean about how hard I press with the pen.
- assistant: How have you been thinking about it?
- user: Can we get back to how hard I press with the pen?  The remark I heard was, "For drawing on a screen protector with texture, please remember that I choose a pressure setting tuned for a light touch. I mean an enduring arrangement rather than a one-off." It is a secondhand account, not a new preference of my own.
- assistant: Did something in particular draw your attention to getting small marks on a slick cover?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e221249bef824ba7a7516` (2027-03-05), gold category general_update
- user: Can we get back to what swiping in from the edge does?  Here is where I have landed: a swipe that moves to another workspace, for the general everyday case. I mean an enduring arrangement rather than a one-off.
- assistant: Is there a connection with whether a gesture interrupts what you were doing?
- user: I want to reach the edge without interrupting what I was doing.
- assistant: How much more do you want to say about whether a gesture interrupts what you were doing?
- user: Not much more than that, really.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m1", "text": "For display edge gesture, the user prefers a swipe that moves to another workspace."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m1", "op": "UPDATE", "text": "For display edge gesture, the user prefers a swipe that moves to another workspace."}]}`

### `e4095fc5b0f837f25b854` (2027-03-06), gold category general_update
- user: Can we get back to how hard I press with the pen?  Pressure settings built around a firm touch is the one I want when we are talking about everyday use with no dedicated arrangement. Leave that as the choice whenever this comes round again.
- assistant: Is how much pressure it takes to make a dark stroke part of what you want to work out?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m4", "text": "For stylus pressure response, the user prefers pressure settings built around a firm touch."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m4", "op": "UPDATE", "text": "For stylus pressure response, the user prefers pressure settings built around a firm touch."}]}`

## 39. `te-0196/p01ff927a0aad0a54bdd7/crud` (scoped_exception, boundary probe)

- Question (2027-05-08): Pick a value for baked potato filling, dated May 8, with the setting described as potatoes eaten from a bowl.
- Options: herbed curd with grated radish | smoky beans with chopped scallions | crushed peas with lemon zest | roasted mushrooms with thyme
- Gold: **crushed peas with lemon zest**; Answer Agent chose: **herbed curd with grated radish**
- Answer Agent reply: "The record that applies on this date and in this situation is m3: \"For baked potato filling when eating the potato out of a bowl, the user prefers herbed curd with grated radish from 2027-05-09 through 2027-05-27.\"  \nAnswer: herbed curd with grated radish"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For baked potato filling, the user prefers crushed peas with lemon zest."
 },
 {
  "id": "m2",
  "text": "For baked potato filling when eating the potato from a little paper tray, the user prefers smoky beans with chopped scallions from 2027-05-05 through 2027-05-25."
 },
 {
  "id": "m3",
  "text": "For baked potato filling when eating the potato out of a bowl, the user prefers herbed curd with grated radish from 2027-05-09 through 2027-05-27."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For baked potato filling, the user prefers crushed peas with lemon zest."
 },
 {
  "id": "m2",
  "text": "For baked potato filling when eating the potato from a little paper tray, the user prefers smoky beans with chopped scallions from 2027-05-05 through 2027-05-25."
 },
 {
  "id": "m3",
  "text": "For baked potato filling when eating the potato out of a bowl, the user prefers herbed curd with grated radish from 2027-05-09 through 2027-05-27."
 }
]
```

Events up to the probe:

### `ef2272cbc8329727a7ddb` (2027-05-04), gold category clarify
- user: I had a point to make about what I put inside the jacket potato. I cannot yet attach smoky beans and scallion pieces to a particular situation: it is between eating the potato from a little paper tray and potatoes eaten from a bowl.
- assistant: Is there a connection with how the herbs and beans balance?
- user: I want the filling to be easy to scoop without coming away in one piece.
- assistant: How much more do you want to say about how neatly the filling stays in the potato?
- user: Not much more than that, really.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `e4a2cc9b5590448318800` (2027-05-05), gold category scoped_exception
- user: Here's what I meant about what I put inside the jacket potato.  My request is to save smoky beans with chopped scallions for eating the potato from a little paper tray. Its first day is May 5; May 25 is included as the last, and then it is over.
- assistant: How did how the herbs and beans balance get on your mind?
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For baked potato filling when eating the potato from a little paper tray, the user prefers smoky beans with chopped scallions from 2027-05-05 through 2027-05-25."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For baked potato filling when eating the potato from a little paper tray, the user prefers smoky beans with chopped scallions from 2027-05-05 through 2027-05-25."}]}`

### `e12bcef3c818d1f5cd7b3` (2027-05-07), gold category clarify
- user: There was one thing about what I put inside the jacket potato I wanted to talk through.
- assistant: Did you want to say what you had in mind?
- user: I had a point to make about what I put inside the jacket potato. I cannot yet attach herbed curd with grated radish to a particular situation: it is between potatoes eaten from a paper boat and potatoes eaten from a bowl.

Gold output: `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "clarify", "operations": [{"op": "NOOP"}]}`

### `e561a2fd6aee9c35df8be` (2027-05-08), gold category scoped_exception
- user: Here's what I meant about what I put inside the jacket potato.  Keep herbed curd with grated radish in mind as the choice I am making for eating the potato out of a bowl. This temporary spell runs from the start of May 9 to the end of May 27. Anything outside this request keeps the choices it already had.
- assistant: There's room to talk more about how the herbs and beans balance if you want.
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For baked potato filling when eating the potato out of a bowl, the user prefers herbed curd with grated radish from 2027-05-09 through 2027-05-27."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For baked potato filling when eating the potato out of a bowl, the user prefers herbed curd with grated radish from 2027-05-09 through 2027-05-27."}]}`

## 40. `te-0197/p9dc8a2737c5619274a51/crud` (stable_preference, default probe)

- Question (2027-07-09): Pick a value for scratch-paper use pattern, dated July 9, with the setting described as an ordinary occasion.
- Options: one calculation per loose square | calculations on folded pocket slips | calculations arranged around a central sketch | several calculations in a spiral column
- Gold: **several calculations in a spiral column**; Answer Agent chose: **one calculation per loose square**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which describes a preference for one calculation per loose square when doing rough calculations at a standing desk, but this is limited to that specific context and does not apply to an ordinary occasion.  \nAnswer: one calculation per loose square"

Memory at the probe (this arm):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers one calculation per loose square for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers doing the math on little folded slips from 2027-07-06 through 2027-07-17."
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "id": "m1",
  "text": "For scratch-paper use pattern, the user prefers several calculations in a spiral column."
 },
 {
  "id": "m2",
  "text": "For scratch-paper use pattern when rough calculations at a standing desk, the user prefers one calculation per loose square for now, with no end date given."
 },
 {
  "id": "m3",
  "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers doing the math on little folded slips from 2027-07-06 through 2027-07-17."
 }
]
```

Events up to the probe:

### `e1401b83bb198725594e9` (2027-07-04), gold category stable_preference
- user: I have something on my mind about how I lay out working on spare paper.
- assistant: How have you been thinking about it?
- user: I had a point to make about how I lay out working on spare paper. The imagined version would be, "Given rough calculations at a standing desk, make the choice calculations on folded pocket slips. Let it run across the coming occasions until I can end this temporary arrangement." I am not putting that into practice.
- assistant: Is there a connection with what stays legible when you stand up?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e9c8f4c29a5e596366821` (2027-07-05), gold category scoped_exception
- user: Being able to follow sums on a small scrap has been on my mind. Can we get back to how I lay out working on spare paper?
- assistant: What would you like to work through first?
- user: Here's what I meant about how I lay out working on spare paper.  Keep working spread around a sketch in the middle in mind as the choice I am making for working out sums while sitting at the desk. It is a dated exception, beginning July 6 and ending with July 17, both included.
- assistant: What did you find difficult about being able to follow sums on a small scrap?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "ADD", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers working spread around a sketch in the middle from 2027-07-06 through 2027-07-17."}]}`

### `ee4e491d33aa65088fe23` (2027-07-06), gold category exception_revision
- user: There was one thing about how I lay out working on spare paper I wanted to talk through.
- assistant: Feel free to start with whatever's most useful.
- user: Here's what I meant about how I lay out working on spare paper.  Use this choice for rough calculations at a seated desk: doing the math on little folded slips. The request covers July 6 and continues through July 17; then my normal preference takes over. Anything outside this request keeps the choices it already had.

Gold output: `{"decision": "resolved", "operations": [{"op": "UPDATE", "id": "m3", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers doing the math on little folded slips from 2027-07-06 through 2027-07-17."}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"id": "m3", "op": "UPDATE", "text": "For scratch-paper use pattern when working out sums while sitting at the desk, the user prefers doing the math on little folded slips from 2027-07-06 through 2027-07-17."}]}`

### `eeb79ef6f44fc5df1ac46` (2027-07-08), gold category stable_preference
- user: Being able to follow sums on a small scrap has been on my mind. Can we get back to how I lay out working on spare paper?
- assistant: What's your biggest concern around being able to follow sums on a small scrap?
- user: I need to look back at the working without losing which sum is which.
- assistant: Of course. We can talk about being able to follow sums on a small scrap.
- user: I thought again about scratch-paper use pattern.  My usual choice of several calculations in a spiral column holds up. Everything about my established preferences stays as it was.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

### `e3f003b47d20e281b88d6` (2027-07-09), gold category stable_preference
- user: I thought again about scratch-paper use pattern.  For the next instance of rough calculations at a seated desk, I need to pick something. That's the only one I'm thinking about.
- assistant: I'm curious about what stays legible when you stand up, too.
- user: I need to look back at the working without losing which sum is which.
- assistant: What feels right to you?
- user: Let's go with calculations arranged around a central sketch.
- assistant: That gives us enough to go on for now.
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`
Policy output (accepted): `{"decision": "resolved", "operations": [{"op": "NOOP"}]}`

