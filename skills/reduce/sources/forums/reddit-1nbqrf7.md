# Public announcement: AI is cool and all, but please use it wisely. Just because "it works" doesn't mean it's good enough.

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: ashkanahmadi
- Date: 2025-09-08
- Original location: https://www.reddit.com/r/webdev/comments/1nbqrf7/public_announcement_ai_is_cool_and_all_but_please/
- Copied: 2026-11-20, from the post and comment tree of the Arctic Shift Reddit archive API

## Text
I'm working with a friend who is a coder-gone-vibe-coder and he creates parts of the project with Cursor.

There are multiple issues with the code blocks (even though the project works for the end user) but under the hood, so much stuff wrong and it's a mess.

Look at this code.

We have 2 pieces of data coming from the database: `first_name` and `last_name`. Now compare the AI solution at creating the user's initials versus my solution:

AI / Cursor
```
const userName = profile.first_name + ' ' + profile.last_name

const initials = userName
  .split(' ')
  .filter(Boolean)
  .map(n => n[0])
  .join('')
  .slice(0, 2)
```

My code
```
const initials = profile?.first_name?.[0].toUpperCase() + profile?.last_name?.[0].toUpperCase()
```

My point isn't that I'm better than a computer. My point is that do not just mindlessly accept whatever ChatGPT and Cursor and Lovable output just because "well, it works so it's good".

End of public announcement!!!

### IgorFerreiraMoraes

AI isn't cool at all, and yes, you're better than a computer

### eyebrows360

Your formatting is not working well here at all, at least not on old.reddit, which everyone here should still be using.

### fromidable

That’s a really neat example of how these things “work.” Well, not like I really understand. But the way the LLM layers translate the concept of initials as a property of a full name is pretty fascinating. And for it to settle on the variable name of “userName” is pretty hilarious.

#### ashkanahmadi

Yeah. The thing is that, it's overly complicated but the output works only for 1-word first name and 1-word last name. That means if someone's name is Miguel Juan Sanchez Rodriguez, it's going to return "MJ" instead of "MS" haha overly-complicated and dumb is not a good combination.

##### fromidable

Oh no, OF COURSE, I didn’t even notice the naive “slice” right at the end.

##### WonderfulWafflesLast

I'm trying to understand why that name should result in MS for initials.

Not, like, in a computer science sense, but in a societal "what are initials" sense.

Would it not be MR? Or MJSR?

### Tatakai_

I use AI to help me debug and brainstorm. Sometimes I will ask it to write small parts of the code but I will ask it to explain everything in the code that I don't understand.

Basically, AI is great to help coding, but nothing AI does should be trusted unconditionally. Everything should be double checked. 

AI is like a really fast intern. They're useful but they're still learning.

#### myhf

You don't ask it. You prompt it and it autocompletes.

If you keep generating enough random code, you will eventually get something useful. But it's not learning.

##### tomhermans

True about the autocomplete.

If I ask it what does function x or why is OP's solution preferable, it will probably give me a good answer.
End result is I've learned.

And yes, I know to look critically at it's answers. I'd have to do the same with an answer on stackoverflow or someone's blog post

#### HaykoKoryun

If you don't understand the code it wrote, how can you trust the explanation is actually correct?

##### Tatakai_

Because they usually are. I supplement my research with other sources especially when things aren't clicking. And from experience explanations are usually right. 

Just keeping a healthy dose of distrust is usually good enough I think.

###### Ok-Yogurt2360

Usually right can be quite dangerous. I once made a simple tool that was right most of the time with one obvious exception. (Could not automate the check because it was in a limited no-code environment). Thing i learned: most people only do manual checks around 10 times. Afterwards they just stop doing it and get all upset when it bites them in the ass.

###### TheKingElessar

Hey, I found a comment of yours on a post about container heights where you referenced your "oh no, this is not the behavior I expected" checklist. Is this an actual checklist you have and can share? Trying to get more comfortable in the front-end and that sounds really useful considering my recent experiences!

##### Fit-Jeweler-1908

you can still use the web when using AI, & you can ask it to provide sources and read those sources... its really not that complicated.

###### HaykoKoryun

so when using AI to be more productive, you have to spend time coaxing the demon to do what you want after multiple attempts...


once it gets to a stage where there's something working, you have to triple check that it does what it's supposed to, since you don't understand the code... 


after all this you probably didn't learn anything, since you didn't actually write the code, you merely proof read it... 


you improved your prompt engineer-fu though, which is something...


remind me again how this is more productive? 

###### Fit-Jeweler-1908

In this example the purpose would be to learn, lol.. you ask for sources and go verify it's not crazy while learning something new.  How is this any different from reading a blog or tutorial, you still have to verify the author is doing things correctly and you most likely learn something along the way.  Just because a human wrote it in a blog or YouTube video, does not make it right. 


There are many ways to not have to coax it if you know what you want and need, this is just an example of the opposite: having it produce something outside your understanding and asking for assistance on what the code does along with sources, you can then go learn about the thing you didn't understand.  


I get AI can be counter productive in many cases, I won't deny that but it seems like people around here only deal in absolutes - which is quite silly.  It's another tool available to use when appropriate. 

###### ProletariatPat

It’s because devs are mostly sith

###### IlliterateJedi

People already do this, just with code they copy off of StackOverflow or forums without actually fully understanding what the code does.  Acting like this is some how new because people are doing it with AI is silly.

###### HaykoKoryun

Except the people who copy paste from Stackoverflow willy-nilly don't really pat themselves on the back, well most don't or if they do they will get ridiculed faster than you can say that word. 

###### razzzey

Also the reply on stack overflow most likely worked at some point for the person writing the answer (even if it's old). With ai there's a toss between a frankensteined shell command or one that doesn't exist at all.

###### HaykoKoryun

Yeap, and shit questions and answers get down voted at a reputation cost to the person down voting, so good up voted answers are actually mostly correct. There's no equivalent to that with current AI. 

##### Fidodo

The same way you learn anything? You can easily verify what it says by cross referencing it with documentation and by reading the code. Even though you can do that without AI, it's still faster to be given a reason you can verify than to try and figure it out on your own

###### HaykoKoryun

The person I was replying to said that they would get the AI to explain parts of the code that they don't understand. If AI has a high tendency of hallucinating, and you don't understand certain parts of the code, why would you trust the explanation? 

###### Fidodo

They're actually much better at explaining things based on existing data. They're bad at coming up with things though. But still, if you're a competent programmer you can easily tell if the explanation is right or not. Basically it's easier to verify.

#### krileon

>but they're still learning.

LLMs don't learn. They're basically querying a dataset. Please people stop looking at it from this perspective. In your example an intern would learn, remember, and apply the knowledge you've provided it from that point on. The LLM will happily forget by the next chat.

##### Tatakai_

I can tell "learning" is a trigger word when talking about AI because you're not the first person to misunderstand what I meant.

##### Robot_Graffiti

They're also not querying a dataset, the actual process is way more chaotic than a database query & the model doesn't contain any complete or coherent representations of the training data

#### Hands

> they're still learning.

This shows a fundamental lack of understanding of how LLMs work on your part

##### 73tada



 >>   they're still learning.

>This shows a fundamental lack of understanding of how LLMs work on your part


A different interpretation could be "As new models are released and existing models are fine tuned, as far as the consumer is concerned *"they're still learning"*".

"*They're*" can refer both to the models and the model creators.

###### CodeRadDesign

the obvious way to read it! not sure wtf is going on in this thread. if it's being brigaded by humans, they should probably write an AHK script to keep it a little less stupid.

###### Hands

They're still only capable of mimicking statistically likely output based on their training corpus not actual reasoning, and they're lightyears away from anything more fundamentally rational than that sort of thing.  Quite simply if the training data/corpus isn't there to begin with they aren't going to come up with appropriate solutions to new or obscure problems.  

Training them in specific domains can only go so far, especially if actual people mostly stop writing and/or publishing code because LLMs are doing most of it.  Kinda funny when you think about the fact that the future of LLM code agents is entirely dependent on actual OSS devs continuing to solve problems and publish their solutions independently.

I knew what you (and the OP in their reply) meant but I still think you have the wrong idea frankly and my comment still applies.

###### 73tada

It seems you are hinging your response on "AI can't create something new", "AI can't do domain specific", "AI can't reason". 

- 99.9999% of what humans create on a daily basis is not novel; if any thing, even for geniuses, it's incremental. 
- We have RAG, LoRa, and fine tunes for "domain specific".
- Most people can't fucking reason why their soda goes flat if they don't close the cap.


Yes, you can build a game engine with AI. Anything "huge and complex" is broken down into smaller chunks -just like every other software development process.

AI is a force multiplying tool. If you don't know how to use the tool, it's not going to work for you. If you understand programming in general and understand, say, iterating an array in any language and that SQL exists, you're 90% there for day-to-day development. 

Now the AI handles the low end shit that used to take all week while can you focus on the actual business logic that gets it done (which AI can also assist with, as guess what? The business logic isn't novel either!), 
  

>I knew what you (and the OP in their reply) meant but I still think you have the wrong idea frankly and my comment still applies.

I politely disagree and the stubbornness and pedantry helps no one.

##### Tatakai_

I meant that, like interns, LLMs are imperfect but useful. The learning bit was still referring to the intern analogy. 

But even if it wasn't, saying AIs still have much to learn can be said figuratively. I don't think it necessarily shows anything, but I think you're coming from a place of witnessing people misunderstand AI all the time.

#### CompetitionItchy6170

I usually use it to point me in the right direction, then dig into the docs or test things myself to make sure it holds up.

### theloneliestprince

this is a fun exercise!
what about

   `'${profile?.first_name[0]}${profile?.last_name[1]}'.toUppercase()`
(pretend i'm using a template literal here, I can't get it to work in reddit formatting lol)

#### ComfortingSounds53

Just add a nullish check so it wouldn't come out as  `UNDEFINEDUNDEFINED`

##### theloneliestprince

thank you! this is a good catch, I guess it's not any more concise after all. 
(I also sneakily added another check to my second example to avoid the issue)

###### frogic

I think if you just do ?? '' on your first and last name you should be fine. You also wouldn't have to null check your toUpperCase unless we're completely typeless, and optional accessing the string index doesn't do anything because it returns undefined when the index doesn't exist so the null coalicing operator will deal with it.  

###### TerribleLeg8379

Good fix. Adding validation is always better than assuming input types. Defensive programming saves time in the long run

##### Noch_ein_Kamel

I mean, OPs version comes out to "NaN" if profile is not correctly set, so the standards are quite low :p

#### chobinhood

Honestly in most applications there should be no way to have blank first/last or get here without a profile, so we should be asserting both for better observability. Failing silently here is not great.

##### theloneliestprince

I agree! I'm thinking of it more as an exercise in expressing concisely/clearly rather than like how I would right application code though.

##### clairebones

There are people with only one name though, most programmers should read this early in their career before they can enforce design patterns like "You can't have a blank forename or surname": [Falsehoods programmers believe about names](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/)

###### HeinousTugboat

Unfortunately for us, the programmers understand that. It's our report vendors that believe they can never be blank. So it's become a business decision that we can't support blank names.

###### simonraynor

Also the versions of that article about time and places, both excellent to bring up in meetings with the product guys

#### bluebird355

Could use charAt(0) too

### Realistic-Success260

Undefined

### Bubbly_Address_8975

AI is great for rapid prototyping  
AI is helpful for advanced auto complete  
AI is terrible at writing high quality maintanable production code

Thats my point of view, maybe I will be proven wrong in the future, but it hasnt happened yet.

#### Master_Lucario

AI is great for fooling employers they don't need junior Devs anymore -_-

##### HeinousTugboat

They do, they just won't realize it until the seniors start leaving and there's nobody left to fill the gap worth a damn.

###### SixPackOfZaphod

This right here, I'm expecting to be doing a lot of consulting in the future cleaning up garbage code from a whole generation of vibers.

#### kowdermesiter

You have to prompt it right and be specific how to implement something. If the agent gets to a working solution, you can ask it to refactor it and create a clean abstraction, I do it a lot.

##### Bubbly_Address_8975

Yes you do have to prompt it right, but there are limits, a lot of specific stuff it simply cannot do and even then it creates a littlebit of a mess, and the messier the code becomes the messier the outcome is meaning it gets progressively worse. Most stuff you are probably quicker to write by hand in the first place then letting the agent do it.

###### kowdermesiter

First, I'm using Claude Sonnet 4 with VSCode integration. I don't face this issue as you say and I'm using it for months now, on a daily basis. 

I could write these things by hand, but it won't be faster for me, each task takes a non trivial amount of time to build my context that requires to be "zoned in" as complexity grows. Now with AI I can make dinner, watch TV or do the dishes while the agent is grinding. If I have 15 minutes before leaving home, I can squeeze in a small bugfix or feature. 

My tick is to be very explicit what I want and how I want it. I use screenshots and logs, etc, 70% of the time it works on the first try, sometimes I do need to kick it a bit to do the right thing.

The codebase is not getting messier also, as I know what I'm doing, I'm regularly analyzing the codebase and instructing the AI do refactors, optimizations to keep things maintainable.

###### Bubbly_Address_8975

Copilot in VSCode with Sonnet 4 and GPT 5. We started integrating Copilot into our company roughly 1.5 - 2 years ago. I've been on the expert panel that decided on which tool to use in out company, and initially I was really impressed and looked forward to it. I did build some neural networks for computer vision, analysis and reinforcement learning prior (and played around with the original GANs in private).

So I would say I do have some experience with it.

For our production projects at work its completely useless. It cant generate anything useful most of the time, and I have to send back tons of merge request from those developers who try (its always obvious when someone relied on Copilot). It might be due to the fact that we use a unique custom architecture for our projects, maybe copilot has some problems handling that. I always thouhgt our backend architecture might be easier to handle for the AI, but according to our most seasoned and skilled backend engineers it does not seem to be the case there either.

We recently did a small hackathon in our business unit with roughly 20 engineers. The outcome was throughout the same: its great for rapid prototyping, but the code it produces becomes increasingly messy. Most of us used copilot, one colleague I know used a paid ChatGPT 5 subscription.

Maybe its just the fact that I have to switch contexts all the time anyway, but I dont see a difference. I have 15 minutes? Great, I can quickly pick up a small bug fix ticket and fix it, no problem. Faster than using AI. But of course, thats just my experience.

###### kowdermesiter

Sad to hear it doesn't work for you, it's awesome when it works for me.

> It might be due to the fact that we use a unique custom architecture for our projects, maybe copilot has some problems handling that.

Maybe there lies your problem. Have you looked at the faulty "PR-s" and tried to understand why it wanted to solve the problem the way it did? You can ask to describe your architecture and see if it gets it right.

You might want to create custom instructions on your architecture. A readme on your framework's rules and concepts might fix or at least improve things.

I'm using it on a production app with moderate complexity of 32k lines (backend and frontend). I'm a single developer though, so things area not the same.

###### Bubbly_Address_8975

Yes, certainly I write prompts usually specifically tied to the exact needs I have to work within the architecture. Does not help a lot unfortunately.

Regarding the merge request:

Often its just very basic mess. Inconsistent coding style, multiple imports, for tests multiple mocks that do the same thing and such.

### SpaceWanderer22

Alternative perspective: AI moves programming towards higher level declarative structure where it becomes more sensible to reason about systems at higher granularity. A focus on functionalism.

#### eyebrows360

If that were true, then yes, it would be true. It isn't.

##### SpaceWanderer22

I'm talking in the abstract silly.

###### eyebrows360

Then it's still abstractly untrue.

You're imagining these things are good enough to treat them as "higher level declarative structure". They aren't.

###### SpaceWanderer22

Your phrasing shows I framed it poorly - I don't mean that AI is some "higher level declarative structure", I mean that we can move towards a more functional approach with input -> output of higher and higher level systems. We can declare properties of the system and AI can implement it. This has generally been the trend of higher level languages. I don't mean tools are mature enough for this now, I'm speaking about when progressively more complex agents are used.


Arguing about inefficient implementation misses the point. It's anaglous to critiquing the concept of higher order programming languages because a particular implementation produces inefficient assembly.


I get the push against poor LLM code but this sub is reactionary.

###### eyebrows360

> We can declare properties of the system and AI can implement it.

No, dog, *we can't*, because *in reality* these things are too shit. I fully get what you're trying to say, and it's *just wrong*.

##### ashkanahmadi

> If that were true, then yes, it would be true. It isn't.

even Shakespeare couldn't come up with that XD

###### eyebrows360

M'lady \*curtsies and doffs cap*

### DesignerMusician7348

jesus christ that AI solution is a mess

#### kwietog

I hope not even an intern would write that.

#### Realistic-Success260

It's a mess but it's more flexible than his

##### ashkanahmadi

That’s correct. However, in my case, I need a 2-letter initial for the user’s profile avatar in case there is no profile picture uploaded. Also, the AI one has flaw where it relies on a space. However, it wouldn’t output properly for someone with multiple names (which is very common for Arabs and Spanish/Latin people). For example, for “Ahmad Ali Mohamed” it would return Ashkan Ahmadi and for “Maria Rosalin Sanchez Rodriguez” it returns MR. Both incorrect

### cupcakeheavy

Y'all out here like it still matters what the code looks like. AI generated code is the new assembly language. If you need to hand optimize it because the compiler (or AI) didn't get it right, that is one thing, but i don't see anyone modifying bytecode to be more readable for the next person, in practice.

#### eyebrows360

> AI generated code is the new assembly language.

This demonstrates perhaps the least coherent understanding of what this *actually is* that I've ever read. Congratulations?

##### cupcakeheavy

sorry eyebrows, but i'm paid to code, so i will hold my own professional opinions about compilers, IL, and assembly. Did you know that assembly language was created just so we humans don't have to do the icky thing of writing opcodes in binary?

### Klempinator9

This was an unfortunate example to pick, because Cursor's code is better here, and I say that as a general AI-non-enjoyer. It casts a wider net and isn't filled with the ugly chains of safe-access operators that ultimately cause a bug in your code.

If I have the object `{ first_name: null, last_name: "Smith" }`, your code prints `"undefinedS"`. If I have the object `{ first_name: "Ludwig", last_name: "van Beethoven" }`, it prints `"LV"` (it's typically written LvB).  
  
Cursor's issue is the `slice` at the end, which forces a max length of two. It preserves the capitalization of words in names, while yours doesn't. I'd use Cursor's minus the `slice`.

And before someone's like "but it's iterating over an array so many times," let's not forget that modern JavaScript is fast as hell, it's likely going to be a very tiny array, and any performance difference will be entirely negligible unless you're running this many millions of times.

#### ashkanahmadi

Interesting points. I've never seen someone's initials written as LvB though. Also, the AI's issue is that it relies on spaces to tell first name and last name apart. For example, if someone's name as multiple spaces like Juan Antonio Martinez Sanches, it will output "JA" instead of "JM"

##### Klempinator9

That person may typically write their initials as "JAMS"; we don't know.

Initializing names is actually a non-trivial problem to solve because of the variety of both names and how people write their own initials. It can vary by culture and language, as well. What if someone puts a first name of 晓明 (Xiaoming) and a last name of 李 (Li)? This is why it's not all that uncommon for forms to just have a separate field for it.

###### ashkanahmadi

Yeah I see what you mean. In this case, this is for the profile’s avatar which always has 2 letters in it so in this case I’m just going to let it as it is but you’re right. There are so many edge cases

#### hanoian

OP said they needed it to be two letters, so I wouldn't be surprised if that was part of the prompt.

### avidvaulter

I think the problem is you think making an announcement here on reddit, where the intended audience isn't, is engendering change. 

You should be using this example and explaining this to the person you're working with. If that doesn't work you should find a path forward that doesn't include you having to work with them.

Signed,

Someone sick of reading announcements that I didn't need or want.

### Nonikwe

I stand by the belief that the easiest way to wean people off vibe coding is to make necessitate passing tests for their code.

Makes it very clear to them just how limited AI is right now.

#### angrathias

One of the things I like about AI is making it generate test cases, just need to review the test code to make sure it isn’t doing anything sneaky if the tests fail

### [deleted]

[removed]

### misdreavus79

I'm dealing with this at work. I have a coworker who's gone full vibe coder, and he's really fast as a result, so a lot of "doesn't know any better" leadership is falling head over heels.

...mainly because I've been cleaning up after him behind the scenes. After this last major bug, I've now stopped doing that. I've been late on my own tickets because I've been spending so much of my time on his. But, after getting reprimanded for it, I'm done.

#### vytah

Who is accepting his pull requests?

##### misdreavus79

Whoever he harasses to get it merged that day. 

Sometimes I can't look at it right when he DMs me about it, and by the time I get around to it, PR is already merged.

### [deleted]

[removed]

### vexii

Your code misses multiple first names. Potentially creating a wrong initial.

#### ashkanahmadi

Yes that is correct but it’s intentional. I should have mentioned that this is for the avatar image which typically has 2 characters, not all the letters so that’s why it picks the first letters of the first name and the last name. The AI one wouldn’t even output the right initials. For example, if someone is called Antonio Fernando Rodriguez Sanchez, it would return AF instead of AR

##### vexii

It would output AFRS?

###### Rodrigo_s-f

It would if you remove the slice method

###### vexii

ahh yeah true

###### hanoian

Which was probably added because it need to be two letters.

###### ashkanahmadi

Yep but it's wrong because it inherently assumes everyone has one first name and one last name. But at least 20% of the world population have more than 1 first name or last name. For example, the LLM returns "JM" for "John Michael Smith" instead of "JS".

###### hanoian

You said it needed to be two letters in the app. Was this added to the prompt?

###### ashkanahmadi

Im not sure what the prompt was

###### hanoian

My assumption is the prompt included it, or the AI knew it was being used in an icon, so purposefully cut it down in length with the slice.

###### ashkanahmadi

Correct. However it uses a space to separate the first name from the last name which leads to mistakes. If someone writes “Juan Antonio” as their first name (which is a typical Spanish name) and Rodrigo Sanchez, then the AI code returns JA instead of JR.

###### Rodrigo_s-f

Just replace the last chain with:

.replace(/\^(.).\*(.)$/, "$1$2");

Also, i like the AI solution better, works better in case of null or undefined

###### ashkanahmadi

But that makes it even more complicated and unreadable. I can easily check if the first name and last name are undefined or null in a pre-check but it’s interesting to know how different people approach the same seemingly easy objective

###### Rodrigo_s-f

By that logic you could do the same for the AI approach and assign the correct fields for first name and last name in the database.

##### CodeRadDesign

"typically" is the enemy of always

### 30thnight

Not to pick on you but this isn’t a great example. 

Both examples are nearly the same from a readability & perf impact. If this came up in review, your critique would be closer to a style or personal preference issue.

#### ashkanahmadi

> Not to pick on you but this isn’t a great example.

definitely. the overall impression is that LLM cannot make very complex code. but it turns out, it fails even at very basic logic as well since the LLM code doesnt even output the right initials if someone has more than 1 first name or 1 last name which is +20% of the entire world population.

### kyualun

``
const initials = JSON.stringify(profile)
  .split('')
  .reduce((acc, char, i, arr) => {
    if (char === '"' && arr[i - 1] === ':' && arr[i - 2] === 'e' && /[a-z]/i.test(arr[i + 1])) {
      return acc + arr[i + 1].toUpperCase();
    }
    return acc;
  }, '') || "N/A";
``

#### BurningPenguin

Truly beautiful

#### zaidazadkiel

8/10 needs moar magic numbers

### Candid_Budget_7699

That's wild to me that someone would go from actual coder to willingly not thinking about anything and allowing the AI to do everything. LLMs have their place in our workflows, there is no denying that, but if you stop coding completely, keeping up with trends and exercising your mind to solve problems, I personally think that's setting yourself up for failure. Vibe coding to me always seemed like a cope for lay people to feel like they can code too or for really mundane stuff you'd rather not spend a lot of time on.

### okiujh

how about wrapping the logic in in a function?

```javascript
function calc_initial(profile){
//implementation
}
```

#### Noch_ein_Kamel

but are you using [name-initials](https://www.npmjs.com/package/name-initials), [initials](https://www.npmjs.com/package/initials), [avatar-initials](https://www.npmjs.com/package/avatar-initials) or the jquery [initials-js](https://www.jsdelivr.com/package/npm/initial-js)?

##### okiujh

wow they have an npm for that.

##### ashkanahmadi

Damn didnt know those libraries exist haha! I didn't mention in my post but I need the avatar-style initials like when there is a profile picture or avatar missing.

### BigBoicheh

Never blindly accept, just review diffs and better models like gpt 5 should one shot simple stuff in a clean way


Ai is annoying because id rather learn and get faster at coding, than prompting 24/7 and reading diffs, cleaning up after...

#### hanoian

The AI code is straight up better for multiple reasons.

##### ashkanahmadi

It's not though. It doesn't even return the initials. It returns the first letter and then the first letter after the first space. That means it returns the wrong initials for more than a +20% of of the world population where they have multiple first names and multiple last names. If someone's name is "Maria Antonia Gonzalez Rodriguez" which is a very common name in Spain and the entire Latin America, the AI returns "MA" instead of "MG" which is totally wrong.

### BurningPenguin

ChatGPT recommended this, and also explained why it would use the version Cursor did: https://i.imgur.com/QOfpnsL.png 

Doesn't look that bad to me. I'd imagine it would work fine over paginated data or something. Didn't test it, tho. For bigger amount of data, you'd probably be better off with some SQL query or just add a new column for that.

But regardless of that, i do agree to be careful about the output of the parrot machine. Sometimes it really overcomplicates things.

### DustinBrett

You make rules for the AI to follow so that it formats the way you want. When you run into these non-ideal results you work with the AI via prompts, rules, MCP's, etc to make it better for the next time. That is how you improve the AI results.

#### ashkanahmadi

100% correct. But that requires the user/developer to know better. If the user doesn’t know any better, they would accept whatever output it gives them (which isn’t directly the fault of the AI but the fault of the user). But that’s my whole point: don’t blindly accept whatever it outputs. But for that, some knowledge and expertise or even common sense is required

### SwimmingThroughHoney

What the heck did he use for the prompt? If I ask Copilot "I have two variables from a database: `first_name` and `last_name`, both withing an object named "profile". Can you write a solution, in Javascript, for how I can create a single string with the initials?" I get:

    const getInitials = (profile) => {
      const firstInitial = profile.first_name?.charAt(0).toUpperCase() || "";
      const lastInitial = profile.last_name?.charAt(0).toUpperCase() || "";
      return firstInitial + lastInitial;
    };

#### ashkanahmadi

Haha no idea 😆

#### ScallionZestyclose16

There’s been cases where if you google the same thing twice, google’s ai will you show you very different results.

https://san.com/cc/users-catch-google-ai-overviews-inventing-fake-facts/

“When repeating the same search later, Google highlighted entirely different sources.”

So chances are the ai bot gave a different answer at that time.

### idontreddit22

you can get AI to output the way you have it.

it just takes longer and you need to be way more specific.

### [deleted]

[removed]

### Prathamesh9890

That's absolutely right

### ulrjch

your solution is not complete tho. based on your code, if 1 of the variable is undefined, 'undefined' shows up the result string. also, assuming you did not trim user input, the result string can contain white space. AI's solution addresses the latter edge case but not the former.

### ulrjch

your solution is not complete though. when one of the variables is undefined, 'undefined' shows up in the result string. this case is not handled by AI either.  
also, assuming you didn't trim user input, white space shows up in the result string. this case is addressed by AI.

### OrixAY

Just FYI many East Asian names has spaces between their first and last names (mine included). In this case I would argue the generated code does have the more "correct" approach minus the nonsensical `slice()` part.

But yes I feel you. I clean up vibe coded projects daily as well.

### Mosk549

Tbh it does not matter anymore if it works it’s good enough. This is the new meta like it or not.

### McWolke

Yeah the AI solution looks better to me. Much more readable, the steps are clear, while yours is all in one messy line. Yours misses multiple names and would only get the first one (unless that's what you wanted, then you gotta prompt the AI to do so as well). And yours could end in errors or having undefined in the string, if I read that correct. 
the only part about the AI solution I don't get is the slice, which kills the whole multiple names part and might result in only having the first names in the initials. 

### hobby_hobby

This! It's hard when your brain has become accustomed to using AI, because sometimes you just stop trying to think and feed it the problem to it, whatever solution comes out is already enough. It used to be a problem of mine as well.

### HipHopHuman

There are issues with your solution.

    const getInitials = (firstName, lastName) =>
      firstName?.[0].toUpperCase() + lastName?.[0].toUpperCase()
    
    getInitials(undefined, "Davis"); // "undefinedD"
    getInitials(undefined, undefined); // "NaN"
    getInitials("John", ""); // throws an error

Cursor's solution returns "uD", "uu" and "J", which is better than showing `undefined` / `NaN` to the user or throwing an exception.

This is a harder problem to write a correct solution for because many locales with different grammar rules exist. I think solutions like what Github does for placeholder icons are a lot better. Considered using Gravatar, DiceBear, RoboHash or ui-avatars?

Here's something that uses Intl.Segmenter to try to respect locales (but still isn't 100% correct).

    /**
     * @param {object} options
     * @param {string} [options.firstName]
     * @param {string} [options.lastName]
     * @param {string} [options.placeholder="?"]
     * @param {string} [options.separator=""]
     * @param {boolean} [options.suffixSeparator=true]
     * @param {Intl.Segmenter} options.wordSegmenter
     * @param {Intl.Segmenter} options.graphemeSegmenter
     * @returns {string}
     */
    function getInitials(options) {
      const {
        firstName,
        lastName,
        wordSegmenter,
        graphemeSegmenter,
        placeholder = "?",
        separator = "",
        suffixSeparator = true
      } = options;
    
      const fullNames = [firstName, lastName].map(name => typeof name === 'string' ? name : "");
    
      const [firstNames, lastNames] = fullNames
        .map(n =>
          [...wordSegmenter.segment(n)]
            .filter(({ isWordLike }) => isWordLike)
            .map(({ segment }) => segment)
            .map(w =>
              [...graphemeSegmenter.segment(w)].map(({ segment }) => segment)
            )
        );
    
      let initial1 = placeholder;
      let initial2 = placeholder;
    
      if (firstNames.length && lastNames.length) {
        initial1 = firstNames.at(0).at(0);
        initial2 = lastNames.at(0).at(0);
      } else if (firstNames.length) {
        initial1 = firstNames.at(0)?.at(0) ?? placeholder;
        initial2 = firstNames.at(1)?.at(0) ?? firstNames.at(0).at(1) ?? placeholder;
      } else if (lastNames.length) {
        const [lastName1 = [], lastName2 = []] = lastNames;
        if (lastName1.length && lastName2.length) {
          initial1 = lastName1.at(0);
          initial2 = lastName2.at(0);
        } else if (lastName1.length > 1) {
          initial1 = lastName1.at(0);
          initial2 = lastName1.at(1);
        } else {
          initial2 = lastName1.at(0);
        }
      }
    
      return [initial1, initial2].join(separator).toUpperCase() + (suffixSeparator ? separator : "");
    }
    
    const wordSegmenter = new Intl.Segmenter('en-GB', { granularity: 'word' });
    const graphemeSegmenter = new Intl.Segmenter('en-GB', { granularity: 'grapheme' });
    
    getInitials({
      firstName: 'David Howard',
      lastName: 'Wallowitz-Bernard',
      wordSegmenter,
      graphemeSegmenter
    }) // "DW"
    
    getInitials({
      firstName: 'Michael-Antonio',
      lastName: '',
      wordSegmenter,
      graphemeSegmenter
    }) // "MA"
    
    getInitials({
      firstName: '',
      lastName: 'Andrew Copeland',
      wordSegmenter,
      graphemeSegmenter,
      separator: '.',
      suffixSeparator: false
    }) // "A.C"
    
    getInitials({
      firstName: 'Michael',
      lastName: '',
      wordSegmenter,
      graphemeSegmenter
    }) // "MI"
    
    getInitials({
      firstName: 'M',
      lastName: '',
      wordSegmenter,
      graphemeSegmenter
    }) // "M?"
    
    getInitials({
      firstName: '',
      lastName: 'D',
      wordSegmenter,
      graphemeSegmenter,
      placeholder: "_"
    }) // "_D"
    
    getInitials({
      firstName: '晓明',
      lastName: '李',
      wordSegmenter: new Intl.Segmenter('zh-Hans-CN', { granularity: 'word' }),
      graphemeSegmenter: new Intl.Segmenter('zh-Hans-CN', { granularity: 'grapheme' }),
    }) // "晓李"

### tdammers

Side note: https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/ - that list doesn't explicitly mention it, but after reading it, it should be obvious that automatically inferring a set of "initials" from a person's name given in any longer form is fundamentally impossible in the general. Forcing names into a "first name / last name" format is also not appropriate for all names, nor is drawing any conclusion about the semantics of those parts.

### zaidazadkiel

random codegolf

\`\`\`  
let profile = { first\_name: 'firstname' , last\_name: 'lastname'}

\[profile.first\_name, profile.last\_name\].map(

(str)=>typeof str === 'string' && str.length>=1 && str\[0\].toLocaleUpperCase() || ''

)

\>>> \['F', 'L'\]  
\`\`\`

### Xypheric

I’m not some ai shill, but who cares?  You think the codebase for twitter wasn’t full of dumb solutions and then refactored later?

#### ashkanahmadi

Correct, and I agree, but only if the function returned the correct value. In this case, it doesn't even return the correct value for +20% of the world population where they have multiple first names and last names.

### [deleted]

[removed]

### R10t--

Ok but like… if the AI code works, does it matter?

The AI got it done in seconds where it would have taken me 5x as long to type it out myself.

Sure it’s maybe not the cleanest code or most understandable, but it works.

At the end of the day, it’s doing things correctly and making it work. You may have heard the story of the dev who released stardew I think it was? There are massive 200+ case if statements in the codebase that determine dialog that are a mess. But if he took the 4-5 hours to refactor those statements then that’s 4-5 hours he could have spent elsewhere.

AI helps us create faster. If it works, it works.

#### ashkanahmadi

Yes, but that’s my point. Just because it works, doesn’t mean it’s the most efficient way or that it would always work. For example, in this case, the AI solution is unnecessarily complex, and doesn’t return the correct value if someone has more than one last name (which is +20% of the entire world population). 

How can a developer judge if something is written properly unless they have a very good knowledge of the code? Also, it literally can’t simpler than this where you need the first letter of the first name and the first letter of the last name and put them together but even in this case, the AI solution doesn’t behave always reliably

### Purple-Cap4457

Bro this ai shit is literally wtf. I can easily understand your whot it does. Simply get first letter, to uppercase, concat. But ai slop is 5 instructions, i have to think about what this piece of code does? Remember or find out what is slice, join, filter, map, split, why for the love of god ??


Imagine if whole software is done in that way. Pieces and layers of ai generated spaghetti slop that to accomplish one easy task does 5-10 unnecessary complicated operations. Imagine demand for software people that will have to deal with mamuth amount of piles of ai generated shit💩👾

#### ashkanahmadi

Check out LinkedIn. Being a “vibe code clean up expert” is a thing now 😆

### spacechimp

I need to do a few more tests to confirm, but I’d swear that Copilot’s output gets better the angrier I get with it. After an exasperated exchange where I typed something like “It appears that I can’t stop you from attempting to solve every single problem using overcomplicated, unreadable regular expressions” it stepped up its game and produced something good. But boy does it loooove regex.

### Happy_Junket_9540

Am I the only one that thinks the AI code is better? Your code does bot handle undefined values, the AI code does.

#### blidblid

I agree the AI code looks better. Easier to read, handles missing names. That said, Filter(Booelan) is a very ugly line, altough commonly used.

### mrshyvley

I've never tried using AI to code.  
Doesn't copying and pasting AI created code greatly increase the risk of a coder using code they don't fully understand?

#### ashkanahmadi

Well yes and no. Sometimes the AI can really speed things up but usually when the prompt is super clear. The issue is that sometimes, the prompt to get exactly what you want is longer than the function itself if you type it by hand haha

If the developer knows exactly what they want and they can clearly instruct it, then they can evaluate to see if it’s good or no. If not, then yeah you are always at the mercy of the AI

### InThePot

Working vs "good enough" can be a big problem for non-AI-generated code.
I've been on two projects now where PRs were considered not needed or if they were needed then PR rejections were overridden. Why? Because the code "works" and we had to meet deadlines.
