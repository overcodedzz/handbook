# The Technical Handbook of OverCoded
Jump directly to the main points, no "beginner level" tutorials, contain the real case study,... These are what you can expect from our handbook. 

We are using Trello to manage our tasks. You can check it out [here](https://trello.com/b/PpGwCSUY/technical-handbook).

## For editor
First, you need to clone this repository to your local machine. Next, you need to install Ruby and Jekyll, then install every dependencies for this project. There are many online tutorials can help you setup easily so we don't specify the steps here.

### How to contribute
Edit your post in `_posts/`.

Run the local Jekyll server (auto incremental build):
```bash
./serve.sh
```

Build the static site: (you just need this script for local server)
```bash
./build.sh
```

### Structure of a post
Here is a sample: [Docker](https://overcodedzz.github.io/handbook/technology/docker/)

A post should have at least these sections: introduction, references and contributors.

The main contributor should have the dagger symbol next to his name.

## For reviewer
When a post come to the "review" stage, the reviewer assigned to that post can review the post and feedback to the editor. After everything is fine, the reviewer need to make a merge request contains that post to the main branch.

Our admin team will decide which posts can be published on the handbook.

## For guest
You can leave your comment under each post if you like or you can send an email to [this address](overcodedzz@gmail.com).

