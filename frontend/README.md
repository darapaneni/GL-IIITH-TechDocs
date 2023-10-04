# TechDocs - Frontend

It is a dockerized, mobile-ready, offline-storage compatible, JS-powered Latex editor.

- Marketing Pages [Home, Features, Help/FAQ, Pricing, Register, Login ]  
- Dashboard Pages [Dashboard-Home/MyDocuments, User Account, Latex Document Editor, Trash]

## Features

- Signup & Login With email-passowrd or with Google Account 
- Realtime Preview while editing the Latex document
- Save, Edit, View, Mark As Draft, Publish
- Sync Documents with Dropbox, Google Drive
- Share with specific permissions
- Manage Trash
- Download PWA Application into Mobile/Desktop 
- Edit in offline mode


## Tech

Techdocs fronted uses a number of open source projects

- [Bootstrap] : great UI boilerplate for modern web apps
- [Python Flask]  : For URL Based Routing & Rendering HTML Templates
- [jQuery] - UI/UX Actions/Events on HTML Documents
- [LatexJS] - JS Library to preview latex document

## Installation

TechDocs-Frontend requires Docker

Clone the Repository and then run the following commands

```bash
# Get Into the folder
cd GL-TechDocs/frontend
```
### For Linux
```bash
# Run Helper script which will build & Run a docker container
sudo bash start.sh
```

### For Windows
```bash
# Run Helper script which will build & Run a docker container
.\start.ps1
```

Now, Check http://localhost:56733


## Development

Want to contribute? Great!


## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [Bootstrap]: <https://getbootstrap.com>
   [jQuery]: <http://jquery.com>
   [Python Flask]: <https://flask.palletsprojects.com/en/2.2.x/>
   [LatexJS]: <https://latex.js.org/>
   
