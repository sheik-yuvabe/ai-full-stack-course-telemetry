# Frontend Projects: Weeks 1-4

## How to use this file

1. Find your current week and day.
2. Read the main project.
3. If you want, choose one alternative project instead.
4. Build only what is asked for that day.
5. Keep your solution inside the allowed concepts for your current week.
6. If you need help, prompt Codex clearly and ask for one small step at a time.

If you need help with prompting, use:
[STUDENT_PROMPTING_GUIDE.md](STUDENT_PROMPTING_GUIDE.md)

## Important rule

Do not try to build the whole final app in one prompt.
Break the work into small steps.

Good approach:

- plan the feature
- build one part
- test it
- ask Codex about the next small part

## Week 1

Week 1 is about React basics and fast wins.
Keep things simple.
Use local state.
Do not use advanced tools.

### Day 1: Simple interaction

**Main project:** Daily Pulse Board

**Alternatives:** Coffee Preference Picker, Workout Intensity Selector, Team Check-in Board

**Your challenge**
Build a small app where the user selects their current mood, energy, or focus level and the UI updates immediately.

**By the end of the day, your app should**

- show a few selectable options
- update the screen when the user clicks one
- show dynamic text based on the selected option
- use simple conditional styling or conditional rendering

**Practice focus**

- JSX
- components
- props
- `useState`
- click handlers
- dynamic text and classes
- conditional rendering

**Do not use yet**

- `useEffect`
- `localStorage`
- routing
- API calls

### Day 2: Rendering from data

**Main project:** Playlist Duel

**Alternatives:** Trailer Showdown, Startup Name Vote, Weekend Activity Poll

**Your challenge**
Build a voting app where users choose between two items and the UI shows the current leader.

**By the end of the day, your app should**

- render items from an array
- show reusable cards or buttons
- update vote counts
- show which item is leading

**Practice focus**

- arrays of objects
- `map`
- `key`
- reusable components
- derived state
- conditional UI

**Do not use yet**

- `useEffect`
- `localStorage`
- routing
- API calls

### Day 3: First form

**Main project:** Workshop RSVP + Ticket Preview

**Alternatives:** Meetup Registration Form, Conference Session Signup, Film Screening RSVP

**Your challenge**
Build a signup form and show a live preview of the attendee pass or ticket.

**By the end of the day, your app should**

- collect form input
- update form state while typing
- validate simple fields
- show success or error feedback
- reset after submit
- show a live preview from the current state

**Practice focus**

- controlled inputs
- `onChange`
- `onSubmit`
- `preventDefault`
- validation
- success and error states
- reset flow
- live preview from state

**Do not use yet**

- `useEffect`
- `localStorage`
- routing
- API calls

### Days 4-5: First mini app

**Main project:** Movie Night Planner

**Alternatives:** Travel Destination Shortlist, Gift Ideas Selector, Restaurant Picker

**Your challenge**
Build a small app where users browse a mock list, search items, filter them, and save a shortlist.

**By the end of Day 4, your app should**

- show a list of items
- support search
- support simple filters
- have reusable components
- show a good empty state

**By the end of Day 5, your app should**

- let the user save favorites or a shortlist
- use callbacks between components
- place state in the right component
- have a simple, clean folder structure

**Practice focus**

- component decomposition
- props
- list rendering
- search
- filters
- empty states
- lifting state up
- callbacks
- favorites / shortlist
- deciding where state should live
- basic folder structure

**Do not use yet**

- `useEffect`
- `localStorage`
- routing
- API calls

## Week 2

Week 2 is about real state updates.
Now your app should handle arrays and objects more carefully.
You will also start persistence.

### Days 6-7: Local CRUD

**Main project:** Reading Queue

**Alternatives:** Watchlist Manager, Recipe Queue, Workout Plan Board

**Your challenge**
Build an app where users can add items, update them, mark progress, edit notes, and remove items.

**By the end of Day 6, your app should**

- add a new item
- render items from state
- delete an item
- toggle a simple status

**By the end of Day 7, your app should**

- edit an existing item
- update arrays/objects correctly
- filter items
- show derived counts like total, completed, or pending

**Practice focus**

- arrays of objects in state
- add item form
- delete item
- toggle status
- edit flow
- immutable updates with `map`
- filters
- derived counts
- helper functions

**Do not use yet**

- routing
- API calls
- authentication
- state libraries

### Day 8: Derived state

**Main project:** Weekend Budget Splitter

**Alternatives:** Road Trip Cost Splitter, Group Dinner Bill Planner, Festival Budget Calculator

**Your challenge**
Build an app where users enter expenses and the UI calculates totals and a per-person split.

**By the end of the day, your app should**

- accept numeric inputs
- validate input
- calculate totals
- calculate per-person values
- show formatted output

**Practice focus**

- numeric inputs
- parsing and validation
- helper functions
- totals and subtotals
- derived state vs stored state
- formatting numbers

**Do not use yet**

- routing
- API calls
- authentication
- state libraries

### Days 9-10: Persistence

**Main project:** Recipe Box

**Alternatives:** Bookmark Organizer, Closet / Outfit Planner, Local Places Wishlist

**Your challenge**
Build a larger local app where users add items, organize them, mark favorites, and keep data after refresh.

**By the end of Day 9, your app should**

- combine form, list, and filter UI
- support categories or tags
- support favorites
- manage a larger state shape

**By the end of Day 10, your app should**

- load initial state from `localStorage`
- save updates to `localStorage`
- handle first-use and reset flow

**Practice focus**

- larger component tree
- form + list + filters together
- tag/category filtering
- favorites
- array/object updates
- `useEffect`
- `localStorage`
- load initial state
- persist updates
- reset flow

**Do not use yet**

- routing
- API calls
- authentication
- state libraries

## Week 3

Week 3 is one larger frontend app for the whole week.
Stay in one project long enough to practice structure, cleanup, and architecture.

### Days 11-15: Larger single-page app

**Main project:** City Weekend Planner

**Alternatives:** Conference Agenda Builder, Study Sprint Planner, One-Day Travel Itinerary Builder

**Your challenge**
Build a larger single-page app where users explore options, filter them, save a plan, add notes, and keep data locally.

### Day 11: Explore screen

**Build goal**

- show a larger local dataset
- support search
- support category filters
- use a clean card layout
- show empty states well

**Practice focus**

- larger dataset
- list-based structure
- multiple filters
- search + category filters
- card layouts
- empty states

### Day 12: Build the plan

**Build goal**

- let users save items into a plan
- let users remove items
- support notes for planned items
- shape state carefully
- show small summaries

**Practice focus**

- cross-component state flow
- save/remove flow
- notes per item
- state shape design
- derived summaries

### Day 13: Persistence and cleanup

**Build goal**

- keep the plan after refresh
- extract helper functions
- improve folder structure
- create reusable UI pieces

**Practice focus**

- `localStorage`
- `useEffect`
- helper extraction
- better folder structure
- reusable UI

### Day 14: Better UX

**Build goal**

- add sorting
- add reset filters
- add saved indicators
- improve empty states
- improve mobile layout

**Practice focus**

- sorting
- reset filters
- saved indicators
- better empty states
- responsive cleanup
- accessibility basics

### Day 15: Polish and presentation

**Build goal**

- clean up the code
- add one small useful feature
- fix bugs
- prepare to explain your app

**Practice focus**

- code cleanup
- small feature addition
- bug fixing
- demo prep
- explaining component and state choices

**Do not use yet**

- routing
- API calls
- authentication
- state libraries

## Week 4

Week 4 is the frontend capstone.
You will build a routed app that still stays frontend-only.

### Days 16-20: Frontend capstone

**Main project:** Rental Scout

**Alternatives:** Event Discovery App, Coworking Space Browser, Freelancer Portfolio Marketplace

**Your challenge**
Build a frontend-only app with:

- browse page
- filters
- saved/favorite flow
- detail pages
- inquiry/application form

### Day 16: Planning and app skeleton

**Build goal**

- define the pages
- plan the data shape
- create the app shell
- decide folder structure

**Suggested pages**

- Home
- Browse / Listings
- Saved
- Detail
- Inquiry / Apply

**Practice focus**

- planning pages
- data shape
- app shell
- folder structure
- page/component boundaries

### Day 17: Browse page

**Build goal**

- show a larger list
- support multiple filters
- support favorite/save flow
- support filter reset

**Practice focus**

- larger list rendering
- compound filters
- controlled filter inputs
- saved/favorite items
- filter reset flow

### Day 18: React Router

**Build goal**

- move sections into page-based structure
- add routes
- connect pages with links
- build shared layout/navigation

**Practice focus**

- React Router
- routes and pages
- `Link`
- `NavLink`
- shared layout

### Day 19: Detail pages and forms

**Build goal**

- open one item by ID
- show a detail page
- add an inquiry/application form
- validate the form
- show confirmation state

**Practice focus**

- route params
- find item by ID
- detail page pattern
- inquiry/application form
- validation
- confirmation state

### Day 20: Capstone polish

**Build goal**

- improve mobile layout
- improve empty/error/success states
- refactor repeated code
- make the app presentation-ready
- notice which parts can later move to a backend

**Practice focus**

- responsive cleanup
- empty/error/success states
- code refactor
- accessibility basics
- identifying future backend pieces

**Do not use yet**

- real backend integration
- authentication
- state libraries
- advanced abstractions

## Final reminder

Your goal is not to get the fastest answer.
Your goal is to learn how to build projects step by step.

When using Codex:

- tell it your week
- tell it your project
- tell it your current task
- share your code
- ask for one small step at a time
