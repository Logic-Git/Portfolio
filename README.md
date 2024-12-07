# Introduction
Welcome to my Portfolio! This repository showcases a selection of my data science/analytics projects, demonstrating my skills and competencies in the field. Each directory within this repository contains a distinct project I've worked on. 

For example, the **NLP-Contextual-Analysis** directory houses an NLP project focused on contextual analysis.

## Purpose
This portfolio serves to highlight my expertise and provide potential collaborators, employers, and fellow data enthusiasts with insight into my work.

## Navigation
**Project Directories**: Each directory is named after the project it contains.
**README Files**: Inside each project directory, you'll find a README file with detailed information about the project.

## Dependencies

### Global Requirements
- Python 3.12.5

### Project-Specific Dependencies
Each project in this repository may have its own set of dependencies. For detailed information:

1. Navigate to the specific project directory.
2. Refer to the `README.md` file within that directory for project-specific dependencies.
3. If present, check the `requirements.txt` file for a complete list of Python packages required.

### Setting Up
To set up the environment for a specific project:

1. Ensure Python 3.12.3 is installed on your system.
2. Install the project specific dependancies. If a `requirements.txt` file is present in the project directory, run:
```pip install -r requirements.txt```
Otherwise, use the `README.md` file to get more information about the project.

Note: If you encounter any issues with dependencies or setup, or you notice issues with the code, please refer to the individual project's README. If that doesn't help then open an issue in this repository.

## Additional Projects:
Below are some projects that are uploaded as additional repositories.

### Healthcare translation and transcription Web Applicaiton:
This project was completed as a 48-hour challenge to build a full stack web application. The purpose of the application was to transcribe conversations between a doctor and a patient, translate those conversations, and it included the functionality of dictating the translations. The application is made using an HTML, CSS and Javascript frontend with a Flask backend. 

At the end, I was successful in the challenge.

**Note:** I did not know front-end or back-end development at the time of building this application. I was able to build it by figuring out solutions as problems arose and using massive help from GPT models.

[View Project Repository](https://github.com/Logic-Git/healthcare-translation-app)

[Access the Online Deployment of the Application here.](https://nao-medical-transcriber.onrender.com/)

**Disclaimer:** The web application deployed online does not work right away. When you follow the URL, you will see the front end but if you try to transcribe and translate something right away you would not see a translation.  The reason for this is that it is deployed using a free render account. This has limitations including the fact that if the app recieves no traffic in 15 minutes (which it doesn't because this url is not widely shared so no one uses the app), the app spins down and when a new user comes in, it takes a minute for the app to spin back up. Therefore, to test the app properly, wait for a minute after you follow the URL. After that, you can press the start speaking button and it would work as expected. If the app has still not spun up, reload the web page and try again. Once the app spins up, even reloading the web page or visiting it later does not effect the functionality as long as you do it within 15 minutes.

On the other hand, if you follow the link to the repository, clone it and run the app locally, it would work without any problems.
