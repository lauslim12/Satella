# Satella

Satella is a dedicated Windows / Linux tool to get a recommendation of seasonal / yearly anime girls that you might like every day with a personalized algorithm.

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

In order to automate the application, then you will also need these:

* Raspberry Pi (any version is fine, optional, you can use other micro computers)
* Raspbian OS (for the Raspberry Pi, also optional)

## How it Works

Satella works by following below pseudocode (simplified):

1. First off, the program will check if the maximum API calls has been reached by the program or not. If yes, exit the program and ask the user to use it again.

2. If not, the program will then fetch random data based on the GraphQL query on the `main.py` file. There is an extra metric that you should keep your eyes on: a weighed random number generator. In the first iteration, I assume that there are 400 animes for this year. The second and above iteration will always have the maximum possible random number to be the maximum count of current year's anime.

3. The weighed number generator is 85% biased towards the number with higher favorites (means that you are more likely to get a character from a higher-favorited anime). As an added note, 'higher favorites' that we mean here is the top 10% anime for the current year. In other words, you are more likely to get a character from the top 10% anime of this year. Note that if you are querying by an ID, the random number gotten will always be one.

4. If there is no anime based on a query (total page is zero), then retry step (1).

5. If there is an anime, then check if it has supporting characters or not. If not, then only take the main characters. If yes, then it is 50-50 chance to get either a main character or a supporting character. We will take the 'pool' or the array of main characters or the supporting characters.

6. In the same time as step (5), the program will also generate a random number based on a 'page' that we will take the character from.

7. If the page generated is not one, then we will make a query again to get the pool of characters based on that generated page number. If the page generated is one, continue to step (8).

8. We make another randomized choice to take a character from the main characters pool (if in step (5) we had gotten a main character as our character to take from) or from the supporting characters pool (if in step (5) we had gotten a supporting character as our character to take from).

9. Make an API call to the Genderize API (with the Japan country setting) by sending our gained character name. If she is a female, then take her immediately. If the character is a Male or a None, then we make an API call again (this time with Worldwide setting). If after the API call is decided that the character is a male, then start again from step (1). If after the API call is decided that the character is a None or a Female, then continue to step (10). The 'reject male' feature can be disabled by passing an argument to the optional parameters.

10. Check if we have the same character (duplicate) in the CSV output file. If there is, start again from step (1).

11. We simply write the data of the character that we have already taken beforehand into a CSV file (`data/suggestions.csv` in this case).

## Project Structure

The project structure itself is very simple.

* The `auto` folder is used to store the automation scripts.
* The `data` folder contains the output CSV file.
* `clean.py` is a script to clean out the CSV file with the exception of the header.
* `main.py` is the application starting point.
* `auto/main.sh` and `auto/main.bat` are the shell scripts required for automating the system. For Linux and Windows, respectively.
* The `requirements.txt` file is dedicated for the dependencies that I use to make and to keep this application running.
* The rest are usual Git documents (`.gitignore`, `CONTRIBUTING.md`, `README.md`, `LICENSE`).

## Installation

The installation guide assumes that you are using Linux for this part. For those using Windows, you just have to replace the `python3` with `python`. For the automation, just use the `main.bat` (instead of `main.sh`) file. Personally, I use my Raspberry Pi via SSH to do the installation steps.

### General Setup

The following setup is used to start the application on its basic form.

* Ensure that your Python is 3.5 or up!

```bash
python3 --version
```

* First off, fork my repository, then clone it. I am going to assume that you cloned the repository to the `Home` directory.

```bash
git clone <your_fork_url>
cd $HOME/Satella
```

* Second, create a Python Virtual Environment (in your Linux machine), then install the requirements. You can also use the `setup.py` if you wish for it.

```bash
python3 -m venv venv
source "venv/bin/activate"
pip3 install -r requirements.txt
python3 setup.py install
```

* A note to keep in mind, if you just want to install the 'production-ready' environment (also known as plug-and-play), then you just need to install the `requests` library.

```bash
pip3 install requests
```

* As an initial setup, clear all the data that I might have in my repository.

```bash
python3 main.py --clean
```

* Actually, after above steps are done, you can easily run the application using the following command. However, there is no automation yet, as we have not yet set it up.

```bash
python3 main.py <optional_arguments>
```

* The application will then run, and then it will store its results in the `data/suggestions.csv` file.

* As a note, optional arguments are explained in below setup.

### Automation Setup

This project is setup so that it could be automated everyday. I personally recommend you to use low-powered micro computers (also known as single board computers) like Raspberry Pi, BeagleBoard, Odroid, Banana Pi, and any other micro computers that you might have. The reason I recommended you those tools is because they are low-powered computers (electric bills are expensive nowadays) and they are literally equipped to be turned on 24/7 for IoT purposes. I use Raspberry Pi as it already had Git and Python installed the moment I installed the Raspbian OS.

* First, in order to automate the gathering of anime characters, you have to modify the `main.sh` file as you see fit with your own arguments. Below are the list of the arguments available for this program.

| Abbreviation |     Argument    |                                                                  Purpose                                                                 |    Default   |
|:------------:|:---------------:|:----------------------------------------------------------------------------------------------------------------------------------------:|:------------:|
|      -h      |      --help     |                                                        Prints out the help screen.                                                       |     None     |
|      -c      |     --clean     |                                            Clear the CSV file with the exception of the header                                           |     False    |
|      -i      |       --id      | Randomly selects a character from an anime based on its media ID (from AniList). Remember that you can't search by year if you use this! |     None     |
|      -y      |      --year     |                                   Randomly selects a character from animes based on its year of release                                  | Current year |
|      -s      |     --season    |             Used to find a random character based on an anime from a season. Combine this with `--year` for better filtering.            |     None     |
|      -gf     | --gender-filter |                         Used to enable or disable exceptions from being thrown if the character is of male gender                        |     TRUE     |

* Usage example from the `main.sh` file:

```bash
cd $HOME/Satella/auto
nano main.sh

# Modified line in the main.sh file.
python3 main.py --year 2020 -s FALL

# An another alternative is to search for characters from an anime based on its media ID.
python3 main.py --id 113813 # We are searching for characters from Kanojo, Okarishimasu.
```

* Do not forget to check the `PYTHON_VENV` variable. Is it the same as your Python Virtual Environment that you created beforehand? If no, change it to your virtual environment.

```bash
PYTHON_VENV=venv # Replace this 'venv' with your virtual environment.
```

* Even if you did not set up your own custom arguments / filters, you can always just leave it be and it will be run with default arguments.

* After that, we need to setup our own crontab with Linux.

```bash
crontab -l
crontab -e
```

* You need the following script to be entered in your crontab. The following script is used to make automatic updates every 09:00 AM.

```bash
00 09 * * * cd "$HOME/Satella/auto" && bash main.sh
```

* As a precaution, you might need to set permissions for the repository folder.

```bash
sudo chmod -R 777 "$HOME/Satella"
```

* Do not forget to setup your Git account in your machine so you can make automated cronjobs everyday.

```bash
git config user.name <YOUR_USERNAME>
git config user.email <YOUR_EMAIL>
git config --list
# Then, create a random commit to authenticate your password.

git remote -v # Check if the remote exists.
git remote add origin <your_fork_url> # If the remote doesn't exist, then use your fork.
```

* Alternatively, you could use SSH in order to free yourself from the hassle of authenticating Git everyday. The guide to setup your own SSH with Linux can be [seen here (answer from StackOverflow)](https://stackoverflow.com/questions/8588768/how-do-i-avoid-the-specification-of-the-username-and-password-at-every-git-push). Make sure that you have already configured your `git config user.name` and `git config user.email`.

```bash
cd ~
ssh-keygen -t rsa -b 4096 -C <your_github_email>
ls -a # Check out your RSA '.pub' name.
cat <your_linux_username>.pub
# Then, configure your access keys with your GitHub configuration. After that...
ssh -T git@github.com
git remote set-url origin git+ssh://git@github.com/username/reponame.git
```

* Enjoy your new anime character recommendation everyday! Just check your own repository for any new updates!

* To check if our crontab had run successfully:

```bash
sudo grep CRON /var/log/syslog
```

* Note that if you are using Windows as your machine that will run this program, you could bind the `main.bat` script to Windows Task Scheduler. I believe you just need to follow the instructions from the GUI to setup the scheduled tasks.

## Data Inference

* The data can be opened using a spreadsheet application (Microsoft Excel or its open source counterpart) or read raw.

## Contribution

Satella is completely open source and contribution to this tool is highly encouraged for everyone! Please take a look at `CONTRIBUTING.md` file and enjoy contributing!

If you have found any issues during your usage of this program, please submit an issue and I'll go back to you right away.

## License

This application is licensed under BSD-3 License. Please see the `LICENSE` file for more information.

## Credits

I hereby offer thanks and credits to the following services and providers:

* [AniList.co](https://anilist.co/) for providing the GraphQL API.
* [Genderize.io](https://genderize.io/) for providing the API to predict the gender of a person based on their name.

Feel free to cite everything from this repository, as long as you give your credit. Satella is not related in any way, shape, or form to my work or my research. Satella is just a personal interest turned open source.
