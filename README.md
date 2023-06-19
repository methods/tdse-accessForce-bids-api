# tdse-accessForce-bids-api
Bids API training project with Python and MongoDB

# Bid Library

## Contents

- [Background](#background)
  - [Before working on a bid](#before-working-on-a-bid)
  - [Bid phases](#phases)
- [Brief](#brief)
  - [Acceptance Criteria](#acceptance-criteria)
  - [Iterations](#iterations)

## Background

Methods being a consultancy agency to win new work we make to make bids on client tenders.

- A tender is a piece of work that an organisation (potential client) needs an external team to work on or to supplement an existing team
- A bid can comprise of several stages to win a tender, usually there are two phases which comprise of phase 1 and phase 2

### Before working on a bid

Before phase 1, there is time for bidders like Methods to ask questions of the client tender. These questions are open to all those looking to bid on the tender and all questions and answers are available to all bidders on a single tender.

This step is a necessary is really important for Methods to understand whether we really want to bid on a particular tender. Some considerations before bidding:

- Do we like the project and hence want it?
- Is it good value?
- Will this get us known with a new client and give Methods leverage in future work?
- Is the tender something different that would expand our portfolio?
- Can we do it?

### Phases

**Phase 1** compromises of a list of questions set by the tender; in government the scoring system for each question is out of 3, so if there are 6 questions a bidder can achieve a maximum score of 18. The answers to the questions usually have a word limit of 100 or 200 (in this phase).

The client that puts out a tender decides the pass rate in phase 1 to progress to phase 2. The pass rate may not be known until results of all bids are completed for each of the bidders. The list below are common pass criteria you might come across on a bid (remember this can vary from client to client and even within multiple tenders by the same client):

- All questions must have a score greater than 1, (so 2 minimum)
- A minimum overall score, e.g. 14 out of 18
- The 3 highest bids assuming the bids met criteria 1 or/and 2

**Phase 2** is a lot more involved than phase 1, it can comprise of a face to face (or virtual) presentation alongside answers to questions limited to x number of words (limit set by client). These questions will cover team culture and technical solution.

There are usually 3 categories that Methods are scored on and these are weighted by the client. The categories are:

- Technical - questions from presentation or form and results from phase 1
- Culture - questions in phase 2
- Cost (a.k.a. Rate)

The overall score is worked out as a percentage, (out of 100). Whichever bidder scores highest wins the bid and that is the end of the tendering process.

Next steps: Statement of Work (SoW, the contract) is put together by the client, handing over CVs of potential staff Methods are going to supply and agreement on project start dates.

--------------

## Brief

Currently Methods store all the information for tenders and bids in Sharepoint, the way the documents are stored and the information available can vary quite a lot making it hard for the bid team to find good answers to questions and successful bids for reuse. We currently do not store who helped answering questions against a bid and in some cases where Methods have done so it only informs us of their initials.

What intend to build is an API that can store tender/bid information in a structured way to facilitate finding successful bids and high scoring questions.

### Acceptance Criteria

**Must** have:

1. Ability to access all bid data, see list of data below:

    - tender title
    - tender short description (problem statement)
    - client
    - date of the tender
    - were Methods successful
    - what phase did we get to
    - how well we did in each of the phases
    - any technologies or skills reuired by client tender
    - tender questions and Methods answers and the respective scores
    - who helped answer a question
    - provide links to further information on bids stored in sharepoint
    - when was the data last updated
    - any skills or technologies listed in the answers to questions

1. Ability to find any bid
1. Ability to add new bids
1. Ability to update a bid that is still in progress
1. Ability to delete a bid and associated
1. Ability to recover deleted bid data within 4 weeks of deletion
1. Ability to filter bids and questions based on success and score
1. Ability to sort bids and questions alphanumerically and page through the results
1. Ability to secure access to changing the data to certain users

**Should** have:

1. Ability to search for bids containing particular text
1. Ability to search for questions containing particular text

**Could** have:

1. Ability to control different user access (permissions) based on roles

    - Admin
    - Bid writers
    - Bid viewers

1. Ability to access this software anywhere in the UK

**Would not** have:

1. Due to size of some answers and the content not being soley text but images, diagrams etc. Methods does not wish to duplicate this information from Sharepoint into a filesystem like AWS S3 or Azure Storage

### Iterations

**Iteration 1** Build API and initial storage system to find, add, update and remove. Steps 1 to 8 from Must section

**Iteration 2** Secure the API to users who need access, based on the "Principle least priviledge principle. Step 9 from Must section

**Iteration 3** Build search engine to allow for a more sophisticated way of finding questions and bids related to your needs. Steps 1 and 2 from Should section

**Iteration 4** Expand on access control to bid library based on roles, users and teams where necessary. Step 1 of Could section

**Iteration 5** Host the bid library to be accessed by users across the country. Step 2 of Could section

**Iteration 6** Build a web app to integrate with the bids API, create user journeys that allow users to find, add and update bid content

--------------

**Note:** If this is part of your training, you should look for guidance by your mentor of how to progress this project. Your coach can use the [generic project rest API doc](/training/generic-projects/rest-api/README.md) to setup your initial project that will cover iteration 1.

--------------

Return to the [internal projects](https://github.com/methods/tdse-projects/blob/main/internal/README.md) for additional options and information.

--------------
