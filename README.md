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
- Issue tracker: the focus of this project, which will be split into the following features:
	- View tickets shortlist: a page that displays a shortlist of all tickets. It should be paged to avoid extended scrolling. It should also have a simple search function for filtering tickets based on keywords.
	- Submitting new tickets: on a separate page, any user should be able to submit a new ticket by filling in the form.
	- View tickets in detail: each ticket should be displayed in individual pages. These pages allow regular users and developer to further interact with a specific ticket such as commenting and upvoting.
	- Data visualisation: in order to show users how much time has been put into each ticket, there should be graphs showing said data. The graphs should show how much time has been allotted to each ticket on a daily, weekly and monthly basis; as well as tickets being upvoted the most. These graphs should be available in ticket's detail page as well.
	- Payment for upvoting feature request: developing new features requires funding, and it is done when a user decides to support (upvote) a particular feature request. It should allow user to choose how much they would like to offer, with a minimum amount set by developers.
	- Change status of tickets: Changing status of ticket to one of the five mentioned in [UX section](#ux). This feature should only be available to accounts with staff status (i.e. developers).
	- Set threshold for tickets' upvote: As mentioned in [UX section](#ux), once upvote for a ticket under review or on hold reaches a certain threshold it will automatically change to 'to do'. This threshold should be set by developers and developers only.
- Blog: all registered user will be able to write blogs within the web app. Though the structure is simple it allows users to upload an image per blog post.

## Technologies Used
- [Django 2.1.2](https://www.djangoproject.com/)
	- Framework for this project.
- [Bootstrap 4.0](https://getbootstrap.com/)
	- Toolkit for frontend styling. This is used in conjunction with custom CSS code to provide a unified style throughout different page of the webapp.
	- [Litera](https://bootswatch.com/litera/) theme from [Bootswatch](https://bootswatch.com/) has been used for this project.
- [JQuery](https://jquery.com/)
	- Simplifying DOM manipulation. In the scope of this project, it has been used for animation and partially handling form used by [Stripe](https://stripe.com/gb) API.
- [Stripe](https://stripe.com/gb)
	- A service for handling online transaction which can be integrated into Django projects with its API. It has been used to deal with transaction when a user donate for a feature request.
- [Heroku](https://www.heroku.com/home)
	- Platform used for deploying the project.
- [PostgreSQL](https://www.postgresql.org/)
	- For deployment model of this project, PostgreSQL has been used for data handling as a add-on from [Heroku](https://www.heroku.com/home).
	- Used in conjunction with [dj-database-url](https://github.com/kennethreitz/dj-database-url) for deployment model configuration.
- [SQLite3](https://www.sqlite.org/index.html)
	- For local/ testing model of this project, SQLite3 is used instead for data handling as provided by Django in default settings.
- [Amazon Web Service](https://aws.amazon.com/)
	- Since [Heroku](https://www.heroku.com/home) does not provide media upload service, AWS has been used for the said purpose.
	- It is used with [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html), [django-storages](https://django-storages.readthedocs.io/en/latest/) and [Pillow](https://python-pillow.org/) for integration with Django project.
- [django-filter](https://django-filter.readthedocs.io/en/master/), [django-forms-bootstrap](https://github.com/pinax/django-forms-bootstrap), [django-widget-tweaks](https://github.com/jazzband/django-widget-tweaks)
	- These are packages for Django. In this project, these packages are used to simplify the rendering of templates and provide simple filter functionality on data such as list of issue tracker tickets.
- [coverage](https://coverage.readthedocs.io/en/v4.5.x/)
	- It is used during testing to ensure high coverage of code tested.

## Testing
All apps created in this project will be tested on:
- Data models
- Forms
- Views (Logic)
- and in some case, helper function created for specific purpose.
Attempt was made to automate all tests mentioned above with some exceptions. The exceptions are:
- Except portion of a try routine.
- Error handling of an external API as testing on these is not necessary.

For tests and coverage please refer to tests folder of each app, as well as htmlcov folder for coverage report. There is however, a few things worth mentioning:
- Using try routine in setting max_bug and max_feature_request in ProgressLog:
	- The two value mentioned above are used as validator when staff create a progress log for a particular day however, when there is no ticket in the database an error is raised so as a solution, statements for assigning the said values has been put in a try routine. That way, when error is raised (i.e. no ticket) the values are hard coded to 0 and staff can proceed to creating progress log, despite the only valid input is 0.
- Accessing to page that does not make sense:
	- Due to the url pattern user can for example, end up in a funding page for a bug ticket or upvoting (like) a feature request ticket, which is not intended. If fact, this was not addressed until testing. As a solution, a simple check is performed before other logic in such views and make sure users are redirected back to ticket details page when they attempt to access such non-sensical page.

## Deployment
To make sure there is no need to put down the deployed version once it's ready, a separate branch 'deployment' will be used for this purpose. Instead of using different configuration files, certain values in settings are different in master and deployment branch. For example:
- Debug mode is ON in master branch while it is OFF in deployment branch.
- Master branch uses a env.py file for all environmental values (env.py is set to be ignored by git for security reasons). On the other hand, these values are stored in Heroku configuration so there is no need to import env.py into settings in deployment branch.

### Run project locally
While it is possible to run the project locally, please note that all sensitive data are stored in env.py. Because of that, when setting up the project to run locally, users need to prepare their own version of env.py, which includes:
- Secret key for django project (which can be obtained when creating a new Django project)
- Email login details (used for sending password related emails.)
- Stripe API keys (obtained from users' own Stripe account)
- AWS key (obtained from users' own AWS account)
- When running project locally, default database of SQLite will be used and image from blog will be uploaded locally as well (a copy is sent to project folder) so there is no need to configure database url.

## Credits
### Content
Some code used in this project are referenced from site such as [stackoverflow](https://stackoverflow.com/), origin of such code are within the comments.

### Image
The unicorn image used as a logo of this project was originally taken from [HERE](https://png-library.com/images2/watercolor-background/2/kisspng-unicorn-watercolor-painting-clip-art-unicorn-background-5abee8c4b45560.9145471515224608687387.jpg)
