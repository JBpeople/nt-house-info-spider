[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/JBpeople/nt-house-info-spider">
    <img src="docs/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">NT-House-Info-Spider</h3>

  <p align="center">
    南通二手房信息
    <br />
    <a href="https://github.com/JBpeople/nt-house-info-spider"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/JBpeople/nt-house-info-spider">View Demo</a>
    ·
    <a href="https://github.com/JBpeople/nt-house-info-spider/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="hhttps://github.com/JBpeople/nt-house-info-spider/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">关于项目</a>
    </li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## 关于项目

![Product Name Screen Shot][product-screenshot]

为了细致了解南通地区的房产信息，使用Python编写多线程爬虫抓取数据，存入SQLite本地数据库。

## 快速开始

安装 `poetry` 环境。
```bash
pip install poetry
```

克隆当前项目。
```bash
git clone https://github.com/JBpeople/nt-house-info-spider.git
```

进入项目目录。
```bash
cd nt-house-info-spider
```

安装依赖。
```bash
poetry install
```

运行爬虫。
```bash
poetry run python main.py
```

详情页面。
```bash
https://nt.ke.com/ershoufang/{pk}.html
```


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/JBpeople/nt-house-info-spider.svg?style=for-the-badge
[contributors-url]: https://github.com/JBpeople/nt-house-info-spider/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/JBpeople/nt-house-info-spider.svg?style=for-the-badge
[forks-url]: https://github.com/JBpeople/nt-house-info-spider/network/members
[stars-shield]: https://img.shields.io/github/stars/JBpeople/nt-house-info-spider.svg?style=for-the-badge
[stars-url]: https://github.com/JBpeople/nt-house-info-spider/stargazers
[issues-shield]: https://img.shields.io/github/issues/JBpeople/nt-house-info-spider.svg?style=for-the-badge
[issues-url]: https://github.com/JBpeople/nt-house-info-spider/issues
[license-shield]: https://img.shields.io/github/license/JBpeople/nt-house-info-spider.svg?style=for-the-badge
[license-url]: https://github.com/JBpeople/nt-house-info-spider/blob/master/LICENSE.txt
[product-screenshot]: docs/images/product-screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
