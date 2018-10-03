Master branch: [![Build Status](https://travis-ci.org/comacoma/FSF-MilestoneProject.svg?branch=master)](https://travis-ci.org/comacoma/FSF-MilestoneProject)

Deployment branch: [![Build Status](https://travis-ci.org/comacoma/FSF-MilestoneProject.svg?branch=deployment)](https://travis-ci.org/comacoma/FSF-MilestoneProject)

# Unicorn Attractor - Issue Tracker
As the final project of Code Institute's Full stack Web Developer course, this project involves building an issue tracker of an imaginary web service called 'Unicorn Attractor'. As part of the service, free bug fixes and crowd funded development of additional features are being offered, which is represented in forms of an issue tracker.

The issue tracker provides a platform for users of the website to communicate with its developers of bugs found or new features users would like to have on the website.

## <a name="ux"></a>UX
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

Any newly submitted tickets will have their status automatically set to 'Reviewing' until a developer checks out the ticket and decides whether or not to actively work on the issue. If developers agree to work on an issue, they will change the status to 'To do' and continue to update users by commenting in the ticket until the issue is resolved. If developers feels that an issue is of less importance, it will be put 'On hold'. However, users can still upvote tickets that are put 'On hold' if they think otherwise. Furthermore, if a ticket's upvote exceeds a certain threshold its status will automatically change to 'To do' and all developers will be notified of this change. Each ticket will have their individual threshold which can be changed by developers.

## Features
### Existing features
- User authentication: as some features will be limited to registered users, user authentication will be the first to be implemented. It should allow users to be registered and logged into the website. Features such as submitting new tickets to issue tracker should only be available to authenticated users.
	- User login and registration use custom views and templates in which the code are referred from course material. On the other hand, other user authentication features such as password changes and password reset use views as provided by Django, albeit using custom templates.

### Features to implement
- Issue tracker: the focus of this project, which will be split into the following features:
	- View tickets shortlist: a page that displays a shortlist of all tickets. It should be paged to avoid extended scrolling. It should also have a simple search function for filtering tickets based on keywords.
	- Submitting new tickets: on a separate page, any user should be able to submit a new ticket by filling in the form.
	- View tickets in detail: each ticket should be displayed in individual pages. These pages allow regular users and developer to further interact with a specific ticket such as commenting and upvoting.
	- Data visualisation: in order to show users how much time has been put into each ticket, there should be graphs showing said data. The graphs should show how much time has been allotted to each ticket on a daily, weekly and monthly basis; as well as tickets being upvoted the most. These graphs should be available in ticket's detail page as well.
	- Payment for upvoting feature request: developing new features requires funding, and it is done when a user decides to support (upvote) a particular feature request. It should allow user to choose how much they would like to offer, with a minimum amount set by developers.
	- Change status of tickets: Changing status of ticket to one of the five mentioned in [UX section](#ux). This feature should only be available to accounts with staff status (i.e. developers).
	- Set threshold for tickets' upvote: As mentioned in [UX section](#ux), once upvote for a ticket under review or on hold reaches a certain threshold it will automatically change to 'to do'. This threshold should be set by developers and developers only.
