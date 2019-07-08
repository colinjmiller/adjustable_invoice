# Adjustable Invoice

This project was built as part of the [placements.io](https://placements.io/) interview. It allows users to create and manage invoices from a selection of line items. In particular, I chose to implement the following use cases:

* Bucket 1
  * The user can browse through line items as a table via pagination
  * The user can edit line item adjustments
  * The user can see each line item's billable amount
  * The user can see an invoice's grand total

* Bucket 2
  * The user can add comments on individual line items

## Setup

Running this application **requires** Docker, which can be downloaded [here](https://hub.docker.com/editions/community/docker-ce-desktop-mac). To begin developing, [clone the repository on github](https://github.com/colinjmiller/adjustable-invoice) and run the `dev.sh` script:
```
$ git clone git@github.com:colinjmiller/adjustable_invoice.git
$ cd adjustable_invoice
$ ./dev.sh
##############################################
# Creating application docker image
##############################################

...

adjustable_invoice    |  * Running on http://0.0.0.0:9999/ (Press CTRL+C to quit)
adjustable_invoice    |  * Restarting with stat
adjustable_invoice    |  * Debugger is active!
adjustable_invoice    |  * Debugger PIN: 245-443-207
```

This application uses `docker-compose` to start a flask application on port 9999 and a postgres container on a non-default port (5430). This allows the developer to use a local postgres instance on the default port if they need it for some other application. On first run, it may take some time to build the application image.

## Development

After running `./dev.sh` and starting your development server, you can make changes to the application by editing files locally. Behind the scenes, changes you make are instantly reflected on the docker container. Template changes will be visible the next time you refresh your browser window. Python changes will cause your flask server to restart, then be reflected next time you hit the logic you've changed.

## Testing

The application uses two different types of tests and can be run using `./tests.sh`. The tests are run in the following order and must pass before the next set will run.

1. Static analysis: These tests are style/lint tests and verify the Python code conforms to [PEP8](https://www.python.org/dev/peps/pep-0008) standards. It uses the [pycodestyle](https://pypi.org/project/pycodestyle/) module to verify style.
2. Unit tests: These are tests that create a [Flask test_client](http://flask.pocoo.org/docs/1.0/testing/#the-testing-skeleton) and exercise the functionality of the endpoints. The test client retains state and mimics a user's browser, so these verify the basics of logging in and any state changes.

## Design Decisions

There were a lot of trade-offs I had to make for this application. This highlights some of the decisions I made as I created the application:

1. Embrace KISS principles. Build the most basic web app that works and apply progressive enhancements on top of that. In this app, I minimized Javascript dependencies and even allow users who disable javascript to use the application. In my experience, focusing on the basics makes it _much_ easier to add a little UX magic on top at a later time.
2. Audit early and often with an eye on performance and accessibility. I used Google's lighthouse audit tool to get feedback on ways to improve page performance and design.
3. Use an external style framework. I picked a CSS framework called [siimple](https://docs.siimple.xyz/index.html), which provided a light-weight base for theming and components. **If I could change any decision, this would be it.** Siimple was not designed to be a responsive framework and it shows--the mobile view is terrible.

![Lighthouse Report](https://github.com/colinjmiller/adjustable_invoice/blob/master/audit.png?raw=true)

### If I had more time...

1. I would move configuration files and environment secrets into their own gitcrypted files. Right now there are some default configs in use, or some secrets checked into the repo in plain text. I know this is bad. However, for the purposes of a proof-of-concept app, it was simpler to leave them there.
2. Patch up some of the security issues relating to adding and editing invoices and line items. Right now there's no check on if you're editing an invoice or line item that belongs to a different user, and obviously we wouldn't want to allow that in the real world where bad people are.
3. Write a _lot_ more tests. The test suite is super tiny because I wanted to give an example of what it would look like, but writing a comprehensive test suite was beyond the amount of time I had.
