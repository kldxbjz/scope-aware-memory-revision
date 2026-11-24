# Error analysis packet: scope arm

Run `runs/test_p12_sft_s0`: 40 of 275 wrong probes, sampled with seed 0. Label every item in the labels file with one source from docs/analysis.md (action, executor_rejection, reader_matching, answer_reasoning, data, other) and a short note. Label alone first; compare afterwards.

## 1. `te-0016/p3190f8d9e2e42029828e/scope` (exception_revision, neighbor probe)

- Question (2027-09-21): Pick a value for display edge gesture, dated September 21, with the setting described as gestures made with the display upright.
- Options: an edge swipe that does nothing | an edge swipe that switches workspaces | an edge swipe that shows recent items | an edge swipe that opens a tool strip
- Gold: **an edge swipe that opens a tool strip**; Answer Agent chose: **an edge swipe that pulls up the tools**
- Answer Agent reply: "The record that applies on this date and in the situation of gestures made with the display upright is the one with memory_id \"m4\", which states \"a swipe that pulls up the tools\" when swiping the edge with the display propped vertically.  \nAnswer: an edge swipe that pulls up the tools"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m4",
  "attribute": "display edge gesture",
  "value": "a swipe that pulls up the tools",
  "scope": "swiping the edge with the display propped vertically",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m5"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e74b5c8e83bec9fca8f45"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "display edge gesture",
  "value": "an edge swipe that shows recent items",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e4be3132bbff7af89a24e"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "display edge gesture",
  "value": "an edge swipe that opens a tool strip",
  "scope": "gestures made with the display flat",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m5"
   },
   {
    "type": "REPLACES",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "e827b0549dc2a251e2652"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m4",
  "attribute": "display edge gesture",
  "value": "a swipe that pulls up the tools",
  "scope": "swiping the edge with the display propped vertically",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m5"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e74b5c8e83bec9fca8f45"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "display edge gesture",
  "value": "an edge swipe that shows recent items",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e4be3132bbff7af89a24e"
  ]
 },
 {
  "memory_id": "m8",
  "attribute": "display edge gesture",
  "value": "the swipe leaves things as they are",
  "scope": "gestures made with the display flat",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m5"
   },
   {
    "type": "REPLACES",
    "target": "m7"
   }
  ],
  "evidence_ids": [
   "ec35a9f3994ec43b84be3"
  ]
 }
]
```

Events up to the probe:

### `eb2f929ec92e2529d9100` (2027-09-10), gold category exception_retirement
- user: How easy it is to reach the side of the display has been on my mind. Can we get back to what swiping in from the edge does?
- assistant: How have you been thinking about it?
- user: Can we get back to what swiping in from the edge does?  There is nothing to keep apart for gestures made with the display upright anymore. I want it to follow whatever I choose for other occasions.
- assistant: Have you been noticing anything new about how easy it is to reach the side of the display?
- user: I want to reach the edge without interrupting what I was doing.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m2", "evidence_ids": ["eb2f929ec92e2529d9100"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["eb2f929ec92e2529d9100"], "operation": "RETIRE", "target_id": "m2"}], "decision": "resolved"}`

### `ee32ca8f3345167d92e8c` (2027-09-12), gold category scoped_exception
- user: I had a point to make about what swiping in from the edge does. Regarding swiping the edge with the display propped vertically, I am going for an edge swipe that shows recent items. Not permanently, and not just this time: it continues provisionally with no closing date.
- assistant: What do you tend to notice first about how easy it is to reach the side of the display?
- user: I am thinking about how it feels after more than a minute.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "display edge gesture", "value": "an edge swipe that shows recent items", "scope": "swiping the edge with the display propped vertically", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ee32ca8f3345167d92e8c"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "display edge gesture", "evidence_ids": ["ee32ca8f3345167d92e8c"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "swiping the edge with the display propped vertically", "validity": {"kind": "open"}, "value": "an edge swipe that shows recent items"}], "decision": "resolved"}`

### `e47edae834477f258c281` (2027-09-14), gold category stable_preference
- user: Here's what I meant about what swiping in from the edge does.  Just for the gestures made with the display upright occasion in front of me, make it an edge swipe that opens a tool strip. Nothing about my ongoing choices is changing.
- assistant: How did how easy it is to reach the side of the display get on your mind?
- user: I would rather not break what I was doing to adjust anything.
- assistant: Is there anything about whether a gesture interrupts what you were doing we haven’t touched on?
- user: Nothing I wanted to get into this time.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `e74b5c8e83bec9fca8f45` (2027-09-16), gold category exception_revision
- user: There was one thing about what swiping in from the edge does I wanted to talk through.
- assistant: What did you want me to know?
- user: Can we get back to what swiping in from the edge does?  Keep a swipe that pulls up the tools in mind as the choice I am making for swiping the edge with the display propped vertically. There is a temporary need for it whenever this arises; I will let you know when it passes.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "a swipe that pulls up the tools", "scope": "swiping the edge with the display propped vertically", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e74b5c8e83bec9fca8f45"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e74b5c8e83bec9fca8f45"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "swiping the edge with the display propped vertically", "target_id": "m3", "validity": {"kind": "open"}, "value": "a swipe that pulls up the tools"}], "decision": "resolved"}`

### `e4be3132bbff7af89a24e` (2027-09-17), gold category general_update
- user: Can we get back to what swiping in from the edge does?  Here is where I have landed: an edge swipe that shows recent items, for ordinary occasions overall. Leave that as the choice whenever this comes round again.
- assistant: There's room to talk more about how easy it is to reach the side of the display if you want.
- user: I notice it when I go to make a small movement.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "an edge swipe that shows recent items", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e4be3132bbff7af89a24e"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e4be3132bbff7af89a24e"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "an edge swipe that shows recent items"}], "decision": "resolved"}`

### `e23792f2b900ec0ce362f` (2027-09-18), gold category scoped_exception
- user: I've got a minute now to explain what I mean about what swiping in from the edge does.
- assistant: What would you like to work through first?
- user: Can we get back to what swiping in from the edge does?  The option I am selecting where gestures made with the display flat is concerned is a swipe that moves to another workspace. Only as a stopgap, but on each occasion for now. I cannot name the last day.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "display edge gesture", "value": "a swipe that moves to another workspace", "scope": "gestures made with the display flat", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m5"}], "evidence_ids": ["e23792f2b900ec0ce362f"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "display edge gesture", "evidence_ids": ["e23792f2b900ec0ce362f"], "operation": "ADD", "relations": [{"target": "m5", "type": "EXCEPTION_TO"}], "scope": "gestures made with the display flat", "validity": {"kind": "open"}, "value": "a swipe that moves to another workspace"}], "decision": "resolved"}`

### `e827b0549dc2a251e2652` (2027-09-20), gold category exception_revision
- user: There was one thing about what swiping in from the edge does I wanted to talk through.
- assistant: Of course. We can talk about whether a gesture interrupts what you were doing.
- user: Here's what I meant about what swiping in from the edge does.  Use this choice for swiping the edge with the display laid down: an edge swipe that opens a tool strip. There is a temporary need for it whenever this arises; I will let you know when it passes.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m6", "value": "an edge swipe that opens a tool strip", "scope": "gestures made with the display flat", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m5"}], "evidence_ids": ["e827b0549dc2a251e2652"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e827b0549dc2a251e2652"], "operation": "REVISE", "relations": [{"target": "m5", "type": "EXCEPTION_TO"}], "scope": "gestures made with the display flat", "target_id": "m6", "validity": {"kind": "open"}, "value": "an edge swipe that opens a tool strip"}], "decision": "resolved"}`

### `ec35a9f3994ec43b84be3` (2027-09-21), gold category exception_revision
- user: Here's what I meant about what swiping in from the edge does.  I want to choose what I'll keep doing for swiping the edge with the display laid down, not just on the next occasion.
- assistant: Is how easy it is to reach the side of the display part of what you want to work out?
- user: I want to reach the edge without interrupting what I was doing.
- assistant: Which sounds most like what you want?
- user: Let's go with the swipe leaves things as they are.
- assistant: That gives us enough to go on for now.
- user: That'll do. I'm happy with my choice.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m7", "value": "the swipe leaves things as they are", "scope": "gestures made with the display flat", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m5"}], "evidence_ids": ["ec35a9f3994ec43b84be3"]}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 2. `te-0016/p78067f83939e55eabd8e/scope` (scoped_exception, target probe)

- Question (2027-09-12): Pick a value for display edge gesture, dated September 12, with the setting described as gestures made with the display upright.
- Options: an edge swipe that shows recent items | an edge swipe that switches workspaces | an edge swipe that opens a tool strip | an edge swipe that does nothing
- Gold: **an edge swipe that shows recent items**; Answer Agent chose: **an edge swipe that does nothing**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference, as the specific record for swiping with the display propped vertically does not match the condition of the display being upright.  \nAnswer: an edge swipe that does nothing"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "display edge gesture",
  "value": "an edge swipe that does nothing",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "display edge gesture",
  "value": "an edge swipe that shows recent items",
  "scope": "swiping the edge with the display propped vertically",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ee32ca8f3345167d92e8c"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "display edge gesture",
  "value": "an edge swipe that does nothing",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "display edge gesture",
  "value": "an edge swipe that shows recent items",
  "scope": "swiping the edge with the display propped vertically",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ee32ca8f3345167d92e8c"
  ]
 }
]
```

Events up to the probe:

### `eb2f929ec92e2529d9100` (2027-09-10), gold category exception_retirement
- user: How easy it is to reach the side of the display has been on my mind. Can we get back to what swiping in from the edge does?
- assistant: How have you been thinking about it?
- user: Can we get back to what swiping in from the edge does?  There is nothing to keep apart for gestures made with the display upright anymore. I want it to follow whatever I choose for other occasions.
- assistant: Have you been noticing anything new about how easy it is to reach the side of the display?
- user: I want to reach the edge without interrupting what I was doing.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m2", "evidence_ids": ["eb2f929ec92e2529d9100"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["eb2f929ec92e2529d9100"], "operation": "RETIRE", "target_id": "m2"}], "decision": "resolved"}`

### `ee32ca8f3345167d92e8c` (2027-09-12), gold category scoped_exception
- user: I had a point to make about what swiping in from the edge does. Regarding swiping the edge with the display propped vertically, I am going for an edge swipe that shows recent items. Not permanently, and not just this time: it continues provisionally with no closing date.
- assistant: What do you tend to notice first about how easy it is to reach the side of the display?
- user: I am thinking about how it feels after more than a minute.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "display edge gesture", "value": "an edge swipe that shows recent items", "scope": "swiping the edge with the display propped vertically", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ee32ca8f3345167d92e8c"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "display edge gesture", "evidence_ids": ["ee32ca8f3345167d92e8c"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "swiping the edge with the display propped vertically", "validity": {"kind": "open"}, "value": "an edge swipe that shows recent items"}], "decision": "resolved"}`

## 3. `te-0027/p0ff54204917fb225eef1/scope` (general_update, neighbor probe)

- Question (2027-04-12): Pick a value for group-poll update trigger, dated April 12, with the setting described as polls offering more than two choices.
- Options: a notice when a different choice takes the lead | a notice whenever a vote arrives | a notice after every participant has voted | a notice when half the group has voted
- Gold: **a notice after every participant has voted**; Answer Agent chose: **a notice when a different choice takes the lead**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference, as no record specifically addresses polls with more than two choices.  \nAnswer: a notice when a different choice takes the lead"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m3",
  "attribute": "group-poll update trigger",
  "value": "a ping on each incoming vote",
  "scope": "polls with two possible answers",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "ee7881750119349a8a516"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "group-poll update trigger",
  "value": "a notice after every participant has voted",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ea8f03a2526d81a423cb2"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m3",
  "attribute": "group-poll update trigger",
  "value": "a ping on each incoming vote",
  "scope": "polls with two possible answers",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "ee7881750119349a8a516"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "group-poll update trigger",
  "value": "a notice after every participant has voted",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ea8f03a2526d81a423cb2"
  ]
 }
]
```

Events up to the probe:

### `ee73b153b676d26fb784b` (2027-04-08), gold category clarify
- user: Getting an update before the poll closes has been on my mind. Can we get back to when I get news from the poll?
- assistant: Was something about getting an update before the poll closes especially important?
- user: I had a point to make about when I get news from the poll. I cannot yet attach a notice whenever a vote arrives to a particular situation: it is between polls offering exactly two choices and polls with at least three answers.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e6245fb5c541b785fd5d7` (2027-04-09), gold category exception_retirement
- user: I've got a minute now to explain what I mean about when I get news from the poll.
- assistant: How have you been thinking about it?
- user: I thought again about when I get news from the poll.  For polls offering more than two choices, let the default take over permanently instead of preserving its own separate preference.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m2", "evidence_ids": ["e6245fb5c541b785fd5d7"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e6245fb5c541b785fd5d7"], "operation": "RETIRE", "target_id": "m2"}], "decision": "resolved"}`

### `ee7881750119349a8a516` (2027-04-10), gold category scoped_exception
- user: I thought about when I get news from the poll again this morning.
- assistant: Did you want to say what you had in mind?
- user: Here's what I meant about when I get news from the poll.  My request is to save a ping on each incoming vote for polls with two possible answers. Make that the standing arrangement from this point ahead.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "group-poll update trigger", "value": "a ping on each incoming vote", "scope": "polls with two possible answers", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ee7881750119349a8a516"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "group-poll update trigger", "evidence_ids": ["ee7881750119349a8a516"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "polls with two possible answers", "validity": {"kind": "persistent"}, "value": "a ping on each incoming vote"}], "decision": "resolved"}`

### `ea8f03a2526d81a423cb2` (2027-04-12), gold category general_update
- user: I've got a minute now to explain what I mean about when I get news from the poll.
- assistant: Was something about getting an update before the poll closes especially important?
- user: I had a point to make about when I get news from the poll. Given ordinary occasions overall, make the choice a notice after every participant has voted. I mean an enduring arrangement rather than a one-off.
- assistant: Could you say why getting an update before the poll closes matters to you?
- user: I care about a change that actually tells me something about the vote.
- assistant: We can leave not seeing a notice for every small change there if you like.
- user: Let’s do that. That’s all I meant to bring up.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "a notice after every participant has voted", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["ea8f03a2526d81a423cb2"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ea8f03a2526d81a423cb2"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "a notice after every participant has voted"}], "decision": "resolved"}`

## 4. `te-0045/p18fbe6f4a0aa111b80e7/scope` (scoped_exception, boundary probe)

- Question (2027-08-12): Pick a value for unfinished-task handoff note, dated August 12, with the setting described as handoffs to a rotating group.
- Options: a spoken recap with a written pointer | a brief next-step sentence | a sketched dependency chain | a small done-and-pending grid
- Gold: **a brief next-step sentence**; Answer Agent chose: **a spoken recap with a written pointer**
- Answer Agent reply: "The record that applies on this date and in this situation is the one with the scope \"handing over a task to whoever is on rotation\" and the validity window from 2027-08-13 to 2027-09-01. Answer: a spoken recap with a written pointer"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "unfinished-task handoff note",
  "value": "a brief next-step sentence",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "unfinished-task handoff note",
  "value": "a spoken recap with a written pointer",
  "scope": "handing over a task to whoever is on rotation",
  "validity": {
   "from": "2027-08-13",
   "kind": "window",
   "to": "2027-09-01"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e6de045f43a853ea04d2a"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "unfinished-task handoff note",
  "value": "a brief next-step sentence",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "unfinished-task handoff note",
  "value": "a spoken recap with a written pointer",
  "scope": "handing over a task to whoever is on rotation",
  "validity": {
   "from": "2027-08-13",
   "kind": "window",
   "to": "2027-09-01"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e6de045f43a853ea04d2a"
  ]
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

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `e6de045f43a853ea04d2a` (2027-08-12), gold category scoped_exception
- user: I remembered something about what I leave for the next person while thinking about making the next step visible.
- assistant: Feel free to start with whatever's most useful.
- user: I thought again about what I leave for the next person.  When handing over a task to whoever is on rotation comes up, my choice is a spoken recap with a written pointer. Only occasions in August 13 to September 1, with both ends included, get this arrangement.
- assistant: There's room to talk more about making the next step visible if you want.
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "unfinished-task handoff note", "value": "a spoken recap with a written pointer", "scope": "handing over a task to whoever is on rotation", "validity": {"from": "2027-08-13", "kind": "window", "to": "2027-09-01"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e6de045f43a853ea04d2a"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "unfinished-task handoff note", "evidence_ids": ["e6de045f43a853ea04d2a"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "handing over a task to whoever is on rotation", "validity": {"from": "2027-08-13", "kind": "window", "to": "2027-09-01"}, "value": "a spoken recap with a written pointer"}], "decision": "resolved"}`

## 5. `te-0045/p46d0d817f4c8720401e9/scope` (exception_revision, default probe)

- Question (2027-08-13): Pick a value for unfinished-task handoff note, dated August 13, with the setting described as an ordinary occasion.
- Options: a small done-and-pending grid | a brief next-step sentence | a spoken recap with a written pointer | a sketched dependency chain
- Gold: **a brief next-step sentence**; Answer Agent chose: **a sketched dependency chain**
- Answer Agent reply: "The record that applies on this date and in this situation is the one with the window validity from 2027-08-13 to 2027-09-01, which specifies \"a quick drawing of what depends on what\" for task handoff during a handing-over scenario.  \nAnswer: a sketched dependency chain"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "unfinished-task handoff note",
  "value": "a brief next-step sentence",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "unfinished-task handoff note",
  "value": "a quick drawing of what depends on what",
  "scope": "handing over a task to whoever is on rotation",
  "validity": {
   "from": "2027-08-13",
   "kind": "window",
   "to": "2027-09-01"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "eabe912bdf6e216e3fc79"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "unfinished-task handoff note",
  "value": "a brief next-step sentence",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "unfinished-task handoff note",
  "value": "a quick drawing of what depends on what",
  "scope": "handing over a task to whoever is on rotation",
  "validity": {
   "from": "2027-08-13",
   "kind": "window",
   "to": "2027-09-01"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "eabe912bdf6e216e3fc79"
  ]
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

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `e6de045f43a853ea04d2a` (2027-08-12), gold category scoped_exception
- user: I remembered something about what I leave for the next person while thinking about making the next step visible.
- assistant: Feel free to start with whatever's most useful.
- user: I thought again about what I leave for the next person.  When handing over a task to whoever is on rotation comes up, my choice is a spoken recap with a written pointer. Only occasions in August 13 to September 1, with both ends included, get this arrangement.
- assistant: There's room to talk more about making the next step visible if you want.
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "unfinished-task handoff note", "value": "a spoken recap with a written pointer", "scope": "handing over a task to whoever is on rotation", "validity": {"from": "2027-08-13", "kind": "window", "to": "2027-09-01"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e6de045f43a853ea04d2a"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "unfinished-task handoff note", "evidence_ids": ["e6de045f43a853ea04d2a"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "handing over a task to whoever is on rotation", "validity": {"from": "2027-08-13", "kind": "window", "to": "2027-09-01"}, "value": "a spoken recap with a written pointer"}], "decision": "resolved"}`

### `eabe912bdf6e216e3fc79` (2027-08-13), gold category exception_revision
- user: Can we get back to what I leave for the next person?  Let the arrangement be a quick drawing of what depends on what when the situation is handoffs to a rotating group. It is a dated exception, beginning August 13 and ending with September 1, both included.
- assistant: How has making the next step visible worked out in practice?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "a quick drawing of what depends on what", "scope": "handing over a task to whoever is on rotation", "validity": {"from": "2027-08-13", "kind": "window", "to": "2027-09-01"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["eabe912bdf6e216e3fc79"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["eabe912bdf6e216e3fc79"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "handing over a task to whoever is on rotation", "target_id": "m2", "validity": {"from": "2027-08-13", "kind": "window", "to": "2027-09-01"}, "value": "a quick drawing of what depends on what"}], "decision": "resolved"}`

## 6. `te-0047/pe37747263dca2557ed30/scope` (scoped_exception, boundary probe)

- Question (2027-03-29): Pick a value for supper grain accompaniment, dated March 29, with the setting described as suppers served from a single pot.
- Options: fluffy steamed millet | toasted pearl barley | nutty whole buckwheat groats | soft lemon-scented couscous
- Gold: **toasted pearl barley**; Answer Agent chose: **fluffy steamed millet**
- Answer Agent reply: "The record that applies on this date and in this situation is m3, which specifies \"fluffy steamed millet\" for suppers served from one pot between March 8 and March 28, 2027.  \nAnswer: fluffy steamed millet"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "supper grain accompaniment",
  "value": "toasted pearl barley",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "supper grain accompaniment",
  "value": "soft lemon-scented couscous",
  "scope": "suppers served from separate pans",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "supper grain accompaniment",
  "value": "fluffy steamed millet",
  "scope": "a supper served from one pot",
  "validity": {
   "from": "2027-03-08",
   "kind": "window",
   "to": "2027-03-28"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e1be3efd59a5d52f85163"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "supper grain accompaniment",
  "value": "toasted pearl barley",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "supper grain accompaniment",
  "value": "soft lemon-scented couscous",
  "scope": "suppers served from separate pans",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "supper grain accompaniment",
  "value": "fluffy steamed millet",
  "scope": "a supper served from one pot",
  "validity": {
   "from": "2027-03-08",
   "kind": "window",
   "to": "2027-03-28"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e1be3efd59a5d52f85163"
  ]
 }
]
```

Events up to the probe:

### `e1be3efd59a5d52f85163` (2027-03-08), gold category scoped_exception
- user: What sits well alongside the main dish has been on my mind. Can we get back to which grain I serve with supper?
- assistant: What would you like to work through first?
- user: I had a point to make about which grain I serve with supper. Let the arrangement be fluffy steamed millet when the situation is a supper served from one pot. This temporary spell runs from the start of March 8 to the end of March 28. Anything outside this request keeps the choices it already had.
- assistant: Could you say why what sits well alongside the main dish matters to you?
- user: I want the side to sit well with the main dish without covering the flavor.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "supper grain accompaniment", "value": "fluffy steamed millet", "scope": "a supper served from one pot", "validity": {"from": "2027-03-08", "kind": "window", "to": "2027-03-28"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e1be3efd59a5d52f85163"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "supper grain accompaniment", "evidence_ids": ["e1be3efd59a5d52f85163"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "a supper served from one pot", "validity": {"from": "2027-03-08", "kind": "window", "to": "2027-03-28"}, "value": "fluffy steamed millet"}], "decision": "resolved"}`

## 7. `te-0056/p8ed277f446291305f98b/scope` (stable_preference, target probe)

- Question (2027-02-14): Pick a value for museum visit starting point, dated February 14, with the setting described as museum visits on an upper-floor ticket.
- Options: starting with the smallest gallery | starting with the central installation | starting with the oldest display | starting with the newest acquisition
- Gold: **starting with the smallest gallery**; Answer Agent chose: **starting with the tiniest gallery**
- Answer Agent reply: "The record that applies on this date and in this situation is m4, which specifies \"the tiniest gallery comes first\" for museum visits on an upper-floor ticket.  \nAnswer: starting with the tiniest gallery"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m3",
  "attribute": "museum visit starting point",
  "value": "starting with the oldest display",
  "scope": "museum visits on a ground-floor ticket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "museum visit starting point",
  "value": "the tiniest gallery comes first",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "edd90b7ed36711ea16aa7"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "museum visit starting point",
  "value": "starting with the smallest gallery",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "e59f47d93ee4b56819b5e"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m3",
  "attribute": "museum visit starting point",
  "value": "starting with the oldest display",
  "scope": "museum visits on a ground-floor ticket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "museum visit starting point",
  "value": "the tiniest gallery comes first",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "edd90b7ed36711ea16aa7"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "museum visit starting point",
  "value": "starting with the smallest gallery",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "e59f47d93ee4b56819b5e"
  ]
 }
]
```

Events up to the probe:

### `edd90b7ed36711ea16aa7` (2027-02-10), gold category exception_revision
- user: The displays nearest the stairs has been on my mind. Can we get back to which part of the exhibition I see first?
- assistant: Feel free to start with whatever's most useful.
- user: Here's what I meant about museum visit starting point.  It is the tiniest gallery comes first that I want for museum visits on an upper-floor ticket. Not permanently, and not just this time: it continues provisionally with no closing date.
- assistant: What's your biggest concern around the displays nearest the stairs?
- user: It helps me to pick a starting point before I get caught up looking around.
- assistant: Do you have another thought on what there is time to see first?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "the tiniest gallery comes first", "scope": "museum visits on an upper-floor ticket", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["edd90b7ed36711ea16aa7"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["edd90b7ed36711ea16aa7"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "museum visits on an upper-floor ticket", "target_id": "m2", "validity": {"kind": "open"}, "value": "the tiniest gallery comes first"}], "decision": "resolved"}`

### `ee21ef763e5ed9fb808e6` (2027-02-12), gold category general_update
- user: I remembered something about which part of the exhibition I see first while thinking about what there is time to see first.
- assistant: What would you like to work through first?
- user: I thought again about which part of the exhibition I see first.  I would put starting with the newest acquisition first for the everyday situation. This is for the long run rather than a temporary spell.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "starting with the newest acquisition", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["ee21ef763e5ed9fb808e6"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ee21ef763e5ed9fb808e6"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "starting with the newest acquisition"}], "decision": "resolved"}`

### `e59f47d93ee4b56819b5e` (2027-02-13), gold category general_update
- user: I've got a minute now to explain what I mean about which part of the exhibition I see first.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to which part of the exhibition I see first?  It is starting with the smallest gallery that I want for everyday use with no dedicated arrangement. That goes for the occasions ahead, with no finishing point.
- assistant: Is there a connection with how to begin walking around the exhibition?
- user: It helps me to pick a starting point before I get caught up looking around.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m5", "value": "starting with the smallest gallery", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e59f47d93ee4b56819b5e"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e59f47d93ee4b56819b5e"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m5", "validity": {"kind": "persistent"}, "value": "starting with the smallest gallery"}], "decision": "resolved"}`

### `e552f98e9720550389d97` (2027-02-14), gold category stable_preference
- user: I thought about which part of the exhibition I see first again this morning.
- assistant: I see why this could come up while thinking about what there is time to see first.
- user: It helps me to pick a starting point before I get caught up looking around.
- assistant: What would you like to work through first?
- user: Can we get back to museum visit starting point?  An acquaintance was saying, "Keep starting with the newest acquisition in mind as the choice I am making for museum visits on an upper-floor ticket. I need it for a while rather than once, and rather than forever. No end is fixed." I am leaving my own arrangements as they are.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 8. `te-0065/p209f8e1c9131f23cbcca/scope` (stable_preference, neighbor probe)

- Question (2027-03-11): Pick a value for museum visit starting point, dated March 11, with the setting described as museum visits on a ground-floor ticket.
- Options: starting with the smallest gallery | starting with the oldest display | starting with the central installation | starting with the newest acquisition
- Gold: **starting with the central installation**; Answer Agent chose: **starting with the smallest gallery**
- Answer Agent reply: "No record specifically applies to \"museum visits on a ground-floor ticket\" on March 11, 2027, as the relevant records are limited to \"upper-floor ticket\" and \"lower floor\" tickets. Therefore, the general preference applies.  \nAnswer: starting with the smallest gallery"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "lodging unpacking routine",
  "value": "clothes folded on an open luggage shelf",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "museum visit starting point",
  "value": "starting with the smallest gallery",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "museum visit starting point",
  "value": "starting with the central installation",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "museum visit starting point",
  "value": "starting with the central installation",
  "scope": "a museum ticket for the lower floor",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e81790ab64cffb0f28992"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "lodging unpacking routine",
  "value": "clothes folded on an open luggage shelf",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "museum visit starting point",
  "value": "starting with the smallest gallery",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "museum visit starting point",
  "value": "starting with the central installation",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "museum visit starting point",
  "value": "starting with the central installation",
  "scope": "a museum ticket for the lower floor",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e81790ab64cffb0f28992"
  ]
 }
]
```

Events up to the probe:

### `e8fa8b81b42cf6a0b1fdf` (2027-03-09), gold category exception_retirement
- user: Here's what I meant about which part of the exhibition I see first.  The distinction we used for museum visits on a ground-floor ticket is over; whatever my usual choice becomes should apply there too.
- assistant: How did how to begin walking around the exhibition get on your mind?
- user: It helps me to pick a starting point before I get caught up looking around.
- assistant: We can leave the displays nearest the stairs there if you like.
- user: Let’s do that. That’s all I meant to bring up.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m4", "evidence_ids": ["e8fa8b81b42cf6a0b1fdf"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e8fa8b81b42cf6a0b1fdf"], "operation": "RETIRE", "target_id": "m4"}], "decision": "resolved"}`

### `e81790ab64cffb0f28992` (2027-03-10), gold category scoped_exception
- user: I thought again about which part of the exhibition I see first.  Here is where I have landed: starting with the central installation, for a museum ticket for the lower floor. That goes for the occasions ahead, with no finishing point.
- assistant: Tell me what struck you about what there is time to see first.
- user: It helps me to pick a starting point before I get caught up looking around.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "museum visit starting point", "value": "starting with the central installation", "scope": "a museum ticket for the lower floor", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m2"}], "evidence_ids": ["e81790ab64cffb0f28992"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "museum visit starting point", "evidence_ids": ["e81790ab64cffb0f28992"], "operation": "ADD", "relations": [{"target": "m2", "type": "EXCEPTION_TO"}], "scope": "a museum ticket for the lower floor", "validity": {"kind": "persistent"}, "value": "starting with the central installation"}], "decision": "resolved"}`

### `e3b2dbc2a4a77208fcbe3` (2027-03-11), gold category stable_preference
- user: I thought about which part of the exhibition I see first again this morning.
- assistant: I'm listening. What's on your mind?
- user: I thought again about which part of the exhibition I see first.  One occasion of a museum ticket to the level upstairs, one use of the oldest exhibit comes first. The ongoing arrangement stays as it was.
- assistant: What would make how to begin walking around the exhibition easier to deal with?
- user: It helps me to pick a starting point before I get caught up looking around.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 9. `te-0070/p08a31f6a6821dda031c6/scope` (scoped_exception, target probe)

- Question (2027-07-14): Pick a value for step-drill hand position, dated July 14, with the setting described as step drills using a medium platform.
- Options: fingertips resting on opposite shoulders | hands loosely joined behind the back | arms hanging with palms facing inward | hands lightly resting at the waist
- Gold: **fingertips resting on opposite shoulders**; Answer Agent chose: **hands lightly resting at the waist**
- Answer Agent reply: "On 2027-07-14, with the setting of step drills using a medium platform, the record that applies is the one specifying \"fingertips touching the opposite shoulders\" for step drills using a low platform, which is an exception to the general rule and applies during the window from 2027-07-12 to 2027-07-25. However, since \"medium platform\" is not explicitly covered in the records, and the only relevant exception is for a \"low platform,\" and no record explicitly covers a \"medium platform,\" the general preference should be used. Therefore, the correct value is \"hands lightly resting at the waist.\"  \nAnswer: hands lightly resting at the waist"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m2",
  "attribute": "step-drill hand position",
  "value": "hands lightly resting at the waist",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e1f8fdbda0969add68cd1"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "step-drill hand position",
  "value": "fingertips touching the opposite shoulders",
  "scope": "step drills using a low platform",
  "validity": {
   "from": "2027-07-12",
   "kind": "window",
   "to": "2027-07-25"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "ed1c35b6671a11c85c533"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "step-drill hand position",
  "value": "fingertips touching the opposite shoulders",
  "scope": "stepping on the middle-height platform",
  "validity": {
   "from": "2027-07-14",
   "kind": "window",
   "to": "2027-08-04"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e9f8a456368a644aebfd1"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m2",
  "attribute": "step-drill hand position",
  "value": "hands lightly resting at the waist",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e1f8fdbda0969add68cd1"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "step-drill hand position",
  "value": "fingertips touching the opposite shoulders",
  "scope": "step drills using a low platform",
  "validity": {
   "from": "2027-07-12",
   "kind": "window",
   "to": "2027-07-25"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "ed1c35b6671a11c85c533"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "step-drill hand position",
  "value": "fingertips touching the opposite shoulders",
  "scope": "stepping on the middle-height platform",
  "validity": {
   "from": "2027-07-14",
   "kind": "window",
   "to": "2027-08-04"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e9f8a456368a644aebfd1"
  ]
 }
]
```

Events up to the probe:

### `e1f8fdbda0969add68cd1` (2027-07-10), gold category general_update
- user: Can we get back to step-drill hand position?  I am settling the question of the general everyday case with hands lightly resting at the waist. Make that the standing arrangement from this point ahead.
- assistant: How did where your arms naturally fall get on your mind?
- user: I can feel myself go off balance when I am thinking about where my arms are.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "hands lightly resting at the waist", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e1f8fdbda0969add68cd1"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e1f8fdbda0969add68cd1"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "hands lightly resting at the waist"}], "decision": "resolved"}`

### `ed1c35b6671a11c85c533` (2027-07-11), gold category scoped_exception
- user: I remembered something about what I do with my hands on the step while thinking about where your arms naturally fall.
- assistant: Of course. We can talk about where your arms naturally fall.
- user: I thought again about step-drill hand position.  Use this choice for step drills using a low platform: fingertips touching the opposite shoulders. Its first day is July 12; July 25 is included as the last, and then it is over.
- assistant: Have you been noticing anything new about where your arms naturally fall?
- user: I can feel myself go off balance when I am thinking about where my arms are.
- assistant: Do you have another thought on keeping your balance as you step up?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "step-drill hand position", "value": "fingertips touching the opposite shoulders", "scope": "step drills using a low platform", "validity": {"from": "2027-07-12", "kind": "window", "to": "2027-07-25"}, "relations": [{"type": "EXCEPTION_TO", "target": "m2"}], "evidence_ids": ["ed1c35b6671a11c85c533"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "step-drill hand position", "evidence_ids": ["ed1c35b6671a11c85c533"], "operation": "ADD", "relations": [{"target": "m2", "type": "EXCEPTION_TO"}], "scope": "step drills using a low platform", "validity": {"from": "2027-07-12", "kind": "window", "to": "2027-07-25"}, "value": "fingertips touching the opposite shoulders"}], "decision": "resolved"}`

### `e9f8a456368a644aebfd1` (2027-07-13), gold category scoped_exception
- user: I thought again about what I do with my hands on the step.  Use this choice for stepping on the middle-height platform: fingertips touching the opposite shoulders. The first included date is July 14; it runs until August 4 has finished, then I want the usual arrangement back.
- assistant: I'm curious about getting off the platform without reaching for anything, too.
- user: I can feel myself go off balance when I am thinking about where my arms are.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "step-drill hand position", "value": "fingertips touching the opposite shoulders", "scope": "stepping on the middle-height platform", "validity": {"from": "2027-07-14", "kind": "window", "to": "2027-08-04"}, "relations": [{"type": "EXCEPTION_TO", "target": "m2"}], "evidence_ids": ["e9f8a456368a644aebfd1"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "step-drill hand position", "evidence_ids": ["e9f8a456368a644aebfd1"], "operation": "ADD", "relations": [{"target": "m2", "type": "EXCEPTION_TO"}], "scope": "stepping on the middle-height platform", "validity": {"from": "2027-07-14", "kind": "window", "to": "2027-08-04"}, "value": "fingertips touching the opposite shoulders"}], "decision": "resolved"}`

## 10. `te-0071/pa3c369340750a026f03c/scope` (stable_preference, target probe)

- Question (2027-02-04): Pick a value for bath-towel border style, dated February 4, with the setting described as towels hung on a wall hook.
- Options: a soft fringed edge without a band | a doubled terry border with rounded corners | a narrow woven herringbone border | a broad flat linen border
- Gold: **a doubled terry border with rounded corners**; Answer Agent chose: **a narrow woven herringbone border**
- Answer Agent reply: "The record that applies on this date and in the situation of towels hung on a wall hook is the one with a narrow woven herringbone border, as it is specifically limited to \"towels hung across a rail\" and thus relevant to a similar hanging context.  \nAnswer: a narrow woven herringbone border"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "bath-towel border style",
  "value": "a doubled terry border with rounded corners",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "bath-towel border style",
  "value": "a narrow woven herringbone border",
  "scope": "towels hung across a rail",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "bath-towel border style",
  "value": "a doubled terry border with rounded corners",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "bath-towel border style",
  "value": "a narrow woven herringbone border",
  "scope": "towels hung across a rail",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 }
]
```

Events up to the probe:

### `e2083bf4ceae35602b33c` (2027-02-02), gold category exception_retirement
- user: I've got a minute now to explain what I mean about the edge finish on the bath towel.
- assistant: How have you been thinking about it?
- user: Can we get back to the edge finish on the bath towel?  For drying the towel on a hook, let the default take over permanently instead of preserving its own separate preference.
- assistant: Could you say why finding the right towel from its border matters to you?
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m3", "evidence_ids": ["e2083bf4ceae35602b33c"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e2083bf4ceae35602b33c"], "operation": "RETIRE", "target_id": "m3"}], "decision": "resolved"}`

### `e22e558329b5d4eda92db` (2027-02-03), gold category clarify
- user: Can we get back to the edge finish on the bath towel?  I am torn about where a wide smooth linen strip should apply, with drying the towel over a bar on one side and towels hung on a wall hook on the other.
- assistant: What do you tend to notice first about whether the fringe catches on the hook?
- user: I use the edge to tell which towel is which in a stack.
- assistant: Would you prefer to talk more about how the edge sits on the rail another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e63a9349ea9e757d4b9c5` (2027-02-04), gold category stable_preference
- user: There was one thing about the edge finish on the bath towel I wanted to talk through.
- assistant: What's your impression of whether the fringe catches on the hook so far?
- user: I use the edge to tell which towel is which in a stack.
- assistant: How have you been thinking about it?
- user: I thought again about bath-towel border style.  An acquaintance was saying, "A broad flat linen border is the one I want when we are talking about towels hung on a wall hook. That is what I always want under those circumstances." I am leaving my own arrangements as they are.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 11. `te-0077/pc15d2547c5d511ad1619/scope` (general_update, target probe)

- Question (2027-05-07): Pick a value for mobility drill rhythm, dated May 7, with the setting described as an ordinary occasion.
- Options: two gentle movements per breathing cycle | a smooth continuous uncounted motion | one slow movement per exhale | three small pulses followed by a pause
- Gold: **two gentle movements per breathing cycle**; Answer Agent chose: **one slow movement per exhale**
- Answer Agent reply: "The general preference for mobility drill rhythm applies on this date and in this situation.  \nAnswer: one slow movement per exhale"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m2",
  "attribute": "mobility drill rhythm",
  "value": "a pair of easy movements per full breath",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e0576099582bfe81885f1"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m2",
  "attribute": "mobility drill rhythm",
  "value": "a pair of easy movements per full breath",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e0576099582bfe81885f1"
  ]
 }
]
```

Events up to the probe:

### `e0576099582bfe81885f1` (2027-05-07), gold category general_update
- user: I've got a minute now to explain what I mean about the pace for mobility work.
- assistant: Feel free to start with whatever's most useful.
- user: Can we get back to the pace for mobility work?  Here is where I have landed: a pair of easy movements per full breath, for regular occasions without a special choice. I want to keep coming back to that choice, not try it once.
- assistant: Is there a connection with finding a pace without pushing too hard?
- user: It feels easier when I am not counting and moving at the same time.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "a pair of easy movements per full breath", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e0576099582bfe81885f1"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e0576099582bfe81885f1"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "a pair of easy movements per full breath"}], "decision": "resolved"}`

## 12. `te-0093/pe1d7ff4ad981f0b58b6c/scope` (exception_revision, target probe)

- Question (2027-07-17): Pick a value for scratch-paper use pattern, dated July 17, with the setting described as rough calculations at a seated desk.
- Options: calculations arranged around a central sketch | one calculation per loose square | calculations on folded pocket slips | several calculations in a spiral column
- Gold: **calculations on folded pocket slips**; Answer Agent chose: **one calculation per loose square**
- Answer Agent reply: "The record that applies on July 17, 2027, for rough calculations at a seated desk is \"one calculation per loose square,\" as it matches the specified situation and date range, and is explicitly limited to that context.  \nAnswer: one calculation per loose square"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "scratch-paper use pattern",
  "value": "several calculations in a spiral column",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "scratch-paper use pattern",
  "value": "one calculation per loose square",
  "scope": "rough calculations at a standing desk",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "scratch-paper use pattern",
  "value": "doing the math on little folded slips",
  "scope": "working out sums while sitting at the desk",
  "validity": {
   "from": "2027-07-06",
   "kind": "window",
   "to": "2027-07-17"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "ec6fd2da78dd6f3e76441"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "scratch-paper use pattern",
  "value": "several calculations in a spiral column",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "scratch-paper use pattern",
  "value": "one calculation per loose square",
  "scope": "rough calculations at a standing desk",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "scratch-paper use pattern",
  "value": "doing the math on little folded slips",
  "scope": "working out sums while sitting at the desk",
  "validity": {
   "from": "2027-07-06",
   "kind": "window",
   "to": "2027-07-17"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "ec6fd2da78dd6f3e76441"
  ]
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

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `e5ceec10fbcb56bdb5737` (2027-07-05), gold category scoped_exception
- user: Being able to follow sums on a small scrap has been on my mind. Can we get back to how I lay out working on spare paper?
- assistant: What would you like to work through first?
- user: Here's what I meant about how I lay out working on spare paper.  Keep working spread around a sketch in the middle in mind as the choice I am making for working out sums while sitting at the desk. It is a dated exception, beginning July 6 and ending with July 17, both included.
- assistant: What did you find difficult about being able to follow sums on a small scrap?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "scratch-paper use pattern", "value": "working spread around a sketch in the middle", "scope": "working out sums while sitting at the desk", "validity": {"from": "2027-07-06", "kind": "window", "to": "2027-07-17"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e5ceec10fbcb56bdb5737"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "scratch-paper use pattern", "evidence_ids": ["e5ceec10fbcb56bdb5737"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "working out sums while sitting at the desk", "validity": {"from": "2027-07-06", "kind": "window", "to": "2027-07-17"}, "value": "working spread around a sketch in the middle"}], "decision": "resolved"}`

### `ec6fd2da78dd6f3e76441` (2027-07-06), gold category exception_revision
- user: There was one thing about how I lay out working on spare paper I wanted to talk through.
- assistant: Feel free to start with whatever's most useful.
- user: Here's what I meant about how I lay out working on spare paper.  Use this choice for rough calculations at a seated desk: doing the math on little folded slips. The request covers July 6 and continues through July 17; then my normal preference takes over. Anything outside this request keeps the choices it already had.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "doing the math on little folded slips", "scope": "working out sums while sitting at the desk", "validity": {"from": "2027-07-06", "kind": "window", "to": "2027-07-17"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ec6fd2da78dd6f3e76441"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ec6fd2da78dd6f3e76441"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "working out sums while sitting at the desk", "target_id": "m3", "validity": {"from": "2027-07-06", "kind": "window", "to": "2027-07-17"}, "value": "doing the math on little folded slips"}], "decision": "resolved"}`

## 13. `te-0094/p6c9c2499928054b3a0d2/scope` (scoped_exception, neighbor probe)

- Question (2027-12-10): Pick a value for scratch-paper use pattern, dated December 10, with the setting described as rough calculations at a standing desk.
- Options: calculations on folded pocket slips | several calculations in a spiral column | calculations arranged around a central sketch | one calculation per loose square
- Gold: **calculations arranged around a central sketch**; Answer Agent chose: **several calculations in a spiral column**
- Answer Agent reply: "The record that applies on this date and in this situation is the window-record \"several calculations in a spiral column\" from 2027-12-10 to 2027-12-27, which pertains to working out sums while sitting at the desk, but not specifically to standing desks or rough calculations. Answer: several calculations in a spiral column"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "scratch-paper use pattern",
  "value": "calculations arranged around a central sketch",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "scratch-paper use pattern",
  "value": "several calculations in a spiral column first",
  "scope": "working out sums while sitting at the desk",
  "validity": {
   "from": "2027-12-10",
   "kind": "window",
   "to": "2027-12-27"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e7202f27835bae6594644"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "scratch-paper use pattern",
  "value": "calculations arranged around a central sketch",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "scratch-paper use pattern",
  "value": "several calculations in a spiral column",
  "scope": "working out sums while sitting at the desk",
  "validity": {
   "from": "2027-12-10",
   "kind": "window",
   "to": "2027-12-27"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e7202f27835bae6594644"
  ]
 }
]
```

Events up to the probe:

### `e19a5778ccf1c67f8237a` (2027-12-07), gold category scoped_exception
- user: Being able to follow sums on a small scrap has been on my mind. Can we get back to how I lay out working on spare paper?
- assistant: Of course. We can talk about being able to follow sums on a small scrap.
- user: I had a point to make about how I lay out working on spare paper. Keep calculations on folded pocket slips in mind as the choice I am making for working out sums on my feet at the desk. The dates are December 8 through December 23, with both counted; after that I am back to the ordinary choice.
- assistant: Tell me what struck you about being able to follow sums on a small scrap.
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "scratch-paper use pattern", "value": "calculations on folded pocket slips", "scope": "working out sums on my feet at the desk", "validity": {"from": "2027-12-08", "kind": "window", "to": "2027-12-23"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e19a5778ccf1c67f8237a"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "scratch-paper use pattern", "evidence_ids": ["e19a5778ccf1c67f8237a"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "working out sums on my feet at the desk", "validity": {"from": "2027-12-08", "kind": "window", "to": "2027-12-23"}, "value": "calculations on folded pocket slips"}], "decision": "resolved"}`

### `e50551457d5cb876da398` (2027-12-08), gold category exception_retirement
- user: I thought about how I lay out working on spare paper again this morning.
- assistant: Was something about room to draw the rough shape first especially important?
- user: I had a point to make about how I lay out working on spare paper. The special case for working out sums on my feet at the desk can go. I want those occasions to use the ordinary choice from here ahead.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m2", "evidence_ids": ["e50551457d5cb876da398"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e50551457d5cb876da398"], "operation": "RETIRE", "target_id": "m2"}], "decision": "resolved"}`

### `e7202f27835bae6594644` (2027-12-10), gold category scoped_exception
- user: I had a point to make about how I lay out working on spare paper. I would put several calculations in a spiral column first for working out sums while sitting at the desk. This temporary spell runs from the start of December 10 to the end of December 27. Leave the other arrangements alone.
- assistant: Have you been noticing anything new about being able to follow sums on a small scrap?
- user: I need to look back at the working without losing which sum is which.
- assistant: Do you have another thought on being able to follow sums on a small scrap?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "scratch-paper use pattern", "value": "several calculations in a spiral column", "scope": "working out sums while sitting at the desk", "validity": {"from": "2027-12-10", "kind": "window", "to": "2027-12-27"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e7202f27835bae6594644"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "scratch-paper use pattern", "evidence_ids": ["e7202f27835bae6594644"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "working out sums while sitting at the desk", "validity": {"from": "2027-12-10", "kind": "window", "to": "2027-12-27"}, "value": "several calculations in a spiral column first"}], "decision": "resolved"}`

## 14. `te-0100/pd0edcfa4b6ef4438ae5b/scope` (stable_preference, target probe)

- Question (2027-03-17): Pick a value for sweater cuff construction, dated March 17, with the setting described as sweaters worn beneath a jacket.
- Options: a broad turned-back cuff | a close rib-knit cuff | a tapered split-knit cuff | a loose rolled-edge cuff
- Gold: **a broad turned-back cuff**; Answer Agent chose: **a close rib-knit cuff**
- Answer Agent reply: "The record that applies on March 17, 2027, for sweaters worn beneath a jacket is \"a snug ribbed wrist cuff.\"  \nAnswer: a snug ribbed wrist cuff"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m6",
  "attribute": "sweater cuff construction",
  "value": "a tapered split-knit cuff",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e7fe06c209a068820042d"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "sweater cuff construction",
  "value": "a close rib-knit cuff",
  "scope": "sweaters worn without a jacket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "e4ce919f212163b7bef10"
  ]
 },
 {
  "memory_id": "m8",
  "attribute": "sweater cuff construction",
  "value": "a snug ribbed wrist cuff",
  "scope": "sweaters worn beneath a jacket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "ee168632782743f5b96fb"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m3",
  "attribute": "sweater cuff construction",
  "value": "a broad turned-back cuff",
  "scope": "sweaters worn beneath a jacket",
  "validity": {
   "from": "2027-03-11",
   "kind": "window",
   "to": "2027-03-30"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "eb90d57941164f6d366fa"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "sweater cuff construction",
  "value": "a tapered split-knit cuff",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e7fe06c209a068820042d"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "sweater cuff construction",
  "value": "a close rib-knit cuff",
  "scope": "sweaters worn without a jacket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "e4ce919f212163b7bef10"
  ]
 }
]
```

Events up to the probe:

### `e962860b91fefb5226174` (2027-03-09), gold category stable_preference
- user: I remembered something about what I want at the sweater wrist while thinking about keeping the edge from turning inside out.
- assistant: Of course. We can talk about keeping the edge from turning inside out.
- user: I thought again about sweater cuff construction.  Here is a hypothetical to think about: "I am stuck on the situation for a wide cuff folded back: sweaters worn without a jacket and sweaters worn beneath a jacket are both still in the running." It is not permission to change my preferences.
- assistant: How has keeping the edge from turning inside out worked out in practice?
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `eb90d57941164f6d366fa` (2027-03-10), gold category scoped_exception
- user: I thought again about what I want at the sweater wrist.  Given sweaters worn beneath a jacket, make the choice a broad turned-back cuff. The request covers March 11 and continues through March 30; then my normal preference takes over. Anything outside this request keeps the choices it already had.
- assistant: What's your biggest concern around keeping the edge from turning inside out?
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "sweater cuff construction", "value": "a broad turned-back cuff", "scope": "sweaters worn beneath a jacket", "validity": {"from": "2027-03-11", "kind": "window", "to": "2027-03-30"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["eb90d57941164f6d366fa"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "sweater cuff construction", "evidence_ids": ["eb90d57941164f6d366fa"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "sweaters worn beneath a jacket", "validity": {"from": "2027-03-11", "kind": "window", "to": "2027-03-30"}, "value": "a broad turned-back cuff"}], "decision": "resolved"}`

### `ee3bc2bb33b830b03414a` (2027-03-12), gold category general_update
- user: Can we get back to what I want at the sweater wrist?  When ordinary occasions overall comes up, my choice is a close rib-knit cuff. This should carry on; it is not just a test.
- assistant: How has keeping the edge from turning inside out worked out in practice?
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "a close rib-knit cuff", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["ee3bc2bb33b830b03414a"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ee3bc2bb33b830b03414a"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "a close rib-knit cuff"}], "decision": "resolved"}`

### `e33f0e3a6bfbda47b8e3a` (2027-03-13), gold category exception_revision
- user: I had a point to make about sweater cuff construction. The option I am selecting where sweaters worn without a jacket is concerned is a broad turned-back cuff. I want to keep coming back to that choice, not try it once.
- assistant: What would make keeping the edge from turning inside out easier to deal with?
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "a broad turned-back cuff", "scope": "sweaters worn without a jacket", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m4"}], "evidence_ids": ["e33f0e3a6bfbda47b8e3a"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e33f0e3a6bfbda47b8e3a"], "operation": "REVISE", "relations": [{"target": "m4", "type": "EXCEPTION_TO"}], "scope": "sweaters worn without a jacket", "target_id": "m2", "validity": {"kind": "persistent"}, "value": "a broad turned-back cuff"}], "decision": "resolved"}`

### `e7fe06c209a068820042d` (2027-03-14), gold category general_update
- user: There was one thing about what I want at the sweater wrist I wanted to talk through.
- assistant: Of course. We can talk about how bulky the cuff feels under a jacket.
- user: I thought again about what I want at the sweater wrist.  My request is to save a tapered split-knit cuff for the general choice rather than a special case. I want to keep coming back to that choice, not try it once.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m4", "value": "a tapered split-knit cuff", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e7fe06c209a068820042d"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e7fe06c209a068820042d"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m4", "validity": {"kind": "persistent"}, "value": "a tapered split-knit cuff"}], "decision": "resolved"}`

### `e3edc5a7cb30edd2afd94` (2027-03-15), gold category clarify
- user: I thought about what I want at the sweater wrist again this morning.
- assistant: Of course. We can talk about keeping the edge from turning inside out.
- user: Here's what I meant about sweater cuff construction.  I have not sorted out the intended setting for a close rib-knit cuff. Wearing the sweater by itself and sweaters worn beneath a jacket are the possibilities.
- assistant: Tell me what struck you about keeping the edge from turning inside out.
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e4ce919f212163b7bef10` (2027-03-16), gold category exception_revision
- user: I've got a minute now to explain what I mean about what I want at the sweater wrist.
- assistant: Of course. We can talk about how bulky the cuff feels under a jacket.
- user: Can we get back to what I want at the sweater wrist?  My request is to save a close rib-knit cuff for sweaters worn without a jacket. I want to keep coming back to that choice, not try it once.
- assistant: What would make how bulky the cuff feels under a jacket easier to deal with?
- user: I notice the cuff mostly when I take the jacket off.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m5", "value": "a close rib-knit cuff", "scope": "sweaters worn without a jacket", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m6"}], "evidence_ids": ["e4ce919f212163b7bef10"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e4ce919f212163b7bef10"], "operation": "REVISE", "relations": [{"target": "m6", "type": "EXCEPTION_TO"}], "scope": "sweaters worn without a jacket", "target_id": "m5", "validity": {"kind": "persistent"}, "value": "a close rib-knit cuff"}], "decision": "resolved"}`

### `ee168632782743f5b96fb` (2027-03-17), gold category stable_preference
- user: Can we get back to what I want at the sweater wrist?  For the next instance of sweaters worn beneath a jacket, I need to pick something. That's the only one I'm thinking about.
- assistant: Have you been noticing anything new about getting a loose sleeve to sit at the wrist?
- user: I notice the cuff mostly when I take the jacket off.
- assistant: What's the choice you'd make?
- user: For me it'd be a snug ribbed wrist cuff.
- assistant: Are you happy to stop there about getting a loose sleeve to sit at the wrist?
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ee168632782743f5b96fb"], "operation": "REVISE", "relations": [{"target": "m6", "type": "EXCEPTION_TO"}], "scope": "sweaters worn beneath a jacket", "target_id": "m3", "validity": {"kind": "persistent"}, "value": "a snug ribbed wrist cuff"}], "decision": "resolved"}`

## 15. `te-0103/pcdc65e30f69972bf33cd/scope` (stable_preference, default probe)

- Question (2027-10-09): Pick a value for figure caption alignment, dated October 9, with the setting described as an ordinary occasion.
- Options: captions indented beneath the figure center | captions centered under the figure | captions aligned to a narrow right column | captions flush with the figure's left edge
- Gold: **captions aligned to a narrow right column**; Answer Agent chose: **captions centered under the figure**
- Answer Agent reply: "The record that applies on this date and in this situation is \"captions centered under the figure,\" as it is a persistent rule for captions under wide illustrations and square illustrations, and there is no limited record applying to an ordinary occasion.  \nAnswer: captions centered under the figure"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "figure caption alignment",
  "value": "captions aligned to a narrow right column",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "figure caption alignment",
  "value": "captions centered under the figure",
  "scope": "captions under wide illustrations",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "figure caption alignment",
  "value": "captions centered under the figure",
  "scope": "captions under square illustrations",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e52cbf094307ef8b9cbd3"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "figure caption alignment",
  "value": "captions aligned to a narrow right column",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "figure caption alignment",
  "value": "captions centered under the figure",
  "scope": "captions under wide illustrations",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "figure caption alignment",
  "value": "captions centered under the figure",
  "scope": "captions under square illustrations",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e52cbf094307ef8b9cbd3"
  ]
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

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `e52cbf094307ef8b9cbd3` (2027-10-08), gold category exception_revision
- user: I thought again about figure caption alignment.  The answer for labeling a picture that's square, as far as I am concerned, is captions centered under the figure. I mean an enduring arrangement rather than a one-off. Leave the other arrangements alone.
- assistant: What would make seeing which figure a line belongs to easier to deal with?
- user: I want each line of text to look connected to the right picture.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "captions centered under the figure", "scope": "captions under square illustrations", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e52cbf094307ef8b9cbd3"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e52cbf094307ef8b9cbd3"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "captions under square illustrations", "target_id": "m3", "validity": {"kind": "persistent"}, "value": "captions centered under the figure"}], "decision": "resolved"}`

### `e91e52c3e466b212a8df6` (2027-10-09), gold category stable_preference
- user: I have something on my mind about where the caption sits.
- assistant: Feel free to start with whatever's most useful.
- user: I had a point to make about where the caption sits. Picture me asking, "There is a missing piece before I can ask for captions flush with the figure's left edge: whether I mean labeling a picture that's square rather than captions under wide illustrations." This is make-believe; none of my real choices should change.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 16. `te-0108/pa4241e3f03ee1466e57d/scope` (stable_preference, target probe)

- Question (2027-01-13): Pick a value for digital magnifier tracking, dated January 13, with the setting described as magnifier use with a physical keyboard.
- Options: a magnifier that centers the selected line | a magnifier fixed over a chosen rectangle | a magnifier that follows pointer movement | a magnifier that follows the insertion point
- Gold: **a magnifier fixed over a chosen rectangle**; Answer Agent chose: **a magnifier that follows pointer movement**
- Answer Agent reply: "On 2027-01-13, the record that applies is the one for \"magnifier use with an onscreen keyboard\" with the value \"zoom follows where the pointer moves,\" as it is within its validity window (January 9–25, 2027) and matches the situation, even though the question refers to a \"physical keyboard.\" However, since the situation specified is \"magnifier use with a physical keyboard\" and no record explicitly covers that, and the only related record (m2) refers to an onscreen keyboard, there is no direct match. Therefore, the general preference applies.  \nAnswer: a magnifier that follows pointer movement"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "digital magnifier tracking",
  "value": "a magnifier that centers the selected line",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "digital magnifier tracking",
  "value": "zoom follows where the pointer moves",
  "scope": "magnifier use with an onscreen keyboard",
  "validity": {
   "from": "2027-01-09",
   "kind": "window",
   "to": "2027-01-25"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ee41701e67193e593e86f"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "digital magnifier tracking",
  "value": "zoom stays on a rectangle I pick",
  "scope": "magnifying with a hardware keyboard",
  "validity": {
   "from": "2027-01-10",
   "kind": "window",
   "to": "2027-02-02"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ec6ceef486bdbf000cfa7"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "digital magnifier tracking",
  "value": "a magnifier that centers the selected line",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "digital magnifier tracking",
  "value": "zoom follows where the pointer moves",
  "scope": "magnifier use with an onscreen keyboard",
  "validity": {
   "from": "2027-01-09",
   "kind": "window",
   "to": "2027-01-25"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ee41701e67193e593e86f"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "digital magnifier tracking",
  "value": "zoom stays on a rectangle I pick",
  "scope": "magnifying with a hardware keyboard",
  "validity": {
   "from": "2027-01-10",
   "kind": "window",
   "to": "2027-02-02"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ec6ceef486bdbf000cfa7"
  ]
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

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "digital magnifier tracking", "value": "zoom follows where the pointer moves", "scope": "magnifier use with an onscreen keyboard", "validity": {"from": "2027-01-09", "kind": "window", "to": "2027-01-25"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ee41701e67193e593e86f"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "digital magnifier tracking", "evidence_ids": ["ee41701e67193e593e86f"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "magnifier use with an onscreen keyboard", "validity": {"from": "2027-01-09", "kind": "window", "to": "2027-01-25"}, "value": "zoom follows where the pointer moves"}], "decision": "resolved"}`

### `ec6ceef486bdbf000cfa7` (2027-01-10), gold category scoped_exception
- user: Here's what I meant about what the zoom box follows.  Use this choice for magnifying with a hardware keyboard: zoom stays on a rectangle I pick. Only occasions in January 10 to February 2, with both ends included, get this arrangement.
- assistant: What did you find difficult about following the line without hunting?
- user: I lose my place when the enlarged area moves while I am looking at it.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "digital magnifier tracking", "value": "zoom stays on a rectangle I pick", "scope": "magnifying with a hardware keyboard", "validity": {"from": "2027-01-10", "kind": "window", "to": "2027-02-02"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ec6ceef486bdbf000cfa7"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "digital magnifier tracking", "evidence_ids": ["ec6ceef486bdbf000cfa7"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "magnifying with a hardware keyboard", "validity": {"from": "2027-01-10", "kind": "window", "to": "2027-02-02"}, "value": "zoom stays on a rectangle I pick"}], "decision": "resolved"}`

### `ee9c303d4228272f108d3` (2027-01-12), gold category clarify
- user: I've got a minute now to explain what I mean about what the zoom box follows.
- assistant: Feel free to start with whatever's most useful.
- user: I had a point to make about what the zoom box follows. I cannot pin down whether this idea of a magnifier that follows the insertion point goes with magnifying with the keyboard shown on screen or magnifier use with a physical keyboard.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e5b4321b8f0370bd439fe` (2027-01-13), gold category stable_preference
- user: I thought again about what the zoom box follows.  I'm not picking a lasting arrangement for magnifying with a hardware keyboard; I need something for this instance.
- assistant: I can see how keeping the enlarged region on the right spot could make a difference.
- user: I lose my place when the enlarged area moves while I am looking at it.
- assistant: Which sounds most like what you want?
- user: I'd choose zoom follows where the pointer moves, I think.
- assistant: That gives us enough to go on for now.
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 17. `te-0109/p7f41beac8b5c02001f76/scope` (general_update, target probe)

- Question (2027-06-09): Pick a value for unfinished-task handoff note, dated June 9, with the setting described as an ordinary occasion.
- Options: a small done-and-pending grid | a sketched dependency chain | a spoken recap with a written pointer | a brief next-step sentence
- Gold: **a sketched dependency chain**; Answer Agent chose: **a small done-and-pending grid**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference for unfinished-task handoff notes, as no specific record is limited to an \"ordinary occasion\" or dated June 9.  \nAnswer: a small done-and-pending grid"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m2",
  "attribute": "scratch-paper use pattern",
  "value": "several calculations in a spiral column",
  "scope": "rough calculations at a seated desk",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "scratch-paper use pattern",
  "value": "calculations arranged around a central sketch",
  "scope": "rough calculations at a standing desk",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "unfinished-task handoff note",
  "value": "a small done-and-pending grid",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "unfinished-task handoff note",
  "value": "a spoken recap with a written pointer",
  "scope": "handoffs to a single collaborator",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "scratch-paper use pattern",
  "value": "a quick drawing of what depends on what",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e85ce98264db9bfd6bf10"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "scratch-paper use pattern",
  "value": "one calculation per loose square",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "scratch-paper use pattern",
  "value": "several calculations in a spiral column",
  "scope": "rough calculations at a seated desk",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "scratch-paper use pattern",
  "value": "calculations arranged around a central sketch",
  "scope": "rough calculations at a standing desk",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "unfinished-task handoff note",
  "value": "a spoken recap with a written pointer",
  "scope": "handoffs to a single collaborator",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "unfinished-task handoff note",
  "value": "a quick drawing of what depends on what",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e85ce98264db9bfd6bf10"
  ]
 }
]
```

Events up to the probe:

### `e85ce98264db9bfd6bf10` (2027-06-09), gold category general_update
- user: I thought again about what I leave for the next person.  My request is to save a quick drawing of what depends on what for the general choice rather than a special case. This is for the long run rather than a temporary spell.
- assistant: Did something in particular draw your attention to how much history the next person needs?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m4", "value": "a quick drawing of what depends on what", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e85ce98264db9bfd6bf10"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e85ce98264db9bfd6bf10"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "a quick drawing of what depends on what"}], "decision": "resolved"}`

## 18. `te-0116/pa0b9d7d7fc234d9b4ccc/scope` (scoped_exception, target probe)

- Question (2027-03-15): Pick a value for figure caption alignment, dated March 15, with the setting described as captions under square illustrations.
- Options: captions indented beneath the figure center | captions centered under the figure | captions flush with the figure's left edge | captions aligned to a narrow right column
- Gold: **captions indented beneath the figure center**; Answer Agent chose: **captions centered under the figure**
- Answer Agent reply: "The record that applies on this date and in this situation is \"figure caption alignment: caption set in under the middle of the figure\" for \"labeling a picture that's square.\"  \nAnswer: captions centered under the figure"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m5",
  "attribute": "section-opening decoration",
  "value": "a fine dotted line under the title",
  "scope": "sections beginning on a left-hand page",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "ebb6bfc5e891998c4c96c"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "section-opening decoration",
  "value": "a little leaf shape over the heading",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e472a8a258187ae2b0427"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "figure caption alignment",
  "value": "captions aligned to a narrow right column",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e95cdb4d23324575b3c93"
  ]
 },
 {
  "memory_id": "m8",
  "attribute": "figure caption alignment",
  "value": "caption set in under the middle of the figure",
  "scope": "labeling a picture that's square",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m7"
   }
  ],
  "evidence_ids": [
   "e9092bffe65ffedbf6d0d"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m5",
  "attribute": "section-opening decoration",
  "value": "a fine dotted line under the title",
  "scope": "sections beginning on a left-hand page",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "ebb6bfc5e891998c4c96c"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "section-opening decoration",
  "value": "a little leaf shape over the heading",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e472a8a258187ae2b0427"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "figure caption alignment",
  "value": "captions aligned to a narrow right column",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e95cdb4d23324575b3c93"
  ]
 },
 {
  "memory_id": "m8",
  "attribute": "figure caption alignment",
  "value": "caption set in under the middle of the figure",
  "scope": "labeling a picture that's square",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m7"
   }
  ],
  "evidence_ids": [
   "e9092bffe65ffedbf6d0d"
  ]
 }
]
```

Events up to the probe:

### `e820805bcfead4bfe299f` (2027-03-09), gold category general_update
- user: I thought about where the caption sits again this morning.
- assistant: What's your biggest concern around keeping the caption visually close to the picture?
- user: I want each line of text to look connected to the right picture.
- assistant: Was something about keeping the caption visually close to the picture especially important?
- user: I thought again about where the caption sits.  Here is where I have landed: caption set in under the middle of the figure, for my usual default outside exceptions. I want to keep coming back to that choice, not try it once.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "caption set in under the middle of the figure", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e820805bcfead4bfe299f"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e820805bcfead4bfe299f"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "caption set in under the middle of the figure"}], "decision": "resolved"}`

### `ebb6bfc5e891998c4c96c` (2027-03-11), gold category exception_revision
- user: I thought about what I put above a section start again this morning.
- assistant: What would you like to work through first?
- user: I had a point to make about what I put above a section start. It is a fine dotted line under the title that I want for sections beginning on a left-hand page. That is what I always want under those circumstances.
- assistant: Have you been noticing anything new about making a new section visible as you flip?
- user: It is hard to tell where a section starts if the opening looks like any other page.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "a fine dotted line under the title", "scope": "sections beginning on a left-hand page", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m2"}], "evidence_ids": ["ebb6bfc5e891998c4c96c"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ebb6bfc5e891998c4c96c"], "operation": "REVISE", "relations": [{"target": "m2", "type": "EXCEPTION_TO"}], "scope": "sections beginning on a left-hand page", "target_id": "m3", "validity": {"kind": "persistent"}, "value": "a fine dotted line under the title"}], "decision": "resolved"}`

### `e472a8a258187ae2b0427` (2027-03-12), gold category general_update
- user: I remembered something about what I put above a section start while thinking about making a new section visible as you flip.
- assistant: Did you want to say what you had in mind?
- user: Here's what I meant about what I put above a section start.  It is a little leaf shape over the heading that I want for the broad run of ordinary occasions. Next time, and after that, I still want this choice.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "a little leaf shape over the heading", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e472a8a258187ae2b0427"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e472a8a258187ae2b0427"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m2", "validity": {"kind": "persistent"}, "value": "a little leaf shape over the heading"}], "decision": "resolved"}`

### `e95cdb4d23324575b3c93` (2027-03-14), gold category general_update
- user: I've got a minute now to explain what I mean about where the caption sits.
- assistant: Of course. We can talk about seeing which figure a line belongs to.
- user: Can we get back to where the caption sits?  The answer for normal use in general, as far as I am concerned, is captions aligned to a narrow right column. Leave that as the choice whenever this comes round again.
- assistant: I can see how seeing which figure a line belongs to could make a difference.
- user: I want each line of text to look connected to the right picture.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m4", "value": "captions aligned to a narrow right column", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e95cdb4d23324575b3c93"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e95cdb4d23324575b3c93"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m4", "validity": {"kind": "persistent"}, "value": "captions aligned to a narrow right column"}], "decision": "resolved"}`

### `e9092bffe65ffedbf6d0d` (2027-03-15), gold category scoped_exception
- user: I had a point to make about where the caption sits. Whatever I decide for labeling a picture that's square now is what I want to carry forward.
- assistant: How has keeping the caption visually close to the picture worked out in practice?
- user: I want each line of text to look connected to the right picture.
- assistant: What's the choice you'd make?
- user: I'd choose caption set in under the middle of the figure, I think.
- assistant: That gives us enough to go on for now.
- user: That'll do. I'm happy with my choice.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "figure caption alignment", "value": "caption set in under the middle of the figure", "scope": "labeling a picture that's square", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m7"}], "evidence_ids": ["e9092bffe65ffedbf6d0d"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "figure caption alignment", "evidence_ids": ["e9092bffe65ffedbf6d0d"], "operation": "ADD", "relations": [{"target": "m7", "type": "EXCEPTION_TO"}], "scope": "labeling a picture that's square", "validity": {"kind": "persistent"}, "value": "caption set in under the middle of the figure"}], "decision": "resolved"}`

## 19. `te-0118/p991e3a4ba18381fcc69d/scope` (scoped_exception, boundary probe)

- Question (2027-02-01): Pick a value for lodging unpacking routine, dated February 1, with the setting described as lodgings used for several nights.
- Options: clothes kept in labeled packing rolls | clothes folded on an open luggage shelf | clothes arranged in a shallow drawer | clothes hung immediately on arrival
- Gold: **clothes hung immediately on arrival**; Answer Agent chose: **clothes folded on an open luggage shelf**
- Answer Agent reply: "The record that applies on this date and in this situation is m3, which specifies \"stacking folded clothes on the luggage shelf\" for lodgings used for several nights during the window from January 9 to January 31, 2027.  \nAnswer: clothes folded on an open luggage shelf"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "lodging unpacking routine",
  "value": "clothes hung immediately on arrival",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "lodging unpacking routine",
  "value": "clothes kept in labeled packing rolls",
  "scope": "lodgings used for a single night",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "lodging unpacking routine",
  "value": "stacking folded clothes on the luggage shelf",
  "scope": "lodgings used for several nights",
  "validity": {
   "from": "2027-01-09",
   "kind": "window",
   "to": "2027-01-31"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "eb86c68c1c4bbf2aaf1fc"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "lodging unpacking routine",
  "value": "clothes hung immediately on arrival",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "lodging unpacking routine",
  "value": "clothes kept in labeled packing rolls",
  "scope": "lodgings used for a single night",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "lodging unpacking routine",
  "value": "stacking folded clothes on the luggage shelf",
  "scope": "lodgings used for several nights",
  "validity": {
   "from": "2027-01-09",
   "kind": "window",
   "to": "2027-01-31"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "eb86c68c1c4bbf2aaf1fc"
  ]
 }
]
```

Events up to the probe:

### `e2e5874f68ddfbcc3dbd3` (2027-01-07), gold category clarify
- user: I remembered something about what I do with clothes when I arrive while thinking about getting changed on arrival.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to what I do with clothes when I arrive?  The plan involving stacking folded clothes on the luggage shelf is not complete. I still need to settle whether it is about lodgings used for several nights or checking in for one night.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `eb86c68c1c4bbf2aaf1fc` (2027-01-09), gold category scoped_exception
- user: I had a point to make about what I do with clothes when I arrive. Stacking folded clothes on the luggage shelf is the one I want when we are talking about lodgings used for several nights. I want it for the full period January 9 through January 31, not before or afterward.
- assistant: How did what will crease if left folded get on your mind?
- user: I want the arrival to take a little less effort.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "lodging unpacking routine", "value": "stacking folded clothes on the luggage shelf", "scope": "lodgings used for several nights", "validity": {"from": "2027-01-09", "kind": "window", "to": "2027-01-31"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["eb86c68c1c4bbf2aaf1fc"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "lodging unpacking routine", "evidence_ids": ["eb86c68c1c4bbf2aaf1fc"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "lodgings used for several nights", "validity": {"from": "2027-01-09", "kind": "window", "to": "2027-01-31"}, "value": "stacking folded clothes on the luggage shelf"}], "decision": "resolved"}`

## 20. `te-0118/pc595b04770579534c593/scope` (scoped_exception, default probe)

- Question (2027-01-09): Pick a value for lodging unpacking routine, dated January 9, with the setting described as an ordinary occasion.
- Options: clothes arranged in a shallow drawer | clothes folded on an open luggage shelf | clothes hung immediately on arrival | clothes kept in labeled packing rolls
- Gold: **clothes hung immediately on arrival**; Answer Agent chose: **clothes folded on an open luggage shelf**
- Answer Agent reply: "On this date and in this situation, the record that applies is \"clothes stacked on the luggage shelf\" (m3), which is valid from January 9 to January 31, 2027, and specifically applies to lodgings used for several nights.  \nAnswer: clothes folded on an open luggage shelf"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "lodging unpacking routine",
  "value": "clothes hung immediately on arrival",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "lodging unpacking routine",
  "value": "clothes kept in labeled packing rolls",
  "scope": "lodgings used for a single night",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "lodging unpacking routine",
  "value": "stacking folded clothes on the luggage shelf",
  "scope": "lodgings used for several nights",
  "validity": {
   "from": "2027-01-09",
   "kind": "window",
   "to": "2027-01-31"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "eb86c68c1c4bbf2aaf1fc"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "lodging unpacking routine",
  "value": "clothes hung immediately on arrival",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "lodging unpacking routine",
  "value": "clothes kept in labeled packing rolls",
  "scope": "lodgings used for a single night",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "lodging unpacking routine",
  "value": "stacking folded clothes on the luggage shelf",
  "scope": "lodgings used for several nights",
  "validity": {
   "from": "2027-01-09",
   "kind": "window",
   "to": "2027-01-31"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "eb86c68c1c4bbf2aaf1fc"
  ]
 }
]
```

Events up to the probe:

### `e2e5874f68ddfbcc3dbd3` (2027-01-07), gold category clarify
- user: I remembered something about what I do with clothes when I arrive while thinking about getting changed on arrival.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to what I do with clothes when I arrive?  The plan involving stacking folded clothes on the luggage shelf is not complete. I still need to settle whether it is about lodgings used for several nights or checking in for one night.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `eb86c68c1c4bbf2aaf1fc` (2027-01-09), gold category scoped_exception
- user: I had a point to make about what I do with clothes when I arrive. Stacking folded clothes on the luggage shelf is the one I want when we are talking about lodgings used for several nights. I want it for the full period January 9 through January 31, not before or afterward.
- assistant: How did what will crease if left folded get on your mind?
- user: I want the arrival to take a little less effort.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "lodging unpacking routine", "value": "stacking folded clothes on the luggage shelf", "scope": "lodgings used for several nights", "validity": {"from": "2027-01-09", "kind": "window", "to": "2027-01-31"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["eb86c68c1c4bbf2aaf1fc"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "lodging unpacking routine", "evidence_ids": ["eb86c68c1c4bbf2aaf1fc"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "lodgings used for several nights", "validity": {"from": "2027-01-09", "kind": "window", "to": "2027-01-31"}, "value": "stacking folded clothes on the luggage shelf"}], "decision": "resolved"}`

## 21. `te-0119/pda2fdca4a4a090557132/scope` (scoped_exception, neighbor probe)

- Question (2027-01-08): Pick a value for desk reference placement, dated January 8, with the setting described as reference use while writing by hand.
- Options: reference pages clipped to a vertical board | reference pages laid above the work area | reference pages propped on a side easel | reference pages held in a low rotating stand
- Gold: **reference pages clipped to a vertical board**; Answer Agent chose: **reference pages laid above the work area**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference for \"desk reference placement\" with the value \"an out-loud recap plus a written pointer.\"  \nAnswer: reference pages laid above the work area"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m3",
  "attribute": "unfinished-task handoff note",
  "value": "a small done-and-pending grid",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "unfinished-task handoff note",
  "value": "a quick drawing of what depends on what",
  "scope": "passing a task to just one colleague",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "edaf2e8d7850868ad7a12"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "desk reference placement",
  "value": "an out-loud recap plus a written pointer",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e42e96239ee31c224b0bc"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "desk reference placement",
  "value": "reference pages clipped to a vertical board",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "unfinished-task handoff note",
  "value": "an out-loud recap plus a written pointer",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e42e96239ee31c224b0bc"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "desk reference placement",
  "value": "reference pages laid above the work area",
  "scope": "reference use while typing",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e2b1109dd2fe0120b52f1"
  ]
 }
]
```

Events up to the probe:

### `edaf2e8d7850868ad7a12` (2027-01-03), gold category stable_preference
- user: I had a point to make about what I leave for the next person. What if someone said, "Use this choice for passing a task to just one colleague: a quick drawing of what depends on what. Let it run across the coming occasions until I can end this temporary arrangement."? I mean an imaginary situation, not an actual request from me.
- assistant: I'm curious about how much history the next person needs, too.
- user: It is the sort of detail I notice while there is a lot going on.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"attribute": "unfinished-task handoff note", "evidence_ids": ["edaf2e8d7850868ad7a12"], "operation": "ADD", "relations": [{"target": "m3", "type": "EXCEPTION_TO"}], "scope": "passing a task to just one colleague", "validity": {"kind": "persistent"}, "value": "a quick drawing of what depends on what"}], "decision": "resolved"}`

### `e42e96239ee31c224b0bc` (2027-01-04), gold category general_update
- user: I had a point to make about what I leave for the next person. I am settling the question of regular occasions without a special choice with an out-loud recap plus a written pointer. I want to keep coming back to that choice, not try it once. That does not change the rest of my preferences.
- assistant: Is making the next step visible part of what you want to work out?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "an out-loud recap plus a written pointer", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e42e96239ee31c224b0bc"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e42e96239ee31c224b0bc"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "an out-loud recap plus a written pointer"}], "decision": "resolved"}`

### `ea28017e4f5a9e8f1f92f` (2027-01-05), gold category exception_retirement
- user: I've got a minute now to explain what I mean about where I put pages I'm looking at.
- assistant: I'm listening. What's on your mind?
- user: I thought again about where I put pages I'm looking at.  The distinction we used for reference use while typing is over; whatever my usual choice becomes should apply there too.
- assistant: What do you tend to notice first about looking at a reference without turning around?
- user: I am trying to see the reference without moving the work out of the way.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m2", "evidence_ids": ["ea28017e4f5a9e8f1f92f"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ea28017e4f5a9e8f1f92f"], "operation": "RETIRE", "target_id": "m2"}], "decision": "resolved"}`

### `efae1052a67294b05c6f4` (2027-01-07), gold category clarify
- user: I remembered something about what I leave for the next person while thinking about making the next step visible.
- assistant: Was something about making the next step visible especially important?
- user: Here's what I meant about what I leave for the next person.  The choice sounds like a small done-and-pending grid; the situation is still a question between handoffs to a single collaborator and handing over a task to whoever is on rotation.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e2b1109dd2fe0120b52f1` (2027-01-08), gold category scoped_exception
- user: There was one thing about where I put pages I'm looking at I wanted to talk through.
- assistant: Feel free to start with whatever's most useful.
- user: I had a point to make about where I put pages I'm looking at. The option I am selecting where reference use while typing is concerned is reference pages laid above the work area. Only as a stopgap, but on each occasion for now. I cannot name the last day. That does not change the rest of my preferences.
- assistant: Have you been noticing anything new about where the pages sit relative to a hand?
- user: I am trying to see the reference without moving the work out of the way.
- assistant: Would you prefer to talk more about looking at a reference without turning around another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "desk reference placement", "value": "reference pages laid above the work area", "scope": "reference use while typing", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e2b1109dd2fe0120b52f1"]}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 22. `te-0119/pee983961b0dc31f6cb41/scope` (exception_revision, target probe)

- Question (2027-01-05): Pick a value for desk reference placement, dated January 5, with the setting described as reference use while typing.
- Options: reference pages clipped to a vertical board | reference pages held in a low rotating stand | reference pages propped on a side easel | reference pages laid above the work area
- Gold: **reference pages clipped to a vertical board**; Answer Agent chose: **an out-loud recap plus a written pointer**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference for \"desk reference placement\" with the value \"an out-loud recap plus a written pointer.\"  \nAnswer: an out-loud recap plus a written pointer"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m3",
  "attribute": "unfinished-task handoff note",
  "value": "a small done-and-pending grid",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "unfinished-task handoff note",
  "value": "a quick drawing of what depends on what",
  "scope": "passing a task to just one colleague",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "edaf2e8d7850868ad7a12"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "desk reference placement",
  "value": "an out-loud recap plus a written pointer",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e42e96239ee31c224b0bc"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "desk reference placement",
  "value": "reference pages clipped to a vertical board",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "unfinished-task handoff note",
  "value": "an out-loud recap plus a written pointer",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e42e96239ee31c224b0bc"
  ]
 }
]
```

Events up to the probe:

### `edaf2e8d7850868ad7a12` (2027-01-03), gold category stable_preference
- user: I had a point to make about what I leave for the next person. What if someone said, "Use this choice for passing a task to just one colleague: a quick drawing of what depends on what. Let it run across the coming occasions until I can end this temporary arrangement."? I mean an imaginary situation, not an actual request from me.
- assistant: I'm curious about how much history the next person needs, too.
- user: It is the sort of detail I notice while there is a lot going on.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"attribute": "unfinished-task handoff note", "evidence_ids": ["edaf2e8d7850868ad7a12"], "operation": "ADD", "relations": [{"target": "m3", "type": "EXCEPTION_TO"}], "scope": "passing a task to just one colleague", "validity": {"kind": "persistent"}, "value": "a quick drawing of what depends on what"}], "decision": "resolved"}`

### `e42e96239ee31c224b0bc` (2027-01-04), gold category general_update
- user: I had a point to make about what I leave for the next person. I am settling the question of regular occasions without a special choice with an out-loud recap plus a written pointer. I want to keep coming back to that choice, not try it once. That does not change the rest of my preferences.
- assistant: Is making the next step visible part of what you want to work out?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "an out-loud recap plus a written pointer", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e42e96239ee31c224b0bc"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e42e96239ee31c224b0bc"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "an out-loud recap plus a written pointer"}], "decision": "resolved"}`

### `ea28017e4f5a9e8f1f92f` (2027-01-05), gold category exception_retirement
- user: I've got a minute now to explain what I mean about where I put pages I'm looking at.
- assistant: I'm listening. What's on your mind?
- user: I thought again about where I put pages I'm looking at.  The distinction we used for reference use while typing is over; whatever my usual choice becomes should apply there too.
- assistant: What do you tend to notice first about looking at a reference without turning around?
- user: I am trying to see the reference without moving the work out of the way.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m2", "evidence_ids": ["ea28017e4f5a9e8f1f92f"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ea28017e4f5a9e8f1f92f"], "operation": "RETIRE", "target_id": "m2"}], "decision": "resolved"}`

## 23. `te-0123/p6d35a592a8f907455b1a/scope` (general_update, neighbor probe)

- Question (2027-12-04): Pick a value for baked potato filling, dated December 4, with the setting described as potatoes eaten from a bowl.
- Options: smoky beans with chopped scallions | herbed curd with grated radish | roasted mushrooms with thyme | crushed peas with lemon zest
- Gold: **crushed peas with lemon zest**; Answer Agent chose: **smoky beans with chopped scallions**
- Answer Agent reply: "The record that applies on this date and in the situation of potatoes eaten from a bowl is the one with the scope \"potatoes eaten from a paper boat,\" which has the value \"smoky beans with chopped scallions.\"  \nAnswer: smoky beans with chopped scallions"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m2",
  "attribute": "baked potato filling",
  "value": "smoky beans with chopped scallions",
  "scope": "potatoes eaten from a paper boat",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m7"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "supper grain accompaniment",
  "value": "toasted pearl barley",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "supper grain accompaniment",
  "value": "soft lemon-scented couscous",
  "scope": "suppers served from separate pans",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "supper grain accompaniment",
  "value": "fluffy steamed millet",
  "scope": "suppers served from a single pot",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "baked potato filling",
  "value": "crushed peas seasoned with lemon peel",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e58c379ec8e8cfab9c327"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m2",
  "attribute": "baked potato filling",
  "value": "smoky beans with chopped scallions",
  "scope": "potatoes eaten from a paper boat",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m7"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "supper grain accompaniment",
  "value": "toasted pearl barley",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "supper grain accompaniment",
  "value": "soft lemon-scented couscous",
  "scope": "suppers served from separate pans",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "supper grain accompaniment",
  "value": "fluffy steamed millet",
  "scope": "suppers served from a single pot",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "baked potato filling",
  "value": "crushed peas seasoned with lemon peel",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e58c379ec8e8cfab9c327"
  ]
 }
]
```

Events up to the probe:

### `e2f53cba60672b24a02ca` (2027-12-03), gold category exception_retirement
- user: Here's what I meant about what I put inside the jacket potato.  There is nothing to keep apart for eating the potato out of a bowl anymore. I want it to follow whatever I choose for other occasions.
- assistant: I can see how how the herbs and beans balance could make a difference.
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m3", "evidence_ids": ["e2f53cba60672b24a02ca"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e2f53cba60672b24a02ca"], "operation": "RETIRE", "target_id": "m3"}], "decision": "resolved"}`

### `e58c379ec8e8cfab9c327` (2027-12-04), gold category general_update
- user: I thought about what I put inside the jacket potato again this morning.
- assistant: What did you find difficult about what you can scoop up from a paper tray?
- user: I want the filling to be easy to scoop without coming away in one piece.
- assistant: How have you been thinking about it?
- user: I had a point to make about what I put inside the jacket potato. Let the arrangement be crushed peas seasoned with lemon peel when the situation is the usual situation. Make that the standing arrangement from this point ahead. Leave the other arrangements alone.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "crushed peas seasoned with lemon peel", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e58c379ec8e8cfab9c327"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e58c379ec8e8cfab9c327"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "crushed peas seasoned with lemon peel"}], "decision": "resolved"}`

## 24. `te-0127/p5b562092dcc6b30eed13/scope` (scoped_exception, boundary probe)

- Question (2027-08-12): Pick a value for unfinished-task handoff note, dated August 12, with the setting described as handoffs to a rotating group.
- Options: a spoken recap with a written pointer | a brief next-step sentence | a sketched dependency chain | a small done-and-pending grid
- Gold: **a brief next-step sentence**; Answer Agent chose: **a spoken recap with a written pointer**
- Answer Agent reply: "The record that applies on this date and in this situation is the one with the scope \"handing over a task to whoever is on rotation\" and the validity window from 2027-08-13 to 2027-09-01. Answer: a spoken recap with a written pointer"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "unfinished-task handoff note",
  "value": "a brief next-step sentence",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "unfinished-task handoff note",
  "value": "a spoken recap with a written pointer",
  "scope": "handing over a task to whoever is on rotation",
  "validity": {
   "from": "2027-08-13",
   "kind": "window",
   "to": "2027-09-01"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e0bf5f69e7743efc6b08e"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "unfinished-task handoff note",
  "value": "a brief next-step sentence",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "unfinished-task handoff note",
  "value": "a spoken recap with a written pointer",
  "scope": "handing over a task to whoever is on rotation",
  "validity": {
   "from": "2027-08-13",
   "kind": "window",
   "to": "2027-09-01"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e0bf5f69e7743efc6b08e"
  ]
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

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `e0bf5f69e7743efc6b08e` (2027-08-12), gold category scoped_exception
- user: I remembered something about what I leave for the next person while thinking about making the next step visible.
- assistant: Feel free to start with whatever's most useful.
- user: I thought again about what I leave for the next person.  When handing over a task to whoever is on rotation comes up, my choice is a spoken recap with a written pointer. Only occasions in August 13 to September 1, with both ends included, get this arrangement.
- assistant: There's room to talk more about making the next step visible if you want.
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "unfinished-task handoff note", "value": "a spoken recap with a written pointer", "scope": "handing over a task to whoever is on rotation", "validity": {"from": "2027-08-13", "kind": "window", "to": "2027-09-01"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e0bf5f69e7743efc6b08e"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "unfinished-task handoff note", "evidence_ids": ["e0bf5f69e7743efc6b08e"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "handing over a task to whoever is on rotation", "validity": {"from": "2027-08-13", "kind": "window", "to": "2027-09-01"}, "value": "a spoken recap with a written pointer"}], "decision": "resolved"}`

## 25. `te-0138/p08de6a7d3f71d0a5ec9f/scope` (scoped_exception, boundary probe)

- Question (2027-11-10): Pick a value for unfinished-task handoff note, dated November 10, with the setting described as handoffs to a rotating group.
- Options: a spoken recap with a written pointer | a brief next-step sentence | a small done-and-pending grid | a sketched dependency chain
- Gold: **a brief next-step sentence**; Answer Agent chose: **a small done-and-pending grid**
- Answer Agent reply: "The record that applies on this date and in this situation is the one with scope \"handoffs to a rotating group\" and validity from November 11 to November 26, 2027.  \nAnswer: a small done-and-pending grid"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m2",
  "attribute": "unfinished-task handoff note",
  "value": "a brief next-step sentence",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e0ccd890da72c32c00bef"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "unfinished-task handoff note",
  "value": "a small done-and-pending grid",
  "scope": "handoffs to a rotating group",
  "validity": {
   "from": "2027-11-11",
   "kind": "window",
   "to": "2027-11-26"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "ead1727f5170909887826"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m2",
  "attribute": "unfinished-task handoff note",
  "value": "a brief next-step sentence",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e0ccd890da72c32c00bef"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "unfinished-task handoff note",
  "value": "a small done-and-pending grid",
  "scope": "handoffs to a rotating group",
  "validity": {
   "from": "2027-11-11",
   "kind": "window",
   "to": "2027-11-26"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "ead1727f5170909887826"
  ]
 }
]
```

Events up to the probe:

### `e0ccd890da72c32c00bef` (2027-11-07), gold category general_update
- user: How much history the next person needs has been on my mind. Can we get back to what I leave for the next person?
- assistant: Of course. We can talk about how much history the next person needs.
- user: I thought again about what I leave for the next person.  Use this choice for cases that have no separate preference: a brief next-step sentence. I am not putting an end date on this preference.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "a brief next-step sentence", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e0ccd890da72c32c00bef"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e0ccd890da72c32c00bef"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "a brief next-step sentence"}], "decision": "resolved"}`

### `ec048614829469c400a1a` (2027-11-09), gold category stable_preference
- user: Can we get back to unfinished-task handoff note?  I nearly asked, "No more separate treatment for handoffs to a single collaborator. Let it follow the general choice now and when that changes." I have thought better of it. Keep the preferences we already had.
- assistant: Is how much history the next person needs part of what you want to work out?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `ead1727f5170909887826` (2027-11-10), gold category scoped_exception
- user: I have something on my mind about what I leave for the next person.
- assistant: Could you say why how much history the next person needs matters to you?
- user: I care about keeping track without adding another chore.
- assistant: What did you want me to know?
- user: I had a point to make about what I leave for the next person. When handoffs to a rotating group comes up, my choice is a small done-and-pending grid. Only occasions in November 11 to November 26, with both ends included, get this arrangement.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "unfinished-task handoff note", "value": "a small done-and-pending grid", "scope": "handoffs to a rotating group", "validity": {"from": "2027-11-11", "kind": "window", "to": "2027-11-26"}, "relations": [{"type": "EXCEPTION_TO", "target": "m2"}], "evidence_ids": ["ead1727f5170909887826"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "unfinished-task handoff note", "evidence_ids": ["ead1727f5170909887826"], "operation": "ADD", "relations": [{"target": "m2", "type": "EXCEPTION_TO"}], "scope": "handoffs to a rotating group", "validity": {"from": "2027-11-11", "kind": "window", "to": "2027-11-26"}, "value": "a small done-and-pending grid"}], "decision": "resolved"}`

## 26. `te-0144/p06bcafd9c753721a2472/scope` (exception_revision, neighbor probe)

- Question (2027-09-10): Pick a value for water-flask refill alert, dated September 10, with the setting described as refill tracking with a large flask.
- Options: a soft ripple animation | a pair of short vibration pulses | a quiet descending whistle | a tiny glowing droplet symbol
- Gold: **a pair of short vibration pulses**; Answer Agent chose: **a quiet descending whistle**
- Answer Agent reply: "The record that applies on this date and in this situation is the one with the attribute \"water-flask refill alert\" and scope \"refill tracking with a small flask,\" which specifies \"a quiet descending whistle,\" as no record matches \"refill tracking with a large flask.\"  \nAnswer: a quiet descending whistle"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "group-poll update trigger",
  "value": "a notice when a different choice takes the lead",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "water-flask refill alert",
  "value": "two little buzzes in a row",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e93f6e43c116d2d697f2a"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "water-flask refill alert",
  "value": "a quiet descending whistle",
  "scope": "refill tracking with a small flask",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e7041db104956c2c1235c"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "group-poll update trigger",
  "value": "a notice when a different choice takes the lead",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "water-flask refill alert",
  "value": "two little buzzes in a row",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e93f6e43c116d2d697f2a"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "water-flask refill alert",
  "value": "a quiet descending whistle",
  "scope": "refill tracking with a small flask",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e7041db104956c2c1235c"
  ]
 }
]
```

Events up to the probe:

### `e93f6e43c116d2d697f2a` (2027-09-05), gold category general_update
- user: I had a point to make about what reminds me to top up the flask. It is two little buzzes in a row that I want for the general everyday case. It is meant to last beyond the occasion in front of us.
- assistant: What do you tend to notice first about knowing when the little flask is empty?
- user: I want to notice the refill cue without distracting anyone nearby.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "two little buzzes in a row", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e93f6e43c116d2d697f2a"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e93f6e43c116d2d697f2a"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m2", "validity": {"kind": "persistent"}, "value": "two little buzzes in a row"}], "decision": "resolved"}`

### `e124852dadbf4040624df` (2027-09-07), gold category scoped_exception
- user: There was one thing about when I get news from the poll I wanted to talk through.
- assistant: Did you want to say what you had in mind?
- user: Can we get back to when I get news from the poll?  Given polls with two possible answers, make the choice a ping on each incoming vote. Only occasions in September 7 to September 30, with both ends included, get this arrangement.
- assistant: What do you tend to notice first about finding out that the vote has changed?
- user: I care about a change that actually tells me something about the vote.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "group-poll update trigger", "value": "a ping on each incoming vote", "scope": "polls with two possible answers", "validity": {"from": "2027-09-07", "kind": "window", "to": "2027-09-30"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e124852dadbf4040624df"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "group-poll update trigger", "evidence_ids": ["e124852dadbf4040624df"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "polls with two possible answers", "validity": {"from": "2027-09-07", "kind": "window", "to": "2027-09-30"}, "value": "a ping on each incoming vote"}], "decision": "resolved"}`

### `e89c666a3d844878002d1` (2027-09-08), gold category exception_retirement
- user: I have something on my mind about when I get news from the poll.
- assistant: What did you want me to know?
- user: Here's what I meant about when I get news from the poll.  I want polls with two possible answers covered by my general arrangement again, not by an instruction of its own.
- assistant: There's room to talk more about finding out that the vote has changed if you want.
- user: I care about a change that actually tells me something about the vote.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m5", "evidence_ids": ["e89c666a3d844878002d1"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e89c666a3d844878002d1"], "operation": "RETIRE", "target_id": "m5"}], "decision": "resolved"}`

### `e7041db104956c2c1235c` (2027-09-10), gold category exception_revision
- user: Can we get back to what reminds me to top up the flask?  Whatever I decide for tracking refills of the smaller flask now is what I want to carry forward.
- assistant: I'm curious about catching a refill reminder while putting the flask down, too.
- user: I want to notice the refill cue without distracting anyone nearby.
- assistant: What's the choice you'd make?
- user: For me it'd be a quiet descending whistle.
- assistant: That gives us enough to go on for now.
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "a quiet descending whistle", "scope": "refill tracking with a small flask", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m4"}], "evidence_ids": ["e7041db104956c2c1235c"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e7041db104956c2c1235c"], "operation": "REVISE", "relations": [{"target": "m4", "type": "EXCEPTION_TO"}], "scope": "refill tracking with a small flask", "target_id": "m3", "validity": {"kind": "persistent"}, "value": "a quiet descending whistle"}], "decision": "resolved"}`

## 27. `te-0144/pedd8969f636b23e67d6a/scope` (scoped_exception, default probe)

- Question (2027-09-07): Pick a value for group-poll update trigger, dated September 7, with the setting described as an ordinary occasion.
- Options: a notice whenever a vote arrives | a notice when a different choice takes the lead | a notice after every participant has voted | a notice when half the group has voted
- Gold: **a notice when a different choice takes the lead**; Answer Agent chose: **a notice whenever a vote arrives**
- Answer Agent reply: "On this date and in this situation, the record for \"group-poll update trigger\" that applies is the one with a window from 2027-09-07 to 2027-09-30, which specifies a \"ping on each incoming vote\" for polls with two possible answers.  \nAnswer: a notice whenever a vote arrives"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "group-poll update trigger",
  "value": "a notice when a different choice takes the lead",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "water-flask refill alert",
  "value": "a pair of short vibration pulses",
  "scope": "refill tracking with a small flask",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "water-flask refill alert",
  "value": "two little buzzes in a row",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e93f6e43c116d2d697f2a"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "group-poll update trigger",
  "value": "a ping on each incoming vote",
  "scope": "polls with two possible answers",
  "validity": {
   "from": "2027-09-07",
   "kind": "window",
   "to": "2027-09-30"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e124852dadbf4040624df"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "group-poll update trigger",
  "value": "a notice when a different choice takes the lead",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "water-flask refill alert",
  "value": "a pair of short vibration pulses",
  "scope": "refill tracking with a small flask",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "water-flask refill alert",
  "value": "two little buzzes in a row",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e93f6e43c116d2d697f2a"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "group-poll update trigger",
  "value": "a ping on each incoming vote",
  "scope": "polls with two possible answers",
  "validity": {
   "from": "2027-09-07",
   "kind": "window",
   "to": "2027-09-30"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e124852dadbf4040624df"
  ]
 }
]
```

Events up to the probe:

### `e93f6e43c116d2d697f2a` (2027-09-05), gold category general_update
- user: I had a point to make about what reminds me to top up the flask. It is two little buzzes in a row that I want for the general everyday case. It is meant to last beyond the occasion in front of us.
- assistant: What do you tend to notice first about knowing when the little flask is empty?
- user: I want to notice the refill cue without distracting anyone nearby.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "two little buzzes in a row", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e93f6e43c116d2d697f2a"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e93f6e43c116d2d697f2a"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m2", "validity": {"kind": "persistent"}, "value": "two little buzzes in a row"}], "decision": "resolved"}`

### `e124852dadbf4040624df` (2027-09-07), gold category scoped_exception
- user: There was one thing about when I get news from the poll I wanted to talk through.
- assistant: Did you want to say what you had in mind?
- user: Can we get back to when I get news from the poll?  Given polls with two possible answers, make the choice a ping on each incoming vote. Only occasions in September 7 to September 30, with both ends included, get this arrangement.
- assistant: What do you tend to notice first about finding out that the vote has changed?
- user: I care about a change that actually tells me something about the vote.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "group-poll update trigger", "value": "a ping on each incoming vote", "scope": "polls with two possible answers", "validity": {"from": "2027-09-07", "kind": "window", "to": "2027-09-30"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e124852dadbf4040624df"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "group-poll update trigger", "evidence_ids": ["e124852dadbf4040624df"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "polls with two possible answers", "validity": {"from": "2027-09-07", "kind": "window", "to": "2027-09-30"}, "value": "a ping on each incoming vote"}], "decision": "resolved"}`

## 28. `te-0158/p1c0355afe44c525ea09c/scope` (exception_revision, default probe)

- Question (2027-01-05): Pick a value for desk reference placement, dated January 5, with the setting described as an ordinary occasion.
- Options: reference pages laid above the work area | reference pages held in a low rotating stand | reference pages propped on a side easel | reference pages clipped to a vertical board
- Gold: **reference pages clipped to a vertical board**; Answer Agent chose: **an out-loud recap plus a written pointer**
- Answer Agent reply: "The record that applies on this date and in this situation is the general preference for \"desk reference placement\" with the value \"an out-loud recap plus a written pointer.\"  \nAnswer: an out-loud recap plus a written pointer"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m3",
  "attribute": "unfinished-task handoff note",
  "value": "a small done-and-pending grid",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "unfinished-task handoff note",
  "value": "a quick drawing of what depends on what",
  "scope": "passing a task to just one colleague",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "ed6ff4e9134a3371dcf8c"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "desk reference placement",
  "value": "an out-loud recap plus a written pointer",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e2a64f8890d60698bb3da"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "desk reference placement",
  "value": "reference pages clipped to a vertical board",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "unfinished-task handoff note",
  "value": "an out-loud recap plus a written pointer",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e2a64f8890d60698bb3da"
  ]
 }
]
```

Events up to the probe:

### `ed6ff4e9134a3371dcf8c` (2027-01-03), gold category stable_preference
- user: I had a point to make about what I leave for the next person. What if someone said, "Use this choice for passing a task to just one colleague: a quick drawing of what depends on what. Let it run across the coming occasions until I can end this temporary arrangement."? I mean an imaginary situation, not an actual request from me.
- assistant: I'm curious about how much history the next person needs, too.
- user: It is the sort of detail I notice while there is a lot going on.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"attribute": "unfinished-task handoff note", "evidence_ids": ["ed6ff4e9134a3371dcf8c"], "operation": "ADD", "relations": [{"target": "m3", "type": "EXCEPTION_TO"}], "scope": "passing a task to just one colleague", "validity": {"kind": "persistent"}, "value": "a quick drawing of what depends on what"}], "decision": "resolved"}`

### `e2a64f8890d60698bb3da` (2027-01-04), gold category general_update
- user: I had a point to make about what I leave for the next person. I am settling the question of regular occasions without a special choice with an out-loud recap plus a written pointer. I want to keep coming back to that choice, not try it once. That does not change the rest of my preferences.
- assistant: Is making the next step visible part of what you want to work out?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "an out-loud recap plus a written pointer", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e2a64f8890d60698bb3da"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e2a64f8890d60698bb3da"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "an out-loud recap plus a written pointer"}], "decision": "resolved"}`

### `e1aa0c6681d5cbf236f14` (2027-01-05), gold category exception_retirement
- user: I've got a minute now to explain what I mean about where I put pages I'm looking at.
- assistant: I'm listening. What's on your mind?
- user: I thought again about where I put pages I'm looking at.  The distinction we used for reference use while typing is over; whatever my usual choice becomes should apply there too.
- assistant: What do you tend to notice first about looking at a reference without turning around?
- user: I am trying to see the reference without moving the work out of the way.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m2", "evidence_ids": ["e1aa0c6681d5cbf236f14"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e1aa0c6681d5cbf236f14"], "operation": "RETIRE", "target_id": "m2"}], "decision": "resolved"}`

## 29. `te-0160/p5d10365d5e696d6f5ff8/scope` (exception_revision, target probe)

- Question (2027-04-12): Pick a value for museum visit starting point, dated April 12, with the setting described as museum visits on a ground-floor ticket.
- Options: starting with the newest acquisition | starting with the oldest display | starting with the smallest gallery | starting with the central installation
- Gold: **starting with the newest acquisition**; Answer Agent chose: **starting with the smallest gallery**
- Answer Agent reply: "The record that applies on April 12, for museum visits on a ground-floor ticket, is not explicitly present in the memory records. The record \"starting with the newest acquisition\" applies to \"museum visits on an upper-floor ticket,\" which does not match the ground-floor setting. The record \"starting with the smallest gallery\" is general and persistent, and no specific record limits it to a floor. Since no record is explicitly tied to ground-floor tickets, the general preference applies.  \nAnswer: starting with the smallest gallery"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "museum visit starting point",
  "value": "starting with the smallest gallery",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "museum visit starting point",
  "value": "starting with the newest acquisition",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "museum visit starting point",
  "value": "the most recently acquired piece comes first",
  "scope": "a museum ticket for the lower floor",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e476e765fc08ef2a40d59"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "museum visit starting point",
  "value": "starting with the smallest gallery",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "museum visit starting point",
  "value": "starting with the newest acquisition",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "museum visit starting point",
  "value": "the most recently acquired piece comes first",
  "scope": "a museum ticket for the lower floor",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e476e765fc08ef2a40d59"
  ]
 }
]
```

Events up to the probe:

### `edafaa1c06146562f749b` (2027-04-09), gold category scoped_exception
- user: I have something on my mind about which part of the exhibition I see first.
- assistant: Of course. We can talk about what there is time to see first.
- user: I thought again about which part of the exhibition I see first.  It is the most recently acquired piece comes first that I want for a museum ticket for the lower floor. This should carry on; it is not just a test. Leave the other arrangements alone.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "museum visit starting point", "value": "the most recently acquired piece comes first", "scope": "a museum ticket for the lower floor", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["edafaa1c06146562f749b"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "museum visit starting point", "evidence_ids": ["edafaa1c06146562f749b"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "a museum ticket for the lower floor", "validity": {"kind": "persistent"}, "value": "the most recently acquired piece comes first"}], "decision": "resolved"}`

### `efb16bf74c009d6f5dea1` (2027-04-10), gold category exception_revision
- user: Can we get back to which part of the exhibition I see first?  Starting with the central installation is the one I want when we are talking about a museum ticket for the lower floor. Leave that as the choice whenever this comes round again.
- assistant: Tell me what struck you about how to begin walking around the exhibition.
- user: It comes down to what would feel right when I get to my stop.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "starting with the central installation", "scope": "a museum ticket for the lower floor", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["efb16bf74c009d6f5dea1"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["efb16bf74c009d6f5dea1"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "a museum ticket for the lower floor", "target_id": "m3", "validity": {"kind": "persistent"}, "value": "starting with the central installation"}], "decision": "resolved"}`

### `e476e765fc08ef2a40d59` (2027-04-12), gold category exception_revision
- user: How to begin walking around the exhibition has been on my mind. Can we get back to which part of the exhibition I see first?
- assistant: Was something about how to begin walking around the exhibition especially important?
- user: Can we get back to which part of the exhibition I see first?  It is the most recently acquired piece comes first that I want for museum visits on a ground-floor ticket. Leave that as the choice whenever this comes round again.
- assistant: What would make how to begin walking around the exhibition easier to deal with?
- user: It helps me to pick a starting point before I get caught up looking around.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m4", "value": "the most recently acquired piece comes first", "scope": "a museum ticket for the lower floor", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e476e765fc08ef2a40d59"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e476e765fc08ef2a40d59"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "a museum ticket for the lower floor", "target_id": "m4", "validity": {"kind": "persistent"}, "value": "the most recently acquired piece comes first"}], "decision": "resolved"}`

## 30. `te-0165/pf9759317e790b4395c35/scope` (scoped_exception, target probe)

- Question (2027-08-27): Pick a value for floor exercise head support, dated August 27, with the setting described as floor practice on uncarpeted flooring.
- Options: a soft rolled fleece support | a thin flat wool pad | a low folded cotton towel | a small crescent-shaped foam rest
- Gold: **a thin flat wool pad**; Answer Agent chose: **a small crescent-shaped foam rest**
- Answer Agent reply: "The record that applies on August 27, 2027, for floor practice on uncarpeted flooring is the temporary window-record (m5) specifying a thin piece of wool padding, which ends on August 27, so it no longer applies. Answer: a small crescent-shaped foam rest"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m3",
  "attribute": "floor exercise head support",
  "value": "a soft rolled fleece support",
  "scope": "floor practice on carpeted flooring",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "floor exercise head support",
  "value": "a small crescent-shaped foam rest",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ed95f01f4069b545e503e"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "floor exercise head support",
  "value": "a thin piece of wool padding",
  "scope": "floor practice on uncarpeted flooring",
  "validity": {
   "from": "2027-08-11",
   "kind": "window",
   "to": "2027-08-27"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e93b5def45d3164841543"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m3",
  "attribute": "floor exercise head support",
  "value": "a soft rolled fleece support",
  "scope": "floor practice on carpeted flooring",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "floor exercise head support",
  "value": "a small crescent-shaped foam rest",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ed95f01f4069b545e503e"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "floor exercise head support",
  "value": "a thin piece of wool padding",
  "scope": "floor practice on uncarpeted flooring",
  "validity": {
   "from": "2027-08-11",
   "kind": "window",
   "to": "2027-08-27"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e93b5def45d3164841543"
  ]
 }
]
```

Events up to the probe:

### `ec1dd30a188e5e819898b` (2027-08-05), gold category exception_retirement
- user: I had a point to make about what goes under my head on the floor. Undo the separate arrangement we gave doing the exercises on a bare floor; my everyday preference is what should govern it again.
- assistant: Have you been noticing anything new about whether a pad shifts on a bare floor?
- user: If it raises my head too much I end up adjusting it between movements.
- assistant: Do you have another thought on how much the head support raises you?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m2", "evidence_ids": ["ec1dd30a188e5e819898b"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ec1dd30a188e5e819898b"], "operation": "RETIRE", "target_id": "m2"}], "decision": "resolved"}`

### `ee114fa1c50cb0f2f2084` (2027-08-07), gold category stable_preference
- user: There was one thing about what goes under my head on the floor I wanted to talk through.
- assistant: Was something about getting comfortable while staying level especially important?
- user: I thought again about what goes under my head on the floor.  The person beside me said, "I do not want a dedicated preference for floor practice on carpeted flooring now. Fold it into the ordinary arrangement." That belongs to their preferences, not to mine.
- assistant: There's room to talk more about getting comfortable while staying level if you want.
- user: If it raises my head too much I end up adjusting it between movements.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `ed95f01f4069b545e503e` (2027-08-08), gold category general_update
- user: I thought again about what goes under my head on the floor.  Here is where I have landed: a small crescent-shaped foam rest, for the broad run of ordinary occasions. I mean an enduring arrangement rather than a one-off.
- assistant: What would make getting comfortable while staying level easier to deal with?
- user: If it raises my head too much I end up adjusting it between movements.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "a small crescent-shaped foam rest", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["ed95f01f4069b545e503e"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ed95f01f4069b545e503e"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "a small crescent-shaped foam rest"}], "decision": "resolved"}`

### `e93b5def45d3164841543` (2027-08-10), gold category scoped_exception
- user: There was one thing about what goes under my head on the floor I wanted to talk through.
- assistant: What do you tend to notice first about whether a pad shifts on a bare floor?
- user: If it raises my head too much I end up adjusting it between movements.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to floor exercise head support?  Let the arrangement be a thin piece of wool padding when the situation is floor practice on uncarpeted flooring. This temporary spell runs from the start of August 11 to the end of August 27.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "floor exercise head support", "value": "a thin piece of wool padding", "scope": "floor practice on uncarpeted flooring", "validity": {"from": "2027-08-11", "kind": "window", "to": "2027-08-27"}, "relations": [{"type": "EXCEPTION_TO", "target": "m4"}], "evidence_ids": ["e93b5def45d3164841543"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "floor exercise head support", "evidence_ids": ["e93b5def45d3164841543"], "operation": "ADD", "relations": [{"target": "m4", "type": "EXCEPTION_TO"}], "scope": "floor practice on uncarpeted flooring", "validity": {"from": "2027-08-11", "kind": "window", "to": "2027-08-27"}, "value": "a thin piece of wool padding"}], "decision": "resolved"}`

## 31. `te-0166/p31fff457ba0f093b0299/scope` (exception_revision, target probe)

- Question (2027-05-12): Pick a value for fruit crumble topping, dated May 12, with the setting described as crumbles baked in a shared dish.
- Options: a crisp buckwheat-cluster topping | a fine almond-sand topping | a loose rye-and-sunflower topping | a chunky oat-and-hazelnut topping
- Gold: **a loose rye-and-sunflower topping**; Answer Agent chose: **a crisp buckwheat-cluster topping**
- Answer Agent reply: "The record that applies on this date and in the situation of crumbles baked in a shared dish is the one with the scope \"crumbles baked in individual dishes\" and the value \"a crisp buckwheat-cluster topping,\" which is an exception to the general record.  \nAnswer: a crisp buckwheat-cluster topping"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "baked potato filling",
  "value": "herbed curd with grated radish",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "fruit crumble topping",
  "value": "a loose rye-and-sunflower topping",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "fruit crumble topping",
  "value": "a crisp buckwheat-cluster topping",
  "scope": "crumbles baked in individual dishes",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "baked potato filling",
  "value": "herbed curd with grated radish",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "fruit crumble topping",
  "value": "a loose rye-and-sunflower topping",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "fruit crumble topping",
  "value": "a crisp buckwheat-cluster topping",
  "scope": "crumbles baked in individual dishes",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 }
]
```

Events up to the probe:

### `e282df56befc50cc0eca1` (2027-05-08), gold category scoped_exception
- user: I remembered something about what I put inside the jacket potato while thinking about what you can scoop up from a paper tray.
- assistant: I'm listening. What's on your mind?
- user: Here's what I meant about what I put inside the jacket potato.  I am settling the question of eating the potato from a little paper tray with smoky beans with chopped scallions. I am not putting an end date on this preference.
- assistant: Is what you can scoop up from a paper tray part of what you want to work out?
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "baked potato filling", "value": "smoky beans with chopped scallions", "scope": "eating the potato from a little paper tray", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e282df56befc50cc0eca1"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "baked potato filling", "evidence_ids": ["e282df56befc50cc0eca1"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "eating the potato from a little paper tray with smoky beans", "validity": {"kind": "persistent"}, "value": "chopped scallions"}], "decision": "resolved"}`

### `ec71d6e97d9cac45f1d3a` (2027-05-09), gold category exception_revision
- user: I thought about what I put inside the jacket potato again this morning.
- assistant: How have you been thinking about it?
- user: Here's what I meant about what I put inside the jacket potato.  Let the arrangement be crushed peas with lemon zest when the situation is eating the potato from a little paper tray. That is what I always want under those circumstances.
- assistant: Did something in particular draw your attention to what you can scoop up from a paper tray?
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m5", "value": "crushed peas with lemon zest", "scope": "eating the potato from a little paper tray", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ec71d6e97d9cac45f1d3a"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ec71d6e97d9cac45f1d3a"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "eating the potato from a little paper tray", "target_id": "m5", "validity": {"kind": "persistent"}, "value": "crushed peas with lemon zest"}], "decision": "resolved"}`

### `ec8acd5937c3d8b99a086` (2027-05-10), gold category exception_retirement
- user: How neatly the filling stays in the potato has been on my mind. Can we get back to what I put inside the jacket potato?
- assistant: What would you like to work through first?
- user: I thought again about baked potato filling.  The normal choice should cover potatoes eaten from a paper boat, including future changes. I don’t need a different choice for that anymore.
- assistant: Could you say why how neatly the filling stays in the potato matters to you?
- user: I am accounting for how the food is served as well.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m6", "evidence_ids": ["ec8acd5937c3d8b99a086"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ec8acd5937c3d8b99a086"], "operation": "RETIRE", "target_id": "m6"}], "decision": "resolved"}`

### `e281508f138ecb852a705` (2027-05-12), gold category exception_retirement
- user: I had a point to make about what goes on top of the crumble. That separate choice for crumbles baked in a shared dish has run its course. Put it back under whatever I generally want.
- assistant: Is this partly about sharing a crumble without losing the crisp edge?
- user: I like the crisp part to hold up after I have served it.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m3", "evidence_ids": ["e281508f138ecb852a705"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e281508f138ecb852a705"], "operation": "RETIRE", "target_id": "m3"}], "decision": "resolved"}`

## 32. `te-0168/pd40d120398bffc488301/scope` (scoped_exception, boundary probe)

- Question (2027-05-08): Pick a value for baked potato filling, dated May 8, with the setting described as potatoes eaten from a bowl.
- Options: herbed curd with grated radish | smoky beans with chopped scallions | crushed peas with lemon zest | roasted mushrooms with thyme
- Gold: **crushed peas with lemon zest**; Answer Agent chose: **herbed curd with grated radish**
- Answer Agent reply: "The record that applies on May 8, 2027, with potatoes eaten from a bowl is \"herbed curd with grated radish,\" as it matches the specified situation and date within its validity window.  \nAnswer: herbed curd with grated radish"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "baked potato filling",
  "value": "crushed peas with lemon zest",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "baked potato filling",
  "value": "smoky beans with chopped scallions",
  "scope": "eating the potato from a little paper tray",
  "validity": {
   "from": "2027-05-05",
   "kind": "window",
   "to": "2027-05-25"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "eb84843a39724a9abc7fa"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "baked potato filling",
  "value": "herbed curd with grated radish",
  "scope": "eating the potato out of a bowl",
  "validity": {
   "from": "2027-05-09",
   "kind": "window",
   "to": "2027-05-27"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e4132236b728bf1959647"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "baked potato filling",
  "value": "crushed peas with lemon zest",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "baked potato filling",
  "value": "smoky beans with chopped scallions",
  "scope": "eating the potato from a little paper tray",
  "validity": {
   "from": "2027-05-05",
   "kind": "window",
   "to": "2027-05-25"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "eb84843a39724a9abc7fa"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "baked potato filling",
  "value": "herbed curd with grated radish",
  "scope": "eating the potato out of a bowl",
  "validity": {
   "from": "2027-05-09",
   "kind": "window",
   "to": "2027-05-27"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e4132236b728bf1959647"
  ]
 }
]
```

Events up to the probe:

### `e16b232f2ff3c51a3193b` (2027-05-04), gold category clarify
- user: I had a point to make about what I put inside the jacket potato. I cannot yet attach smoky beans and scallion pieces to a particular situation: it is between eating the potato from a little paper tray and potatoes eaten from a bowl.
- assistant: Is there a connection with how the herbs and beans balance?
- user: I want the filling to be easy to scoop without coming away in one piece.
- assistant: How much more do you want to say about how neatly the filling stays in the potato?
- user: Not much more than that, really.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `eb84843a39724a9abc7fa` (2027-05-05), gold category scoped_exception
- user: Here's what I meant about what I put inside the jacket potato.  My request is to save smoky beans with chopped scallions for eating the potato from a little paper tray. Its first day is May 5; May 25 is included as the last, and then it is over.
- assistant: How did how the herbs and beans balance get on your mind?
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "baked potato filling", "value": "smoky beans with chopped scallions", "scope": "eating the potato from a little paper tray", "validity": {"from": "2027-05-05", "kind": "window", "to": "2027-05-25"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["eb84843a39724a9abc7fa"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "baked potato filling", "evidence_ids": ["eb84843a39724a9abc7fa"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "eating the potato from a little paper tray", "validity": {"from": "2027-05-05", "kind": "window", "to": "2027-05-25"}, "value": "smoky beans with chopped scallions"}], "decision": "resolved"}`

### `e8410e9b57ab0390ee3e1` (2027-05-07), gold category clarify
- user: There was one thing about what I put inside the jacket potato I wanted to talk through.
- assistant: Did you want to say what you had in mind?
- user: I had a point to make about what I put inside the jacket potato. I cannot yet attach herbed curd with grated radish to a particular situation: it is between potatoes eaten from a paper boat and potatoes eaten from a bowl.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e4132236b728bf1959647` (2027-05-08), gold category scoped_exception
- user: Here's what I meant about what I put inside the jacket potato.  Keep herbed curd with grated radish in mind as the choice I am making for eating the potato out of a bowl. This temporary spell runs from the start of May 9 to the end of May 27. Anything outside this request keeps the choices it already had.
- assistant: There's room to talk more about how the herbs and beans balance if you want.
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "baked potato filling", "value": "herbed curd with grated radish", "scope": "eating the potato out of a bowl", "validity": {"from": "2027-05-09", "kind": "window", "to": "2027-05-27"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e4132236b728bf1959647"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "baked potato filling", "evidence_ids": ["e4132236b728bf1959647"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "eating the potato out of a bowl", "validity": {"from": "2027-05-09", "kind": "window", "to": "2027-05-27"}, "value": "herbed curd with grated radish"}], "decision": "resolved"}`

## 33. `te-0176/p03fd4d904ff08a612ad8/scope` (scoped_exception, neighbor probe)

- Question (2027-04-13): Pick a value for baked potato filling, dated April 13, with the setting described as potatoes eaten from a paper boat.
- Options: roasted mushrooms with thyme | smoky beans with chopped scallions | herbed curd with grated radish | crushed peas with lemon zest
- Gold: **crushed peas with lemon zest**; Answer Agent chose: **smoky beans with chopped scallions**
- Answer Agent reply: "The record that applies on April 13, 2027, with the setting of potatoes eaten from a paper boat is \"smoky beans with chopped scallions\".  \nAnswer: smoky beans with chopped scallions"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "baked potato filling",
  "value": "roasted mushrooms with thyme",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "baked potato filling",
  "value": "smoky beans with chopped scallions",
  "scope": "potatoes eaten from a paper boat",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "baked potato filling",
  "value": "crushed peas with lemon zest",
  "scope": "eating the potato from a little paper tray",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e23a6811900e516a61c14"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "baked potato filling",
  "value": "herbed curd with grated radish",
  "scope": "eating the potato out of a bowl",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ef44ecb96deb19a32f824"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "baked potato filling",
  "value": "roasted mushrooms with thyme",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "baked potato filling",
  "value": "crushed peas with lemon zest",
  "scope": "potatoes eaten from a paper boat",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e23a6811900e516a61c14"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "baked potato filling",
  "value": "herbed curd with grated radish",
  "scope": "eating the potato out of a bowl",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ef44ecb96deb19a32f824"
  ]
 }
]
```

Events up to the probe:

### `ec0ff7b0c575cba29e151` (2027-04-10), gold category clarify
- user: Can we get back to baked potato filling?  The choice sounds like crushed peas with lemon zest; the situation is still a question between eating the potato from a little paper tray and eating the potato out of a bowl.
- assistant: I can see how how neatly the filling stays in the potato could make a difference.
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e975d5afa4081696cc630` (2027-04-11), gold category exception_retirement
- user: I thought about what I put inside the jacket potato again this morning.
- assistant: What did you want me to know?
- user: I had a point to make about what I put inside the jacket potato. Undo the separate arrangement we gave potatoes eaten from a bowl; my everyday preference is what should govern it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "RETIRE", "target_id": "m3", "evidence_ids": ["e975d5afa4081696cc630"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e975d5afa4081696cc630"], "operation": "RETIRE", "target_id": "m3"}], "decision": "resolved"}`

### `e23a6811900e516a61c14` (2027-04-12), gold category exception_revision
- user: I thought about what I put inside the jacket potato again this morning.
- assistant: What would you like to work through first?
- user: I thought again about what I put inside the jacket potato.  The option I am selecting where eating the potato from a little paper tray is concerned is crushed peas with lemon zest. I need it for a while rather than once, and rather than forever. No end is fixed.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "crushed peas with lemon zest", "scope": "potatoes eaten from a paper boat", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e23a6811900e516a61c14"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "baked potato filling", "evidence_ids": ["e23a6811900e516a61c14"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "eating the potato from a little paper tray", "validity": {"kind": "open"}, "value": "crushed peas with lemon zest"}], "decision": "resolved"}`

### `ef44ecb96deb19a32f824` (2027-04-13), gold category scoped_exception
- user: I thought again about what I put inside the jacket potato.  When eating the potato out of a bowl comes up, my choice is herbed curd with grated radish. For the time being, keep using it. The need is temporary, but its duration is unknown.
- assistant: There's room to talk more about how neatly the filling stays in the potato if you want.
- user: I want the filling to be easy to scoop without coming away in one piece.
- assistant: Would you prefer to talk more about how the herbs and beans balance another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "baked potato filling", "value": "herbed curd with grated radish", "scope": "eating the potato out of a bowl", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ef44ecb96deb19a32f824"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "baked potato filling", "evidence_ids": ["ef44ecb96deb19a32f824"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "eating the potato out of a bowl", "validity": {"kind": "open"}, "value": "herbed curd with grated radish"}], "decision": "resolved"}`

## 34. `te-0177/p3995abd209ad4a15c6a9/scope` (exception_revision, neighbor probe)

- Question (2027-08-06): Pick a value for stylus pressure response, dated August 6, with the setting described as stylus work on a smooth screen cover.
- Options: a firm-pressure response curve | a nearly uniform stroke response | a light-touch pressure curve | a gradual midrange pressure curve
- Gold: **a light-touch pressure curve**; Answer Agent chose: **a firm-pressure response curve**
- Answer Agent reply: "The record that applies on this date and in the situation of stylus work on a smooth screen cover is the general preference, as no specific record matches the condition of a smooth screen cover.  \nAnswer: a firm-pressure response curve"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "stylus pressure response",
  "value": "a firm-pressure response curve",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "stylus pressure response",
  "value": "a light-touch pressure curve",
  "scope": "drawing on a slick screen protector",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "efba7975566ee19469f57"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "stylus pressure response",
  "value": "a gradual midrange pressure curve",
  "scope": "stylus work on a textured screen cover",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e85dc831fdb328072e56a"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "stylus pressure response",
  "value": "a firm-pressure response curve",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "stylus pressure response",
  "value": "a light-touch pressure curve",
  "scope": "drawing on a slick screen protector",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "efba7975566ee19469f57"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "stylus pressure response",
  "value": "a gradual midrange pressure curve",
  "scope": "stylus work on a textured screen cover",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e85dc831fdb328072e56a"
  ]
 }
]
```

Events up to the probe:

### `e43aa74b34ab070fd06df` (2027-08-02), gold category clarify
- user: I had a point to make about how hard I press with the pen. There are two possible homes for a pressure setting tuned for a light touch, stylus work on a smooth screen cover and drawing on a screen protector with texture, and I have not picked one.
- assistant: Is this partly about getting small marks on a slick cover?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `efba7975566ee19469f57` (2027-08-03), gold category scoped_exception
- user: I thought again about how hard I press with the pen.  Let the arrangement be a light-touch pressure curve when the situation is drawing on a slick screen protector. That is what I always want under those circumstances.
- assistant: Tell me what struck you about keeping the line from jumping in width.
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "stylus pressure response", "value": "a light-touch pressure curve", "scope": "drawing on a slick screen protector", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["efba7975566ee19469f57"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "stylus pressure response", "evidence_ids": ["efba7975566ee19469f57"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "drawing on a slick screen protector", "validity": {"kind": "persistent"}, "value": "a light-touch pressure curve"}], "decision": "resolved"}`

### `ebe29db3c0c7dc8153b12` (2027-08-04), gold category stable_preference
- user: Can we get back to how hard I press with the pen?  I came back to the same general preference, pressure settings built around a firm touch. The choices I already have still stand.
- assistant: How has keeping the line from jumping in width worked out in practice?
- user: It bothers me when a small change in pressure makes the stroke jump.
- assistant: Is there anything about how much pressure it takes to make a dark stroke we haven’t touched on?
- user: Nothing I wanted to get into this time.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `ee3b609c3026c2371c143` (2027-08-05), gold category exception_revision
- user: I thought again about how hard I press with the pen.  For drawing on a screen protector with texture, please remember that I choose a light-touch pressure curve. This is for the long run rather than a temporary spell.
- assistant: Is there a connection with keeping the line from jumping in width?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "a light-touch pressure curve", "scope": "stylus work on a textured screen cover", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["ee3b609c3026c2371c143"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ee3b609c3026c2371c143"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "stylus work on a textured screen cover", "target_id": "m2", "validity": {"kind": "persistent"}, "value": "a light-touch pressure curve"}], "decision": "resolved"}`

### `e85dc831fdb328072e56a` (2027-08-06), gold category exception_revision
- user: Can we get back to how hard I press with the pen?  Given stylus work on a textured screen cover, make the choice a gradual midrange pressure curve. Next time, and after that, I still want this choice.
- assistant: What's your biggest concern around getting small marks on a slick cover?
- user: It bothers me when a small change in pressure makes the stroke jump.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m4", "value": "a gradual midrange pressure curve", "scope": "stylus work on a textured screen cover", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e85dc831fdb328072e56a"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e85dc831fdb328072e56a"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "stylus work on a textured screen cover", "target_id": "m4", "validity": {"kind": "persistent"}, "value": "a gradual midrange pressure curve"}], "decision": "resolved"}`

## 35. `te-0188/p4d0a574d20f41de9bb39/scope` (stable_preference, target probe)

- Question (2027-12-09): Pick a value for bath-towel border style, dated December 9, with the setting described as towels hung across a rail.
- Options: a broad flat linen border | a narrow woven herringbone border | a doubled terry border with rounded corners | a soft fringed edge without a band
- Gold: **a broad flat linen border**; Answer Agent chose: **a doubled terry border with rounded corners**
- Answer Agent reply: "The record that applies on this date and in this situation is m2, which specifies \"a doubled terry border with rounded corners\" for towels hung on a wall hook, and since the situation \"towels hung across a rail\" is similar to \"towels hung on a wall hook,\" this record is relevant.  \nAnswer: a doubled terry border with rounded corners"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "bath-towel border style",
  "value": "a soft fringed edge without a band",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "bath-towel border style",
  "value": "a doubled terry border with rounded corners",
  "scope": "towels hung on a wall hook",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "bath-towel border style",
  "value": "a wide smooth linen strip",
  "scope": "drying the towel over a bar",
  "validity": {
   "from": "2027-12-08",
   "kind": "window",
   "to": "2027-12-31"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e00ea88869c7b4728836e"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "bath-towel border style",
  "value": "a soft fringed edge without a band",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "bath-towel border style",
  "value": "a doubled terry border with rounded corners",
  "scope": "towels hung on a wall hook",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "bath-towel border style",
  "value": "a wide smooth linen strip",
  "scope": "drying the towel over a bar",
  "validity": {
   "from": "2027-12-08",
   "kind": "window",
   "to": "2027-12-31"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e00ea88869c7b4728836e"
  ]
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

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

### `e00ea88869c7b4728836e` (2027-12-08), gold category scoped_exception
- user: I had a point to make about bath-towel border style. A wide smooth linen strip is the one I want when we are talking about drying the towel over a bar. The dates are December 8 through December 31, with both counted; after that I am back to the ordinary choice.
- assistant: There's room to talk more about how the edge sits on the rail if you want.
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "bath-towel border style", "value": "a wide smooth linen strip", "scope": "drying the towel over a bar", "validity": {"from": "2027-12-08", "kind": "window", "to": "2027-12-31"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e00ea88869c7b4728836e"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "bath-towel border style", "evidence_ids": ["e00ea88869c7b4728836e"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "drying the towel over a bar", "validity": {"from": "2027-12-08", "kind": "window", "to": "2027-12-31"}, "value": "a wide smooth linen strip"}], "decision": "resolved"}`

### `e08cdf59a4a986509f57b` (2027-12-09), gold category stable_preference
- user: Whether the fringe catches on the hook has been on my mind. Can we get back to the edge finish on the bath towel?
- assistant: Did you want to say what you had in mind?
- user: Can we get back to the edge finish on the bath towel?  I came back to the same general preference, a soft fringed edge without a band. The choices I already have still stand.
- assistant: How did whether the fringe catches on the hook get on your mind?
- user: I use the edge to tell which towel is which in a stack.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 36. `te-0189/p117a239d2a41245e01d9/scope` (stable_preference, default probe)

- Question (2027-06-15): Pick a value for scratch-paper use pattern, dated June 15, with the setting described as an ordinary occasion.
- Options: several calculations in a spiral column | calculations arranged around a central sketch | calculations on folded pocket slips | one calculation per loose square
- Gold: **one calculation per loose square**; Answer Agent chose: **several calculations in a spiral column**
- Answer Agent reply: "The record that applies on this date and in this situation is the general scratch-paper use pattern, as no specific record is limited to an \"ordinary occasion\" or a particular setting.  \nAnswer: several calculations in a spiral column"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m2",
  "attribute": "scratch-paper use pattern",
  "value": "several calculations in a spiral column",
  "scope": "rough calculations at a seated desk",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "unfinished-task handoff note",
  "value": "a small done-and-pending grid",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "scratch-paper use pattern",
  "value": "a quick drawing of what depends on what",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e9a46563b751baa4bc78a"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "scratch-paper use pattern",
  "value": "calculations on folded pocket slips first",
  "scope": "rough calculations at a standing desk",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e912eae96fd811d4d2847"
  ]
 },
 {
  "memory_id": "m8",
  "attribute": "unfinished-task handoff note",
  "value": "one short line about the next step",
  "scope": "handoffs to a single collaborator",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   },
   {
    "type": "REPLACES",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "ee02f9c049d6084833be8"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "scratch-paper use pattern",
  "value": "one calculation per loose square",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "scratch-paper use pattern",
  "value": "several calculations in a spiral column",
  "scope": "rough calculations at a seated desk",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "unfinished-task handoff note",
  "value": "a quick drawing of what depends on what",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "e9a46563b751baa4bc78a"
  ]
 },
 {
  "memory_id": "m7",
  "attribute": "scratch-paper use pattern",
  "value": "calculations on folded pocket slips",
  "scope": "rough calculations at a standing desk",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   },
   {
    "type": "REPLACES",
    "target": "m3"
   }
  ],
  "evidence_ids": [
   "e912eae96fd811d4d2847"
  ]
 },
 {
  "memory_id": "m8",
  "attribute": "unfinished-task handoff note",
  "value": "one short line about the next step",
  "scope": "handoffs to a single collaborator",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "ee02f9c049d6084833be8"
  ]
 }
]
```

Events up to the probe:

### `e9a46563b751baa4bc78a` (2027-06-09), gold category general_update
- user: I thought again about what I leave for the next person.  My request is to save a quick drawing of what depends on what for the general choice rather than a special case. This is for the long run rather than a temporary spell.
- assistant: Did something in particular draw your attention to how much history the next person needs?
- user: I want the next person to see where to begin without asking me to explain it again.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m4", "value": "a quick drawing of what depends on what", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e9a46563b751baa4bc78a"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e9a46563b751baa4bc78a"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "a quick drawing of what depends on what"}], "decision": "resolved"}`

### `e668ad20aa975dac31372` (2027-06-10), gold category clarify
- user: I had a point to make about what I leave for the next person. Do not put a brief next-step sentence anywhere yet. I have not answered whether it is for handoffs to a single collaborator or handoffs to a rotating group.
- assistant: Is there a connection with how much history the next person needs?
- user: I want the next person to see where to begin without asking me to explain it again.
- assistant: Do you have another thought on making the next step visible?
- user: Not one I can put into words right now.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e912eae96fd811d4d2847` (2027-06-11), gold category exception_revision
- user: I thought about how I lay out working on spare paper again this morning.
- assistant: What did you want me to know?
- user: Here's what I meant about how I lay out working on spare paper.  I would put calculations on folded pocket slips first for working out sums on my feet at the desk. I mean an enduring arrangement rather than a one-off. That does not change the rest of my preferences.
- assistant: How did being able to follow sums on a small scrap get on your mind?
- user: I need to look back at the working without losing which sum is which.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m3", "value": "calculations on folded pocket slips", "scope": "rough calculations at a standing desk", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e912eae96fd811d4d2847"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e912eae96fd811d4d2847"], "operation": "REVISE", "relations": [{"target": "m6", "type": "EXCEPTION_TO"}], "scope": "rough calculations at a standing desk", "target_id": "m3", "validity": {"kind": "persistent"}, "value": "calculations on folded pocket slips first"}], "decision": "resolved"}`

### `ee02f9c049d6084833be8` (2027-06-13), gold category exception_revision
- user: How much history the next person needs has been on my mind. Can we get back to what I leave for the next person?
- assistant: Was something about how much history the next person needs especially important?
- user: Here's what I meant about what I leave for the next person.  For handoffs to a single collaborator, please remember that I choose one short line about the next step. Keep it in place for recurring occasions of this sort.
- assistant: Could you say why how much history the next person needs matters to you?
- user: I want the next person to see where to begin without asking me to explain it again.
- assistant: Would you prefer to talk more about how much history the next person needs another time?
- user: Sure, there’s no need to get into it further right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m5", "value": "one short line about the next step", "scope": "handoffs to a single collaborator", "validity": {"kind": "persistent"}, "relations": [{"type": "EXCEPTION_TO", "target": "m6"}], "evidence_ids": ["ee02f9c049d6084833be8"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ee02f9c049d6084833be8"], "operation": "REVISE", "relations": [{"target": "m4", "type": "EXCEPTION_TO"}], "scope": "handoffs to a single collaborator", "target_id": "m5", "validity": {"kind": "persistent"}, "value": "one short line about the next step"}], "decision": "resolved"}`

### `e90002fe87e0a15ac6f00` (2027-06-15), gold category stable_preference
- user: Can we get back to how I lay out working on spare paper?  I'm not picking a lasting arrangement for rough calculations at a seated desk; I need something for this instance.
- assistant: How has being able to follow sums on a small scrap worked out in practice?
- user: I need to look back at the working without losing which sum is which.
- assistant: What's the choice you'd make?
- user: Let's go with calculations arranged around a central sketch.
- assistant: Are you happy to stop there about being able to follow sums on a small scrap?
- user: Yes, I don't have anything to add.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 37. `te-0192/p9511a82cf48e46e81104/scope` (scoped_exception, boundary probe)

- Question (2027-10-01): Pick a value for group-poll update trigger, dated October 1, with the setting described as polls offering exactly two choices.
- Options: a notice when a different choice takes the lead | a notice when half the group has voted | a notice whenever a vote arrives | a notice after every participant has voted
- Gold: **a notice when a different choice takes the lead**; Answer Agent chose: **a notice whenever a vote arrives**
- Answer Agent reply: "On 2027-10-01, for polls offering exactly two choices, the record that applies is the time-limited one (\"a ping on each incoming vote\") from m5, which is valid from 2027-09-07 to 2027-09-30.  \nAnswer: a notice whenever a vote arrives"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "group-poll update trigger",
  "value": "a notice when a different choice takes the lead",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "water-flask refill alert",
  "value": "a pair of short vibration pulses",
  "scope": "refill tracking with a small flask",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "water-flask refill alert",
  "value": "two little buzzes in a row",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "ebca23f881d6abbce7ec9"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "group-poll update trigger",
  "value": "a ping on each incoming vote",
  "scope": "polls with two possible answers",
  "validity": {
   "from": "2027-09-07",
   "kind": "window",
   "to": "2027-09-30"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "edf1884d970297ea218fd"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "group-poll update trigger",
  "value": "a notice when a different choice takes the lead",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "water-flask refill alert",
  "value": "a pair of short vibration pulses",
  "scope": "refill tracking with a small flask",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m4"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "water-flask refill alert",
  "value": "two little buzzes in a row",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "ebca23f881d6abbce7ec9"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "group-poll update trigger",
  "value": "a ping on each incoming vote",
  "scope": "polls with two possible answers",
  "validity": {
   "from": "2027-09-07",
   "kind": "window",
   "to": "2027-09-30"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "edf1884d970297ea218fd"
  ]
 }
]
```

Events up to the probe:

### `ebca23f881d6abbce7ec9` (2027-09-05), gold category general_update
- user: I had a point to make about what reminds me to top up the flask. It is two little buzzes in a row that I want for the general everyday case. It is meant to last beyond the occasion in front of us.
- assistant: What do you tend to notice first about knowing when the little flask is empty?
- user: I want to notice the refill cue without distracting anyone nearby.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "two little buzzes in a row", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["ebca23f881d6abbce7ec9"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ebca23f881d6abbce7ec9"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m2", "validity": {"kind": "persistent"}, "value": "two little buzzes in a row"}], "decision": "resolved"}`

### `edf1884d970297ea218fd` (2027-09-07), gold category scoped_exception
- user: There was one thing about when I get news from the poll I wanted to talk through.
- assistant: Did you want to say what you had in mind?
- user: Can we get back to when I get news from the poll?  Given polls with two possible answers, make the choice a ping on each incoming vote. Only occasions in September 7 to September 30, with both ends included, get this arrangement.
- assistant: What do you tend to notice first about finding out that the vote has changed?
- user: I care about a change that actually tells me something about the vote.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "group-poll update trigger", "value": "a ping on each incoming vote", "scope": "polls with two possible answers", "validity": {"from": "2027-09-07", "kind": "window", "to": "2027-09-30"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["edf1884d970297ea218fd"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "group-poll update trigger", "evidence_ids": ["edf1884d970297ea218fd"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "polls with two possible answers", "validity": {"from": "2027-09-07", "kind": "window", "to": "2027-09-30"}, "value": "a ping on each incoming vote"}], "decision": "resolved"}`

## 38. `te-0194/p2fb7c9a64cb4b990f241/scope` (stable_preference, target probe)

- Question (2027-02-14): Pick a value for museum visit starting point, dated February 14, with the setting described as museum visits on an upper-floor ticket.
- Options: starting with the smallest gallery | starting with the central installation | starting with the oldest display | starting with the newest acquisition
- Gold: **starting with the smallest gallery**; Answer Agent chose: **starting with the tiniest gallery**
- Answer Agent reply: "The record that applies on this date and in this situation is m4, which specifies \"the tiniest gallery comes first\" for museum visits on an upper-floor ticket.  \nAnswer: starting with the tiniest gallery"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m3",
  "attribute": "museum visit starting point",
  "value": "starting with the oldest display",
  "scope": "museum visits on a ground-floor ticket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "museum visit starting point",
  "value": "the tiniest gallery comes first",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e52c38b78a4caab758ca4"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "museum visit starting point",
  "value": "starting with the smallest gallery",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "e5cb178619c201e961f7b"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m3",
  "attribute": "museum visit starting point",
  "value": "starting with the oldest display",
  "scope": "museum visits on a ground-floor ticket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "museum visit starting point",
  "value": "the tiniest gallery comes first",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m6"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e52c38b78a4caab758ca4"
  ]
 },
 {
  "memory_id": "m6",
  "attribute": "museum visit starting point",
  "value": "starting with the smallest gallery",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "e5cb178619c201e961f7b"
  ]
 }
]
```

Events up to the probe:

### `e52c38b78a4caab758ca4` (2027-02-10), gold category exception_revision
- user: The displays nearest the stairs has been on my mind. Can we get back to which part of the exhibition I see first?
- assistant: Feel free to start with whatever's most useful.
- user: Here's what I meant about museum visit starting point.  It is the tiniest gallery comes first that I want for museum visits on an upper-floor ticket. Not permanently, and not just this time: it continues provisionally with no closing date.
- assistant: What's your biggest concern around the displays nearest the stairs?
- user: It helps me to pick a starting point before I get caught up looking around.
- assistant: Do you have another thought on what there is time to see first?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "the tiniest gallery comes first", "scope": "museum visits on an upper-floor ticket", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e52c38b78a4caab758ca4"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e52c38b78a4caab758ca4"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "museum visits on an upper-floor ticket", "target_id": "m2", "validity": {"kind": "open"}, "value": "the tiniest gallery comes first"}], "decision": "resolved"}`

### `ee23a8bcead4a4111ad56` (2027-02-12), gold category general_update
- user: I remembered something about which part of the exhibition I see first while thinking about what there is time to see first.
- assistant: What would you like to work through first?
- user: I thought again about which part of the exhibition I see first.  I would put starting with the newest acquisition first for the everyday situation. This is for the long run rather than a temporary spell.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "starting with the newest acquisition", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["ee23a8bcead4a4111ad56"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ee23a8bcead4a4111ad56"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "starting with the newest acquisition"}], "decision": "resolved"}`

### `e5cb178619c201e961f7b` (2027-02-13), gold category general_update
- user: I've got a minute now to explain what I mean about which part of the exhibition I see first.
- assistant: I'm listening. What's on your mind?
- user: Can we get back to which part of the exhibition I see first?  It is starting with the smallest gallery that I want for everyday use with no dedicated arrangement. That goes for the occasions ahead, with no finishing point.
- assistant: Is there a connection with how to begin walking around the exhibition?
- user: It helps me to pick a starting point before I get caught up looking around.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m5", "value": "starting with the smallest gallery", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["e5cb178619c201e961f7b"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e5cb178619c201e961f7b"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m5", "validity": {"kind": "persistent"}, "value": "starting with the smallest gallery"}], "decision": "resolved"}`

### `e4a9f6b7bca45db397658` (2027-02-14), gold category stable_preference
- user: I thought about which part of the exhibition I see first again this morning.
- assistant: I see why this could come up while thinking about what there is time to see first.
- user: It helps me to pick a starting point before I get caught up looking around.
- assistant: What would you like to work through first?
- user: Can we get back to museum visit starting point?  An acquaintance was saying, "Keep starting with the newest acquisition in mind as the choice I am making for museum visits on an upper-floor ticket. I need it for a while rather than once, and rather than forever. No end is fixed." I am leaving my own arrangements as they are.

Gold output: `{"decision": "resolved", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "resolved"}`

## 39. `te-0194/p5bcc6135dade052818a6/scope` (general_update, target probe)

- Question (2027-02-12): Pick a value for museum visit starting point, dated February 12, with the setting described as an ordinary occasion.
- Options: starting with the oldest display | starting with the newest acquisition | starting with the smallest gallery | starting with the central installation
- Gold: **starting with the newest acquisition**; Answer Agent chose: **starting with the oldest display**
- Answer Agent reply: "The record that applies on this date and in this situation is \"starting with the oldest display,\" as it is a persistent record for museum visits on a ground-floor ticket, which aligns with an ordinary occasion and no specific ticket type is mentioned.  \nAnswer: starting with the oldest display"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m3",
  "attribute": "museum visit starting point",
  "value": "starting with the oldest display",
  "scope": "museum visits on a ground-floor ticket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "museum visit starting point",
  "value": "the tiniest gallery comes first",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m5"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e52c38b78a4caab758ca4"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "museum visit starting point",
  "value": "starting with the newest acquisition",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ee23a8bcead4a4111ad56"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m3",
  "attribute": "museum visit starting point",
  "value": "starting with the oldest display",
  "scope": "museum visits on a ground-floor ticket",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m5"
   }
  ],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m4",
  "attribute": "museum visit starting point",
  "value": "the tiniest gallery comes first",
  "scope": "museum visits on an upper-floor ticket",
  "validity": {
   "kind": "open"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m5"
   },
   {
    "type": "REPLACES",
    "target": "m2"
   }
  ],
  "evidence_ids": [
   "e52c38b78a4caab758ca4"
  ]
 },
 {
  "memory_id": "m5",
  "attribute": "museum visit starting point",
  "value": "starting with the newest acquisition",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [
   {
    "type": "REPLACES",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "ee23a8bcead4a4111ad56"
  ]
 }
]
```

Events up to the probe:

### `e52c38b78a4caab758ca4` (2027-02-10), gold category exception_revision
- user: The displays nearest the stairs has been on my mind. Can we get back to which part of the exhibition I see first?
- assistant: Feel free to start with whatever's most useful.
- user: Here's what I meant about museum visit starting point.  It is the tiniest gallery comes first that I want for museum visits on an upper-floor ticket. Not permanently, and not just this time: it continues provisionally with no closing date.
- assistant: What's your biggest concern around the displays nearest the stairs?
- user: It helps me to pick a starting point before I get caught up looking around.
- assistant: Do you have another thought on what there is time to see first?
- user: Not one I can put into words right now.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m2", "value": "the tiniest gallery comes first", "scope": "museum visits on an upper-floor ticket", "validity": {"kind": "open"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e52c38b78a4caab758ca4"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["e52c38b78a4caab758ca4"], "operation": "REVISE", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "museum visits on an upper-floor ticket", "target_id": "m2", "validity": {"kind": "open"}, "value": "the tiniest gallery comes first"}], "decision": "resolved"}`

### `ee23a8bcead4a4111ad56` (2027-02-12), gold category general_update
- user: I remembered something about which part of the exhibition I see first while thinking about what there is time to see first.
- assistant: What would you like to work through first?
- user: I thought again about which part of the exhibition I see first.  I would put starting with the newest acquisition first for the everyday situation. This is for the long run rather than a temporary spell.

Gold output: `{"decision": "resolved", "actions": [{"operation": "REVISE", "target_id": "m1", "value": "starting with the newest acquisition", "scope": "general", "validity": {"kind": "persistent"}, "relations": [], "evidence_ids": ["ee23a8bcead4a4111ad56"]}]}`
Policy output (accepted): `{"actions": [{"evidence_ids": ["ee23a8bcead4a4111ad56"], "operation": "REVISE", "relations": [], "scope": "general", "target_id": "m1", "validity": {"kind": "persistent"}, "value": "starting with the newest acquisition"}], "decision": "resolved"}`

## 40. `te-0196/p01ff927a0aad0a54bdd7/scope` (scoped_exception, boundary probe)

- Question (2027-05-08): Pick a value for baked potato filling, dated May 8, with the setting described as potatoes eaten from a bowl.
- Options: herbed curd with grated radish | smoky beans with chopped scallions | crushed peas with lemon zest | roasted mushrooms with thyme
- Gold: **crushed peas with lemon zest**; Answer Agent chose: **herbed curd with grated radish**
- Answer Agent reply: "The record that applies on May 8, 2027, with potatoes eaten from a bowl is \"herbed curd with grated radish,\" as it matches the specified situation and falls within the validity window (May 9 to May 27, 2027).  \nAnswer: herbed curd with grated radish"

Memory at the probe (this arm):
```json
[
 {
  "memory_id": "m1",
  "attribute": "baked potato filling",
  "value": "crushed peas with lemon zest",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "baked potato filling",
  "value": "smoky beans with chopped scallions",
  "scope": "eating the potato from a little paper tray",
  "validity": {
   "from": "2027-05-05",
   "kind": "window",
   "to": "2027-05-25"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e4a2cc9b5590448318800"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "baked potato filling",
  "value": "herbed curd with grated radish",
  "scope": "eating the potato out of a bowl",
  "validity": {
   "from": "2027-05-09",
   "kind": "window",
   "to": "2027-05-27"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e561a2fd6aee9c35df8be"
  ]
 }
]
```

Gold memory at the probe (same format):
```json
[
 {
  "memory_id": "m1",
  "attribute": "baked potato filling",
  "value": "crushed peas with lemon zest",
  "scope": "general",
  "validity": {
   "kind": "persistent"
  },
  "relations": [],
  "evidence_ids": [
   "seed"
  ]
 },
 {
  "memory_id": "m2",
  "attribute": "baked potato filling",
  "value": "smoky beans with chopped scallions",
  "scope": "eating the potato from a little paper tray",
  "validity": {
   "from": "2027-05-05",
   "kind": "window",
   "to": "2027-05-25"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e4a2cc9b5590448318800"
  ]
 },
 {
  "memory_id": "m3",
  "attribute": "baked potato filling",
  "value": "herbed curd with grated radish",
  "scope": "eating the potato out of a bowl",
  "validity": {
   "from": "2027-05-09",
   "kind": "window",
   "to": "2027-05-27"
  },
  "relations": [
   {
    "type": "EXCEPTION_TO",
    "target": "m1"
   }
  ],
  "evidence_ids": [
   "e561a2fd6aee9c35df8be"
  ]
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

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e4a2cc9b5590448318800` (2027-05-05), gold category scoped_exception
- user: Here's what I meant about what I put inside the jacket potato.  My request is to save smoky beans with chopped scallions for eating the potato from a little paper tray. Its first day is May 5; May 25 is included as the last, and then it is over.
- assistant: How did how the herbs and beans balance get on your mind?
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "baked potato filling", "value": "smoky beans with chopped scallions", "scope": "eating the potato from a little paper tray", "validity": {"from": "2027-05-05", "kind": "window", "to": "2027-05-25"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e4a2cc9b5590448318800"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "baked potato filling", "evidence_ids": ["e4a2cc9b5590448318800"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "eating the potato from a little paper tray", "validity": {"from": "2027-05-05", "kind": "window", "to": "2027-05-25"}, "value": "smoky beans with chopped scallions"}], "decision": "resolved"}`

### `e12bcef3c818d1f5cd7b3` (2027-05-07), gold category clarify
- user: There was one thing about what I put inside the jacket potato I wanted to talk through.
- assistant: Did you want to say what you had in mind?
- user: I had a point to make about what I put inside the jacket potato. I cannot yet attach herbed curd with grated radish to a particular situation: it is between potatoes eaten from a paper boat and potatoes eaten from a bowl.

Gold output: `{"decision": "clarify", "actions": [{"operation": "NOOP"}]}`
Policy output (accepted): `{"actions": [{"operation": "NOOP"}], "decision": "clarify"}`

### `e561a2fd6aee9c35df8be` (2027-05-08), gold category scoped_exception
- user: Here's what I meant about what I put inside the jacket potato.  Keep herbed curd with grated radish in mind as the choice I am making for eating the potato out of a bowl. This temporary spell runs from the start of May 9 to the end of May 27. Anything outside this request keeps the choices it already had.
- assistant: There's room to talk more about how the herbs and beans balance if you want.
- user: I want the filling to be easy to scoop without coming away in one piece.

Gold output: `{"decision": "resolved", "actions": [{"operation": "ADD", "attribute": "baked potato filling", "value": "herbed curd with grated radish", "scope": "eating the potato out of a bowl", "validity": {"from": "2027-05-09", "kind": "window", "to": "2027-05-27"}, "relations": [{"type": "EXCEPTION_TO", "target": "m1"}], "evidence_ids": ["e561a2fd6aee9c35df8be"]}]}`
Policy output (accepted): `{"actions": [{"attribute": "baked potato filling", "evidence_ids": ["e561a2fd6aee9c35df8be"], "operation": "ADD", "relations": [{"target": "m1", "type": "EXCEPTION_TO"}], "scope": "eating the potato out of a bowl", "validity": {"from": "2027-05-09", "kind": "window", "to": "2027-05-27"}, "value": "herbed curd with grated radish"}], "decision": "resolved"}`

