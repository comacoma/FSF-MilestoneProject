# Unicorn Attractor - Issue Tracker
As the final project of Code Institute's Fullstack Web Developer course, this project involves building an issue tracker of an imaginary web service called 'Unicorn Attractor'.

The issue tracker provides a platform for users of the website to communicate with its developers of bugs found or new features users would like to have on the website.

## UX
Whilst the project will include pages that describes the imaginary web service, the main focus will be the issue tracker part of the website. Users of the service can use the issue tracker to report any bugs they found on the website, as well as voicing their interest in additional features that they would like developers to look into in forms of a ticket. A ticket briefly describes the gist of an issue and tells users the current state of an issue. Specifically, a user can:
- Submit tickets of issue they would like to report, whether it's a bug or a feature request.
- Fellow users can comment and upvote tickets in order to raise developers' attention.
- Whilst upvoting for bug reports is free, upvoting for feature request requires payment which serves as funding for development.
Upvote figures slightly differ depending on whether the ticket is a bug report or feature request. If it is a bug report, upvote simply represents the number of users upvoted the ticket. However, if it is a feature request, the number of upvote equals to the sum put in by users rather than the number of users who have upvoted the said feature request.

On the other hand, developers can respond to tickets in the following ways:
- Comment on tickets, similar to regular users.
- Change status of tickets which ranges from:
	- Reviewing
	- To do
	- Doing
	- Done
	- On hold

in order to show users whether or not an issue is being worked on.

Any newly submitted tickets will have their status atuomatically set to 'Reviewing' until a developer checks out the ticket and decides whether or not to actively work on the issue. If developers agree to work on an issue, they will change the status to 'To do' and continue to update users by commenting in the ticket until the issue is resolved. If developers feels that an issue is of less importance, it will be put 'On hold'. However, users can still upvote tickets that are put 'On hold' if they think otherwise. Furthermore, if a ticket's upvote exceeds a certain threshold its status will automatically change to 'To do' and all developers will be notified of this change. Each ticket will have their individual threshold which can be changed by developers.

## Features
### Existing features
To be updated.

### Features to implement
- User authentication: as some features will be limited to registered users, user authentication will be the first to be implemented. It should allow users to be registered and logged into the website. Features such as submitting new tickets to issue tracker should only be available to authenticated users.
