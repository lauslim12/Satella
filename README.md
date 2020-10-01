# Satella

Satella is a dedicated Windows/Linux tool to get a recommendation of seasonal / yearly anime girls that you might like every day.

<p align="center">
  <img src="https://img.shields.io/badge/License-BSD--3--Revised-yellow"/>
  <img src="https://img.shields.io/badge/Coded%20with-Python-%233572A5"/>
</p>

## Introduction

Satella is a dedicated repository that helps you to get a recommendation of seasonal anime girls that you might like every day. Satella gathers data from [AniList GraphQL API](https://anilist.gitbook.io/anilist-apiv2-docs/) and [Genderize API](https://genderize.io/). How Satella gathers data depends on a multitude of factors, such as a specified year, number of times the character has been favorited, how popular is the anime, and the character role is taken into account (main characters are prioritized over supporting characters). However, duplicate data is not allowed in this application, as it is highly redundant.

This application runs on Shell and Python (3.5 and up) and mostly relies on crontabs to get it working automatically each day. Data gathered from Satella will be stored in a CSV (soon SQL) file for further processing (further processing could be displaying it in a website, or even as simple as opening the CSV on a Microsoft Excel and inferring it by yourself).

It is recommended to run Satella on a low-power micro-computer such as Raspberry Pi Model A+. I personally use them and it makes the automation easier and less costly.

## Development

Satella is still under continuous development and there are still more features in my mind that I am coding currently! Keep in touch by starring this repository!

## Architecture

* Internet Of Things
* Object Oriented Programming
* Python Programming Language
* Shell Scripts and Micro Computers for Automation

## Philosophy

The name 'Satella' comes from the the character 'Satella' from Re:Zero. I actually like the name, so I named the repository after her.

## Requirements

In order to run the baseline of this application, you just need the following two things.

* Windows / Linux Environment (Linux is recommended)
* Python 3.5 and up, complete with PIP

In order to automate the application, then you will also need the following things.

* Raspberry Pi (any version is fine, optional)
* Raspbian OS (for the Raspberry Pi, also optional)
