# The Technical Handbook of OverCoded
Jump directly to the main points, no "beginner level" tutorials, contain the real case study,... These are what you can expect from our handbook. 

We are using Trello to manage our tasks. You can check it out [here](https://trello.com/b/PpGwCSUY/technical-handbook).

## Installation

### Using Docker
```bash
docker-compose up
```
This will automatically create a local server run at port 4000.
### Vanila
You need to install Ruby and Jekyll, then install every dependencies for this project. We are using theme _Minimal Mistakes_ for the handbook. There are many online tutorials can help you setup easily so we don't specify the steps here.

Build the website:
```bash
./build.sh
```

Build the website and run a live reload server: (similar to running docker compose)
```bash
./serve.sh
```
## For editor


### How to contribute
Edit your post in `docs/_posts/`.

The category of the post should be one of these:
- Computer science
- Economics & Finance

### Structure of a post
Here is a sample: [Docker](https://overcodedzz.github.io/handbook/technology/docker/)

A post should have at least these sections: introduction, references and contributors.

The main contributor should have the dagger symbol next to his name.

## For reviewer
When a post come to the "review" stage, the reviewer assigned to that post should review the post and feedback to the editor. After everything is fine, the author need to make a merge request contains that post to the `main` branch.

Our admin team will decide which posts can be published on the handbook.

## For guest
If you feel interested in our handbook, please leave comment under each post or send an email to [this address](mailto:overcodedzz@gmail.com).

