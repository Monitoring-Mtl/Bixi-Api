[![CC BY 4.0][cc-by-shield]][cc-by]

<!-- Improved compatibility of haut link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->

<!-- SHIELDS PROJET -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<div align="center">

<a href="">![GitHub
contributors](https://img.shields.io/github/contributors/Monitoring-Mtl/Bixi-Api?color=green)</a>
<a href="">![GitHub last commit
(branch)](https://img.shields.io/github/last-commit/Monitoring-Mtl/Bixi-Api/main)</a>
<a href="">![GitHub
issues](https://img.shields.io/github/issues/Monitoring-Mtl/Bixi-Api)</a> <a
href="">![GitHub top
language](https://img.shields.io/github/languages/top/Monitoring-Mtl/Bixi-Api)</a>

</div>
<!-- [![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url] -->

<!-- LOGO ETS -->
<br />
<div align="center">
  <a href="https://www.etsmtl.ca/">
    <img src="https://www.etsmtl.ca/getmedia/a38cc621-8248-453b-a24e-ff22bd68ada5/Logo_ETS_SansTypo_FR" alt="Logo" width="200" height="200">
  </a>

  <h3 align="center">Monitoring Mtl - Bixi-Api</h3>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About the Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#test-coverage-report">Test Coverage Report</a></li>
      </ul>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About the Project

</br>
<div align="center">
  <a href="https://www.etsmtl.ca/">
    <img src="https://github.com/Monitoring-Mtl/Serverless-API/assets/113111772/f4646e57-50f7-4394-a698-2e81f886870e" alt="Logo" width="200" height="200">
  </a>
</div>
</br>

This is a REST API for querying public Bixi data aggregated over time in
`Monitoring-Mtl`

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

Here is the list of frameworks and tools we use in the project:

- [![Python][Python]][Python-url]
- [![AWS][AWS]][AWS-url]
- [![GitHub][GitHub]][GitHub-url]
- [![GitHubActions][GitHubActions]][GitHubActions-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- TO GET STARTED -->

## To Get Started

### Prerequisites

- Python 3.11 or newer
- AWS CLI
- Docker for local testing

### Installation

_Below is an example of the procedure to install the project locally and launch
the project to test that your work environment is functional._

1. Clone the repository

   ```sh
   git clone https://github.com/Monitoring-Mtl/Bixi-Api.git
   ```

2. Install Python packages

   ```sh
   pip install -r requirements.txt
   ```

3. Launch the local serverless application using AWS SAM

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   sam local start-api
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

TODO

### Test Coverage Report

TODO

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Roadmap

See the [open issues](https://github.com/Monitoring-Mtl/Serverless-API/issues)
for the full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contributing

Hoping that the project continues to grow with your contributions. **Thank you**

We have decided to use a Trunk Based Development structure for branch
management. To ensure every Pull Request (PR) correlates with tracked work, all
PRs must be associated with an existing issue. If the relevant issue does not
exist, please create one before proceeding with your contribution. Here's the
updated procedure:

1. Clone the Project (_if not already done_).
2. Check if an issue exists for your contribution; if not, create one.
3. Create a Feature or Documentation branch, including the issue number in the
   branch name (`git checkout -b feature/123-AmazingFeature`).
4. Commit your Changes (`git commit -m '#123: Add AmazingFeature'`).
5. Push the Branch (`git push origin feature/123-AmazingFeature`).
6. Open a Pull Request and link it to the issue.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

- Francis Bordeleau -
  [@linkedin](https://www.linkedin.com/in/francis-bordeleau-b2aa273/)
- Julien Gascon-Samson -
  [@linkedin](https://www.linkedin.com/in/julien-gascon-samson-4585b11a/)
- Mohammed Sayagh -
  [@linkedin](https://www.linkedin.com/in/mohammed-sayagh-24bab978/)


<p align="right">(<a href="#readme-top">haut</a>)</p>

<!-- ACKNOWLEDGMENTS -->

## Acknowledgments

Special thanks to

- [Badges](https://github.com/Ileriayo/markdown-badges#markdown-badges)
- [Readme Template](https://github.com/othneildrew/Best-README-Template)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]:
    https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]:
    https://github.com/Monitoring-Mtl/Serverless-API/graphs/contributors
[forks-shield]:
    https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]:
    https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]:
    https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]:
    https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]:
    https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]:
    https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png
[AWS]:
    https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white
[AWS-url]: https://aws.amazon.com/
[GitHub]:
    https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white
[GitHub-url]: https://www.github.com
[GitHubActions]:
    https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white
[GitHubActions-url]: https://github.com/features/actions
[AWS]:
    https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white
[AWS-url]: https://aws.amazon.com/
[Python]:
    https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://docs.python.org/3/

## LICENSE

This work is licensed under a [Creative Commons Attribution 4.0 International
License][cc-by].

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
